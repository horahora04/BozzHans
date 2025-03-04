import os
import time
import json
import sys
import subprocess
from colorama import init, Fore, Style

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

