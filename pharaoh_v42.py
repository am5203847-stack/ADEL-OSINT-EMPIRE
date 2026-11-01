# PHARAOH V42 - SHODAN+VT HUNTER
# Eng. Adel | #EngAdel_Pharaoh
import socket, requests, re
from datetime import datetime

def clean_domain(raw):
    raw=raw.strip().lower()
    raw=re.sub(r'^https?://','',raw)
    raw=re.sub(r'^www\.','',raw)
    raw=raw.split('/')[0]
    m=re.search(r'([a-z0-9.-]+\.[a-z]{2,})',raw)
    return m.group(1) if m else raw

print("PHARAOH V42 SHODAN+VT - #EngAdel_Pharaoh")
raw=input("\nEnter Domain: ")
domain=clean_domain(raw)
print(f"\n[TARGET] {domain}")

try:
    ip=socket.gethostbyname(domain)
    print(f"[IP] {ip}")
    r=requests.get(f"https://api.hackertarget.com/httpheaders/?q={domain}",timeout=10)
    print(f"\n[HEADERS]:\n{r.text[:600]}")
    r2=requests.get(f"https://api.hackertarget.com/nmap/?q={ip}",timeout=15)
    print(f"\n[PORTS]:\n{r2.text[:800]}")
    r3=requests.get(f"https://api.hackertarget.com/whois/?q={domain}",timeout=10)
    print(f"\n[WHOIS]:\n{r3.text[:800]}")
except Exception as e:
    print(f"Error: {e}")

print(f"\nDONE V42 - {datetime.now()}")
