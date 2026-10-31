import re
from urllib.parse import urlparse
from datetime import datetime

def analyze_url(url):
    risks = []
    score = 100
    parsed = urlparse(url if '://' in url else 'http://'+url)

    if '@' in url:
        risks.append("🚨 @ TRICK - تحويل خبيث")
        score -= 40
    if len(url) > 75:
        risks.append("⚠️ لينك طويل مشبوه")
        score -= 20
    if parsed.scheme == 'http':
        risks.append("🔓 HTTP غير آمن")
        score -= 15
    return max(score,0), risks

def analyze_email_header(header):
    ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', header)
    spoof = 'evil.com' in header and 'paypal.com' in header
    return ips, spoof

print("="*60)
print("👁️ PHARAOH ULTIMATE CYBER REPORT - LEVEL 7")
print(f"OPERATOR: ADEL89.ROOT | SAGITTARIUS | GOD MODE")
print(f"DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)

url = input("\n[1] حط لينك مشبوه: ").strip() or "http://google.com@evil.com/login"
header = input("[2] حط Email Header (Enter للتخطي): ").strip()

url_score, url_risks = analyze_url(url)
print(f"\n--- URL ANALYSIS ---\nTarget: {url}\nScore: {url_score}/100")
for r in url_risks: print(f" - {r}")

if header:
    ips, spoof = analyze_email_header(header)
    print(f"\n--- EMAIL ANALYSIS ---\nIPs: {ips}\nSpoofing: {'YES 🚨' if spoof else 'NO'}")
else:
    print("\n--- EMAIL ANALYSIS --- SKIPPED (Demo mode)")

final = url_score
if final < 40:
    verdict = "🔴 CRITICAL - تصيد مؤكد!"
elif final < 70:
    verdict = "🟡 SUSPICIOUS - خلي بالك!"
else:
    verdict = "🟢 SAFE - آمن"

print("\n"+"="*60)
print(f"FINAL VERDICT: {verdict}")
print(f"TOTAL THREAT SCORE: {final}/100")
print("MOTO: ما خلقت الحماية الا لكي تخترق")
print("STATUS: 21000P | GOD MODE | LEVEL 7 MASTER")
print("="*60)
