import os

# Hangi kanalı istiyorsan onun ID'sini buraya yaz
# Örnek: UC... şeklinde olan kanal ID'si
CHANNELS = {
    "Kanal_Adi": "UC_KANAL_ID_BURAYA" 
}

def get_link(channel_id):
    # Bu kısım yt-dlp kullanarak linki yakalar
    link = os.popen(f"yt-dlp -g -f best https://www.youtube.com/channel/{channel_id}/live").read().strip()
    return link

with open("yayinlar.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for name, cid in CHANNELS.items():
        m3u8 = get_link(cid)
        f.write(f"#EXTINF:-1,{name}\n{m3u8}\n")
