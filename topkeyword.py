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

def colorize_keyword(text):
    """Memberikan warna putih tebal pada nama bookmark"""
    return f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"

def get_top_search_keywords():
    db_path = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History'
    )
    db_copy = os.path.join(os.environ['USERPROFILE'], 'History Copy')
    shutil.copyfile(db_path, db_copy)

    conn = sqlite3.connect(db_copy)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT term, COUNT(term) as freq
        FROM keyword_search_terms
        GROUP BY term
        ORDER BY freq DESC
        LIMIT 5
    """)

    top_keywords = cursor.fetchall()

    if top_keywords:
        # Top 5 Most Frequently Searched Keywords
        print(colorize_keyword("\nTop 5 Most Frequently Searched Keywords"))

        # Menyiapkan data untuk ditampilkan dalam tabel
        table_data = [(colorize_value(keyword), colorize_value(freq)) for keyword, freq in top_keywords]

        print(tabulate(table_data, headers=[colorize_header("Keyword"), colorize_header("Frequency")], tablefmt="pretty"))
    else:
        print("No search terms found.")

    cursor.close()
    conn.close()
    os.remove(db_copy)

if __name__ == '__main__':
    get_top_search_keywords()
