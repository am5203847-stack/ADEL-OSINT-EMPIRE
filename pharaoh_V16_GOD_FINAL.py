#!/usr/bin/env python3
# EYE - PHARAOH V16 ULTIMATE GOD - By Adel El Tabarex King
import os, sys, socket, requests, json, phonenumbers
from phonenumbers import geocoder, carrier, number_type
from datetime import datetime
import time

G="\033[92m"; C="\033[96m"; Y="\033[93m"; R="\033[91m"; W="\033[97m"
BOLD="\033[1m"; RESET="\033[0m"

def banner():
    os.system('clear')
    print(f"{G}{BOLD}")
    print("  ███████╗██╗   ██╗███████╗")
    print("  ██╔════╝╚██╗ ██╔╝██╔════╝")
    print("  █████╗   ╚████╔╝ █████╗")
    print("  ██╔══╝    ╚██╔╝  ██╔══╝")
    print("  ███████╗   ██║   ███████╗")
    print(f"{C}{BOLD}        EYE - PHARAOH V16 ULTIMATE GOD")
    print(f"{Y}{BOLD}[+] Welcome Pharaoh Adel - El Tabarex King 👑 GOD ULTIMATE")
    print(f"{W}--------------------------------------------------")
    print(f"Date: {datetime.now().strftime('%a %b %d %H:%M:%S %Y')} | Location: Giza EG")
    print(f"--------------------------------------------------{RESET}")
    print(f"  {G}[1] OSINT GOD   [2] SCAN GOD   [3] TOOLS ULTIMATE   [4] EXIT GOD{RESET}\n")

def osint_god():
    banner()
    print(f"{Y}--- OSINT GOD V16 ---{RESET}")
    username=input(f"{C}Username > {RESET}").strip()
    if not username: return
    sites=[f"https://github.com/{username}",f"https://instagram.com/{username}",f"https://twitter.com/{username}",f"https://www.tiktok.com/@{username}",f"https://www.facebook.com/{username}",f"https://www.reddit.com/user/{username}",f"https://t.me/{username}",f"https://medium.com/@{username}",f"https://www.youtube.com/@{username}",f"https://www.pinterest.com/{username}/",f"https://www.snapchat.com/add/{username}"]
    found=[]
    for url in sites:
        try:
            r=requests.get(url, timeout=5, headers={"User-Agent":"Mozilla/5.0"})
            if r.status_code==200:
                print(f"{G}[FOUND] {url}{RESET}")
                found.append(url)
            else:
                print(f"{R}[NOT] {url}{RESET}")
        except:
            print(f"{R}[ERR] {url}{RESET}")
    with open(f"{username}_V16.txt","w") as f:
        f.write("\n".join(found))
    print(f"{W}Saved to {username}_V16.txt - {len(found)} found{RESET}")
    input("Enter...")

def scan_god():
    banner()
    print(f"{Y}--- SCAN GOD V16 ---{RESET}")
    target=input(f"{C}IP/Domain > {RESET}").strip()
    if not target: return
    try:
        ip=socket.gethostbyname(target)
        print(f"{C}Target IP: {ip}{RESET}")
        ports=[21,22,23,25,53,80,110,135,139,443,445,993,995,3306,3389,8080,8443]
        for p in ports:
            s=socket.socket()
            s.settimeout(0.8)
            try:
                if s.connect_ex((ip,p))==0:
                    print(f"{G}[OPEN] {p}{RESET}")
                else:
                    print(f"{R}[CLOSED] {p}{RESET}")
            except: pass
            s.close()
    except Exception as e:
        print(f"{R}Error: {e}{RESET}")
    input("Enter...")

def my_ip_god():
    banner()
    print(f"{Y}--- MY IP & AUTO MAP GOD ---{RESET}")
    try:
        r=requests.get("https://ipinfo.io/json", timeout=8).json()
        ip=r.get('ip','?'); city=r.get('city','?'); country=r.get('country','?'); loc=r.get('loc','')
        print(f"{G}IP: {ip}{RESET}")
        print(f"{C}City: {city} - {country}{RESET}")
        print(f"{C}Loc: {loc}{RESET}")
        if loc:
            lat,lon=loc.split(',')
            print(f"{W}Map: https://maps.google.com/?q={lat},{lon}{RESET}")
    except Exception as e:
        print(f"{R}Error: {e}{RESET}")
    input("Enter...")

def whois_god():
    banner()
    target=input(f"{C}Domain/IP > {RESET}").strip()
    if not target: return
    try:
        r=requests.get(f"https://who.is/whois/{target}", timeout=8, headers={"User-Agent":"Mozilla/5.0"})
        print(f"{W}{r.text[:1000]}{RESET}")
    except Exception as e:
        print(f"{R}Error: {e}{RESET}")
    input("Enter...")

