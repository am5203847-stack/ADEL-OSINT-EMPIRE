import requests

def ip_lookup(ip):
    print(f"\n[+] IP Lookup: {ip}\n")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}").json()
        if r['status'] == 'success':
            print(f"Country: {r['country']}")
            print(f"City: {r['city']}")
            print(f"ISP: {r['isp']}")
            print(f"Lat/Lon: {r['lat']}, {r['lon']}")
            print(f"Map: https://www.google.com/maps?q={r['lat']},{r['lon']}")
        else:
            print("[!] Invalid IP")
    except Exception as e:
        print(f"[ERROR] {e}")
