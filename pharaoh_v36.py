#!/usr/bin/env python3
# PHARAOH EYE V36 - FINAL BOSS
# By ADEL DIAMOND

import requests, socket, ssl, re
from datetime import datetime as dt

Y = "\033[93m"; G = "\033[92m"; R = "\033[91m"; C = "\033[96m"; W = "\033[0m"

def banner():
    print(f"{Y}╔════════════════════════════════════╗{W}")
    print(f"{Y}║  PHARAOH EYE V36 - FINAL BOSS    ║{W}")
    print(f"{Y}╚════════════════════════════════════╝{W}")

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        print(f"{G}[IP] {ip}{W}\n{C}[LOC] {r.get('country')}/{r.get('city')} - {r.get('isp')}{W}")
        return ip, r
    except: return "N/A", {}

def dns(domain):
    print("\n--- [2] DNS ---")
    for t in ["A","MX","NS","TXT"]:
        try:
            j = requests.get(f"https://dns.google/resolve?name={domain}&type={t}", timeout=5).json()
            if "Answer" in j:
                for a in j["Answer"][:3]:
                    print(f"{G}[{t}] {a['data']}{W}")
        except: pass

def whois(domain):
    print("\n--- [3] WHOIS ---")
    try:
        j = requests.get(f"https://rdap.org/domain/{domain}", timeout=7).json()
        for ev in j.get("events",[]):
            if ev["eventAction"]=="registration":
                d=ev["eventDate"][:10]
                print(f"{G}[CREATED] {d}{W}")
                try:
                    age=(dt.now()-dt.strptime(d,"%Y-%m-%d")).days//365
                    print(f"{C}[AGE] {age} Years{W}")
                except: pass
    except: print(f"{Y}[INFO] RDAP busy{W}")

def ssl_check(domain):
    print("\n--- [4] SSL [V36] ---")
    try:
        ctx=ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5); s.connect((domain,443))
            cert=s.getpeercert()
            exp=dt.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            print(f"{G}[EXPIRE] {exp.date()} - {(exp-dt.now()).days} days left{W}")
    except Exception as e:
        print(f"{R}[ERR] {e}{W}")

def bypass(domain):
    print("\n--- [5] CLOUDFLARE BYPASS [NEW] ---")
    try:
        r=requests.get(f"https://api.hackertarget.io/dnslookup/?q={domain}",timeout=8).text
        print(f"{C}{r[:500]}{W}")
    except: print(f"{Y}[INFO] Protected by Cloudflare{W}")

banner()
domain=input("Domain: ").strip().replace("https://","").replace("/","")
get_ip(domain); dns(domain); whois(domain); ssl_check(domain); bypass(domain)

print(f"\n{G}V36 DONE - FINAL BOSS COMPLETE{W}")
