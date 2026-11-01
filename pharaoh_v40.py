import socket, ssl, whois, requests, re, json
from datetime import datetime as dt

def banner():
    print("\n╔════════════════════════════════════╗\n║  PHARAOH V40 SUBDOMAIN HUNTER   ║\n╚════════════════════════════════════╝\n")

def get_whois(domain):
    try:
        w=whois.whois(domain)
        c=w.creation_date[0] if isinstance(w.creation_date,list) else w.creation_date
        if c and hasattr(c,'tzinfo') and c.tzinfo: c=c.replace(tzinfo=None)
        age=(dt.now()-c).days//365 if c else 0
        return f"[CREATED] {c}\n[AGE] {age} Years"
    except Exception as e: return f"[ERROR] {e}"

def get_ssl(domain):
    try:
        ctx=ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5); s.connect((domain,443)); cert=s.getpeercert()
            exp=dt.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z'); left=(exp-dt.now()).days
            return f"[EXPIRE] {exp.date()} - {left} days left"
    except Exception as e: return f"[ERROR] {e}"

def get_dns(domain):
    try: return f"[A] {socket.gethostbyname(domain)}"
    except Exception as e: return f"[ERROR] {e}"

def get_ports(domain):
    res=""
    for p in [80,443,21,22,25,3306,8080]:
        try:
            sock=socket.socket(); sock.settimeout(1)
            if sock.connect_ex((domain,p))==0: res+=f"[OPEN] {p}\n"
            sock.close()
        except: pass
    return res or "[CLOSED] All checked"

def get_subdomains(domain):
    try:
        url=f"https://crt.sh/?q=%25.{domain}&output=json"
        r=requests.get(url, timeout=10)
        data=r.json()
        subs=set()
        for entry in data:
            name=entry.get('name_value','')
            for s in name.split('\n'):
                s=s.strip().lower()
                if domain in s and '*' not in s:
                    subs.add(s)
        subs=list(subs)[:20]
        return "\n".join([f"[SUB] {s}" for s in subs]) if subs else "[INFO] No subs found"
    except Exception as e:
        return f"[ERROR] {e} - crt.sh may rate limit"

def get_emails(domain):
    try:
        r=requests.get(f"https://{domain}", timeout=5)
        emails=set(re.findall(r"[a-zA-Z0-9_.+-]+@"+re.escape(domain), r.text))
        emails.update(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", r.text)[:5])
        return "\n".join([f"[EMAIL] {e}" for e in list(emails)[:10]]) if emails else "[INFO] No public emails"
    except Exception as e: return f"[ERROR] {e}"

def make_html(domain, whois_t, ssl_t, dns_t, ports_t, subs_t, emails_t):
    html=f"""<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;border:4px solid gold'>
<h1 style='color:gold'>PHARAOH V40 - {domain}</h1><pre>
WHOIS
{whois_t}

SSL
{ssl_t}

DNS
{dns_t}

PORTS
{ports_t}

SUBDOMAINS crt.sh (Top 20)
{subs_t}

EMAILS
{emails_t}

V40 DONE - SUBDOMAIN HUNTER
</pre></body></html>"""
    f=f"{domain}_V40_REPORT.html"; open(f,'w',encoding='utf-8').write(html); return f

banner()
d=input("Enter domain: ").strip()

print("\n--- [3] WHOIS ---"); wt=get_whois(d); print(wt)
print("\n--- [4] SSL ---"); st=get_ssl(d); print(st)
print("\n--- [5] DNS ---"); dnst=get_dns(d); print(dnst)
print("\n--- [6] PORTS ---"); pt=get_ports(d); print(pt)
print("\n--- [7] SUBDOMAINS (crt.sh) ---"); subt=get_subdomains(d); print(subt)
print("\n--- [8] EMAILS ---"); et=get_emails(d); print(et)

rep=make_html(d,wt,st,dnst,pt,subt,et)
print(f"\n[+] GOLD REPORT SAVED: {rep}\n\nV40 DONE - SUBDOMAIN HUNTER")
