import os
import json
from datetime import datetime, timedelta
from tabulate import tabulate
from colorama import Fore, Style, init

# Inisialisasi colorama untuk Windows agar warna bekerja
init(autoreset=True)

# Fungsi untuk mengonversi waktu dari microseconds since Unix epoch
def convert_chrome_time(chrome_time):
    # Chrome menyimpan waktu dalam microseconds sejak 1 Januari 1601
    epoch_start = datetime(1601, 1, 1)
    return epoch_start + timedelta(microseconds=int(chrome_time))

def format_time(date_time):
    """Mengonversi datetime menjadi format yang lebih singkat (YYYY-MM-DD HH:MM)"""
    if isinstance(date_time, datetime):
        return date_time.strftime('%Y-%m-%d %H:%M')
    return date_time

def colorize_header(text):
    """Memberikan warna biru muda pada header"""
    return f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{text}{Style.RESET_ALL}"

def colorize_value(text):
    """Memberikan warna cyan pada nilai"""
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"

def colorize_bookmark(text):
    """Memberikan warna putih tebal pada nama bookmark"""
    return f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"

def get_chrome_bookmarks():
    # Path ke file Bookmarks di Chrome
    bookmarks_path = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Bookmarks'
    )

    if not os.path.exists(bookmarks_path):
        print("File Bookmarks tidak ditemukan.")
        return

    # Membaca file Bookmarks JSON
    with open(bookmarks_path, 'r', encoding='utf-8') as file:
        bookmarks_data = json.load(file)

    # Bookmark disimpan di 'roots' di file JSON
    bookmark_list = []

    def parse_bookmark_tree(bookmark_node, parent_folder=""):
        if bookmark_node.get('type') == 'url':
            # Mengonversi `date_added` dan `date_last_used` jika ada
            date_added = bookmark_node.get('date_added')
            date_added = convert_chrome_time(date_added) if date_added else "N/A"
            date_last_used = bookmark_node.get('date_last_used')
            date_last_used = convert_chrome_time(date_last_used) if date_last_used else "N/A"

            # Cek apakah `date_last_used` masih di default (1601-01-01) atau kosong
            if date_last_used == "N/A" or date_last_used.year == 1601:
                date_last_used = "Not Used"

            # Tambahkan ke list bookmark dengan format waktu yang lebih singkat
            bookmark_list.append({
                colorize_header('Name'): colorize_value(bookmark_node.get('name')),
                colorize_header('URL'): colorize_value(bookmark_node.get('url')),
                colorize_header('Folder'): colorize_value(parent_folder),
                colorize_header('Date Added'): colorize_value(format_time(date_added)),
                colorize_header('Last Used'): colorize_value(format_time(date_last_used))
            })
        elif bookmark_node.get('type') == 'folder':
            # Jika node ini folder, parse isinya secara rekursif
            folder_name = bookmark_node.get('name')
            for child_node in bookmark_node.get('children', []):
                parse_bookmark_tree(child_node, parent_folder=f"{parent_folder}/{folder_name}" if parent_folder else folder_name)

    # Parse bagian 'bookmark_bar' dan 'other'
    roots = bookmarks_data.get('roots', {})
    for root_key in ['bookmark_bar', 'other']:
        if root_key in roots:
            parse_bookmark_tree(roots[root_key])

    if bookmark_list:
        # Tampilkan bookmark dalam bentuk tabel
        print(colorize_bookmark("\nBookmarks"))  # Mengubah judul menjadi berwarna putih dan tebal
        print(tabulate(bookmark_list, headers="keys", tablefmt="pretty"))
    else:
        print("Tidak ada bookmark yang ditemukan.")

if __name__ == '__main__':
    get_chrome_bookmarks()
