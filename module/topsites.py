import os
import sqlite3
import shutil
from tabulate import tabulate  # Untuk tampilan data dalam bentuk tabel
from colorama import Fore, Style, init  # Import colorama for coloring output

# Inisialisasi colorama untuk Windows agar warna bekerja
init(autoreset=True)

def colorize_header(text):
    """Memberikan warna biru muda pada header"""
    return f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{text}{Style.RESET_ALL}"

def colorize_value(text):
    """Memberikan warna cyan pada nilai"""
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"

def colorize_sites(text):
    """Memberikan warna putih tebal pada nama bookmark"""
    return f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"

def get_top_sites():
    db_path = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Top Sites'
    )
    db_copy = os.path.join(os.environ['USERPROFILE'], 'Top Sites Copy')
    shutil.copyfile(db_path, db_copy)

    conn = sqlite3.connect(db_copy)
    cursor = conn.cursor()

    cursor.execute("SELECT url, title FROM top_sites")

    top_sites = []
    for row in cursor.fetchall():
        url = row[0]
        title = row[1]
        top_sites.append([title, url])

    cursor.close()
    conn.close()
    os.remove(db_copy)

    if top_sites:
        print(colorize_sites("\nTop Sites"))

        # Menyiapkan data untuk ditampilkan dalam tabel dengan warna
        table_data = [(colorize_value(title), colorize_value(url)) for title, url in top_sites]

        print(tabulate(table_data, headers=[colorize_header("Title"), colorize_header("URL")], tablefmt="pretty"))
    else:
        print("No top sites found.")

if __name__ == '__main__':
    get_top_sites()
