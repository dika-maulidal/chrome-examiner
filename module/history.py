import os
import sqlite3
import shutil
from datetime import datetime, timedelta
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

def get_last_5_history():
    db_path = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History'
    )
    db_copy = os.path.join(os.environ['USERPROFILE'], 'History Copy')
    shutil.copyfile(db_path, db_copy)

    conn = sqlite3.connect(db_copy)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT url, title, visit_count, last_visit_time 
        FROM urls 
        ORDER BY last_visit_time DESC 
        LIMIT 5
    """)
    history_entries = cursor.fetchall()

    formatted_history = []
    for row in history_entries:
        url = row[0]
        title = row[1]
        visit_count = row[2]
        last_visit_time = row[3]

        # Convert last_visit_time from WebKit format to datetime
        last_visit_time = datetime(1601, 1, 1) + timedelta(microseconds=last_visit_time)
        formatted_history.append({
            "Title": title,
            "URL": url,
            "Visit Count": visit_count,
            "Last Visited": last_visit_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    cursor.close()
    conn.close()
    os.remove(db_copy)

    # Output formatted browsing history
    if formatted_history:
        # Title with white bold
        print(f"\n{colorize_keyword('Last 5 Browsing History Entries')}")
        for i, entry in enumerate(formatted_history, start=1):
            # Brackets in white bold, content inside brackets in cyan, and content values in light blue
            print(f"\n{colorize_bracket('[')}{colorize_header(f'Entry {i}')}{colorize_bracket(']')}")
            print(f"{colorize_bracket('[')}{colorize_header('Title')}{colorize_bracket(']')} {colorize_value(entry['Title'])}")
            print(f"{colorize_bracket('[')}{colorize_header('URL')}{colorize_bracket(']')} {colorize_value(entry['URL'])}")
            print(f"{colorize_bracket('[')}{colorize_header('Visit Count')}{colorize_bracket(']')} {colorize_value(entry['Visit Count'])}")
            print(f"{colorize_bracket('[')}{colorize_header('Last Visited')}{colorize_bracket(']')} {colorize_value(entry['Last Visited'])}")
    else:
        print("No browsing history found.")

if __name__ == '__main__':
    get_last_5_history()
