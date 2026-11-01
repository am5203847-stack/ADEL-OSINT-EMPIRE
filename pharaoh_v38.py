import socket, ssl, whois
from datetime import datetime as dt

def get_whois(domain):
    try:
        w = whois.whois(domain)
        created = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
        if created and hasattr(created, 'tzinfo') and created.tzinfo:
            created = created.replace(tzinfo=None)
        age = (dt.now() - created).days // 365 if created else 0
        print(f"--- [3] WHOIS ---\n[CREATED] {created}\n[AGE] {age} Years\n")
    except Exception as e:
        print(f"WHOIS Error: {e}\n")

def get_ssl(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()
            exp = dt.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            left = (exp - dt.now()).days
            print(f"--- [4] SSL ---\n[EXPIRE] {exp.date()} - {left} days left\n")
    except Exception as e:
        print(f"SSL Error: {e}\n")

def get_ports(domain):
    print("--- [6] PORTS ---")
    for p in [80, 443]:
        try:
            sock = socket.socket()
            sock.settimeout(2)
            if sock.connect_ex((domain, p)) == 0:
                print(f"[OPEN] {p}")
            sock.close()
        except:
            pass
    print("\nV38 DONE - FIXED")

d = input("Enter domain: ").strip()
get_whois(d)
get_ssl(d)
get_ports(d)
