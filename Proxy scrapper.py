import requests
import socket
import time
import os
from colorama import Fore, Style
from pystyle import Colors, Colorate
from datetime import datetime
import platform
import threading

colored_error_txt = (
Colors.red + "\n[" + Colors.white + "!" + Colors.red + "] " +
Colorate.Horizontal(Colors.red_to_white, "Invalid choice. try again")
)

colored_quitt_txt = (
Colors.purple + "\n[" + Colors.white + "?" + Colors.purple + "] " +
Colorate.Horizontal(Colors.purple_to_blue, "Do you want to return to the main menu? (yes/no): ")
)


colored_exit_txt = (
Colors.blue + "\n[" + Colors.white + "~" + Colors.blue + "] " +
Colorate.Horizontal(Colors.blue_to_white, "Exiting the program. Goodbye!")
)

colored_returnmenu_txt = (
Colors.blue + "\n[" + Colors.white + "~" + Colors.blue + "] " +
Colorate.Horizontal(Colors.blue_to_white, "Returning to the main menu...\n")
)

def get_pc_name():
    pc_name = os.getenv('COMPUTERNAME')
    if pc_name:
        return pc_name
    else:
        return os.uname()[1]


def show_invalid_choice():
    print(colored_error_txt)
    time.sleep(1)
    clear_console()

def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def print_settings(protocol=None, country=None, proxy_count=None):
    option_text = Colorate.Vertical(Colors.green_to_yellow, "[option] : ")
    protocol_text = Colorate.Horizontal(Colors.green_to_white, f" protocole -> {protocol if protocol else 'not set'}")
    country_text = Colorate.Horizontal(Colors.green_to_white, f"country -> {country if country else 'all'}")
    quantity_text = Colorate.Horizontal(Colors.green_to_white, f"quantity -> {proxy_count if proxy_count else 'not set'}")

    print(option_text + protocol_text + " | " + country_text + " | " + quantity_text)

def get_proxies_from_source(source_url):
    try:
        response = requests.get(source_url, timeout=10)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            return proxies
    except Exception as e:
        print(f"Error fetching from {source_url}: {e}")
    return []

def print_menu():
    print(Colorate.Horizontal(Colors.green_to_cyan, """
 ▄▄▄·▄▄▄        ▐▄• ▄  ▄· ▄▌    .▄▄ ·  ▄▄· ▄▄▄   ▄▄▄·  ▄▄▄· ▄▄▄·▄▄▄ .▄▄▄    +---------------------------+
▐█ ▄█▀▄ █·▪      █▌█▌▪▐█▪██▌    ▐█ ▀. ▐█ ▌▪▀▄ █·▐█ ▀█ ▐█ ▄█▐█ ▄█▀▄.▀·▀▄ █·   [-] UHQ PROXY SCRAPPER
 ██▀·▐▀▀▄  ▄█▀▄  ·██· ▐█▌▐█▪    ▄▀▀▀█▄██ ▄▄▐▀▀▄ ▄█▀▀█  ██▀· ██▀·▐▀▀▪▄▐▀▀▄    [-] Dev by 124P
▐█▪·•▐█•█▌▐█▌.▐▌▪▐█·█▌ ▐█▀·.    ▐█▄▪▐█▐███▌▐█•█▌▐█ ▪▐▌▐█▪·•▐█▪·•▐█▄▄▌▐█•█▌   https://github.com/124Px
.▀   .▀  ▀ ▀█▄▀▪•▀▀ ▀▀  ▀ •      ▀▀▀▀ ·▀▀▀ .▀  ▀ ▀  ▀ .▀   .▀    ▀▀▀ .▀  ▀         
    """,))

def get_proxies(proxy_type, count, country=None):
    sources = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/socks4.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/socks5.txt",
        "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxies.txt",
        "https://raw.githubusercontent.com/Volodichev/proxy-list/main/proxy-list.txt",
    ]

    proxies = []
    threads = []
    for source in sources:
        if len(proxies) >= count * 2:
            break
        thread = threading.Thread(target=get_proxies_from_source_threaded, args=(source, proxies, count))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return proxies[:count * 2]

def get_proxies_from_source_threaded(source_url, proxies, count):
    new_proxies = get_proxies_from_source(source_url)
    if new_proxies:
        proxies.extend(new_proxies)


def check_proxy(proxy, valid_proxies, country_name=None, country_code=None):
    try:
        ip, port = proxy.split(':')
        start_time = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, int(port)))
        end_time = time.time()
        latency = int((end_time - start_time) * 1000)
        sock.close()
        if latency <= 1000:
            if country_name and country_code:
                valid_proxies.append({
                    'proxy': proxy,
                    'country_code': country_code,
                    'country': country_name,
                    'latency': latency
                })
            else:
                try:
                    response = requests.get(f"http://ip-api.com/json/{ip}").json()
                    country_code = response['countryCode']
                    country_name = response['country']
                    valid_proxies.append({
                        'proxy': proxy,
                        'country_code': country_code,
                        'country': country_name,
                        'latency': latency
                    })
                except:
                    valid_proxies.append({
                        'proxy': proxy,
                        'country_code': "Unknown",
                        'country': "Unknown",
                        'latency': latency
                    })
    except:
        pass

