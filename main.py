""" DIKA MAULIDAL_ """

import os
import sys
import colorama
from colorama import Fore, Style
from module import ascii, email, password, google_account, topsites, topkeyword, last_keyword, history, favicon, bookmark

colorama.init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    clear_screen()
    ascii.show_ascii()

    # Menampilkan menu dengan warna sesuai permintaan
    menu_text = (
        f"{Fore.BLUE}{Style.BRIGHT}\nWelcome to Chrome Examiner choose an option:\n{Style.RESET_ALL}"
        "============================================\n"
        f"{Fore.WHITE}{Style.BRIGHT}[{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}1{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}] {Style.RESET_ALL}{Fore.CYAN}Login Data{Style.RESET_ALL}\n"
        f"{Fore.WHITE}{Style.BRIGHT}[{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}2{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}] {Style.RESET_ALL}{Fore.CYAN}Email{Style.RESET_ALL}\n"
        f"{Fore.WHITE}{Style.BRIGHT}[{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}3{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}] {Style.RESET_ALL}{Fore.CYAN}Google Account{Style.RESET_ALL}\n"
        f"{Fore.WHITE}{Style.BRIGHT}[{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}4{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}] {Style.RESET_ALL}{Fore.CYAN}Top Sites{Style.RESET_ALL}\n"
        f"{Fore.WHITE}{Style.BRIGHT}[{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}5{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}] {Style.RESET_ALL}{Fore.CYAN}Top Keyword{Style.RESET_ALL}\n"
        f"{Fore.WHITE}{Style.BRIGHT}[{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}6{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}] {Style.RESET_ALL}{Fore.CYAN}Last Keyword{Style.RESET_ALL}\n"
        f"{Fore.WHITE}{Style.BRIGHT}[{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}7{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}] {Style.RESET_ALL}{Fore.CYAN}Bookmark{Style.RESET_ALL}\n"
        f"{Fore.WHITE}{Style.BRIGHT}[{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}8{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}] {Style.RESET_ALL}{Fore.CYAN}History{Style.RESET_ALL}\n"
        f"{Fore.WHITE}{Style.BRIGHT}[{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}9{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}] {Style.RESET_ALL}{Fore.CYAN}Favicon{Style.RESET_ALL}\n"
        f"{Fore.WHITE}{Style.BRIGHT}[{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}99{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}] {Style.RESET_ALL}{Fore.CYAN}Exit{Style.RESET_ALL}\n"
    )
    
    print(menu_text)
    sys.stdout.flush()

def main():
    while True:
        show_menu()
        choice = input("Choose an option: ")
        if choice == '1':
            password.get_chrome_passwords()  # Pemanggilan fungsi yang benar
        elif choice == '2':
            email.show_email()
        elif choice == '3':
            google_account.get_google_account_info()
        elif choice == '4':
            topsites.get_top_sites()
        elif choice == '5':
            topkeyword.get_top_search_keywords()
        elif choice == '6':
            last_keyword.get_last_10_keywords()
        elif choice == '7':
            bookmark.get_chrome_bookmarks()
        elif choice == '8':
            history.get_last_5_history()
        elif choice == '9':
            favicon.get_favicon_info()
        elif choice == '99':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose again.")
        
        input("\nPress Enter to return to the menu...")

if __name__ == '__main__':
    main()
