import os
import json
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
    """Memberikan warna putih tebal pada nama akun"""
    return f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"

def get_google_account_info():
    # Specify the path to the Preferences file
    preferences_path = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Preferences'
    )

    # Check if the Preferences file exists
    if not os.path.exists(preferences_path):
        print("Preferences file not found.")
        return

    # Load the JSON data from the Preferences file
    with open(preferences_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract the account information
    account_info = data.get('account_info', [])

    # Display Google Account Information title once
    print(f"\n{colorize_keyword('Google Account Information')}")

    # Output formatted account information
    if account_info:
        for idx, account in enumerate(account_info, start=1):
            given_name = account.get('given_name', 'N/A')
            full_name = account.get('full_name', 'N/A')
            email = account.get('email', 'N/A')
            gaia_id = account.get('gaia', 'N/A')
            profile_pic_url = account.get('picture_url', 'N/A')

            # Display the account information for each account
            print(f"\n{colorize_keyword(f'Account {idx}')}")
            print(f"{colorize_bracket('[')}{colorize_header('Given Name')}{colorize_bracket(']')} {colorize_value(given_name)}")
            print(f"{colorize_bracket('[')}{colorize_header('Full Name')}{colorize_bracket(']')} {colorize_value(full_name)}")
            print(f"{colorize_bracket('[')}{colorize_header('Email')}{colorize_bracket(']')} {colorize_value(email)}")
            print(f"{colorize_bracket('[')}{colorize_header('GAIA ID')}{colorize_bracket(']')} {colorize_value(gaia_id)}")
            print(f"{colorize_bracket('[')}{colorize_header('Profile Picture URL')}{colorize_bracket(']')} {colorize_value(profile_pic_url)}")
    else:
        print("No Google account information found.")

if __name__ == '__main__':
    get_google_account_info()
