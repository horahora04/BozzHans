import os
import time
import json
import sys
import subprocess
from colorama import init, Fore, Style
#from modules.proxy_manager import ProxyManager
from pymongo import MongoClient
from utils.helpers import log_info
from config import MONGODB_URI, DB_NAME, COLLECTION_NAME

# Inisialisasi Colorama untuk pewarnaan terminal
init(autoreset=True)

def clear_screen():
    """Membersihkan layar terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    """Menampilkan logo Shopee di terminal"""
    print(Fore.RED + Style.BRIGHT + "  SSSSS   H     H  OOOOO  PPPPP   EEEEE  EEEEE   " + Fore.YELLOW + "  UU    UU  RRRRRR    LL      " + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + " S        H     H O     O P    P  E      E       " + Fore.YELLOW + "  UU    UU  RR  RRR   LL      " + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "  SSSSS   HHHHHHH O     O PPPPP   EEEE   EEEE    " + Fore.YELLOW + "  UU    UU  RRRRRR    LL      " + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "       S  H     H O     O P       E      E        " + Fore.YELLOW + " UU    UU  RR  RR    LL      " + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "  SSSSS   H     H  OOOOO  P       EEEEE  EEEEE     " + Fore.YELLOW + " UUUUUU   RR   RR   LLLLLL " + Style.RESET_ALL)

def show_menu():
    """Menampilkan menu utama"""
    #proxy_manager = ProxyManager()

    while True:
        clear_screen()
        print_logo()

        print("\n")
        print(f"{' '*20}Menu Pilihan:")
        print(Fore.GREEN + f"{' '*25}[1] Jalankan Scraping Shopee" + Style.RESET_ALL)
        print(Fore.YELLOW + f"{' '*25}[2] Lihat Hasil Scraping" + Style.RESET_ALL)
        print(Fore.RED + f"{' '*25}[E] Keluar" + Style.RESET_ALL)
        python_executable = sys.executable

        choice = input(f"{' '*20}Masukkan pilihan Anda: ").strip().lower()

        if choice == "1":            
            print("\n[INFO] Memulai proses scraping...\n")            
            subprocess.Popen([python_executable, "modules/scraper.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
            #proxy_manager.start_proxy()
            #input("\nTekan Enter untuk menghentikan scraping...")
            #roxy_manager.stop_proxy()

        elif choice == "2":
            print("\n[INFO] Menampilkan hasil scraping...\n")
            log_info("Pengguna melihat hasil scraping.")
            show_results()

        elif choice == "e":
            print("\n[INFO] Keluar dari program.")
            log_info("Pengguna keluar dari aplikasi.")
            break

        else:
            print("\n[ERROR] Pilihan tidak valid. Coba lagi.")
            input("\nTekan Enter untuk kembali ke menu...")

def show_results():
    """Menampilkan hasil scraping dari MongoDB"""
    try:
        # Koneksi ke MongoDB
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Mengambil data dari MongoDB
        data = list(collection.find({}, {"_id": 1, "title": 1, "price_max": 1}))

        if not data:
            print(Fore.YELLOW + "\n[INFO] Tidak ada data scraping yang ditemukan.\n" + Style.RESET_ALL)
        else:
            print(Fore.CYAN + "\n[INFO] Hasil Scraping:\n" + Style.RESET_ALL)
            for item in data:
                print(f"- {item['_id']}: {item['title']} - Rp {item['price_max']}")

        input("\nTekan Enter untuk kembali ke menu...")

    except Exception as e:
        print(Fore.RED + f"\n[ERROR] Terjadi kesalahan: {e}\n" + Style.RESET_ALL)
        input("\nTekan Enter untuk kembali ke menu...")
