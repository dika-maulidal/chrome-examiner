import os
import sqlite3
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)

def colorize_bracket(text):
    """Memberikan warna putih tebal pada bracket []"""
    return f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"

def colorize_header(text):
    """Memberikan warna biru muda pada header"""
    return f"{Fore.LIGHTBLUE_EX}{text}{Style.RESET_ALL}"

def colorize_value(text):
    """Memberikan warna cyan pada nilai"""
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"

def colorize_keyword(text):
    """Memberikan warna putih tebal pada nama bookmark"""
    return f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"

def get_favicon_info():
    favicons_path = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Favicons'
    )

    if not os.path.exists(favicons_path):
        print("Favicons file tidak ditemukan.")
        return

    conn = sqlite3.connect(favicons_path)
    cursor = conn.cursor()

    # Kueri untuk mengambil hanya favicon yang memiliki page_url di icon_mapping
    cursor.execute("""
        SELECT favicons.id, favicons.url, icon_mapping.page_url
        FROM favicons
        JOIN icon_mapping ON favicons.id = icon_mapping.icon_id
    """)
    favicon_entries = cursor.fetchall()

    # Format data favicon dan hapus duplikat berdasarkan favicon URL
    formatted_favicons = []
    seen_urls = set()  # Set untuk melacak URL yang sudah ditampilkan

    for row in favicon_entries:
        icon_id = row[0]
        favicon_url = row[1]
        page_url = row[2]

        # Hanya tambahkan favicon jika URL belum ada dalam set
        if favicon_url not in seen_urls:
            seen_urls.add(favicon_url)  # Tambahkan URL ke set untuk pelacakan
            formatted_favicons.append({
                "Icon ID": icon_id,
                "Favicon URL": favicon_url,
                "Page URL": page_url,
            })

    cursor.close()
    conn.close()

    # Output formatted favicon info
    if formatted_favicons:
        # Title with white bold
        print(f"\n{colorize_keyword('Favicon Information')}")
        for i, entry in enumerate(formatted_favicons, start=1):  # Menampilkan semua entri unik
            # Brackets in white bold, content inside brackets in cyan, and content values in light blue
            print(f"\n{colorize_bracket('[')}{colorize_header(f'Favicon {i}')}{colorize_bracket(']')}")
            print(f"{colorize_bracket('[')}{colorize_header('Icon ID')}{colorize_bracket(']')} {colorize_value(entry['Icon ID'])}")
            print(f"{colorize_bracket('[')}{colorize_header('Favicon URL')}{colorize_bracket(']')} {colorize_value(entry['Favicon URL'])}")
            print(f"{colorize_bracket('[')}{colorize_header('Page URL')}{colorize_bracket(']')} {colorize_value(entry['Page URL'])}")
    else:
        print("No favicon information found.")

if __name__ == '__main__':
    get_favicon_info()
