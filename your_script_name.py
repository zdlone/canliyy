import os, sys, threading, time, requests
from threading import active_count

# --- AYARLAR ---
TARGET_LINK = 'https://t.me/fluxorjinal/15'
N_THREADS = 100 # GitHub Actions için 100 daha stabildir, kilitlenmeyi önler.

def send_seen(channel, msgid, proxy):
    s = requests.Session()
    proxies = {'http': proxy, 'https': proxy}
    try:
        # Telegram embed sayfasından cookie ve anahtar alımı
        a = s.get(f"https://t.me/{channel}/{msgid}?embed=1", timeout=10, proxies=proxies)
        cookie = a.headers.get('set-cookie', '').split(';')[0]
        key = a.text.split('data-view="')[1].split('"')[0]
        
        h2 = {
            "Accept": "*/*", 
            "Cookie": cookie, 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        # İzlenmeyi gönder
        i = s.get(f'https://t.me/v/?views={key}', timeout=10, headers=h2, proxies=proxies)
        if i.text == "true":
            print(f'[+] View Eklendi: {proxy}')
    except:
        return False

def scrap():
    print("⏳ Taze proxyler toplaniyor...")
    try:
        # Sadece hızlı ve taze proxyleri çekiyoruz
        https = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=https&timeout=5000").text
        http = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=5000").text
        proxies = (https + "\n" + http).splitlines()
        return [p.strip() for p in proxies if p.strip()]
    except:
        return []

def start():
    proxies = scrap()
    if not proxies:
        print("[-] Proxy bulunamadi.")
        return

    channel = TARGET_LINK.split('/')[3]
    msgid = TARGET_LINK.split('/')[4]
    
    threads = []
    print(f"🚀 {len(proxies)} proxy ile islem baslatiliyor...")

    for p in proxies:
        while active_count() > N_THREADS:
            time.sleep(0.01)
        
        t = threading.Thread(target=send_seen, args=(channel, msgid, p))
        t.start()
        threads.append(t)

    # Tüm threadlerin bitmesini bekle
    for t in threads:
        t.join(timeout=1)
    print("✅ Bu tur tamamlandi. GitHub Actions kapaniyor.")

if __name__ == "__main__":
    start() # Sonsuz döngü kaldırıldı (GitHub Actions için)
