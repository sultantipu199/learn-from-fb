import time
import json
import re
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

def deep_crawl_group():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--lang=bn-BD')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    url = "https://www.facebook.com/groups/ictcarecommunity/"
    print(f"Deep crawling group: {url} ...", flush=True)

    try:
        driver.get(url)
        time.sleep(6)

        dismiss_js = """
        try {
            document.querySelectorAll('[role="dialog"]').forEach(e => e.remove());
            document.querySelectorAll('div[data-nosnippet="true"]').forEach(e => e.remove());
            document.querySelectorAll('div[aria-label="Close"]').forEach(e => e.click());
            document.body.style.overflow = "auto";
        } catch(e) {}
        """
        driver.execute_script(dismiss_js)

        for i in range(35):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script(dismiss_js)
            if (i + 1) % 5 == 0:
                print(f"  Scroll {i+1}/35 completed...", flush=True)

        page_src = driver.page_source
        with open("data/group_page_deep.html", "w", encoding="utf-8") as f:
            f.write(page_src)

        print(f"Deep group page saved ({len(page_src)} bytes)", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)
    finally:
        driver.quit()

if __name__ == '__main__':
    deep_crawl_group()
