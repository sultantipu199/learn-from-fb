import time
import json
import re
import sys
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def super_deep_crawl():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--lang=bn-BD')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    
    targets = [
        ('https://www.facebook.com/ictcare.com.bd/videos/', 'ictcare_videos'),
        ('https://www.facebook.com/ictcare.com.bd/reels/', 'ictcare_reels'),
        ('https://www.facebook.com/mdshouvikurrahman/videos/', 'shouvik_videos'),
        ('https://www.facebook.com/mdshouvikurrahman/reels/', 'shouvik_reels'),
        ('https://www.facebook.com/ictcare.com.bd/', 'ictcare_home'),
        ('https://www.facebook.com/mdshouvikurrahman/', 'shouvik_home')
    ]
    
    discovered_videos = {}

    for url, label in targets:
        print(f"\n==========================================", flush=True)
        print(f"Crawling: {label} ({url})", flush=True)
        print(f"==========================================", flush=True)
        try:
            driver.get(url)
            time.sleep(6)
            
            # Dismiss login modal if present
            dismiss_js = """
            try {
                document.querySelectorAll('[role="dialog"]').forEach(e => e.remove());
                document.querySelectorAll('div[data-nosnippet="true"]').forEach(e => e.remove());
                document.querySelectorAll('div[aria-label="Close"]').forEach(e => e.click());
                document.body.style.overflow = "auto";
            } catch(e) {}
            """
            driver.execute_script(dismiss_js)
            
            # Scroll 30 times
            for scroll in range(30):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                driver.execute_script(dismiss_js)
                if (scroll + 1) % 5 == 0:
                    links = driver.find_elements(By.TAG_NAME, "a")
                    print(f"  Scroll {scroll+1}/30: current links on page = {len(links)}", flush=True)

            page_src = driver.page_source
            
            # Extract hrefs from elements
            for a in driver.find_elements(By.TAG_NAME, "a"):
                try:
                    href = a.get_attribute("href") or ""
                    decoded_href = urllib.parse.unquote(href)
                    m = re.search(r'(?:/videos/(?:[^/"]+/)?|/watch/\?v=|/reel/)(\d{10,20})', decoded_href)
                    if m:
                        vid_id = m.group(1)
                        if vid_id not in ['100086700362704', '100067541701446', '61593174121107']:
                            if vid_id not in discovered_videos:
                                discovered_videos[vid_id] = {
                                    'id': vid_id,
                                    'href': href,
                                    'decoded_href': decoded_href,
                                    'source': label
                                }
                                print(f"  [NEW] {vid_id} -> {decoded_href[:80]}", flush=True)
                except Exception:
                    pass

            # Extract from page source directly
            raw_matches = re.findall(r'href=["\']([^"\']*(?:/videos/|/watch/\?v=|/reel/)(\d{10,20})[^"\']*)["\']', page_src)
            for full_href, vid_id in raw_matches:
                decoded = urllib.parse.unquote(full_href)
                if vid_id not in ['100086700362704', '100067541701446', '61593174121107']:
                    if vid_id not in discovered_videos:
                        discovered_videos[vid_id] = {
                            'id': vid_id,
                            'href': full_href,
                            'decoded_href': decoded,
                            'source': label
                        }
                        print(f"  [RAW NEW] {vid_id} -> {decoded[:80]}", flush=True)

        except Exception as e:
            print(f"Error crawling {url}: {e}", flush=True)

    driver.quit()

    print(f"\n==========================================", flush=True)
    print(f"Total Unique Discovered Video IDs: {len(discovered_videos)}", flush=True)
    print(f"==========================================", flush=True)

    with open('data/super_deep_discovered.json', 'w', encoding='utf-8') as f:
        json.dump(discovered_videos, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    super_deep_crawl()
