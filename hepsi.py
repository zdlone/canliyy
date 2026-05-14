import os
import sys
import threading
import time
import requests
import re
from threading import active_count

# --- AYARLAR ---
TARGET_LINK = 'https://t.me/fluxorjinal/17' # Buraya temiz linki veya parametreli linki koyabilirsin
MAX_THREADS = 1500

def send_view(channel, msgid, proxy):
    session = requests.Session()
    # Proxy formatını netleştiriyoruz
    proxies_dict = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive"
    }

    try:
        # 1. Adım: Embed sayfasını ziyaret et ve token (data-view) ara
        embed_url = f"https://t.me/{channel}/{msgid}?embed=1"
        r1 = session.get(embed_url, timeout=10, proxies=proxies_dict, headers=headers)
        
        # Regex ile data-view değerini çekiyoruz (Fotoğraflarda daha güvenlidir)
        search_view = re.search(r'data-view="([^"]+)"', r1.text)
        if not search_view:
            return # Anahtar bulunamadıysa çık
            
        key = search_view.group(1)
        
        # 2. Adım: İzlenme isteğini gönder
        # Çekilen cookie değerini ekliyoruz
        headers["Referer"] = embed_url
        headers["X-Requested-With"] = "XMLHttpRequest"
        
        view_url = f'https://t.me/v/?views={key}'
        r2 = session.get(view_url, timeout=10, headers=headers, proxies=proxies_dict)
        
        if "true" in r2.text.lower():
            print(f"\033[1;32m[BAŞARILI]\033[0m {proxy} -> İzlenme Basıldı")
    except:
        # Hataları sessizce geç (proxy kopmaları vb.)
        pass

def get_proxies():
    print("🌐 Proxy listesi güncelleniyor...")
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000&country=all",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://www.proxyscan.io/download?type=http"
    ]
    all_found = []
    for url in urls:
        try:
            res = requests.get(url, timeout=10).text
            all_found.extend(res.splitlines())
        except:
            continue
    return list(set(all_found))

def run_cycle():
    # Linki temizleme (Örn: ?single kısmını atma)
    try:
        clean_url = TARGET_LINK.split('?')[0]
        parts = clean_url.split('/')
        channel = parts[3]
        msgid = parts[4]
        print(f"✅ Hedef Kanal: {channel} | Mesaj ID: {msgid}")
    except Exception as e:
        print(f"❌ Link Ayrıştırma Hatası: {e}")
        return

    while True:
        proxies = get_proxies()
        if not proxies:
            print("⚠️ Proxy listesi boş, 10sn bekleniyor...")
            time.sleep(10)
            continue

        print(f"🚀 {len(proxies)} Proxy aktif. İşlem başlıyor...")
        
        for p in proxies:
            p = p.strip()
            if not p:
                continue

            # Thread limitini kontrol et
            while active_count() > MAX_THREADS:
                time.sleep(0.01)

            threading.Thread(target=send_view, args=(channel, msgid, p)).start()

        print("🔄 Tur tamamlandı, 5 saniye sonra yeni liste çekilecek...")
        time.sleep(5)

if __name__ == "__main__":
    # Konsolu temizle
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-" * 30)
    print("   TELEGRAM VIEW BOT 2026   ")
    print("-" * 30)
    run_cycle()
