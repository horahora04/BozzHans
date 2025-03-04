import os
import sys
import subprocess
import signal
import win32api
import win32con
from pymongo import MongoClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# **Konfigurasi Proxy**
PROXY_IP = "127.0.0.1"
PROXY_PORT = "8080"

# **Cek dan Tutup Hanya Proses mitmdump**
def kill_mitmdump():
    try:
        result = subprocess.run("tasklist", capture_output=True, text=True, shell=True)
        lines = result.stdout.strip().split("\n")

        for line in lines:
            if "mitmdump.exe" in line:  # Cari proses mitmdump
                parts = line.split()
                pid = parts[1]  # PID ada di kolom kedua
                #print(f"[INFO] Menutup proses mitmdump dengan PID: {pid}...")
                subprocess.run(f'taskkill /PID {pid} /F', shell=True)
                return  # Hanya tutup satu proses mitmdump, lalu keluar
    except Exception as e:
        print(f"Error Closing port 8080")

# **Jalankan Fungsi Kill mitmdump**
kill_mitmdump()

def enable_proxy():
    """Mengaktifkan Proxy di Windows untuk Semua Browser"""
    subprocess.run([
        "reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        "/v", "ProxyEnable", "/t", "REG_DWORD", "/d", "1", "/f"
    ], shell=True)

    subprocess.run([
        "reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        "/v", "ProxyServer", "/t", "REG_SZ", "/d", f"{PROXY_IP}:{PROXY_PORT}", "/f"
    ], shell=True)

def disable_proxy():
    """Menonaktifkan Proxy di Windows"""
    subprocess.run([
        "reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        "/v", "ProxyEnable", "/t", "REG_DWORD", "/d", "0", "/f"
    ], shell=True)

def handle_exit(signum=None, frame=None):
    """Menangani semua cara keluar program"""
    disable_proxy()
    os._exit(0)

def on_close(event):
    """Menangani saat jendela CMD ditutup dengan tombol 'X'"""
    disable_proxy()
    os._exit(0)

# Tangkap sinyal keluar seperti CTRL+C dan kill
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

# Tangani jika CMD ditutup dengan tombol "X"
win32api.SetConsoleCtrlHandler(on_close, True)

# **Menjalankan Proxy dan mitmdump sebagai Subproses**
try:
    enable_proxy()
    #print("[INFO] Menjalankan mitmdump...")
    
    # Jalankan mitmdump dengan intercept.py dan opsi http2=false dan --quiet
    #mitmproxy_process = subprocess.Popen(["mitmdump", "-s", "intercept.py", "--set", "http2=false", "--quiet"])
    mitmproxy_process = subprocess.Popen(
    ["mitmdump", "-s", os.path.join(os.path.dirname(__file__), "intercept.py"), "--set", "http2=false", "--quiet"]
)

    
    # Tunggu proses mitmdump hingga selesai
    mitmproxy_process.wait()

finally:
    disable_proxy()
