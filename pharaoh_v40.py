import socket, ssl, whois, requests, re, time
from datetime import datetime as dt
import unicodedata

def clean_domain(raw):
    # يشيل أي حرف عربي أو رمز غريب
    raw = raw.strip().lower()
    # خد أول كلمة فيها نقطة بس
    m = re.search(r'([a-z0-9.-]+\.[a-z]{2,})', raw)
    if m: return m.group(1)
    # fallback: شيل كل حاجة مش انجليزي/رقم/نقطة/شرطة
    return re.sub(r'[^a-z0-9.-]', '', raw)

def banner():
    print("\n╔════════════════════════════════════╗\n║  PHARAOH V40.2 ULTRA FIXED       ║\n╚════════════════════════════════════╝\n")

def get_whois(d):
    try:
        w=whois.whois(d); c=w.creation_date[0] if isinstance(w.creation_date,list) else w.creation_date
        if c and hasattr(c,'tzinfo') and c.tzinfo: c=c.replace(tzinfo=None)
        age=(dt.now()-c).days//365 if c else 0
        return f"[CREATED] {c}\n[AGE] {age} Years"
    except Exception as e: return f"[INFO] WHOIS private / {e}"

def get_ssl(d):
    try:
        ctx=ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=d) as s:
            s.settimeout(5); s.connect((d,443)); cert=s.getpeercert()
            exp=dt.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z'); left=(exp-dt.now()).days
            return f"[EXPIRE] {exp.date()} - {left} days left"
    except Exception as e: return f"[ERROR] {e}"

def get_dns(d):
    try: return f"[A] {socket.gethostbyname(d)}"
    except Exception as e: return f"[ERROR] {e}"

def get_ports(d):
    res=""
    for p in [80,443]:
        try:
            sock=socket.create_connection((d,p), timeout=2); sock.close()
            res+=f"[OPEN] {p}\n"
        except: res+=f"[CLOSED] {p}\n"
    return res

def get_subs(d):
    # crt.sh with headers + retry
    try:
        url=f"https://crt.sh/?q=%25.{d}&output=json"
        r=requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=15)
        if r.status_code==200 and r.text.startswith('['):
            data=r.json(); subs=set()
            for entry in data:
                for s in entry.get('name_value','').split('\n'):
                    s=s.strip().lower()
                    if d in s and '*' not in s and len(s)<80: subs.add(s)
            subs=list(subs)[:15]
            if subs: return "\n".join([f"[SUB] {s}" for s in subs])
    except: pass
    # fallback hackertarget
    try:
        r=requests.get(f"https://api.hackertarget.com/hostsearch/?q={d}", timeout=10)
        if "error" not in r.text.lower() and "," in r.text:
            return "\n".join([f"[SUB] {l.split(',')[0]}" for l in r.text.split('\n')[:15] if l])
    except: pass
    return "[INFO] No subs - try again after 2 min (rate limit)"

def get_emails(d):
    try:
        r=requests.get(f"https://{d}", headers={'User-Agent':'Mozilla/5.0'}, timeout=6)
        emails=set(re.findall(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", r.text.lower()))
        emails=[e for e in emails if len(e)<50][:5]
        return "\n".join([f"[EMAIL] {e}" for e in emails]) if emails else "[INFO] No public emails"
    except: return "[INFO] No public emails"

def make_html(domain, w,s,dns,p,subs,emails):
    html=f"<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;border:3px solid gold'><h2 style='color:gold'>V40.2 - {domain}</h2><pre>{w}\n\n{s}\n\n{dns}\n\n{p}\n\n{subs}\n\n{emails}</pre></body></html>"
    fn=f"{domain}_V40_REPORT.html"; open(fn,'w',encoding='utf-8').write(html); return fn

banner()
raw=input("Enter domain: ")
d=clean_domain(raw)
print(f"[CLEANED] {raw} -> {d}")

print("\n--- [3] WHOIS ---"); wt=get_whois(d); print(wt)
print("\n--- [4] SSL ---"); st=get_ssl(d); print(st)
print("\n--- [5] DNS ---"); dnst=get_dns(d); print(dnst)
print("\n--- [6] PORTS ---"); pt=get_ports(d); print(pt)
print("\n--- [7] SUBDOMAINS ---"); subt=get_subs(d); print(subt)
print("\n--- [8] EMAILS ---"); et=get_emails(d); print(et)
rep=make_html(d,wt,st,dnst,pt,subt,et)
print(f"\n[+] GOLD REPORT SAVED: {rep}\n\nV40.2 DONE")
