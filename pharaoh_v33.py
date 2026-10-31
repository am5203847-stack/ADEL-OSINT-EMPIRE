#!/usr/bin/env python3
# PHARAOH EYE V33 - FINAL EMPIRE
# By ADEL DIAMOND - For your own sites only

import requests, socket, re, json
from datetime import datetime

Y = "\033[93m"; G = "\033[92m"; R = "\033[91m"; C = "\033[96m"; W = "\033[0m"

def banner():
    print(f"{Y}╔════════════════════════════════════╗{W}")
    print(f"{Y}║  PHARAOH EYE V33 - FINAL EMPIRE  ║{W}")
    print(f"{Y}╚════════════════════════════════════╝{W}")

def get_ip_info(domain):
    print(f"\n--- [1] IP & LOCATION [NEW V33] ---")
    try:
        ip = socket.gethostbyname(domain)
        print(f"{G}[IP] {domain} -> {ip}{W}")
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
            print(f"{C}[LOC] {r.get('country')} / {r.get('city')} - ISP: {r.get('isp')}{W}")
            return ip, r
        except:
            return ip, {}
    except Exception as e:
        print(f"{R}[ERR] {e}{W}")
        return "N/A", {}

def web_scan(domain):
    print(f"\n--- [2] WEB SCAN ---")
    paths = ["robots.txt","sitemap.xml",".env","backup.zip",".git/","wp-admin/","admin/",".htaccess"]
    for p in paths:
        try:
            r = requests.get(f"https://{domain}/{p}", timeout=5, headers={"User-Agent":"Pharaoh-V33"})
            if r.status_code == 404:
                print(f"{G}[SAFE] {p} -> 404{W}")
            else:
                print(f"{Y}[FOUND] {p} -> {r.status_code}{W}")
        except:
            print(f"{R}[ERR] {p}{W}")

def header_check(domain):
    print(f"\n--- [3] HEADER & TECH ---")
    try:
        r = requests.get(f"https://{domain}", timeout=5)
        tech = []
        if "cloudflare" in str(r.headers).lower(): tech.append("Cloudflare")
        if "wordpress" in r.text.lower(): tech.append("WordPress")
        if "nginx" in str(r.headers).lower(): tech.append("Nginx")
        if "gws" in str(r.headers).lower(): tech.append("Google GWS")
        
        for h in ["X-Frame-Options","Content-Security-Policy","X-Content-Type-Options","Strict-Transport-Security"]:
            status = "OK" if any(h.lower() in k.lower() for k in r.headers) else "MISSING"
            col = G if status=="OK" else Y
            print(f"{col}[{status}] {h}{W}")
        if tech:
            print(f"{C}[TECH] {', '.join(tech)}{W}")
    except Exception as e:
        print(f"{R}[ERR] {e}{W}")

def port_check(domain):
    print(f"\n--- [4] PORT (Safe 80,443) ---")
    for port in [80,443]:
        try:
            s = socket.socket(); s.settimeout(2)
            s.connect((domain, port))
            print(f"{G}[OPEN] Port {port}{W}"); s.close()
        except:
            print(f"{R}[CLOSED] Port {port}{W}")

def subdomain_scan(domain):
    print(f"\n--- [5] SUBDOMAIN FINDER ---")
    subs = set()
    try:
        r = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=10)
        if r.status_code == 200:
            for entry in r.json()[:20]:
                subs.add(entry['name_value'])
        for s in list(subs)[:15]:
            print(f"{C}[SUB] {s}{W}")
        return list(subs)
    except:
        print(f"{Y}[INFO] crt.sh busy{W}")
        return []

# MAIN
banner()
domain = input("Domain (ex: google.com): ").strip().replace("https://","").replace("/","")
ip, loc = get_ip_info(domain)
web_scan(domain)
header_check(domain)
port_check(domain)
subs = subdomain_scan(domain)

# HTML REPORT V33
html = f"""
<html><head><title>Pharaoh V33 - {domain}</title>
<style>body{{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:20px}}h1{{color:gold}}</style>
</head><body>
<h1>PHARAOH EYE V33 - {domain}</h1>
<p>IP: {ip} | {loc.get('country','')}/{loc.get('city','')} | ISP: {loc.get('isp','')}</p>
<p>Date: {datetime.now()}</p>
<h2>Subdomains Found: {len(subs)}</h2>
<pre>{chr(10).join(subs)}</pre>
<p>By ADEL DIAMOND</p>
</body></html>
"""
with open(f"{domain}_V33.html","w") as f:
    f.write(html)
with open(f"{domain}_V33.txt","w") as f:
    f.write(f"Report {domain} - IP {ip} - {len(subs)} subs\n")

print(f"\n{G}Done V33! Reports: {domain}_V33.html + .txt - Open HTML in browser{W}")
