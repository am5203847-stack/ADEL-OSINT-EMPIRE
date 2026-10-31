#!/usr/bin/env python3
# PHARAOH EYE V35 - ULTIMATE
# By ADEL DIAMOND - Use only on your own sites

import requests, socket, ssl, re
from datetime import datetime as dt

Y = "\033[93m"; G = "\033[92m"; R = "\033[91m"; C = "\033[96m"; W = "\033[0m"

def banner():
    print(f"{Y}╔════════════════════════════════════╗{W}")
    print(f"{Y}║  PHARAOH EYE V35 - ULTIMATE      ║{W}")
    print(f"{Y}╚════════════════════════════════════╝{W}")

def get_ip_info(domain):
    print(f"\n--- [1] IP & LOCATION ---")
    try:
        ip = socket.gethostbyname(domain)
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        print(f"{G}[IP] {domain} -> {ip}{W}")
        print(f"{C}[LOC] {r.get('country')} / {r.get('city')} - ISP: {r.get('isp')}{W}")
        print(f"{C}[COORD] {r.get('lat')},{r.get('lon')} - TZ: {r.get('timezone')}{W}")
        return ip, r
    except: return "N/A", {}

def dns_records(domain):
    print(f"\n--- [2] DNS RECORDS ---")
    for t in ["A","MX","NS","TXT"]:
        try:
            r = requests.get(f"https://dns.google/resolve?name={domain}&type={t}", timeout=5).json()
            if "Answer" in r:
                for ans in r["Answer"][:4]:
                    print(f"{G}[{t}] {ans['data']}{W}")
        except: pass

def whois_info(domain):
    print(f"\n--- [3] WHOIS & AGE ---")
    try:
        r = requests.get(f"https://rdap.org/domain/{domain}", timeout=8).json()
        for ev in r.get("events",[]):
            if ev.get("eventAction")=="registration":
                d=ev.get("eventDate","")[:10]
                print(f"{G}[CREATED] {d}{W}")
                try:
                    d1=dt.strptime(d,"%Y-%m-%d")
                    age=(dt.now()-d1).days//365
                    print(f"{C}[AGE] {age} Years old{W}")
                except: pass
    except:
        print(f"{Y}[INFO] RDAP busy{W}")

def ssl_check(domain):
    print(f"\n--- [4] SSL CERT [NEW V35] ---")
    try:
        ctx=ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain,443))
            cert=s.getpeercert()
            exp=dt.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            issuer=dict(x[0] for x in cert['issuer'])
            print(f"{G}[ISSUER] {issuer.get('organizationName')}{W}")
            print(f"{G}[EXPIRE] {exp.date()} - {(exp-dt.now()).days} days left{W}")
            return f"{exp.date()}", issuer.get('organizationName')
    except Exception as e:
        print(f"{R}[ERR SSL] {e}{W}")
        return "N/A","N/A"

def web_scan(domain):
    print(f"\n--- [5] WEB SCAN ---")
    for p in ["robots.txt","sitemap.xml",".env","backup.zip",".git/","wp-admin/"]:
        try:
            r=requests.get(f"https://{domain}/{p}",timeout=5,headers={"User-Agent":"Pharaoh-V35"})
            col=G if r.status_code==404 else Y
            print(f"{col}[{r.status_code}] {p}{W}")
        except: pass

def email_social_scan(domain):
    print(f"\n--- [6] EMAIL & SOCIAL [NEW V35] ---")
    try:
        r=requests.get(f"https://{domain}",timeout=8,headers={"User-Agent":"Pharaoh-V35"}).text
        emails=set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", r))
        socials=re.findall(r"https?://(?:www\.)?(facebook|twitter|x\.com|linkedin|instagram|youtube)\.com/[^\s\"']+", r)

        if emails:
            for e in list(emails)[:10]:
                if domain not in e and "example" not in e and "w3.org" not in e:
                    print(f"{G}[EMAIL] {e}{W}")
        else:
            print(f"{Y}[INFO] No public emails on homepage{W}")

        if socials:
            for s in set(socials):
                print(f"{C}[SOCIAL] {s}{W}")
        else:
            print(f"{Y}[INFO] No social links found{W}")
        
        return list(emails)[:5], list(set(socials))[:5]
    except Exception as e:
        print(f"{R}[ERR] {e}{W}")
        return [], []

def subdomain_scan(domain):
    print(f"\n--- [7] SUBDOMAIN FINDER ---")
    subs=set()
    try:
        r=requests.get(f"https://crt.sh/?q=%.{domain}&output=json",timeout=10)
        if r.status_code==200:
            for entry in r.json()[:30]:
                subs.add(entry['name_value'])
        for s in list(subs)[:20]:
            print(f"{C}[SUB] {s}{W}")
        return list(subs)
    except:
        print(f"{Y}[INFO] crt.sh busy{W}")
        return []

# MAIN
banner()
domain=input("Domain (ex: google.com): ").strip().replace("https://","").replace("/","")
ip, loc = get_ip_info(domain)
dns_records(domain)
whois_info(domain)
ssl_exp, ssl_issuer = ssl_check(domain)
web_scan(domain)
emails, socials = email_social_scan(domain)
subs = subdomain_scan(domain)

# HTML ULTIMATE REPORT
html=f"""
<html><head><title>V35 {domain}</title>
<style>body{{background:#050505;color:#00ff88;font-family:monospace;padding:20px}}h1{{color:gold;text-shadow:0 0 15px gold}} .box{{border:1px solid #333;padding:15px;margin:12px 0;background:#111}} b{{color:gold}}</style>
</head><body>
<h1>PHARAOH EYE V35 - {domain}</h1>
<div class="box"><b>IP:</b> {ip}<br><b>LOC:</b> {loc.get('country')}/{loc.get('city')}<br><b>ISP:</b> {loc.get('isp')}<br><b>SSL:</b> {ssl_issuer} Exp: {ssl_exp}</div>
<div class="box"><b>Emails:</b><br>{'<br>'.join(emails) if emails else 'None on homepage'}</div>
<div class="box"><b>Socials:</b><br>{'<br>'.join(socials) if socials else 'None'}</div>
<div class="box"><b>Subdomains ({len(subs)}):</b><br><pre>{chr(10).join(subs)}</pre></div>
<p>By ADEL DIAMOND - {dt.now()}</p>
</body></html>
"""
open(f"{domain}_V35.html","w").write(html)
print(f"\n{G}Done V35! Open {domain}_V35.html - ULTIMATE COMPLETE{W}")

