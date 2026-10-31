#!/usr/bin/env python3
# PHARAOH EYE V32 - FIXED EMPIRE EDITION
# By ADEL - Use only on your own sites

import requests, socket, re
from datetime import datetime

Y = "\033[93m"; G = "\033[92m"; R = "\033[91m"; C = "\033[96m"; W = "\033[0m"

def banner():
    print(f"{Y}╔════════════════════════════════════╗{W}")
    print(f"{Y}║  PHARAOH EYE V32 - EMPIRE FIXED   ║{W}")
    print(f"{Y}╚════════════════════════════════════╝{W}")

def web_scan(domain):
    print(f"\n--- [1] WEB SCAN ---")
    paths = ["robots.txt","sitemap.xml",".env",".env.bak","backup.zip",".git/","wp-admin/","admin/",".htaccess"]
    for p in paths:
        try:
            r = requests.get(f"https://{domain}/{p}", timeout=5, headers={"User-Agent":"PharaohEye-V32"})
            if r.status_code == 200 and p in ["robots.txt","sitemap.xml"]:
                print(f"{C}[INFO]{W} {p} -> 200 (فروع ميزلو يحيط)")
            elif r.status_code == 404:
                print(f"{G}[SAFE]{W} {p} -> 404")
            else:
                print(f"{Y}[FOUND]{W} {p} -> {r.status_code}")
        except:
            print(f"{R}[ERR]{W} {p}")

def header_check(domain):
    print(f"\n--- [2] HEADER CHECK ---")
    try:
        r = requests.get(f"https://{domain}", timeout=5)
        headers = r.headers
        checks = ["X-Frame-Options","Content-Security-Policy","X-Content-Type-Options","Strict-Transport-Security"]
        tech = []
        if "cloudflare" in str(headers).lower(): tech.append("Cloudflare")
        if "wordpress" in r.text.lower(): tech.append("WordPress")
        if "nginx" in str(headers).lower(): tech.append("Nginx")
        
        for h in checks:
            if any(h.lower() in k.lower() for k in headers):
                print(f"{G}[OK] {h}{W}")
            else:
                print(f"{Y}[MISSING] {h}{W}")
        
        if tech:
            print(f"{C}[TECH] Detected: {', '.join(tech)}{W}")
    except Exception as e:
        print(f"{R}[ERR] {e}{W}")

def port_check(domain):
    print(f"\n--- [3] PORT (Safe Check) ---")
    for port in [80,443]:
        try:
            s = socket.socket(); s.settimeout(2)
            s.connect((domain, port))
            print(f"{G}[OPEN] Port {port} ({'HTTP' if port==80 else 'HTTPS'}){W}")
            s.close()
        except:
            print(f"{R}[CLOSED] Port {port}{W}")

def subdomain_scan(domain):
    print(f"\n--- [4] SUBDOMAIN FINDER [NEW] ---")
    try:
        r = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=10)
        subs = set()
        if r.status_code == 200:
            data = r.json()
            for entry in data[:15]:
                name = entry['name_value']
                subs.add(name)
        for s in list(subs)[:10]:
            print(f"{C}[SUB] {s}{W}")
        if not subs:
            print(f"{G}[SAFE] No public subs found{W}")
    except:
        print(f"{Y}[INFO] crt.sh busy, try later{W}")

# MAIN
banner()
domain = input("Domain (ex: google.com): ").strip().replace("https://","").replace("/","")
print(f"\n{Y}[*] Target: {domain} | Server: gws{W}")

report = []
web_scan(domain)
header_check(domain)
port_check(domain)
subdomain_scan(domain)

print(f"\n{Y}Done V32 - Report saved to {domain}_report.txt - Use only on your own sites{W}")
with open(f"{domain}_report.txt","w") as f:
    f.write(f"Pharaoh Eye V32 Report for {domain} - {datetime.now()}\nDone\n")
