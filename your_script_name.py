# ------- Import Library's
import os, sys
import threading
from threading import active_count
import urllib
import time

# requests kontrolü ve kurulumu
try:
    import requests
except:
    os.system('pip install requests')
    import requests

# Ayarlar
n_threads = 400  
threads = []

# Hedef link sabitlendi
TARGET_LINK = 'https://t.me/fluxorjinal/15'

print('\033[1;32m[!] Bot Baslatildi: ' + TARGET_LINK)
print('\033[1;33m[!] Yonlendirmeler ve reklamlar iptal edildi.\033[0m')

def view2(proxy):
    # Orijinal döngü yapısı korundu ama link sabitlendi
    links = [TARGET_LINK] * 6 
    for i in links:
        try:
            channel = i.split('/')[3]
            msgid = i.split('/')[4]
            send_seen(channel, msgid, proxy)
        except:
            pass

def send_seen(channel, msgid, proxy):
    s = requests.Session()
    proxies = {'http': proxy, 'https': proxy}
    try:
        a = s.get(f"https://t.me/{channel}/{msgid}", timeout=10, proxies=proxies)
        cookie = a.headers['set-cookie'].split(';')[0]
    except:
        return False

    h1 = {
        "Accept": "*/*", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en-US,en;q=0.9", 
        "Connection": "keep-alive", 
        "Content-type": "application/x-www-form-urlencoded",
        "Cookie": cookie, 
        "Host": "t.me", 
        "Origin": "https://t.me", 
        "Referer": f"https://t.me/{channel}/{msgid}?embed=1", 
        "User-Agent": "Chrome"
    }
    
    try:
        r = s.post(f'https://t.me/{channel}/{msgid}?embed=1', json={"_rl": "1"}, headers=h1, proxies=proxies)
        key = r.text.split('data-view="')[1].split('"')[0]
        now_view = r.text.split('<span class="tgme_widget_message_views">')[1].split('</span>')[0]
    except:
        return False

    h2 = {
        "Accept": "*/*", 
        "Cookie": cookie, 
        "Host": "t.me",
        "Referer": f"https://t.me/{channel}/{msgid}?embed=1", 
        "User-Agent": "Chrome", 
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        i = s.get(f'https://t.me/v/?views={key}', timeout=10, headers=h2, proxies=proxies)
        if i.text == "true":
            print(f'\033[1;32m[+] View Eklendi: {now_view}\033[0m')           
    except:
        return False

def scrap():
    try:
        https = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=https&timeout=0", timeout=5).text
        http = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=0", timeout=5).text
        socks = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=0", timeout=5).text
        
        with open("proxies.txt", "w") as f: f.write(https + "\n" + http)
        with open("socks.txt", "w") as f: f.write(socks)
        return True
    except:
        return False

def checker(proxy):
    try:
        view2(proxy)
    except:
        return False

def start():
    if not scrap(): return
    
    # HTTP/HTTPS Proxies
    with open('proxies.txt', 'r') as f:
        for i in f.readlines():
            p = i.strip()
            if not p: continue
            while active_count() > n_threads: time.sleep(0.05)
            threading.Thread(target=checker, args=(p,)).start()

    # SOCKS5 Proxies
    with open('socks.txt', 'r') as f:
        for i in f.readlines():
            p = i.strip()
            if not p: continue
            while active_count() > n_threads: time.sleep(0.05)
            threading.Thread(target=checker, args=("socks5://"+p,)).start()
    
    return True

def process(run_for_ever:bool = False):
    if run_for_ever:
        while True:
            start()
    else:
        start()

if __name__ == "__main__":
    process(True)
