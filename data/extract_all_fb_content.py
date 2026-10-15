import sys
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

def get_links(url, scroll_count=5):
    print(f"\nVisiting {url} ...")
    driver.get(url)
    time.sleep(4)
    for _ in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
    
    links = driver.find_elements(By.TAG_NAME, "a")
    items = []
    for a in links:
        href = a.get_attribute("href")
        text = a.text.strip()
        if href and any(k in href for k in ["/videos/", "/reel/"]):
            # clean url
            clean_url = urllib.parse.unquote(href.split('?')[0])
            items.append({"url": clean_url, "text": text})
    return items

video_items = get_links("https://www.facebook.com/mdshouvikurrahman/videos/", 8)
reel_items = get_links("https://www.facebook.com/mdshouvikurrahman/reels/", 8)

all_items = {}
for it in video_items + reel_items:
    u = it['url']
    if u not in all_items or not all_items[u]:
        all_items[u] = it['text']

print(f"\n==========================================")
print(f"Total Unique Videos & Reels Extracted: {len(all_items)}")
print(f"==========================================")
for i, (u, t) in enumerate(all_items.items(), 1):
    print(f"[{i:02d}] {u}")
    if t:
        print(f"     Title/Text: {t}")

driver.quit()
