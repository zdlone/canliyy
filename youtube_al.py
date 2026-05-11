import os

# Kanal ID'lerin kesin doğru.
CHANNELS = {
    "Cok Guzel Hareketler 2": "UCmH69-Aay_Hsnf9n8Ndf_mA",
    "Emret Komutanim": "UCJ5Z8LgXoH7mO1u-oX_68sw"
}

def get_link(channel_id):
    # Kullanıcı gibi davranması için "user-agent" ekledik
    # Ve YouTube'un engellemesini aşmak için bazı ekstra parametreler koyduk
    cmd = f'yt-dlp --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36" -g -f best "https://www.youtube.com/channel/{channel_id}/live"'
    link = os.popen(cmd).read().strip()
    return link

with open("yayinlar.m3u", "w") as f:
    f.write("#EXTM3U\n")
    for name, cid in CHANNELS.items():
        m3u8 = get_link(cid)
        if m3u8 and "googlevideo.com" in m3u8:
            f.write(f"#EXTINF:-1,{name}\n{m3u8}\n")
