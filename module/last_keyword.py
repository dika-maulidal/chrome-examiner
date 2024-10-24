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

def colorize_lastkey(text):
    """Memberikan warna putih tebal pada nama bookmark"""
    return f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"

def get_last_10_keywords():
    db_path = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History'
    )
    db_copy = os.path.join(os.environ['USERPROFILE'], 'History Copy')
    shutil.copyfile(db_path, db_copy)

    conn = sqlite3.connect(db_copy)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT term FROM keyword_search_terms 
        ORDER BY ROWID DESC 
        LIMIT 10
    """)
    search_terms = cursor.fetchall()

    if search_terms:
        print(colorize_lastkey("\nLast 10 Search Terms."))

        # Menyiapkan data untuk ditampilkan dalam tabel dengan warna
        table_data = [(colorize_value(term[0]),) for term in search_terms]

        print(tabulate(table_data, headers=[colorize_header("Search Term")], tablefmt="pretty"))
    else:
        print("No search terms found.")

    cursor.close()
    conn.close()
    os.remove(db_copy)

if __name__ == '__main__':
    get_last_10_keywords()
