#!/usr/bin/env python3
"""
Facebook Video Learning Series Orchestrator & Google Docs Generator
===================================================================
Automates extraction, sequential lesson formatting, AI enrichment,
and Google Docs output for Facebook video series (e.g. Md Shouvikur Rahman).
"""

import os
import sys
import json
import argparse
import http.server
import socketserver
import webbrowser

# Ensure Windows terminal handles UTF-8 (Bengali & emojis) gracefully
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from generate_lessons import main as generate_all_outputs, load_lessons

PORT = 8080

def show_banner():
    print("=" * 65)
    print(" 🚀 FACEBOOK VIDEO TO GOOGLE DOCS ORCHESTRATOR")
    print("    Antigravity Autonomous Educational Workflow")
    print("=" * 65)

def list_lessons():
    lessons = load_lessons()
    print(f"\nTotal Lessons: {len(lessons)}\n")
    for l in lessons:
        print(f"[{l['lesson_number']}] {l['title']} ({l['learning_level']}) - {l['duration']}")
    print("-" * 65)

def serve_web_viewer():
    web_dir = os.path.join(os.path.dirname(__file__), 'web_viewer')
    os.chdir(web_dir)
    handler = http.server.SimpleHTTPRequestHandler
    
    print(f"\n🌐 Desktop Local URL: http://localhost:{PORT}")
    print(f"📶 Same Wi-Fi LAN:    http://10.0.0.91:{PORT}")
    print(f"🌍 Worldwide GitHub:  https://sultantipu199.github.io/learn-from-fb/")
    print("   (যেকোনো স্মার্টফোন বা কম্পিউটার থেকে সরাসরি ওপেন বা কিউআর কোড স্ক্যান করুন)\n")
    
    # Try opening the web browser
    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except Exception:
        pass

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

def main():
    parser = argparse.ArgumentParser(description="Facebook Video Learning Series Automation")
    parser.add_argument("--list", action="store_true", help="List all processed lessons")
    parser.add_argument("--generate", action="store_true", help="Regenerate all Markdown & Google Docs outputs")
    parser.add_argument("--serve", action="store_true", help="Start the web viewer dashboard")
    
    args = parser.parse_args()
    show_banner()

    if args.list:
        list_lessons()
    elif args.serve:
        serve_web_viewer()
    else:
        # Default action: generate outputs and display summary
        generate_all_outputs()
        print("\n✅ All documents generated successfully!")
        print("📁 1. MASTER_FACEBOOK_LESSONS_GOOGLE_DOC.md (Workspace root)")
        print("📁 2. output/google_docs_formatted_text.txt (Ready for Google Docs)")
        print("🌐 3. web_viewer/ (Interactive web viewer with 1-click Google Docs copy)")
        print("\nTip: Run with --serve to preview lessons in your browser.")

if __name__ == "__main__":
    main()
