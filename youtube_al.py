import os

# Linklerini verdiğin videoların ID'lerini buraya koydum
# https://www.youtube.com/live/Odt0ixuucfc -> Odt0ixuucfc
# https://www.youtube.com/live/6kQpSqTkN88 -> 6kQpSqTkN88
VIDEOS = {
    "Cok Guzel Hareketler 2": "Odt0ixuucfc",
    "Emret Komutanim": "6kQpSqTkN88"
}

def get_link(video_id):
    # Doğrudan video linki üzerinden m3u8 çekiyoruz
    cmd = f'yt-dlp --geo-bypass -g -f best "https://www.youtube.com/watch?v={video_id}"'
    link = os.popen(cmd).read().strip()
    return link

with open("yayinlar.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for name, vid in VIDEOS.items():
        print(f"{name} aliniyor...")
        m3u8 = get_link(vid)
        if m3u8.startswith("http"):
            f.write(f"#EXTINF:-1,{name}\n{m3u8}\n")
            print(f"{name} Tamam.")
        else:
            print(f"{name} HATA!")
