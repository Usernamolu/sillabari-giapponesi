import os
import re

def update_google_fonts():
    base_dir = r"c:\Users\Gabriele Errico\Downloads\alfabeto-giapponese"
    
    # Target import line
    # We want to add Klee One to the existing Noto Sans JP import
    # Old could be Noto+Sans+JP:wght@300;400;700 or Noto+Sans+JP:wght@300;500;700
    
    new_font_link = '<link href="https://fonts.googleapis.com/css2?family=Klee+One:wght@400;600&family=Noto+Sans+JP:wght@300;400;700&display=swap" rel="stylesheet">'
    
    # Regex to find any Google Fonts link that includes Noto Sans JP
    font_pattern = re.compile(r'<link href="https://fonts\.googleapis\.com/css2\?family=Noto\+Sans\+JP:wght@[0-9;]+&display=swap" rel="stylesheet">')

    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))

    print(f"Updating {len(html_files)} files with Klee One font...")

    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if font_pattern.search(content):
            new_content = font_pattern.sub(new_font_link, content)
            
            # Also ensure Noto Serif JP is there as fallback in the CSS (already handled)
            # But we might want to import it too just in case Klee One fails
            # Let's stick to Klee One + Noto Sans JP as per plan
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {filepath}")
        else:
            print(f"Font link not found in: {filepath}")

if __name__ == "__main__":
    update_google_fonts()
