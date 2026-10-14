import requests

def search_username(username):
    print(f"\n[+] Searching for username: {username}\n")
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "TikTok": f"https://tiktok.com/@{username}",
        "Facebook": f"https://facebook.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}"
    }
    for platform, url in sites.items():
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print(f"[FOUND] {platform}: {url}")
            else:
                print(f"[NOT FOUND] {platform}")
        except:
            print(f"[ERROR] {platform}")
