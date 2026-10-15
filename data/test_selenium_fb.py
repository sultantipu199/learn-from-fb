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

print("Initializing Chrome driver...")
try:
    driver = webdriver.Chrome(options=options)
    print("Driver started. Navigating to https://www.facebook.com/share/14nc19UVKkk/ ...")
    driver.get("https://www.facebook.com/share/14nc19UVKkk/")
    time.sleep(5)
    print("Current URL after redirect:", driver.current_url)
    print("Page title:", driver.title)
    
    # Save page source to inspect
    with open("data/chrome_fb_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("Saved page source to data/chrome_fb_page.html")
    
    # Check if we were redirected to login
    if "login" in driver.current_url:
        print("Redirected to Facebook login page.")
    else:
        print("Not redirected to login! Searching for video links...")
        links = driver.find_elements(By.TAG_NAME, "a")
        vlinks = [a.get_attribute("href") for a in links if a.get_attribute("href") and ("/videos/" in a.get_attribute("href") or "/reel/" in a.get_attribute("href") or "watch" in a.get_attribute("href"))]
        print(f"Found {len(vlinks)} video/reel links:")
        for v in vlinks[:10]:
            print("  ", v)
            
    driver.quit()
except Exception as e:
    print("Error:", e)
