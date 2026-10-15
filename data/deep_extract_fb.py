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

def get_links(url, scroll_count=15):
    print(f"Visiting {url} ...")
    driver.get(url)
    time.sleep(5)
    last_count = 0
    for s in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        cur_links = len(driver.find_elements(By.TAG_NAME, "a"))
        if cur_links == last_count and s > 5:
            # Reached end of page
            break
        last_count = cur_links
    
    links = driver.find_elements(By.TAG_NAME, "a")
    items = []
    for a in links:
        try:
            href = a.get_attribute("href")
            text = a.text.strip()
            if href and any(k in href for k in ["/videos/", "/reel/"]):
                clean_url = urllib.parse.unquote(href.split('?')[0])
                items.append({"url": clean_url, "text": text})
        except Exception:
            pass
    return items

video_items = get_links("https://www.facebook.com/mdshouvikurrahman/videos/", 20)
reel_items = get_links("https://www.facebook.com/mdshouvikurrahman/reels/", 20)

all_items = {}
for it in video_items + reel_items:
    u = it['url']
    if u not in all_items or (not all_items[u] and it['text']):
        all_items[u] = it['text']

print(f"\n==========================================")
print(f"Total Unique Facebook Videos/Reels Found: {len(all_items)}")
print(f"==========================================")

with open("data/extracted_fb_videos.txt", "w", encoding="utf-8") as f:
    for i, (u, t) in enumerate(all_items.items(), 1):
        line = f"[{i:02d}] {u} | Text: {t}"
        print(line)
        f.write(line + "\n")

driver.quit()
