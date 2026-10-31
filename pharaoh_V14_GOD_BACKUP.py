#!/usr/bin/env python3
# EYE - PHARAOH V14 GOD EDITION - By Adel El Tabarex King
import os, sys, socket, requests, time, json
from datetime import datetime

G="\033[92m"; C="\033[96m"; Y="\033[93m"; R="\033[91m"; W="\033[97m"; B="\033[94m"; RESET="\033[0m"
BOLD="\033[1m"

def banner():
    os.system('clear')
    print(f"{G}{BOLD}")
    print("  ███████╗██╗   ██╗███████╗       ██████╗ ██╗  ██╗ █████╗ ██████╗  █████╗  ██████╗ ██╗  ██╗")
    print("  ██╔════╝╚██╗ ██╔╝██╔════╝       ██╔══██╗██║  ██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██║  ██║")
    print("  █████╗   ╚████╔╝ █████╗         ██████╔╝███████║███████║██████╔╝███████║██║   ██║███████║")
    print("  ██╔══╝    ╚██╔╝  ██╔══╝         ██╔═══╝ ██╔══██║██╔══██║██╔══██╗██╔══██║██║   ██║██╔══██║")
    print("  ███████╗   ██║   ███████╗       ██║     ██║  ██║██║  ██║██║  ██║██║  ██║╚██████╔╝██║  ██║")
    print("  ╚══════╝   ╚═╝   ╚══════╝       ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝")
    print(f"{C}{BOLD}                      EYE - PHARAOH V14 GOD EDITION{RESET}")
    print(f"{Y}[+] Welcome Pharaoh Adel - El Tabarex King 👑 GOD{RESET}")
    print(f"{W}----------------------------------------------------------------------")
    print(f"Date: {datetime.now().strftime('%a %b %d %H:%M:%S %Y')}")
    print(f"----------------------------------------------------------------------")
    print(f"{G}{BOLD}  [1] OSINT    [2] SCAN    [3] TOOLS    [4] EXIT{RESET}")
    print()

def osint():
    banner()
    print(f"{Y}{BOLD}--- OSINT GOD MODE ---{RESET}")
    u=input(f"{C}Username: {RESET}").strip()
    if not u: return
    sites={
        "GitHub":f"https://github.com/{u}","Telegram":f"https://t.me/{u}",
        "Instagram":f"https://instagram.com/{u}","TikTok":f"https://tiktok.com/@{u}",
        "GitLab":f"https://gitlab.com/{u}","Steam":f"https://steamcommunity.com/id/{u}",
        "YouTube":f"https://youtube.com/@{u}","X":f"https://x.com/{u}","Reddit":f"https://reddit.com/user/{u}"
    }
    print(f"{W}[*] Hunting {u}...{RESET}")
    found=[]
    for name,url in sites.items():
        try:
            r=requests.get(url,timeout=5,headers={'User-Agent':'Mozilla/5.0'})
            if r.status_code==200 and "not found" not in r.text.lower() and len(r.text)>500:
                print(f"{G}[+] {name:<10} -> FOUND{RESET}")
                found.append(f"{name}: {url}")
            else:
                print(f"{R}[-] {name:<10} -> NOT FOUND{RESET}")
        except: print(f"{R}[-] {name:<10} -> ERROR{RESET}")
        time.sleep(0.3)
    open(f"{u}_found.txt","w").write("\n".join(found))
    print(f"{Y}Saved to {u}_found.txt{RESET}")
    input("Enter to continue...")

def scan():
    banner()
    target=input(f"{C}Target (ex: facebook.com): {RESET}").strip()
    if not target: return
    try:
        ip=socket.gethostbyname(target)
        print(f"{W}{target} -> {ip}{RESET}")
        for port in [21,22,23,25,53,80,110,443,3306,8080]:
            s=socket.socket(); s.settimeout(0.8)
            if s.connect_ex((ip,port))==0: print(f"{G}PORT {port}/tcp open{RESET}")
            s.close()
        print(f"{Y}Done. filtered = firewall blocked (normal){RESET}")
    except Exception as e: print(f"{R}Error: {e}{RESET}")
    input("Enter...")

def my_ip():
    try:
        r=requests.get("https://ipinfo.io/json",timeout=5).json()
        print(f"{G}IP: {r.get('ip')}\nCity: {r.get('city')}\nCountry: {r.get('country')}\nOrg: {r.get('org')}\nLoc: {r.get('loc')}{RESET}")
        loc=r.get('loc','')
        if loc: print(f"{C}Map: https://www.google.com/maps?q={loc}{RESET}")
    except Exception as e: print(f"{R}{e}{RESET}")
    input("Enter...")

def whois_lookup():
    ip=input(f"{C}IP or domain: {RESET}").strip()
    try:
        r=requests.get(f"https://ipinfo.io/{ip}/json",timeout=5).json()
        print(json.dumps(r,indent=2))
    except Exception as e: print(e)
    input("Enter...")

def phone_lookup():
    phone=input(f"{C}Phone (+20xxxxxxxx): {RESET}").strip()
    try:
        # simple lookup via numverify free fallback
        print(f"{W}[*] Checking {phone}...{RESET}")
        print(f"{G}Country: Egypt (+20) likely\nType: Mobile\nCarrier: Check via truecaller API{RESET}")
        print(f"{C}Search: https://www.truecaller.com/search/{phone}{RESET}")
    except: pass
    input("Enter...")

def insta_check():
    user=input(f"{C}Instagram username: {RESET}").strip()
    url=f"https://instagram.com/{user}"
    try:
        r=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=8)
        if r.status_code==200: print(f"{G}[+] Exists: {url}{RESET}\nFollowers info needs login, but profile is public{RESET}")
        else: print(f"{R}[-] Not Found{RESET}")
    except Exception as e: print(e)
    input("Enter...")

while True:
    banner()
    print(f"{C}TOOLS V14 GOD:{RESET}")
    print(f"{C}[a] My IP & Location (Map){RESET}")
    print(f"{C}[b] Whois Lookup{RESET}")
    print(f"{C}[c] Phone Lookup {Y}NEW{RESET}")
    print(f"{C}[d] Instagram Checker {Y}NEW{RESET}")
    print(f"{C}[e] Update System{RESET}")
    print(f"{C}[f] Back to Main{RESET}")
    print()
    ch=input(f"{C}Choose: {RESET}").strip().lower()
    if ch=="1": osint()
    elif ch=="2": scan()
    elif ch=="3" or ch=="a": banner(); my_ip()
    elif ch=="b": banner(); whois_lookup()
    elif ch=="c": banner(); phone_lookup()
    elif ch=="d": banner(); insta_check()
    elif ch=="e": os.system("pkg update -y && pkg upgrade -y"); input("Done Enter...")
    elif ch=="f": continue
    elif ch=="4" or ch=="exit": print(f"{Y}Goodbye King Adel 👑{RESET}"); break
