import pyfiglet
import colorama
from colorama import Fore
import sys

colorama.init(autoreset=True)

def show_ascii():
    chrome_text = r"""
          ⠀⠀⠀⠀ ⠀⠀⢀⣠⣤⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀
          ⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀
          ⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀
          ⠀⢀⣾⣯⠻⣿⣿⣿⣿⡿⠟⠛⠉⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣷⡀⠀
          ⠀⣾⣿⣿⣧⠈⠻⡿⠋⠀⠀⣀⣠⣄⣀⠀⠀⠀⠀⠀⣀⣤⣴⣾⣷⠀
          ⢠⣿⣿⣿⣿⣧⠀⠀⠀⢠⣾⣿⣿⣿⣿⣷⡄⠀⠈⣿⣿⣿⣿⣿⣿⡄
          ⢸⣿⣿⣿⣿⣿⡇⠀⠀⢾⣿⣿⣿⣿⣿⣿⡷⠀⠀⢸⣿⣿⣿⣿⣿⡇
          ⠘⣿⣿⣿⣿⣿⣿⡀⠀⠘⢿⣿⣿⣿⣿⡿⠃⠀⢀⣿⣿⣿⣿⣿⣿⠃
          ⠀⢿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠉⠙⠋⠉⠀⠀⣠⣾⣿⣿⣿⣿⣿⡿⠀
          ⠀⠈⢿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣀⡀⠀⢀⣾⣿⣿⣿⣿⣿⣿⡿⠁⠀
          ⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⣠⣾⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀
          ⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⡏⣰⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀
          ⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠼⠿⠿⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀
    """
    forensic_text = pyfiglet.figlet_format("EXAMINER")
    colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLUE_EX]

    output = ""  # Menyimpan output dalam string
    for i, line in enumerate(chrome_text.splitlines()):
        color = colors[i % len(colors)]
        output += color + line + '\n'  # Tambahkan baris ke output

    for i, line in enumerate(forensic_text.splitlines()):
        color = colors[i % len(colors)]
        output += color + line + '\n'  # Tambahkan baris ke output

    sys.stdout.write(output)  # Cetak semua output sekaligus
