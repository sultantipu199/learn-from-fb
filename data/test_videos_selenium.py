import sys
import time
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
url = "https://www.facebook.com/mdshouvikurrahman/videos/"
print(f"Visiting {url} ...")
driver.get(url)
time.sleep(5)

# Scroll down to load more videos if possible!
print("Scrolling down to load more videos...")
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

links = driver.find_elements(By.TAG_NAME, "a")
found = []
for a in links:
    href = a.get_attribute("href")
    text = a.text.strip()
    if href and any(k in href for k in ["/videos/", "/reel/", "watch", "fb.watch"]):
        found.append({"url": href, "text": text})

unique_videos = {}
for item in found:
    u = item['url'].split('?')[0] # remove query params
    if u not in unique_videos:
        unique_videos[u] = item['text']

print(f"\n==========================================")
print(f"Total Unique Video Links Found: {len(unique_videos)}")
print(f"==========================================")
for i, (u, t) in enumerate(unique_videos.items(), 1):
    print(f"[{i:02d}] {u} | Title/Text: '{t}'")

driver.quit()
