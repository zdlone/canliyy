import os, sys, threading, time, requests
from threading import active_count

# --- AYARLAR ---
TARGET_LINK = 'https://t.me/fluxorjinal/17'
TARGET_LINK = 'https://t.me/fluxorjinal/17?single'

MAX_THREADS = 1500 

def send_view(channel, msgid, proxy):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest"
    }
    proxies_dict = {'http': proxy, 'https': proxy}
    
    try:
        r1 = session.get(f"https://t.me/{channel}/{msgid}?embed=1", timeout=8, proxies=proxies_dict, headers=headers)
        cookie = r1.headers.get('set-cookie', '').split(';')[0]
        key = r1.text.split('data-view="')[1].split('"')[0]
        
        headers["Cookie"] = cookie
        headers["Referer"] = f"https://t.me/{channel}/{msgid}?embed=1"
        
        r2 = session.get(f'https://t.me/v/?views={key}', timeout=8, headers=headers, proxies=proxies_dict)
        
        if "true" in r2.text.lower():
            print(f"\033[1;32m[SUCCESS]\033[0m {proxy} -> View Basıldı!")
    except:
        pass

def get_proxies():
    print("🌐 2026 Proxy Listesi Güncelleniyor...")
    urls = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000&country=all"
    ]
    all_found = []
    for url in urls:
        try:
            res = requests.get(url, timeout=10).text
            all_found.extend(res.splitlines())
        except: continue
    return list(set(all_found))

def run_cycle():
    # Link parçalama hatasını önlemek için try-except
    try:
        parts = TARGET_LINK.split('/')
        channel = parts[3]
        msgid = parts[4]
    except:
        print("❌ Link formatı hatalı!")
        return

    while True:
        proxies = get_proxies()
        if not proxies:
            print("⚠️ Proxy bulunamadı, 10sn bekliyor...")
            time.sleep(10)
            continue
            
        print(f"🔥 {len(proxies)} Proxy ile saldırı başlıyor...")
        for p in proxies:
            p = p.strip()
            if not p: continue
            
            # Hatalı olan satır düzeltildi: proxies listesi kontrol ediliyor
            full_p = f"socks5://{p}" if len(proxies) > 500 else f"http://{p}"
            
            while active_count() > MAX_THREADS:
                time.sleep(0.05)
            
            threading.Thread(target=send_view, args=(channel, msgid, p)).start()
        
        print("🔄 Tur tamamlandı, yeni liste çekiliyor...")
        time.sleep(5)

if __name__ == "__main__":
    run_cycle()
