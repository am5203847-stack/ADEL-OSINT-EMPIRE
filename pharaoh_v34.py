#!/usr/bin/env python3
# PHARAOH EYE V34 - GOD MODE
# By ADEL DIAMOND

import requests, socket, datetime, re
from datetime import datetime as dt

Y = "\033[93m"; G = "\033[92m"; R = "\033[91m"; C = "\033[96m"; W = "\033[0m"

def banner():
    print(f"{Y}╔════════════════════════════════════╗{W}")
    print(f"{Y}║  PHARAOH EYE V34 - GOD MODE      ║{W}")
    print(f"{Y}╚════════════════════════════════════╝{W}")

def get_ip_info(domain):
    print(f"\n--- [1] IP & LOCATION ---")
    try:
        ip = socket.gethostbyname(domain)
        print(f"{G}[IP] {domain} -> {ip}{W}")
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        print(f"{C}[LOC] {r.get('country')} / {r.get('city')} - ISP: {r.get('isp')}{W}")
        print(f"{C}[COORD] {r.get('lat')}, {r.get('lon')} - TZ: {r.get('timezone')}{W}")
        return ip, r
    except Exception as e:
        print(f"{R}[ERR] {e}{W}")
        return "N/A", {}

def dns_records(domain):
    print(f"\n--- [2] DNS RECORDS [NEW V34] ---")
    try:
        # A, MX, NS, TXT via Google DNS API (Safe)
        for t in ["A","MX","NS","TXT"]:
            r = requests.get(f"https://dns.google/resolve?name={domain}&type={t}", timeout=5).json()
            if "Answer" in r:
                for ans in r["Answer"][:3]:
                    print(f"{G}[{t}] {ans['data']}{W}")
    except Exception as e:
        print(f"{R}[ERR DNS] {e}{W}")

def whois_info(domain):
    print(f"\n--- [3] WHOIS & AGE [NEW V34] ---")
    try:
        # Using who.is API free + RDAP
        r = requests.get(f"https://rdap.org/domain/{domain}", timeout=8).json()
        creation = r.get("events",[])
        for ev in creation:
            if ev.get("eventAction") == "registration":
                date = ev.get("eventDate","")[:10]
                print(f"{G}[CREATED] {date}{W}")
                # حساب العمر
                try:
                    d1 = dt.strptime(date, "%Y-%m-%d")
                    age = (dt.now() - d1).days // 365
                    print(f"{C}[AGE] {age} Years old - OLD DOMAIN{W}")
                except: pass
        print(f"{C}[REGISTRAR] {r.get('registrar','N/A')}{W}")
    except:
        print(f"{Y}[INFO] RDAP busy, try whois manually: whois {domain}{W}")

def web_scan(domain):
    print(f"\n--- [4] WEB SCAN ---")
    paths = ["robots.txt","sitemap.xml",".env","backup.zip",".git/","wp-admin/","admin/"]
    for p in paths:
        try:
            r = requests.get(f"https://{domain}/{p}", timeout=5, headers={"User-Agent":"Pharaoh-V34"})
            col = G if r.status_code==404 else Y
            print(f"{col}[{r.status_code}] {p}{W}")
        except: pass

def header_check(domain):
    print(f"\n--- [5] HEADER & TECH ---")
    try:
        r = requests.get(f"https://{domain}", timeout=5)
        tech = []
        h = str(r.headers).lower() + r.text[:2000].lower()
        if "cloudflare" in h: tech.append("Cloudflare")
        if "wordpress" in h: tech.append("WordPress")
        if "nginx" in h: tech.append("Nginx")
        if "gws" in h: tech.append("Google GWS")
        if tech: print(f"{C}[TECH] {', '.join(tech)}{W}")
    except: pass

def port_check(domain):
    print(f"\n--- [6] PORT (80,443) ---")
    for port in [80,443]:
        try:
            s = socket.socket(); s.settimeout(2)
            s.connect((domain, port))
            print(f"{G}[OPEN] {port}{W}"); s.close()
        except:
            print(f"{R}[CLOSED] {port}{W}")

def subdomain_scan(domain):
    print(f"\n--- [7] SUBDOMAIN FINDER ---")
    subs = set()
    try:
        r = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=10)
        if r.status_code == 200:
            for entry in r.json()[:25]:
                subs.add(entry['name_value'])
        for s in list(subs)[:20]:
            print(f"{C}[SUB] {s}{W}")
        return list(subs)
    except:
        print(f"{Y}[INFO] crt.sh busy{W}")
        return []

# MAIN
banner()
domain = input("Domain (ex: google.com): ").strip().replace("https://","").replace("/","")
ip, loc = get_ip_info(domain)
dns_records(domain)
whois_info(domain)
web_scan(domain)
header_check(domain)
port_check(domain)
subs = subdomain_scan(domain)

# HTML GOD REPORT
html = f"""
<html><head><title>V34 {domain}</title>
<style>body{{background:#000;color:#0f0;font-family:monospace;padding:20px}}h1{{color:gold;text-shadow:0 0 10px gold}} .box{{border:1px solid gold;padding:15px;margin:10px 0}}</style>
</head><body>
<h1>PHARAOH EYE V34 - {domain}</h1>
<div class="box">IP: {ip}<br>Location: {loc.get('country')} / {loc.get('city')}<br>ISP: {loc.get('isp')}<br>Coords: {loc.get('lat')},{loc.get('lon')}</div>
<div class="box"><h2>Subdomains: {len(subs)}</h2><pre>{chr(10).join(subs)}</pre></div>
<p>By ADEL DIAMOND - {dt.now()}</p>
</body></html>
"""
open(f"{domain}_V34.html","w").write(html)
print(f"\n{G}Done V34! Open {domain}_V34.html in browser - GOD MODE COMPLETE{W}")
