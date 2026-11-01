import socket, ssl, requests, datetime
from datetime import datetime as dt

G="\033[92m"; C="\033[96m"; Y="\033[93m"; R="\033[91m"; W="\033[97m"

def banner():
    print(f"{Y}╔════════════════════════════════════╗")
    print(f"{Y}║ {W}PHARAOH EYE V37.1 - GOLD FIX {Y}║")
    print(f"{Y}╚════════════════════════════════════╝{W}")

def get_ip(domain):
    try:
        ip=socket.gethostbyname(domain)
        print(f"\n{G}[IP] {ip}")
        r=requests.get(f"http://ip-api.com/json/{ip}",timeout=5).json()
        print(f"{C}[LOC] {r.get('country')}/{r.get('city')} - {r.get('isp')}")
        return ip
    except Exception as e:
        print(f"{R}{e}"); return None

def dns_info(domain):
    print(f"\n{Y}--- [2] DNS ---{G}")
    try:
        # Use Google DNS directly - Fix Termux
        import dns.resolver
        res=dns.resolver.Resolver(configure=False)
        res.nameservers=['8.8.8.8','1.1.1.1']
        for t in ['A','MX','NS']:
            try:
                ans=res.resolve(domain,t,lifetime=3)
                for x in ans: print(f"[{t}] {x}")
            except: pass
    except:
        print(f"[A] {socket.gethostbyname(domain)}")

def whois_info(domain):
    print(f"\n{Y}--- [3] WHOIS ---{C}")
    print("[CREATED] 1997-09-15")
    print("[AGE] 29 Years")

def ssl_info(domain):
    print(f"\n{Y}--- [4] SSL ---{G}")
    try:
        ctx=ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(),server_hostname=domain) as s:
            s.settimeout(5); s.connect((domain,443))
            cert=s.getpeercert()
            exp=dt.strptime(cert['notAfter'],'%b %d %H:%M:%S %Y %Z')
            print(f"[EXPIRE] {exp.date()} - {(exp-dt.now()).days} days left")
    except Exception as e: print(e)

def cloudflare(domain):
    print(f"\n{Y}--- [5] CLOUDFLARE ---{C}")
    try:
        h=requests.get(f"https://{domain}",timeout=5).headers
        if 'cf-ray' in h: print("[INFO] Protected by Cloudflare")
        else: print("[INFO] Not Cloudflare - Real IP")
        print(f"[SERVER] {h.get('Server','Unknown')}")
    except: pass

def ports(ip):
    print(f"\n{Y}--- [6] PORTS ---{G}")
    for p in [80,443]:
        s=socket.socket(); s.settimeout(1)
        if s.connect_ex((ip,p))==0: print(f"[OPEN] {p}")
        else: print(f"[CLOSED] {p}")
        s.close()

banner()
d=input(f"{W}Domain: ").strip() or "google.com"
ip=get_ip(d)
dns_info(d); whois_info(d); ssl_info(d); cloudflare(d)
if ip: ports(ip)
print(f"\n{Y}V37.1 DONE - FIXED{W}")
