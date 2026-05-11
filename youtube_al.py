import os
import requests
import re

# Buraya sadece izlemek istediğin canlı yayınların linkini yapıştır
LINKS = {
    "Cok Guzel Hareketler 2": "https://www.youtube.com/live/Odt0ixuucfc",
    "Emret Komutanim": "https://www.youtube.com/live/6kQpSqTkN88"
}

def get_link(url):
    # yt-dlp ile doğrudan link üzerinden m3u8 çekiyoruz
    # ID aramadan, direkt linki hedef alıyoruz
    cmd = f'yt-dlp --geo-bypass -g -f best "{url}"'
    link = os.popen(cmd).read().strip()
    return link

with open("yayinlar.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for name, url in LINKS.items():
        print(f"{name} linki aliniyor...")
        m3u8 = get_link(url)
        if m3u8.startswith("http"):
            f.write(f"#EXTINF:-1,{name}\n{m3u8}\n")
            print(f"{name} Basarili.")
        else:
            print(f"{name} Hata: Link bulunamadi.")
