import os
import requests
import re

# Kanallar ve Video ID'leri
VIDEOS = {
    "Cok Guzel Hareketler 2": "Odt0ixuucfc",
    "Emret Komutanim": "6kQpSqTkN88"
}

def get_m3u8(video_id):
    # YouTube'un bot engelini aşmak için alternatif bir köprü kullanıyoruz
    # Bu yöntem GitHub IP'sini gizler
    try:
        url = f"https://vid.priv.au/api/v1/videos/{video_id}"
        response = requests.get(url, timeout=10).json()
        
        # Canlı yayın akışlarını tara
        if "liveNow" in response and response["liveNow"]:
            # m3u8 linkini çekmeye çalış
            adaptive_formats = response.get("adaptiveFormats", [])
            for fmt in adaptive_formats:
                if "m3u8" in fmt.get("type", "") or ".m3u8" in fmt.get("url", ""):
                    return fmt["url"]
            
            # Alternatif: HLS linki
            hls_url = response.get("hlsUrl")
            if hls_url:
                return hls_url
    except Exception as e:
        print(f"Hata oluştu: {e}")
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
            print(f"{name} linki bulunamadi.")
