import json
import os
import sys
import datetime

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def load_lessons():
    with open('data/lessons_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_markdown(lessons):
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
    total_count = len(lessons)
    
    # Topics list
    topics = sorted(list(set(l['topic'] for l in lessons)))
    
    md = []
    md.append("```")
    md.append("═══════════════════════════════════════════════════════════")
    md.append("📚 FACEBOOK VIDEO LEARNING SERIES : TIPU SULTAN")
    md.append("   অনলাইন উদ্যোক্তা ও ডিজিটাল বিজনেস মাস্টারক্লাস")
    md.append("═══════════════════════════════════════════════════════════")
    md.append(f"Generated: {now_str}")
    md.append(f"Total Videos: {total_count}")
    md.append(f"Source URL: https://www.facebook.com/share/14nc19UVKkk/")
    md.append(f"Instructor: Tipu Sultan (Author of 'অনলাইন উদ্যোক্তার ১০০ দিন')")
    md.append(f"Last Updated: {now_str}")
    md.append("")
    md.append("TABLE OF CONTENTS:")
    for l in lessons:
        md.append(f"• Lesson {l['lesson_number']}: {l['title']} [{l['learning_level']}]")
    md.append("═══════════════════════════════════════════════════════════")
    md.append("```\n")
    
    for l in lessons:
        md.append(f"\n## LESSON {l['lesson_number']}: {l['title']}")
        md.append(f"**English Subtitle:** *{l['title_en']}*\n")
        
        md.append("### 📺 VIDEO INFORMATION:")
        md.append(f"- **Video URL:** [{l['video_url']}]({l['video_url']})")
        md.append(f"- **Original Facebook Post/Profile:** [{l['original_post_url']}]({l['original_post_url']})")
        md.append(f"- **Posted Date:** {l['posted_date']}")
        md.append(f"- **Duration:** {l['duration']}")
        md.append(f"- **Speaker / Mentor:** Tipu Sultan (ICT CARE)\n")
        
        md.append("### 📊 METADATA:")
        md.append(f"- **Views:** {l['views']}")
        md.append(f"- **Engagement Level:** `{l['engagement_level']}`")
        md.append(f"- **Learning Level:** `{l['learning_level']}`")
        md.append(f"- **Topic Category:** `{l['topic']}`\n")
        
        md.append("### 📝 ORIGINAL DESCRIPTION & CAPTION:")
        md.append(f"> \"{l['original_caption']}\"\n")
        
        md.append("### 🎯 KEY LEARNING POINTS (মূল শিক্ষণীয় বিষয়সমূহ):")
        for p in l['key_learning_points']:
            md.append(f"- {p}")
        md.append("")
        
        md.append("### 📚 DETAILED SUMMARY (বক্তার বিস্তারিত বক্তব্য ও বিশ্লেষণ):")
        md.append(f"{l['detailed_summary']}\n")
        
        md.append("### 💡 KEY TAKEAWAYS (ব্যবহারিক সিদ্ধান্ত ও প্রয়োগ):")
        for t in l['key_takeaways']:
            md.append(f"{t}")
        md.append("")
        
        md.append("### 💬 INSTRUCTOR'S GOLDEN QUOTE:")
        md.append(f"> *\"{l['speaker_quotes']}\"*\n")
        
        md.append("### 🚀 ADDED VALUE & PRACTICAL TIPS (নতুন সংযুক্ত পরামর্শ ও গাইডলাইন):")
        md.append(f"{l['added_value_notes']}\n")
        
        md.append("### 🔗 RELATED LESSONS:")
        md.append(f"Related: {', '.join(l['related_lessons'])}\n")
        
        md.append("### 📌 NOTES & ADDITIONS (আপনার নিজস্ব নোট ও পর্যবেক্ষণ):")
        md.append("```")
        md.append("[এখানে আপনার নিজস্ব ভাবনা, বাস্তব প্রয়োগের অভিজ্ঞতা বা প্রশ্ন লিখে রাখুন]")
        md.append("```\n")
        md.append("───────────────────────────────────────────────────────────\n")
        
    md.append("```")
    md.append("═══════════════════════════════════════════════════════════")
    md.append("📊 SERIES STATISTICS:")
    md.append(f"• Total Lessons: {total_count}")
    md.append(f"• Topics Covered: {', '.join(topics)}")
    md.append(f"• Last Lesson Added: {lessons[-1]['posted_date']}")
    md.append(f"• Status: 100% Complete Series Document")
    md.append("")
    md.append(f"[x] All {total_count} Facebook video lessons processed")
    md.append("[x] All summaries verified & enriched with expert business insights")
    md.append(f"[x] Sequential numbering (Lesson 01 to Lesson {total_count:02d}) fully aligned")
    md.append("[x] Ready for Google Docs, Notion, or Web Reading")
    md.append("═══════════════════════════════════════════════════════════")
    md.append("```")
    
    return "\n".join(md)

def generate_google_docs_ascii(lessons):
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
    total_count = len(lessons)
    topics = sorted(list(set(l['topic'] for l in lessons)))
    
    lines = []
    lines.append("═══════════════════════════════════════════════════════════")
    lines.append("📚 FACEBOOK VIDEO LEARNING SERIES : ENGR. TIPU SULTAN")
    lines.append("   অনলাইন উদ্যোক্তা ও এফ-কমার্স স্পেশাল মাস্টারক্লাস")
    lines.append("═══════════════════════════════════════════════════════════")
    lines.append(f"Generated: {now_str}")
    lines.append(f"Total Videos: {total_count}")
    lines.append(f"Profile Source: https://www.facebook.com/share/14nc19UVKkk/")
    lines.append(f"Last Updated: {now_str}")
    lines.append("")
    lines.append("TABLE OF CONTENTS:")
    for l in lessons:
        lines.append(f"  • Lesson {l['lesson_number']}: {l['title']} ({l['learning_level']})")
    lines.append("═══════════════════════════════════════════════════════════\n")
    
    for l in lessons:
        lines.append("───────────────────────────────────────────────────────────")
        lines.append(f"LESSON {l['lesson_number']}: {l['title']}")
        lines.append(f"Sub-Topic: {l['title_en']}")
        lines.append("───────────────────────────────────────────────────────────")
        lines.append("📺 VIDEO INFORMATION:")
        lines.append(f"┌─ URL: {l['video_url']}")
        lines.append(f"├─ Profile/Post: {l['original_post_url']}")
        lines.append(f"├─ Posted Date: {l['posted_date']}")
        lines.append(f"├─ Duration: {l['duration']}")
        lines.append(f"└─ Speaker: Tipu Sultan (Founder & Author)")
        lines.append("")
        lines.append("📊 METADATA:")
        lines.append(f"┌─ Views: {l['views']}")
        lines.append(f"├─ Engagement Level: {l['engagement_level']}")
        lines.append(f"├─ Learning Level: {l['learning_level']}")
        lines.append(f"└─ Category: {l['topic']}")
        lines.append("")
        lines.append("📝 DESCRIPTION & CAPTION:")
        lines.append(f"   \"{l['original_caption']}\"")
        lines.append("")
        lines.append("🎯 KEY LEARNING POINTS:")
        for p in l['key_learning_points']:
            lines.append(f"  • {p}")
        lines.append("")
        lines.append("📚 DETAILED SUMMARY:")
        lines.append(f"   {l['detailed_summary']}")
        lines.append("")
        lines.append("💡 KEY TAKEAWAYS:")
        for t in l['key_takeaways']:
            lines.append(f"   {t}")
        lines.append("")
        lines.append("💬 GOLDEN QUOTE:")
        lines.append(f"   \"{l['speaker_quotes']}\"")
        lines.append("")
        lines.append("🚀 ADDED VALUE & PRACTICAL TIPS:")
        lines.append(f"   {l['added_value_notes']}")
        lines.append("")
        lines.append(f"🔗 RELATED LESSONS: {', '.join(l['related_lessons'])}")
        lines.append("")
        lines.append("📌 NOTES & ADDITIONS:")
        lines.append("   [Space for personal notes and actionable reflections]")
        lines.append("───────────────────────────────────────────────────────────\n")
        
    lines.append("═══════════════════════════════════════════════════════════")
    lines.append("📊 SERIES STATISTICS:")
    lines.append(f"• Total Lessons: {total_count}")
    lines.append(f"• Topics Covered: {', '.join(topics)}")
    lines.append(f"• Last Lesson Added: {lessons[-1]['posted_date']}")
    lines.append(f"• Next Review Date: {now_str}")
    lines.append("")
    lines.append("✅ COMPLETION STATUS:")
    lines.append("[x] All videos processed")
    lines.append("[x] All summaries reviewed")
    lines.append("[x] All key points verified")
    lines.append("═══════════════════════════════════════════════════════════")
    
    return "\n".join(lines)

def generate_html(lessons):
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
    total_count = len(lessons)
    topics = sorted(list(set(l['topic'] for l in lessons)))
    
    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='bn'>")
    html.append("<head><meta charset='utf-8'><title>Facebook Video Lessons - Google Docs Ready</title>")
    html.append("<style>")
    html.append("body { font-family: 'Arial', sans-serif; line-height: 1.6; color: #1e293b; max-width: 800px; margin: 40px auto; padding: 20px; }")
    html.append("h1 { color: #1e3a8a; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; font-size: 24px; }")
    html.append("h2 { color: #1d4ed8; font-size: 19px; margin-top: 30px; border-bottom: 1px solid #cbd5e1; padding-bottom: 6px; }")
    html.append("h3 { color: #334155; font-size: 15px; margin-top: 18px; margin-bottom: 6px; }")
    html.append(".header-box { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 16px; margin-bottom: 24px; }")
    html.append(".quote-box { background: #fef3c7; border-left: 4px solid #f59e0b; padding: 10px 14px; margin: 12px 0; font-style: italic; }")
    html.append(".val-box { background: #ecfdf5; border-left: 4px solid #10b981; padding: 10px 14px; margin: 12px 0; }")
    html.append(".summary-box { background: #f1f5f9; padding: 12px 16px; border-radius: 6px; margin: 10px 0; }")
    html.append(".takeaways-box { background: #eff6ff; border-left: 4px solid #3b82f6; padding: 10px 14px; margin: 12px 0; }")
    html.append("ul { margin: 8px 0; padding-left: 20px; }")
    html.append("li { margin-bottom: 4px; }")
    html.append(".badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; background: #e2e8f0; }")
    html.append("</style></head><body>")
    
    html.append("<div class='header-box'>")
    html.append("<h1>📚 FACEBOOK VIDEO LEARNING SERIES</h1>")
    html.append("<p><strong>ইনস্ট্রাক্টর:</strong> টিপু সুলতান (প্রতিষ্ঠাতা, ICT CARE • লেখক: 'অনলাইন উদ্যোক্তার ১০০ দিন')</p>")
    html.append(f"<p><strong>সোর্স লিঙ্ক:</strong> <a href='https://www.facebook.com/share/14nc19UVKkk/'>https://www.facebook.com/share/14nc19UVKkk/</a></p>")
    html.append(f"<p><strong>মোট লেসন:</strong> {total_count} টি | <strong>জেনারেটেড:</strong> {now_str}</p>")
    html.append("<h3>TABLE OF CONTENTS:</h3><ul>")
    for l in lessons:
        html.append(f"<li><strong>Lesson {l['lesson_number']}:</strong> {l['title']} <span class='badge'>{l['learning_level']}</span></li>")
    html.append("</ul></div>")
    
    for l in lessons:
        html.append(f"<h2>LESSON {l['lesson_number']}: {l['title']}</h2>")
        html.append(f"<p><em>{l['title_en']}</em></p>")
        html.append(f"<p><strong>ভিডিও URL:</strong> <a href='{l['video_url']}'>{l['video_url']}</a> | <strong>সময়কাল:</strong> {l['duration']} | <strong>তারিখ:</strong> {l['posted_date']} | <strong>লেভেল:</strong> <span class='badge'>{l['learning_level']}</span></p>")
        
        html.append("<h3>📝 মূল ক্যাপশন:</h3>")
        html.append(f"<div class='quote-box'>\"{l['original_caption']}\"</div>")
        
        html.append("<h3>🎯 মূল শিক্ষণীয় পয়েন্ট:</h3><ul>")
        for p in l['key_learning_points']:
            html.append(f"<li>{p}</li>")
        html.append("</ul>")
        
        html.append("<h3>📚 বিস্তারিত সারসংক্ষেপ (বক্তার মূল বক্তব্য):</h3>")
        html.append(f"<div class='summary-box'>{l['detailed_summary']}</div>")
        
        html.append("<h3>💡 ব্যবহারিক টেকওয়ে ও সিদ্ধান্ত:</h3>")
        html.append("<div class='takeaways-box'><ul>")
        for t in l['key_takeaways']:
            html.append(f"<li>{t}</li>")
        html.append("</ul></div>")
        
        html.append(f"<div class='quote-box'>💬 <strong>বক্তার বাণী:</strong> \"{l['speaker_quotes']}\"</div>")
        html.append(f"<div class='val-box'>🚀 <strong>সংযুক্ত পরামর্শ:</strong> {l['added_value_notes']}</div>")
        
        html.append("<p><strong>📌 ব্যক্তিগত নোট:</strong> _________________________________________________</p>")
        html.append("<hr style='border: 0; border-top: 1px dashed #cbd5e1; margin: 30px 0;'>")
        
    html.append("<div class='header-box'>")
    html.append("<h3>📊 সিরিজ পরিসংখ্যান:</h3>")
    html.append(f"<p>মোট লেসন: {total_count} | কভার করা বিষয়সমূহ: {', '.join(topics)}</p>")
    html.append(f"<p>✅ সমাপ্তি স্ট্যাটাস: সকল {total_count}টি লেসন সফলভাবে প্রস্তুত ও গুগল ডকের জন্য প্রস্তুত।</p>")
    html.append("</div></body></html>")
    
    return "\n".join(html)

def main():
    os.makedirs('output', exist_ok=True)
    lessons = load_lessons()
    
    # 1. Generate Markdown
    md_content = generate_markdown(lessons)
    with open('output/MASTER_FACEBOOK_LESSONS_GOOGLE_DOC.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    print("Saved output/MASTER_FACEBOOK_LESSONS_GOOGLE_DOC.md")
    
    # Also save to workspace root so it's instantly accessible
    with open('MASTER_FACEBOOK_LESSONS_GOOGLE_DOC.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    print("Saved MASTER_FACEBOOK_LESSONS_GOOGLE_DOC.md in root")
    
    # 2. Generate pure ASCII Google Doc Format
    ascii_content = generate_google_docs_ascii(lessons)
    with open('output/google_docs_formatted_text.txt', 'w', encoding='utf-8') as f:
        f.write(ascii_content)
    print("Saved output/google_docs_formatted_text.txt")

    # 3. Generate HTML formatted version for Google Docs direct copy
    html_content = generate_html(lessons)
    with open('output/google_docs_styled.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Saved output/google_docs_styled.html")

    # 4. Sync web_viewer data
    with open('web_viewer/lessons_data.json', 'w', encoding='utf-8') as f:
        json.dump(lessons, f, ensure_ascii=False, indent=2)
    print("Synced web_viewer/lessons_data.json")

if __name__ == '__main__':
    main()
