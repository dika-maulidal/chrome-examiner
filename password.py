import os
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from tabulate import tabulate  # Untuk tampilan data dalam bentuk tabel
import json
import base64
from colorama import Fore, Style, init  # Import colorama for coloring output

# Inisialisasi colorama untuk Windows agar warna bekerja
init(autoreset=True)

def colorize_header(text):
    """Memberikan warna biru muda pada header"""
    return f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{text}{Style.RESET_ALL}"

def colorize_value(text):
    """Memberikan warna cyan pada nilai"""
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"

def colorize_pass(text):
    """Memberikan warna putih tebal pada nama bookmark"""
    return f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"

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
            passwords.append([colorize_value(url), colorize_value(username), colorize_value(decrypted_password)])

    cursor.close()
    conn.close()
    os.remove(db_copy)

    if passwords:
        print(colorize_pass("\nSaved Passwords"))
        print(tabulate(passwords, headers=[colorize_header("URL"), colorize_header("Username"), colorize_header("Password")], tablefmt="pretty"))
    else:
        print("No saved passwords found.")

if __name__ == '__main__':
    get_chrome_passwords()
