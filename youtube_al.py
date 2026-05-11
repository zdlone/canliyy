import os

# Senin istediğin kanallar ve Video ID'leri
LINKS = {
    "Cok Guzel Hareketler 2": "https://www.youtube.com/watch?v=Odt0ixuucfc",
    "Emret Komutanim": "https://www.youtube.com/watch?v=6kQpSqTkN88",
    "beIN SPORTS HABER": "https://www.youtube.com/watch?v=i7UpPgxfZZ8"
}

def get_link(url):
    # yt-dlp'ye 'ben gerçek bir kullanıcıyım' diyoruz
    # --geo-bypass: Bölge engelini aşar
    # --user-agent: Chrome tarayıcı gibi davranır
    cmd = f'yt-dlp --geo-bypass --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" -g -f best "{url}"'
    link = os.popen(cmd).read().strip()
    return link

# Dosyayı oluşturuyoruz
with open("yayinlar.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for name, url in LINKS.items():
        print(f"{name} linki alınıyor...")
        m3u8 = get_link(url)
        if m3u8 and m3u8.startswith("http"):
            f.write(f"#EXTINF:-1,{name}\n{m3u8}\n")
            print(f"Tamam: {name}")
        else:
            print(f"Hata: {name} için link alınamadı.")
