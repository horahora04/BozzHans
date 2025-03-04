from pymongo import MongoClient
from config import MONGODB_URI, DB_NAME, COLLECTION_NAME
from utils.helpers import log_info, log_error

class Database:
    def __init__(self):
        """Inisialisasi koneksi MongoDB dan cek apakah server dapat diakses"""
        try:
            self.client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)  # Timeout 5 detik
            self.client.server_info()  # Cek apakah MongoDB bisa diakses
            self.db = self.client[DB_NAME]
            self.collection = self.db[COLLECTION_NAME]
            #log_info("✅ Berhasil terhubung ke MongoDB.")
        except Exception as e:
            log_error(f"🚨 MongoDB tidak bisa diakses: {e}")

    def insert_data(self, data):
        """Menyimpan data ke MongoDB"""
        try:
            self.collection.insert_one(data)
            #log_info(f"✅ Data berhasil disimpan: {data['_id']}")
        except Exception as e:
            log_error(f"❌ Gagal menyimpan data: {e}")

# Inisialisasi instance global
database = Database()
