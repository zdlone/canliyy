import os
import requests

# Video ID'lerin
VIDEOS = {
    "Cok Guzel Hareketler 2": "Odt0ixuucfc",
    "Emret Komutanim": "6kQpSqTkN88"
}

def get_m3u8(video_id):
    # YouTube'un engellemediği alternatif köprü sunucuları (Sırayla dener)
    instances = [
        "https://inv.riverside.rocks",
        "https://vid.priv.au",
        "https://invidious.namazso.eu"
    ]
    
    for base_url in instances:
        try:
            # API üzerinden m3u8 linkini çekiyoruz
            api_url = f"{base_url}/api/v1/videos/{video_id}"
            r = requests.get(api_url, timeout=5).json()
            
            # HLS (m3u8) linkini bul
            if "hlsUrl" in r:
                return r["hlsUrl"]
            
            # Alternatif formatlarda ara
            for fmt in r.get("adaptiveFormats", []):
                if "m3u8" in fmt.get("type", "") or ".m3u8" in fmt.get("url", ""):
                    return fmt["url"]
        except:
            continue # Bu sunucu çalışmazsa diğerine geç
    return None

with open("yayinlar.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for name, vid in VIDEOS.items():
        print(f"{name} linki aliniyor...")
        link = get_m3u8(vid)
        if link:
            f.write(f"#EXTINF:-1,{name}\n{link}\n")
            print(f"{name} basarili.")
        else:
            print(f"{name} alinamadi.")