def save_proxies(valid_proxies, proxy_type):
    folder_name = f"{proxy_type} [{datetime.now().strftime('%d.%m.%y')}]"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    with open(f"{folder_name}/brut.txt", "w", encoding="utf-8") as brut_file:
        brut_file.write("""                       
┓ ┳┳┳┳┓┳┏┓┏┓  ┏┓┏┓┳┓┏┓┏┓┏┓┏┓┳┓ +-----------------------------+
┃ ┃┃┃┃┃┃ ┃┃   ┗┓┃ ┣┫┣┫┃┃┃┃┣ ┣┫ [-] https://github.com/124Px
┗┛┗┛┛ ┗┻┗┛┗┛  ┗┛┗┛┛┗┛┗┣┛┣┛┗┛┛┗ [-] UHQ Proxy scrapper     
+------------------------------------------------------------+
     """)
        for proxy in valid_proxies:
            brut_file.write(f"{proxy['proxy']}\n")
    
    with open(f"{folder_name}/proxy.txt", "w", encoding="utf-8") as proxy_file:
        proxy_file.write("""    
┓ ┳┳┳┳┓┳┏┓┏┓  ┏┓┏┓┳┓┏┓┏┓┏┓┏┓┳┓ +-----------------------------+
┃ ┃┃┃┃┃┃ ┃┃   ┗┓┃ ┣┫┣┫┃┃┃┃┣ ┣┫ [-] https://github.com/124Px
┗┛┗┛┛ ┗┻┗┛┗┛  ┗┛┗┛┛┗┛┗┣┛┣┛┗┛┛┗ [-] UHQ Proxy scrapper
+------------------------------------------------------------                         
      ╔════════════╦══════╦═════════╦═════════╗
      ║ Proxy:port ║ code ║ country ║ latency ║
      ╚════════════╩══════╩═════════╩═════════╝      

\n""")
        for proxy in valid_proxies:
            proxy_file.write(f"{proxy['proxy']} | {proxy['country_code']} | {proxy['country']} | {proxy['latency']}ms\n")

