import time
import json
import re
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def crawl_all_sources():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--lang=bn-BD')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    
    targets = [
        ('https://www.facebook.com/ictcare.com.bd/videos/', 'ictcare_videos'),
        ('https://www.facebook.com/ictcare.com.bd/reels/', 'ictcare_reels'),
        ('https://www.facebook.com/mdshouvikurrahman/videos/', 'shouvik_videos'),
        ('https://www.facebook.com/mdshouvikurrahman/reels/', 'shouvik_reels'),
        ('https://www.facebook.com/100067541701446/videos/', 'shouvik_id_videos')
    ]
    
    discovered_videos = {}

    for url, label in targets:
        print(f"\n--- Crawling: {label} ({url}) ---")
        try:
            driver.get(url)
            time.sleep(5)
            
            # Scroll down 12 times to load as many items as possible
            for scroll in range(12):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2.5)
                # Check how many links found so far
                links = driver.find_elements(By.TAG_NAME, "a")
                print(f"  Scroll {scroll+1}/12: found {len(links)} links on page")

            page_src = driver.page_source
            
            # Save html for debugging if needed
            with open(f"data/page_{label}.html", "w", encoding="utf-8") as f:
                f.write(page_src)

            # Match URLs:
            # 1. /watch/?v=ID
            # 2. /reel/ID/
            # 3. /videos/ID/
            # 4. /watch?v=ID
            patterns = [
                r'href="([^"]*(?:watch\/?\?v=|reel\/|videos\/)(\d+)[^"]*)"',
                r'"playable_url":"[^"]*","video_id":"(\d+)"',
                r'"story_fbid":"(\d+)"',
                r'/reel/(\d+)',
                r'/videos/(\d+)',
                r'watch\?v=(\d+)'
            ]

            # Direct regex on page_src
            href_matches = re.findall(r'href="([^"]*(?:watch\/?\?v=|reel\/|videos\/)(\d+)[^"]*)"', page_src)
            print(f"  Matched {len(href_matches)} video hrefs directly.")
            for full_href, vid_id in href_matches:
                if vid_id not in discovered_videos:
                    discovered_videos[vid_id] = {
                        'id': vid_id,
                        'href': full_href,
                        'source': label,
                        'source_url': url
                    }

            # Check all <a> elements
            for a in driver.find_elements(By.TAG_NAME, "a"):
                try:
                    href = a.get_attribute("href") or ""
                    m = re.search(r'(?:watch\/?\?v=|reel\/|videos\/)(\d+)', href)
                    if m:
                        vid_id = m.group(1)
                        if vid_id not in discovered_videos:
                            discovered_videos[vid_id] = {
                                'id': vid_id,
                                'href': href,
                                'source': label,
                                'source_url': url
                            }
                except Exception:
                    pass

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    driver.quit()
    
    print(f"\n==========================================")
    print(f"Total Unique Discovered Video IDs: {len(discovered_videos)}")
    print(f"==========================================")
    
    with open('data/all_crawled_video_ids.json', 'w', encoding='utf-8') as f:
        json.dump(discovered_videos, f, indent=2, ensure_ascii=False)
        
    return discovered_videos

if __name__ == '__main__':
    crawl_all_sources()
