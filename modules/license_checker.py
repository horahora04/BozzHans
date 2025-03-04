import requests
import hashlib
import base64
import urllib.parse
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import platform
import subprocess
from config import LICENSE_SERVER, SECRET_KEY

# **Public Key untuk verifikasi tanda tangan digital**
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmAJgPPH7fvYxZdmMNcjl
HcYFER3rUdApa3bSMhGo8cDWvG5nzr2fL7Zh049fbdmghraZFe9Ajyra34ccjpKA
sUX96tR8w+PqD+oV/btvDEQicrthD7Zu4voLL6AmkmMov39CZ/CHEckh+QQv8INm
UDTmMJnRAnmN3ZlwV6A9hARkmbFyelLpWaMxl28Yd7VtPggN7smkoDijP9G4lls0
hQ0qpf3vE+Oqt7S2igOOrlR5mzfoVV1LDU655aWTKM49rHt3vvv+uDuhA35RTW/7
DvOkpt6qmESo/TX0b2P0IEiuVSSebsx+jKRJ+GLUJC85xUZFGBOZuV/B4DXuo12Y
5QIDAQAB
-----END PUBLIC KEY-----"""

def get_hwid():
    """Mendapatkan HWID unik berdasarkan sistem operasi"""
    system = platform.system()
    
    try:
        if system == "Windows":
            output = subprocess.check_output("wmic cpu get ProcessorId", shell=True)
            return output.decode().split("\n")[1].strip()
        elif system == "Linux":
            output = subprocess.check_output("cat /proc/cpuinfo | grep 'Serial'", shell=True)
            return output.decode().split(":")[1].strip()
    except Exception:
        return "ERROR"

    return "UNKNOWN"

def encrypt_hwid(hwid):
    """Mengenkripsi HWID menggunakan AES dengan SECRET_KEY"""
    key = hashlib.sha256(SECRET_KEY.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(hwid.encode(), AES.block_size))
    return base64.b64encode(encrypted).decode()

def verify_signature(hwid_encrypted, signature):
    """Verifikasi tanda tangan digital RSA"""
    try:
        # Load Public Key
        public_key = RSA.import_key(PUBLIC_KEY)

        # Hash HWID terenkripsi
        hash_obj = SHA256.new(hwid_encrypted.encode())

        # Decode Signature dari Base64
        signature_bytes = base64.b64decode(signature)

        # Verifikasi menggunakan kunci publik
        pkcs1_15.new(public_key).verify(hash_obj, signature_bytes)

        return True
    except (ValueError, TypeError):
        return False   

def check_license():
    """Cek lisensi ke server dan verifikasi tanda tangan digital"""
    hwid = get_hwid()
    encrypted_hwid = encrypt_hwid(hwid)
    encoded_hwid = urllib.parse.quote(encrypted_hwid)

    print(f"🔑 HWID Encrypted (Dikirim ke Server): {encoded_hwid}")

    try:
        response = requests.get(f"{LICENSE_SERVER}/?hwid={encoded_hwid}")
        data = response.json()

        if response.status_code == 200 and data.get("status") == "active":
            print("\n✅ Lisensi VALID!")
            print(f"📅 Expired: {data.get('expire')}")
            print(f"🔑 Signature: {data.get('signature')}")

            # **Verifikasi tanda tangan digital RSA**
            if verify_signature(encrypted_hwid, data.get('signature')):
                print("✅ Tanda tangan digital VALID!")
                return True
            else:
                print("❌ Tanda tangan digital TIDAK VALID!")
                return False
        else:
            print("\n❌ Lisensi TIDAK AKTIF!")
            return False
    except Exception as e:
        print("\n🚨 ERROR:", str(e))
        return False
