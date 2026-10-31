import math
print("👑 PHARAOH ADEL V23 - COSMIC MODE INITIALIZING...")

# إحداثياتك الأصلية من 6 أكتوبر
base_lat = 29.924
base_lon = 30.919

# عوالم جديدة V23 - بوابات كونية
portals = {
    "🌌 Portal New York": (40.7128, -74.0060),
    "🌀 Portal Tokyo": (35.6762, 139.6503),
    "💫 Portal Dubai": (25.2048, 55.2708),
    "🌠 Portal London": (51.5074, -0.1278),
    "🔥 Portal Singapore": (1.3521, 103.8198),
    "👁️ Cosmic Origin 6 October": (base_lat, base_lon)
}

kml = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<name>PHARAOH ADEL V23 COSMIC</name>
<Style id="cosmic"><IconStyle><color>ff00ff00</color><scale>1.5</scale></IconStyle></Style>
'''

for name, (lat, lon) in portals.items():
    kml += f'''
<Placemark>
<name>{name}</name>
<styleUrl>#cosmic</styleUrl>
<Point><coordinates>{lon},{lat},0</coordinates></Point>
</Placemark>
'''

kml += "</Document></kml>"

with open("pharaoh_v23_cosmic.kml", "w") as f:
    f.write(kml)

print("✅ V23 COSMIC MAP CREATED!")
for n in portals:
    print(f"  → {n}")
