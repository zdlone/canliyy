import os
import requests
import re

# Sadece video linklerini buraya eklemen yeterli
LINKS = {
    "Cok Guzel Hareketler 2": "https://www.youtube.com/live/Odt0ixuucfc",
    "Emret Komutanim": "https://www.youtube.com/live/6kQpSqTkN88"
}

def get_m3u8(url):
    # Linkten Video ID'sini otomatik çıkarır
    video_id_match = re.search(r"v=([^&]+)", url) or re.search(r"live/([^/?]+)", url)
    if not video_id_match:
        return None
    video_id = video_id_match.group(1)

    # 1. YÖNTEM: Invidious Köprü Sunucuları (YouTube Engelini Aşmak İçin En İyisi)
    instances = ["https://vid.priv.au", "https://iv.ggtyler.dev", "https://invidious.asir.dev"]
    for base in instances:
        try:
            r = requests.get(f"{base}/api/v1/videos/{video_id}", timeout=8).json()
            if "hlsUrl" in r: return r["hlsUrl"]
            for f in r.get("adaptiveFormats", []):
                if "m3u8" in f.get("type", ""): return f["url"]
        except: continue

    # 2. YÖNTEM: Yedek olarak yt-dlp (Eğer köprüler çalışmazsa)
    try:
        cmd = f'yt-dlp --geo-bypass -g -f best "{url}"'
        link = os.popen(cmd).read().strip()
        if link.startswith("http"): return link
    except: pass
    
    return None

with open("yayinlar.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for name, url in LINKS.items():
        print(f"{name} aliniyor...")
        m3u8 = get_m3u8(url)
        if m3u8:
            f.write(f"#EXTINF:-1,{name}\n{m3u8}\n")
            print(f"Başarılı: {name}")
        else:
            print(f"Hata: {name} alınamadı.")
