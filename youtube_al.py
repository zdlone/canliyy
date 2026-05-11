import os
import requests
import re

# Kanallar
LINKS = {
    "Cok Guzel Hareketler 2": "https://www.youtube.com/live/Odt0ixuucfc",
    "Emret Komutanim": "https://www.youtube.com/live/6kQpSqTkN88"
}

def get_m3u8(url):
    # Video ID'sini çek
    vid = re.search(r"(?:v=|\/live\/)([0-9A-Za-z_-]{11})", url).group(1)
    
    # 2026'nın en sağlam 3 Invidious API'si (Sırayla dener, bulduğu an döner)
    apis = [
        f"https://inv.tux.rs/api/v1/videos/{vid}",
        f"https://vid.priv.au/api/v1/videos/{vid}",
        f"https://invidious.lunar.icu/api/v1/videos/{vid}"
    ]

    for api in apis:
        try:
            r = requests.get(api, timeout=10).json()
            # HLS linkini bul
            if "hlsUrl" in r:
                return r["hlsUrl"]
            # Eğer hlsUrl yoksa adaptive formatlara bak
            for fmt in r.get("adaptiveFormats", []):
                if "m3u8" in fmt.get("type", ""):
                    return fmt["url"]
        except:
            continue
    return None

# Dosyayı baştan yarat
with open("yayinlar.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for name, url in LINKS.items():
        print(f"Sistem: {name} için veri çekiliyor...")
        link = get_m3u8(url)
        if link:
            f.write(f"#EXTINF:-1,{name}\n{link}\n")
            print(f"Başarılı: {name} eklendi.")
        else:
            print(f"Hata: {name} köprülerden geçemedi.")
