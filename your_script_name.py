import os, sys, threading, time, requests
from threading import active_count

# --- 2026 TUNING ---
TARGET_LINK = 'https://t.me/fluxorjinal/15'
MAX_THREADS = 150 # GitHub limitlerinde maksimum verim

def send_view(channel, msgid, proxy):
    session = requests.Session()
    # 2026 Modern Tarayıcı Parmak İzi
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest"
    }
    proxies = {'http': proxy, 'https': proxy}
    
    try:
        # Adım 1: Sayfaya gir ve cookie al
        r1 = session.get(f"https://t.me/{channel}/{msgid}?embed=1", timeout=8, proxies=proxies, headers=headers)
        cookie = r1.headers.get('set-cookie', '').split(';')[0]
        key = r1.text.split('data-view="')[1].split('"')[0]
        
        # Adım 2: Onay isteği gönder (View ekleyen asıl kısım)
        headers["Cookie"] = cookie
        headers["Referer"] = f"https://t.me/{channel}/{msgid}?embed=1"
        
        r2 = session.get(f'https://t.me/v/?views={key}', timeout=8, headers=headers, proxies=proxies)
        
        if "true" in r2.text.lower():
            print(f"\033[1;32m[SUCCESS]\033[0m {proxy} -> View Basıldı!")
    except:
        pass # Hatalı proxyleri sessizce geç, konsolu kirletme

def get_proxies():
    print("🌐 2026 Proxy Listesi Güncelleniyor...")
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000&country=all"
    ]
    all_p = []
    for url in urls:
        try:
            res = requests.get(url, timeout=10).text
            all_p.extend(res.splitlines())
        except: continue
    return list(set(all_p))

def run_cycle():
    channel = TARGET_LINK.split('/')[3]
    msgid = TARGET_LINK.split('/')[4]
    
    while True: # İŞTE BURASI: Hiç durmadan başa döner
        proxies = get_proxies()
        if not proxies:
            time.sleep(10); continue
            
        print(f"🔥 {len(proxies)} Proxy ile saldırı başlıyor...")
        for p in proxies:
            p = p.strip()
            if not p: continue
            
            # SOCKS5 kontrolü
            full_p = f"socks5://{p}" if ":" in p and len(all_p) > 500 else f"http://{p}"
            
            while active_count() > MAX_THREADS:
                time.sleep(0.05)
            
            threading.Thread(target=send_view, args=(channel, msgid, p)).start()
        
        print("🔄 Liste bitti, 5 saniye soğuma ve yeni liste...")
        time.sleep(5)

if __name__ == "__main__":
    run_cycle()
