import os

# Linkleri Invidious API üzerinden geçireceğiz
LINKS = {
    "Cok Guzel Hareketler 2": "Odt0ixuucfc",
    "Emret Komutanim": "6kQpSqTkN88"
}

def get_link(video_id):
    # Invidious API'sini kullanarak YouTube'un bot engelini bypass ediyoruz
    # Farklı bir API adresi deniyoruz
    cmd = f'curl -s "https://inv.tux.rs/api/v1/videos/{video_id}" | grep -o "https://[^\\"]*m3u8" | head -1'
    link = os.popen(cmd).read().strip()
    return link

with open("yayinlar.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for name, vid in LINKS.items():
        m3u8 = get_link(vid)
        if m3u8.startswith("http"):
            f.write(f"#EXTINF:-1,{name}\n{m3u8}\n")
