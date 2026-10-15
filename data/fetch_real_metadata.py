import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

# The 13 exact unique Facebook video IDs
video_ids = [
    {"id": "1799107854858722", "type": "video", "raw_title": "সবাই যদি পেজে শুধু সেল পোস্ট করে, তাহলে কাস্টমারগণ কনফিউজড হয়ে যাবে। এই বিষয় নিয়েই আলোচনা করেছি এই ভিডিওতে।"},
    {"id": "1074861638689673", "type": "video", "raw_title": "মানুষ কেনো আসবে আপনার পেজ এ শুধুমাত্র সেল এ ফোকাস করলেই সেল আসবে আসলে কোথায় ফোকাস করা উচিত?"},
    {"id": "4547049732233511", "type": "video", "raw_title": "একটা পেজ এ আসলে কত কিছু নিয়ে বাজেট নির্ধারণ করা হয় কীভাবে টার্গেট নিয়ে আমরা কাজ করি?"},
    {"id": "2164356940816788", "type": "video", "raw_title": "কম্পিটিটরদের নিয়ে আলোচনা করছি এই ভিডিওতে - ব্যবসা টিকিয়ে রাখার কৌশল"},
    {"id": "2103034266972859", "type": "video", "raw_title": "অনেকের ই পেজ হ্যাক হয়ে যায় আর বলেন যে আমি তো কাউকে পাসওয়ার্ড দেইনি তাহলে কীভাবে হ্যাক হলো?"},
    {"id": "1647838006697000", "type": "video", "raw_title": "কি দেখলাম আর কি বলে এলাম আমি - Sew in Style by Farzana তে সরাসরি ভিজিট ও পর্যালোচনা"},
    {"id": "1664378378370632", "type": "video", "raw_title": "আজ যার সাথে কথা বলছি তিনি কলকাতা থেকে কথা বলছেন - ক্রস-বর্ডার গ্রাহক সেবা ও আস্থা"},
    {"id": "1779643576652553", "type": "reel", "raw_title": "দুইটা স্বপ্নকে ছুঁয়ে দেখার পরে মনটা একটু স্বস্তি পেলো - উদ্যোক্তা জীবনের স্বপ্নপূরণ"},
    {"id": "28879471551690198", "type": "reel", "raw_title": "Our Gangstars - আইসিটি কেয়ার ও বিজনেস টিম কালচার"},
    {"id": "1459493229610521", "type": "reel", "raw_title": "আমার আব্বাজানেরা - উদ্যোক্তা ও পারিবারিক অনুপ্রেরণা"},
    {"id": "29212835464966601", "type": "reel", "raw_title": "বিজনেস গ্রোথ ও সোশ্যাল মিডিয়া মার্কেটিং সিক্রেট"},
    {"id": "1005794999198809", "type": "reel", "raw_title": "অনলাইন অর্ডারে গ্রাহক ধরে রাখার সহজ ফর্মুলা"},
    {"id": "1808047586884169", "type": "reel", "raw_title": "উদ্যোক্তার প্রতিদিনের ডিসিশন মেকিং ও টাইম ম্যানেজমেন্ট"}
]

print(f"Total videos to fetch metadata for: {len(video_ids)}")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

results = []

for idx, v in enumerate(video_ids, 1):
    vid_id = v['id']
    url = f"https://www.facebook.com/watch/?v={vid_id}" if v['type'] == 'video' else f"https://www.facebook.com/reel/{vid_id}"
    print(f"\n[{idx}/{len(video_ids)}] Fetching: {url} ...")
    
    try:
        driver.get(url)
        time.sleep(3)
        title = driver.title
        # Look for description in meta tags or spans
        description = ""
        try:
            og_desc = driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute("content")
            if og_desc:
                description = og_desc
        except Exception:
            pass
        
        results.append({
            "id": vid_id,
            "url": url,
            "type": v['type'],
            "raw_title": v['raw_title'],
            "page_title": title,
            "description": description
        })
        print(f"  Title: {title[:60]}")
        if description:
            print(f"  Desc: {description[:80]}")
    except Exception as e:
        print(f"  Error: {e}")
        results.append({
            "id": vid_id,
            "url": url,
            "type": v['type'],
            "raw_title": v['raw_title'],
            "page_title": "",
            "description": ""
        })

driver.quit()

with open("data/real_fb_videos_metadata.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n✅ Saved data/real_fb_videos_metadata.json successfully!")
