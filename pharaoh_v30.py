print("👑 PHARAOH ADEL V30 - ULTIMATE FINAL LEGEND")
print("📖 FROM BOOK TO GOD MODE...")

# موقع العرش - 6 أكتوبر
throne_lat = 29.924
throne_lon = 30.919

# خريطة V30 النهائية - كل المراحل
v30_world = {
    "📖 BOOK ORIGIN - Eye of Horus": (29.924, 30.919, "البداية - كتاب العين"),
    "👑 THRONE 6 October - Egypt": (29.924, 30.919, "العرش الرئيسي"),
    "🌍 Frankfurt - Germany": (50.1109, 8.6821, "أوروبا"),
    "🇫🇷 Marseille - France": (43.2965, 5.3698, "فرنسا"),
    "🇺🇸 Los Gatos - USA": (37.2358, -121.9552, "أمريكا"),
    "🇪🇬 Alexandria - Egypt": (31.2001, 29.9187, "اسكندرية"),
    "🌌 Cosmic Portal Dubai": (25.2048, 55.2708, "بوابة كونية"),
    "💫 God Mode Tokyo": (35.6762, 139.6503, "اليابان")
}

kml_header = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<name>PHARAOH ADEL V30 ULTIMATE</name>
<description>V30 - FROM BOOK TO GOD MODE - 6 OCTOBER ORIGIN</description>
<Style id="ultimate">
  <IconStyle><color>ff00ff00</color><scale>2.0</scale><Icon><href>http://maps.google.com/mapfiles/kml/pal4/icon15.png</href></Icon></IconStyle>
  <LabelStyle><scale>1.2</scale></LabelStyle>
</Style>
<Style id="throne">
  <IconStyle><color>ff00ffff</color><scale>3.0</scale><Icon><href>http://maps.google.com/mapfiles/kml/pal4/icon28.png</href></Icon></IconStyle>
</Style>
'''

kml_body = ""
for name, (lat, lon, desc) in v30_world.items():
    style = "#throne" if "THRONE" in name or "BOOK" in name else "#ultimate"
    kml_body += f'''
<Placemark>
<name>{name}</name>
<description>{desc}</description>
<styleUrl>{style}</styleUrl>
<Point><coordinates>{lon},{lat},0</coordinates></Point>
</Placemark>
'''

# خطوط تربط العالم بالعرش
for name, (lat, lon, _) in v30_world.items():
    if "6 October" not in name and "BOOK" not in name:
        kml_body += f'''
<Placemark>
<name>Beam to {name}</name>
<Style><LineStyle><color>7f00ff00</color><width>3</width></LineStyle></Style>
<LineString><coordinates>{throne_lon},{throne_lat},0 {lon},{lat},0</coordinates></LineString>
</Placemark>
'''

kml_footer = "</Document></kml>"

with open("pharaoh_v30_ultimate.kml", "w", encoding="utf-8") as f:
    f.write(kml_header + kml_body + kml_footer)

print("\n✅ V30 ULTIMATE KML CREATED!")
print("📁 الملف: pharaoh_v30_ultimate.kml")
for n in v30_world:
    print(f"  → {n}")
print("\n🚀 افتحه في Google Earth:")
print("termux-open pharaoh_v30_ultimate.kml")