def phone_god():
    banner()
    print(f"{Y}--- PHONE LOOKUP ULTIMATE V16 ---{RESET}")
    phone=input(f"{C}Phone with + (ex: +201234567890) > {RESET}").strip()
    if not phone: return
    if phone.startswith("01"):
        phone="+2"+phone
        print(f"{Y}[*] Fixed to {phone}{RESET}")
    elif phone.startswith("0"):
        phone="+20"+phone[1:]
        print(f"{Y}[*] Fixed to {phone}{RESET}")
    try:
        num=phonenumbers.parse(phone, None)
        valid=phonenumbers.is_valid_number(num)
        print(f"{G}✅ Valid: {valid}{RESET}")
        print(f"{C}Country: {geocoder.description_for_number(num, 'en')}{RESET}")
        print(f"{C}Carrier: {carrier.name_for_number(num, 'en')}{RESET}")
        print(f"{Y}Type: {number_type(num)} (1=MOBILE){RESET}")
        print(f"{W}TrueCaller: https://www.truecaller.com/search/{phone} ✅{RESET}")
    except Exception as e:
        print(f"{R}Error: {e}{RESET}")
    input("Enter...")

def insta_god():
    banner()
    print(f"{Y}--- INSTAGRAM REAL INFO ULTIMATE V16 ---{RESET}")
    user=input(f"{C}Username > {RESET}").strip()
    if not user: return
    try:
        headers={"User-Agent":"Mozilla/5.0 (Linux; Android 10)"}
        r=requests.get(f"https://www.instagram.com/{user}/", headers=headers, timeout=10)
        if r.status_code==200:
            print(f"{G}[FOUND] https://instagram.com/{user}{RESET}")
            try:
                if '"biography":"' in r.text:
                    bio=r.text.split('"biography":"')[1].split('"')[0][:100]
                    print(f"{C}Bio: {bio}{RESET}")
                if '"edge_followed_by":{"count":' in r.text:
                    foll=r.text.split('"edge_followed_by":{"count":')[1].split('}')[0]
                    print(f"{G}Followers: {foll}{RESET}")
                if '"edge_follow":{"count":' in r.text:
                    following=r.text.split('"edge_follow":{"count":')[1].split('}')[0]
                    print(f"{C}Following: {following}{RESET}")
            except: pass
        else:
            print(f"{R}Not Found {r.status_code}{RESET}")
        print(f"{W}Link: https://instagram.com/{user}{RESET}")
    except Exception as e:
        print(f"{R}Error: {e}{RESET}")
    input("Enter...")

def email_god():
    banner()
    print(f"{Y}--- EMAIL LEAK CHECK V16 ---{RESET}")
    email=input(f"{C}Email > {RESET}").strip()
    if not email: return
    print(f"{W}Checking {email} on haveibeenpwned...{RESET}")
    print(f"{C}Link: https://haveibeenpwned.com/account/{email}{RESET}")
    print(f"{C}Dehashed: https://dehashed.com/search?query={email}{RESET}")
    input("Enter...")

def tools_menu():
    while True:
        banner()
        print(f"{Y}TOOLS V16 ULTIMATE:{RESET}")
        print(f"{C}[a] My IP & Auto Map GOD{RESET}")
        print(f"{W}[b] Whois Lookup{RESET}")
        print(f"{Y}[c] Phone Lookup REAL ULTIMATE NEW{RESET}")
        print(f"{C}[d] Email Leak Check ULTIMATE NEW{RESET}")
        print(f"{G}[e] Instagram Real Info ULTIMATE NEW{RESET}")
        print(f"{W}[f] Full Ultimate Report{RESET}")
        print(f"{Y}[g] Update System{RESET}")
        print(f"{C}[h] Back to Menu{RESET}\n")
        ch=input(f"{Y}Choose > {RESET}").strip().lower()
        if ch=='a': my_ip_god()
        elif ch=='b': whois_god()
        elif ch=='c': phone_god()
        elif ch=='d': email_god()
        elif ch=='e': insta_god()
        elif ch=='f':
            my_ip_god()
        elif ch=='g':
            os.system('apt update && apt upgrade -y')
            input("Enter...")
        elif ch=='h': break

def main():
    while True:
        banner()
        ch=input(f"{Y}Choose [1-4] > {RESET}").strip()
        if ch=='1': osint_god()
        elif ch=='2': scan_god()
        elif ch=='3': tools_menu()
        elif ch=='4':
            print(f"{Y}Goodbye King Adel - V16 ULTIMATE CLOSED 👑{RESET}")
            break

if __name__=="__main__":
    main()