def main():
    protocol = None
    country = None
    proxy_count = None
    country_name = None
    country_code = None

    while True:

        while True:
            clear_console()
            print_menu()
            print(Colorate.Horizontal(Colors.green_to_cyan, """
              ╔════════════════════════════════════════════════╗
              ║           choose your proxy protocol :         ║
              ╠═══════════════╦════════════════╦═══════════════╣
              ║  [1] -> http  ║ [2] -> socks4  ║ [3] -> socks5 ║
              ╚═══════════════╩════════════════╩═══════════════╝
              """))
            print(Style.RESET_ALL + f"{Fore.GREEN}┌───({Fore.WHITE}{get_pc_name()}@{Fore.WHITE}lumix{Fore.GREEN})─[{Fore.WHITE}~{Fore.GREEN}]")
            print(Style.RESET_ALL + f"{Fore.GREEN}|")
            choice = input("└──$ " + Style.RESET_ALL)

            if choice in ["1", "2", "3"]:
                proxy_types = {1: "http", 2: "socks4", 3: "socks5"}
                protocol = proxy_types[int(choice)]
                break
            else:
                show_invalid_choice()
        clear_console()
        while True:
            colored_specific_country = (
            Colors.cyan + "[" + Colors.white + "?" + Colors.cyan + "] " +
            Colorate.Horizontal(Colors.green_to_cyan, "Do you want proxies from a specific country? (yes/no): \n")
            ) 


            print_menu()
            print()
            print(colored_specific_country)
            print()
            print(Style.RESET_ALL + f"{Fore.GREEN}┌───({Fore.WHITE}{get_pc_name()}@{Fore.WHITE}lumix{Fore.GREEN})─[{Fore.WHITE}~{Fore.GREEN}]")
            print(Style.RESET_ALL + f"{Fore.GREEN}|")
            country_choice = input("└──$ " + Style.RESET_ALL)
            if country_choice in ["yes", "y", "no", "n"]:
                break
            else:
                show_invalid_choice()
            
        clear_console()
        if country_choice in ["yes", "y"]:
            while True:
                print_menu()
                print_settings(protocol, country, proxy_count)
                print(Colorate.Horizontal(Colors.green_to_cyan,"""
              ╔══════════════════════════════════════════════════════════════════════════════════════╗
              ║                                  Choose a country :                                  ║
              ╠════════════╦═══════════════════╦════════════════╦════════════════════╦═══════════════╣
              ║ [1] France ║ [2] United States ║ [3] Germany    ║ [4] United Kingdom ║ [5] Canada    ║
              ╠════════════╬═══════════════════╬════════════════╬════════════════════╬═══════════════╣
              ║ [6] Japan  ║ [7] Australia     ║ [8] Netherlands║ [9] Switzerland    ║ [10] Sweden   ║
              ╠════════════╬═══════════════════╬════════════════╬════════════════════╬═══════════════╣
              ║ [11] Spain ║ [12] Italy        ║ [13] Brazil    ║ [14] India         ║ [15] Russia   ║
              ╚════════════╩═══════════════════╩════════════════╩════════════════════╩═══════════════╝     
                  """))


                print(Style.RESET_ALL + f"{Fore.GREEN}┌───({Fore.WHITE}{get_pc_name()}@{Fore.WHITE}lumix{Fore.GREEN})─[{Fore.WHITE}~{Fore.GREEN}]")
                print(Style.RESET_ALL + f"{Fore.GREEN}|")
                country_code_input = input("└──$ " + Style.RESET_ALL)
                countries = {
                    1: ("FR", "France"), 2: ("US", "United States"), 3: ("DE", "Germany"),
                    4: ("GB", "United Kingdom"), 5: ("CA", "Canada"), 6: ("JP", "Japan"),
                    7: ("AU", "Australia"), 8: ("NL", "Netherlands"), 9: ("CH", "Switzerland"),
                    10: ("SE", "Sweden"), 11: ("ES", "Spain"), 12: ("IT", "Italy"),
                    13: ("BR", "Brazil"), 14: ("IN", "India"), 15: ("RU", "Russia")
                }

                if country_code_input.isdigit() and int(country_code_input) in countries:
                    country_code, country_name = countries[int(country_code_input)]
                    country = country_name
                    break
                else:
                    show_invalid_choice()
                    print_settings(protocol, country, proxy_count)

        else:
            country = "all"

        clear_console()

        while True:
            colored_many = (
            Colors.cyan + "\n[" + Colors.white + "?" + Colors.cyan + "] " +
            Colorate.Horizontal(Colors.green_to_cyan, "How many proxies do you want? (0 - 10000)\n")
            ) 


            print_menu()
            print_settings(protocol, country, proxy_count)
            print(colored_many)
            print(Style.RESET_ALL + f"\n{Fore.GREEN}┌───({Fore.WHITE}{get_pc_name()}@{Fore.WHITE}lumix{Fore.GREEN})─[{Fore.WHITE}~{Fore.GREEN}]")
            print(Style.RESET_ALL + f"{Fore.GREEN}|")
            proxy_count_input = input("└──$ " + Style.RESET_ALL)
            if proxy_count_input.isdigit() and int(proxy_count_input) > 0:
                proxy_count = int(proxy_count_input)
                break
            else:
                show_invalid_choice()
                print_settings(protocol, country, proxy_count)

        clear_console()

        print_menu()
        print_settings(protocol, country, proxy_count)
        valid_proxies = []
        attempts = 0
        max_attempts = 30

        while len(valid_proxies) < proxy_count and attempts < max_attempts:
            proxies = get_proxies(protocol, proxy_count * 5, country_code if country != "all" else None)
            threads = []

            for proxy in proxies:
                thread = threading.Thread(target=check_proxy, args=(proxy, valid_proxies, country_name, country_code))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            attempts += 1
            print(Colorate.Horizontal(Colors.green_to_cyan, f"\n[~] Attempt {attempts}: Found {len(valid_proxies)} valid proxies. {proxy_count - len(valid_proxies)} more needed.\n"))

        for proxy in valid_proxies:
            print(f"{Fore.GREEN}[Valid]{Style.RESET_ALL} {proxy['proxy']} | {proxy['country_code']} | {proxy['country']} | {proxy['latency']}ms")

        save_proxies(valid_proxies, protocol)
        print(Colorate.Horizontal(Colors.green_to_cyan, f"\n[~] {len(valid_proxies)} valid proxies saved in '{protocol} [{datetime.now().strftime('%d.%m.%y')}]' folder."))

        while True:
            quit_choice = input(colored_quitt_txt).strip().lower()
            if quit_choice in ["yes", "y"]:
                print(colored_returnmenu_txt)
                time.sleep(1)
                protocol = None
                country = None
                proxy_count = None
                break
            elif quit_choice in ["no", "n"]:
                print(colored_exit_txt)
                time.sleep(2)
                return
            else:
                show_invalid_choice()
                print_settings(protocol, country, proxy_count)





if __name__ == "__main__":
    main()