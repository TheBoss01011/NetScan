#!/usr/bin/env python3
"""
====================================================
  NetScan - Simple Network Scanner
  By: Mosaab Afrit (TheBoss01011)
  GitHub: https://github.com/TheBoss01011
====================================================
"""

import socket
import subprocess
import platform
import sys
from datetime import datetime


# ─────────────────────────────────────────
#  COLORS (for terminal output)
# ─────────────────────────────────────────
class Colors:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    RESET  = "\033[0m"
    BOLD   = "\033[1m"


def banner():
    print(f"""
{Colors.CYAN}{Colors.BOLD}
 ███╗   ██╗███████╗████████╗███████╗ ██████╗ █████╗ ███╗   ██╗
 ████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔════╝██╔══██╗████╗  ██║
 ██╔██╗ ██║█████╗     ██║   ███████╗██║     ███████║██╔██╗ ██║
 ██║╚██╗██║██╔══╝     ██║   ╚════██║██║     ██╔══██║██║╚██╗██║
 ██║ ╚████║███████╗   ██║   ███████║╚██████╗██║  ██║██║ ╚████║
 ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Colors.RESET}
{Colors.YELLOW}         Simple Network Scanner — by Mosaab Afrit{Colors.RESET}
{Colors.WHITE}         GitHub: github.com/TheBoss01011{Colors.RESET}
    """)


# ─────────────────────────────────────────
#  FEATURE 1: Get Your IP Address
# ─────────────────────────────────────────
def get_my_ip():
    print(f"\n{Colors.BOLD}{Colors.BLUE}[ My IP Address ]{Colors.RESET}")
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        # Get public IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        print(f"  {Colors.GREEN}✔ Hostname  :{Colors.RESET} {hostname}")
        print(f"  {Colors.GREEN}✔ Local IP  :{Colors.RESET} {local_ip}")
        return local_ip
    except Exception as e:
        print(f"  {Colors.RED}✘ Error: {e}{Colors.RESET}")
        return None


# ─────────────────────────────────────────
#  FEATURE 2: Ping a Host (is it alive?)
# ─────────────────────────────────────────
def ping_host(host):
    print(f"\n{Colors.BOLD}{Colors.BLUE}[ Ping Host ]{Colors.RESET}")
    print(f"  Pinging {Colors.YELLOW}{host}{Colors.RESET} ...")

    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "3", host]

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"  {Colors.GREEN}✔ Host is ALIVE — {host} is reachable!{Colors.RESET}")
        else:
            print(f"  {Colors.RED}✘ Host is DOWN — {host} did not respond.{Colors.RESET}")
    except subprocess.TimeoutExpired:
        print(f"  {Colors.RED}✘ Timeout — no response from {host}{Colors.RESET}")
    except Exception as e:
        print(f"  {Colors.RED}✘ Error: {e}{Colors.RESET}")


# ─────────────────────────────────────────
#  FEATURE 3: Port Scanner
# ─────────────────────────────────────────
COMMON_PORTS = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    143:  "IMAP",
    443:  "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}

def scan_ports(host):
    print(f"\n{Colors.BOLD}{Colors.BLUE}[ Port Scanner ]{Colors.RESET}")
    print(f"  Scanning {Colors.YELLOW}{host}{Colors.RESET} for open ports...")
    print(f"  {Colors.WHITE}Started at: {datetime.now().strftime('%H:%M:%S')}{Colors.RESET}\n")

    open_ports = []

    for port, service in COMMON_PORTS.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"  {Colors.GREEN}✔ Port {port:5d}  OPEN    [{service}]{Colors.RESET}")
                open_ports.append(port)
            else:
                print(f"  {Colors.RED}✘ Port {port:5d}  closed  [{service}]{Colors.RESET}")
            sock.close()
        except Exception:
            pass

    print(f"\n  {Colors.YELLOW}Scan complete. {len(open_ports)} open port(s) found.{Colors.RESET}")
    return open_ports


# ─────────────────────────────────────────
#  FEATURE 4: DNS Lookup
# ─────────────────────────────────────────
def dns_lookup(domain):
    print(f"\n{Colors.BOLD}{Colors.BLUE}[ DNS Lookup ]{Colors.RESET}")
    print(f"  Looking up: {Colors.YELLOW}{domain}{Colors.RESET}")
    try:
        ip = socket.gethostbyname(domain)
        print(f"  {Colors.GREEN}✔ IP Address: {ip}{Colors.RESET}")
    except socket.gaierror:
        print(f"  {Colors.RED}✘ Could not resolve {domain}{Colors.RESET}")


# ─────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────
def main():
    banner()

    while True:
        print(f"\n{Colors.BOLD}{Colors.WHITE}════════════════════════════════{Colors.RESET}")
        print(f"{Colors.CYAN}  [1] Get My IP Address")
        print(f"  [2] Ping a Host")
        print(f"  [3] Scan Ports")
        print(f"  [4] DNS Lookup")
        print(f"  [0] Exit{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.WHITE}════════════════════════════════{Colors.RESET}")

        choice = input(f"\n{Colors.YELLOW}  Choose an option: {Colors.RESET}").strip()

        if choice == "1":
            get_my_ip()

        elif choice == "2":
            host = input(f"  {Colors.WHITE}Enter host/IP to ping: {Colors.RESET}").strip()
            if host:
                ping_host(host)

        elif choice == "3":
            host = input(f"  {Colors.WHITE}Enter host/IP to scan: {Colors.RESET}").strip()
            if host:
                scan_ports(host)

        elif choice == "4":
            domain = input(f"  {Colors.WHITE}Enter domain (e.g. google.com): {Colors.RESET}").strip()
            if domain:
                dns_lookup(domain)

        elif choice == "0":
            print(f"\n  {Colors.CYAN}Goodbye! Stay secure. 🔐{Colors.RESET}\n")
            sys.exit(0)

        else:
            print(f"  {Colors.RED}Invalid option. Try again.{Colors.RESET}")


if __name__ == "__main__":
    main()
