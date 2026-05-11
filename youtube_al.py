import os

# Buraya ister kanal linki, ister video linki yapıştır, her türlü çalışır.
LINKS = {
    "Cok Guzel Hareketler 2": "https://www.youtube.com/live/Odt0ixuucfc",
    "Emret Komutanim": "https://www.youtube.com/live/6kQpSqTkN88"
}

def get_link(url):
    # yt-dlp verdiğin link ne olursa olsun (kanal veya video) en güncel m3u8'i bulur
    cmd = f'yt-dlp --geo-bypass -g -f best "{url}"'
    link = os.popen(cmd).read().strip()
    return link

with open("yayinlar.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for name, url in LINKS.items():
        print(f"{name} linki cikartiliyor...")
        m3u8 = get_link(url)
        if m3u8.startswith("http"):
            f.write(f"#EXTINF:-1,{name}\n{m3u8}\n")
            print(f"{name} basarili.")
        else:
            print(f"{name} HATA: Link alinmadi.")
