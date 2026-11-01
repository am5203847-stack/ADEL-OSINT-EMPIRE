import socket, ssl, whois, requests
from datetime import datetime as dt

def banner():
    print("""
╔════════════════════════════════════╗
║  PHARAOH V39 EMPEROR - OSINT     ║
║  ADEL-OSINT-EMPIRE               ║
╚════════════════════════════════════╝
""")

def get_whois(domain):
    try:
        w = whois.whois(domain)
        created = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
        if created and hasattr(created, 'tzinfo') and created.tzinfo:
            created = created.replace(tzinfo=None)
        age = (dt.now() - created).days // 365 if created else 0
        return f"WHOIS: {created} | {age} Years", f"[CREATED] {created}\n[AGE] {age} Years"
    except Exception as e:
        return f"WHOIS Error {e}", f"WHOIS Error {e}"

def get_ssl(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()
            exp = dt.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            left = (exp - dt.now()).days
            return f"SSL: {exp.date()} - {left} days", f"[EXPIRE] {exp.date()} - {left} days left"
    except Exception as e:
        return f"SSL Error {e}", f"SSL Error {e}"

def get_dns(domain):
    try:
        ip = socket.gethostbyname(domain)
        return f"DNS A: {ip}", f"[A] {ip}"
    except Exception as e:
        return f"DNS Error {e}", f"DNS Error {e}"

def get_ports(domain):
    opens=[]
    txt=""
    for p in [80,443,21,22,25,3306]:
        try:
            sock=socket.socket()
            sock.settimeout(1)
            if sock.connect_ex((domain,p))==0:
                opens.append(str(p))
                txt+=f"[OPEN] {p}\n"
            sock.close()
        except: pass
    return f"PORTS: {', '.join(opens)}", txt

def get_headers(domain):
    try:
        r=requests.get(f"https://{domain}", timeout=5)
        server=r.headers.get('Server','Unknown')
        return f"Server: {server}", f"[SERVER] {server}\n[STATUS] {r.status_code}"
    except Exception as e:
        return f"Headers Error {e}", f"Headers Error {e}"

def make_html(domain, whois_r, ssl_r, dns_r, ports_r, head_r):
    html=f"""<html><head><title>V39 {domain}</title></head>
<body style='background:#000;color:#0f0;font-family:monospace;padding:20px;border:3px solid gold'>
<h1 style='color:gold'>PHARAOH V39 EMPEROR - {domain}</h1>
<pre>
--- [3] WHOIS ---
{whois_r[1]}

--- [4] SSL ---
{ssl_r[1]}

--- [5] DNS ---
{dns_r[1]}

--- [6] PORTS ---
{ports_r[1]}

--- [7] HEADERS ---
{head_r[1]}

V39 DONE - EMPEROR
</pre>
</body></html>"""
    fname=f"{domain}_V39_REPORT.html"
    with open(fname,'w') as f: f.write(html)
    return fname

# MAIN
banner()
d=input("Enter domain: ").strip()

print("\n--- [3] WHOIS ---")
w_txt,w_print=get_whois(d)
print(w_print)

print("\n--- [4] SSL ---")
s_txt,s_print=get_ssl(d)
print(s_print)

print("\n--- [5] DNS ---")
dns_txt,dns_print=get_dns(d)
print(dns_print)

print("\n--- [6] PORTS ---")
p_txt,p_print=get_ports(d)
print(p_print)

print("\n--- [7] HEADERS ---")
h_txt,h_print=get_headers(d)
print(h_print)

report=make_html(d, (w_txt,w_print), (s_txt,s_print), (dns_txt,dns_print), (p_txt,p_print), (h_txt,h_print))
print(f"\n[+] GOLD REPORT SAVED: {report}")
print("\nV39 DONE - EMPEROR")
