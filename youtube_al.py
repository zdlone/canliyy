import os

# Yeni verdiğin kanalları ekledik
CHANNELS = {
    "Cok Guzel Hareketler 2": "UCmH69-Aay_Hsnf9n8Ndf_mA",
    "Emret Komutanım": "UCJ5Z8LgXoH7mO1u-oX_68sw"
}

def get_link(channel_id):
    # yt-dlp ile canlı yayın linkini çekiyoruz
    link = os.popen(f"yt-dlp -g -f best https://www.youtube.com/channel/{channel_id}/live").read().strip()
    return link

with open("yayinlar.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for name, cid in CHANNELS.items():
        m3u8 = get_link(cid)
        if m3u8:
            f.write(f"#EXTINF:-1,{name}\n{m3u8}\n")
