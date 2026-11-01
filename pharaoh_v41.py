import socket, ssl, whois, requests, re, time
from datetime import datetime as dt

def clean_domain(raw):
    raw=raw.strip().lower()
    m=re.search(r'([a-z0-9.-]+\.[a-z]{2,})', raw)
    return m.group(1) if m else re.sub(r'[^a-z0-9.-]', '', raw)

def banner():
    print("\n╔════════════════════════════════════╗\n║  PHARAOH V41 - WAF + TECH HUNTER  ║\n║  ADEL OSINT EMPIRE               ║\n╚════════════════════════════════════╝\n")

def get_whois(d):
    try:
        w=whois.whois(d); c=w.creation_date[0] if isinstance(w.creation_date,list) else w.creation_date
        if c and hasattr(c,'tzinfo') and c.tzinfo: c=c.replace(tzinfo=None)
        age=(dt.now()-c).days//365 if c else 0
        return f"[CREATED] {c}\n[AGE] {age} Years"
    except: return "[INFO] WHOIS private"

def get_ssl(d):
    try:
        ctx=ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=d) as s:
            s.settimeout(5); s.connect((d,443)); cert=s.getpeercert()
            exp=dt.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z'); left=(exp-dt.now()).days
            return f"[EXPIRE] {exp.date()} - {left} days left\n[ISSUER] {dict(x[0] for x in cert['issuer']).get('organizationName','')}"
    except Exception as e: return f"[ERROR] {e}"

def get_dns(d):
    try: return f"[A] {socket.gethostbyname(d)}"
    except Exception as e: return f"[ERROR] {e}"

def get_ports(d):
    res=""
    for p in [80,443]:
        try: socket.create_connection((d,p),timeout=2).close(); res+=f"[OPEN] {p}\n"
        except: res+=f"[CLOSED] {p}\n"
    return res

def get_waf_tech(d):
    wafs=[]; tech=[]
    try:
        headers={'User-Agent':'Mozilla/5.0'}
        r=requests.get(f"https://{d}", headers=headers, timeout=8, allow_redirects=True)
        h={k.lower():v.lower() for k,v in r.headers.items()}
        txt=r.text.lower()

        # WAF DETECTION
        if 'cf-ray' in h or 'cloudflare' in str(h): wafs.append("Cloudflare WAF")
        if 'akamai' in str(h) or 'akamaighost' in str(h): wafs.append("Akamai WAF")
        if 'sucuri' in str(h): wafs.append("Sucuri WAF")
        if 'awsalb' in str(h) or 'awselb' in str(h): wafs.append("AWS WAF/ELB")
        if 'incap_ses' in str(r.cookies) or 'incapsula' in str(h): wafs.append("Imperva Incapsula")
        if 'x-sucuri' in h: wafs.append("Sucuri")
        if '__cf_bm' in str(r.cookies): wafs.append("Cloudflare Bot Management")
        if not wafs: wafs.append("No WAF detected (or hidden)")

        # TECH STACK
        if 'server' in h: tech.append(f"Server: {r.headers.get('Server','')}")
        if 'x-powered-by' in h: tech.append(f"Powered: {r.headers.get('X-Powered-By','')}")
        if 'nginx' in str(h): tech.append("Tech: Nginx")
        if 'apache' in str(h): tech.append("Tech: Apache")
        if 'wordpress' in txt: tech.append("CMS: WordPress")
        if 'wp-content' in txt: tech.append("CMS: WordPress Confirmed")
        if 'react' in txt: tech.append("JS: React")
        if 'next.js' in txt or '_next' in txt: tech.append("Framework: Next.js")
        if 'shopify' in txt: tech.append("Platform: Shopify")
        if 'cloudflare' in txt and 'Server: cloudflare' not in str(tech): tech.append("CDN: Cloudflare")
        if 'jquery' in txt: tech.append("Lib: jQuery")

        waf_str="\n".join([f"[WAF] {x}" for x in wafs])
        tech_str="\n".join([f"[TECH] {x}" for x in tech]) if tech else "[TECH] Minimal headers"
        return waf_str, tech_str, r.status_code
    except Exception as e:
        return f"[ERROR] {e}", "[INFO] No tech", 0

def get_subs(d):
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
    try:
        r=requests.get(f"https://api.hackertarget.com/hostsearch/?q={d}", timeout=10)
        if "error" not in r.text.lower() and "," in r.text:
            return "\n".join([f"[SUB] {l.split(',')[0]}" for l in r.text.split('\n')[:15] if l])
    except: pass
    return "[INFO] No subs - rate limited"

def make_html(domain, w,s,dns,p,waf,tech,code,subs):
    html=f"<html><head><meta charset='utf-8'><title>V41 - {domain}</title></head><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;border:4px solid gold'><h1 style='color:gold'>PHARAOH V41 - {domain} - HTTP {code}</h1><pre>{w}\n\n{s}\n\n{dns}\n\n{p}\n\n{waf}\n\n{tech}\n\n{subs}\n\nV41 DONE</pre></body></html>"
    fn=f"{domain}_V41_REPORT.html"; open(fn,'w',encoding='utf-8').write(html); return fn

banner()
raw=input("Enter domain: "); d=clean_domain(raw)
print(f"[CLEANED] {raw} -> {d}\n")

print("--- [3] WHOIS ---"); wt=get_whois(d); print(wt)
print("\n--- [4] SSL ---"); st=get_ssl(d); print(st)
print("\n--- [5] DNS ---"); dnst=get_dns(d); print(dnst)
print("\n--- [6] PORTS ---"); pt=get_ports(d); print(pt)
print("\n--- [7] WAF + TECH (NEW) ---"); waf,tech,code=get_waf_tech(d); print(waf); print(tech); print(f"[HTTP] {code}")
print("\n--- [8] SUBDOMAINS ---"); subt=get_subs(d); print(subt)

rep=make_html(d,wt,st,dnst,pt,waf,tech,code,subt)
print(f"\n[+] GOLD REPORT SAVED: {rep}\n\nV41 DONE - WAF HUNTER READY")
