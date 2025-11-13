#!/usr/bin/env python3
import os
import sys
import requests
import dns.resolver
import socket
import subprocess
import ipaddress
import instaloader
from colorama import init as colorama_init, Fore, Style

colorama_init(autoreset=True)
# ----------------------------------------------------
#Dont touch any of the code dm p6sd if having problems
# ----------------------------------------------------
BANNER = f"""
{Fore.MAGENTA}{Style.BRIGHT}
  ██████╗  ██████╗ ███████╗██╗███╗   ██╗████████╗
 ██╔═══██╗██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
 ██║   ██║██║   ██║███████╗██║██╔██╗ ██║   ██║   
 ██║▄▄ ██║██║   ██║╚════██║██║██║╚██╗██║   ██║   
 ╚██████╔╝╚██████╔╝███████║██║██║ ╚████║   ██║   
  ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝    

       OSINT + Network Utility
               by: p6sd
{Style.RESET_ALL}
"""

LEGAL_NOTICE = f"""{Fore.YELLOW}{Style.BRIGHT}
[!] Ethical Use Only — Perform scans and lookups only on assets you own or have permission to test.
Press Enter to continue...{Style.RESET_ALL}
"""

# -----------------------------
# Utility Functions
# -----------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    clear()
    print(BANNER)
    print("=" * 80)

def draw_menu():
    col_w = 32
    gap = 3

    network_scanner = [
        "1. Ping Sweep (CIDR)",
        "2. Port Scanner (host & port range)",
        "3. Subnet Info (CIDR summary)",
        "4. DNS Resolve (hostname → IPs)",
        "5. Ping Host (single)",
        "6. Back"
    ]

    osint_tools = [
        "10. IP Lookup (ip-api)",
        "11. Email Check (format + MX)",
        "12. Instagram Username Lookup",
        "13. Whois Lookup (stub)",
        "14. Metadata Extract (stub)",
        "15. Social Media API (stub)",
        "16. Back"
    ]

    utilities = [
        "20. Clear Screen",
        "21. Check Dependencies",
        "22. Show Config",
        "23. About",
        "24. Exit"
    ]

    # Section Headers with Line Separation
    print(f"{Fore.GREEN}{'Network Scanner'.center(col_w)}{' '*gap}"
          f"{'OSINT Tools'.center(col_w)}{' '*gap}"
          f"{'Utilities'.center(col_w)}{Fore.RESET}")
    print("-" * (col_w * 3 + gap * 2))  # Line separator

    max_len = max(len(network_scanner), len(osint_tools), len(utilities))
    network_scanner += [""] * (max_len - len(network_scanner))
    osint_tools += [""] * (max_len - len(osint_tools))
    utilities += [""] * (max_len - len(utilities))

    for n, o, u in zip(network_scanner, osint_tools, utilities):
        print(f"{n:<{col_w}}{' '*gap}{o:<{col_w}}{' '*gap}{u:<{col_w}}")

    print("-" * (col_w * 3 + gap * 2))  # Line separator
    print(f"{Fore.YELLOW}Discord: p6sd{Fore.RESET}")
    print("-" * (col_w * 3 + gap * 2))

# -----------------------------
# IP Lookup using ip-api (no API key)
# -----------------------------
def ip_lookup(ip=None):
    try:
        url = f"http://ip-api.com/json/{ip}" if ip else "http://ip-api.com/json"
        response = requests.get(url)
        data = response.json()

        if data.get("status") == "fail":
            print(f"{Fore.RED}Error: {data['message']}")
            return

        print(f"{Fore.GREEN}IP: {data.get('query')}")
        print(f"City: {data.get('city')}")
        print(f"Region: {data.get('regionName')}")
        print(f"Country: {data.get('country')}")
        print(f"Org: {data.get('org')}")
    except Exception as e:
        print(f"{Fore.RED}Request failed: {e}")

# -----------------------------
# Instagram Username Lookup
# -----------------------------
def instagram_lookup(username):
    L = instaloader.Instaloader()

    try:
        # Load Instagram profile
        profile = instaloader.Profile.from_username(L.context, username)

        print(f"{Fore.GREEN}Instagram Profile for {username}:")

        # Profile details
        print(f"Username: {profile.username}")
        print(f"Full Name: {profile.full_name}")
        print(f"Bio: {profile.biography}")
        print(f"Followers: {profile.followers}")
        print(f"Following: {profile.followees}")
        print(f"Posts: {profile.mediacount}")
        print(f"Private: {'Yes' if profile.is_private else 'No'}")
        print(f"Verified: {'Yes' if profile.is_verified else 'No'}")

    except Exception as e:
        print(f"{Fore.RED}Error: {e}")

# -----------------------------
# Email Lookup (MX Records)
# -----------------------------
def email_lookup(email):
    try:
        domain = email.split("@")[1]
        records = dns.resolver.resolve(domain, "MX")
        print(f"{Fore.GREEN}MX records for {domain}:")
        for r in records:
            print(f" - {r.exchange}")
    except Exception as e:
        print(f"{Fore.RED}Failed: {e}")

# -----------------------------
# Username Lookup (stub)
# -----------------------------
def username_lookup(username):
    print(f"{Fore.YELLOW}Searching for username '{username}' on social media... (stub)")
    print("Feature not fully implemented yet.")

# -----------------------------
# Network Functions
# -----------------------------
def ping_host(ip):
    param = "-n" if os.name == "nt" else "-c"
    try:
        result = subprocess.run(["ping", param, "1", ip], capture_output=True, text=True, timeout=5)
        print(result.stdout)
    except subprocess.TimeoutExpired:
        print(f"{Fore.RED}Ping timed out.{Fore.RESET}")

