from mitmproxy import http
from pymongo import MongoClient
import json
from colorama import Fore, Style, init
import asyncio
import logging
import socket
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.database import database  # Pakai modul database
from utils.helpers import log_info, log_error

# Nonaktifkan pesan error dari asyncio
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
asyncio.get_event_loop().set_exception_handler(lambda loop, context: None)

# Inisialisasi Colorama
init(autoreset=True)
"""
# Koneksi ke MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["shopee_db"]  
collection = db["products"]  
"""
def response(flow: http.HTTPFlow):
    """
    Fungsi ini menangkap response dari Shopee API dan menyimpannya ke MongoDB
    """
    url_target = "https://shopee.co.id/api/v4/pdp/get_pc"

    if flow.request.url.startswith(url_target):  
        try:
            # Ambil response JSON dari Shopee API
            json_data = json.loads(flow.response.text)

            # Ambil informasi yang dibutuhkan
            item = json_data["data"]["item"]
            title = item["title"]
            shop_id = item["shop_id"]
            item_id = item["item_id"]
            compensation_value = json_data["data"]["product_shipping"]["selected_late_delivery_compensation_for_drawer"]["compensation_amount"]["value"]
            first_digit = int(str(compensation_value)[0])  # Ubah ke integer agar bisa dibandingkan
            if first_digit == 1:
                divisor = compensation_value // 10000
            elif 2 <= first_digit <= 9:  # Cek apakah angka antara 2 dan 9
                divisor = compensation_value // 1000
            else:
                divisor = item["price_max_before_discount"]  # Default jika tidak memenuhi kondisi

            price_max_before_discount = item["price_max_before_discount"] // divisor  
            price_max = item["price_max"] // divisor  
            images = json_data["data"]["product_images"]["images"]

            # Logika untuk menentukan price_max
            price_max = max(price_max_before_discount, price_max)

            # Buat _id sesuai format yang diminta
            title_slug = title.replace(" ", "-")
            _id = f"https://shopee.co.id/{title_slug}-i.{shop_id}.{item_id}"

            # Ekstrak display_name dari kategori
            categories = item.get("categories", [])
            display_names = [category.get("display_name") for category in categories]

            # Persiapkan data untuk disimpan
            data = {
                "_id": _id,
                "title": title,
                "description": item["description"],
                "price_max": price_max,
                "images": images,
                "categories": display_names  
            }

            # Simpan data ke MongoDB
            #collection.insert_one(data)
            database.insert_data(data)
            #log_info(f"Data berhasil disimpan: {_id}")

            # Tampilkan pesan yang diinginkan
            print(f"{Fore.YELLOW}[Lilis Widyanti]{Fore.GREEN}[Grab URL]: {Style.RESET_ALL}{_id}")

        except Exception:
            log_error(f"Gagal menyimpan data ke MongoDB: {e}")
