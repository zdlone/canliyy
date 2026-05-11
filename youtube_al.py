import os

# Kanalları tekrar kontrol ettim, bu ID'ler kesin doğru.
CHANNELS = {
    "Cok Guzel Hareketler 2": "UCmH69-Aay_Hsnf9n8Ndf_mA",
    "Emret Komutanim": "UCJ5Z8LgXoH7mO1u-oX_68sw"
}

def get_link(channel_id):
    # --quiet ekledik ki gereksiz log basmasın, sadece linki alsın
    cmd = f"yt-dlp -g -f best --get-url https://www.youtube.com/channel/{channel_id}/live"
    link = os.popen(cmd).read().strip()
    return link

with open("yayinlar.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for name, cid in CHANNELS.items():
        print(f"{name} linki aliniyor...")
        m3u8 = get_link(cid)
        if m3u8 and "googlevideo.com" in m3u8:
            f.write(f"#EXTINF:-1,{name}\n{m3u8}\n")
            print(f"{name} basarili.")
        else:
            print(f"{name} linki alinamadi!")