def ping_sweep_cidr(cidr):
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except ValueError:
        print(f"{Fore.RED}Invalid CIDR notation.{Fore.RESET}")
        return
    print(f"Pinging all hosts in {cidr}...")
    live_hosts = []
    param = "-n" if os.name == "nt" else "-c"
    for ip in net.hosts():
        ip_str = str(ip)
        result = subprocess.run(["ping", param, "1", ip_str], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{ip_str} is alive")
            live_hosts.append(ip_str)
        else:
            print(f"{ip_str} no response")
    print(f"Live hosts: {', '.join(live_hosts) if live_hosts else 'None'}")

def port_scanner(host, port_range):
    try:
        start_port, end_port = map(int, port_range.split("-"))
        if not (0 < start_port <= end_port < 65536):
            raise ValueError
    except Exception:
        print(f"{Fore.RED}Invalid port range. Use format: start-end (e.g. 20-80){Fore.RESET}")
        return

    print(f"Scanning ports {start_port}-{end_port} on {host} ...")
    open_ports = []
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            try:
                s.connect((host, port))
                print(f"Port {port}: OPEN")
                open_ports.append(port)
            except Exception:
                pass
    if open_ports:
        print(f"Open ports on {host}: {', '.join(map(str, open_ports))}")
    else:
        print("No open ports found.")

def subnet_info(cidr):
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except ValueError:
        print(f"{Fore.RED}Invalid CIDR.{Fore.RESET}")
        return
    print(f"Network: {net.network_address}")
    print(f"Netmask: {net.netmask}")
    print(f"Broadcast: {net.broadcast_address}")
    print(f"Number of hosts: {net.num_addresses}")
    print(f"Usable hosts: {net.num_addresses - 2 if net.num_addresses > 2 else net.num_addresses}")

def dns_resolve(hostname):
    try:
        ips = socket.gethostbyname_ex(hostname)[2]
        print(f"IPs for {hostname}: {', '.join(ips)}")
    except socket.gaierror:
        print(f"{Fore.RED}Hostname could not be resolved.{Fore.RESET}")

# -----------------------------
# Utility functions
# -----------------------------
def check_dependencies():
    print("Checking installed dependencies:")
    modules = {
        "requests": requests,
        "dnspython": dns,
        "instaloader": instaloader,
        "colorama": "Available"  # colorama is loaded or fallback
    }
    for mod, val in modules.items():
        status = "Installed" if val else "Not Installed"
        print(f" - {mod}: {status}")

def show_config():
    import platform
    print(f"Python version: {platform.python_version()}")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"User: {os.getlogin()}")
    print(f"Working directory: {os.getcwd()}")

def about():
    print(Fore.CYAN + "OSINT Dashboard" + Fore.RESET)
    print("Created by p6sd")
    print("Ethical use only! Use responsibly.")

# -----------------------------
# Main menu handler
# -----------------------------
def handle_network_scanner(choice):
    if choice == "1":
        cidr = input("Enter CIDR (e.g. 192.168.1.0/24): ").strip()
        ping_sweep_cidr(cidr)
    elif choice == "2":
        host = input("Enter hostname or IP: ").strip()
        port_range = input("Enter port range (start-end, e.g. 20-80): ").strip()
        port_scanner(host, port_range)
    elif choice == "3":
        cidr = input("Enter CIDR (e.g. 192.168.1.0/24): ").strip()
        subnet_info(cidr)
    elif choice == "4":
        hostname = input("Enter hostname: ").strip()
        dns_resolve(hostname)
    elif choice == "5":
        ip = input("Enter IP address: ").strip()
        ping_host(ip)
    elif choice == "6":
        return "back"
    else:
        print(f"{Fore.RED}Invalid option.{Fore.RESET}")

def handle_osint_tools(choice):
    if choice == "10":
        ip = input("Enter IP (leave blank for your own): ").strip() or "json"
        ip_lookup(ip)
    elif choice == "11":
        email = input("Enter email: ").strip()
        email_lookup(email)
    elif choice == "12":
        username = input("Enter Instagram username: ").strip()
        instagram_lookup(username)
    elif choice == "13":
        print("Whois Lookup is a stub - coming soon.")
    elif choice == "14":
        print("Metadata Extract is a stub - coming soon.")
    elif choice == "15":
        print("Social Media API is a stub - coming soon.")
    elif choice == "16":
        return "back"
    else:
        print(f"{Fore.RED}Invalid option.{Fore.RESET}")

def handle_utilities(choice):
    if choice == "20":
        clear()
    elif choice == "21":
        check_dependencies()
    elif choice == "22":
        show_config()
    elif choice == "23":
        about()
    elif choice == "24":
        print("Exiting...")
        sys.exit()
    else:
        print(f"{Fore.RED}Invalid option.{Fore.RESET}")

def main():
    while True:
        print_banner()
        draw_menu()
        choice = input("Select an option: ").strip()

        if choice in ["1", "2", "3", "4", "5", "6"]:
            handle_network_scanner(choice)
        elif choice in ["10", "11", "12", "13", "14", "15", "16"]:
            handle_osint_tools(choice)
        elif choice in ["20", "21", "22", "23", "24"]:
            handle_utilities(choice)
        else:
            print(f"{Fore.RED}Invalid choice.{Fore.RESET}")

        input(f"{Fore.MAGENTA}Press Enter to continue...")

if __name__ == "__main__":
    main()
