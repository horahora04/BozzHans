from modules.license_checker import check_license
from colorama import init, Fore, Style
#from modules.proxy_manager import ProxyManager
from modules.menu import print_logo
import subprocess
import os
import sys
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
            #subprocess.Popen([python_executable, "modules/run.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
            subprocess.Popen([python_executable, os.path.join(os.path.dirname(__file__), "modules", "run.py")], creationflags=subprocess.CREATE_NEW_CONSOLE)


        elif choice == "e":
            print("\n[INFO] Keluar dari program.")
            exit(0)

        else:
            print("\n[ERROR] Pilihan tidak valid. Coba lagi.")
            input("\nTekan Enter untuk kembali ke menu...")


if __name__ == "__main__":
    clear_screen()
    while True:
        if check_license():
            #show_menu()
            break  # Keluar dari loop jika lisensi valid
        else:
            print("Lisensi Belum Aktif, Kirim kode ini ke Admin..")
            check_license()            
            #print(f"{get_hwid()}")
            #print(Fore.CYAN + "Coba lagi dalam 10 detik...\n" + Style.RESET_ALL)
            time.sleep(10)  # Tunggu sebelum mencoba lagi

    while True:
        show_menu()
        time.sleep(10)

