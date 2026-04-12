import os
import re

def improve_details():
    base_dir = r"c:\Users\Gabriele Errico\Downloads\alfabeto-giapponese"
    
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        if "hiragana" in root or "katakana" in root:
            for file in files:
                if file.endswith(".html"):
                    html_files.append(os.path.join(root, file))

    print(f"Updating {len(html_files)} detail pages for accessibility...")

    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Add lang="ja" to main-kana
        content = content.replace('<h1 class="main-kana">', '<h1 class="main-kana" lang="ja">')
        
        # 2. Add lang="ja" to word-jp
        content = content.replace('<span class="word-jp">', '<span class="word-jp" lang="ja">')
        
        # 3. Add lang="ja" to ref-char
        content = content.replace('<span class="ref-char">', '<span class="ref-char" lang="ja">')
        
        # 4. Add aria-label to back-btn
        # Find if it's hiragana or katakana back button
        if 'class="back-btn">&larr; Tabella Hiragana</a>' in content:
             content = content.replace('class="back-btn">', 'class="back-btn" aria-label="Torna alla tabella Hiragana">')
        elif 'class="back-btn">&larr; Tabella Katakana</a>' in content:
             content = content.replace('class="back-btn">', 'class="back-btn" aria-label="Torna alla tabella Katakana">')

        # 5. Semantic fix: Ensure <img> for stroke order has alt text?
        # Wait, the current pages use <div> for stroke order assets? 
        # No, they use an image or GIF eventually. 
        # Let's check a detail page structure again.
        
        # Currently detail pages have <h2> sections.
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated A11y: {filepath}")

if __name__ == "__main__":
    improve_details()
