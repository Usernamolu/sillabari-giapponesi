import os
import re
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'a' and 'href' in attrs_dict:
            self.links.append(attrs_dict['href'])
        if 'id' in attrs_dict:
            self.anchors.append(attrs_dict['id'])
        if 'name' in attrs_dict:
            self.anchors.append(attrs_dict['name'])

def get_file_anchors(filepath):
    if not os.path.exists(filepath):
        return []
    parser = LinkParser()
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        parser.feed(f.read())
    return parser.anchors

def check_links():
    base_dir = r"c:\Users\Gabriele Errico\Downloads\alfabeto-giapponese"
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        if ".git" in dirs:
            dirs.remove(".git")
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))

    print(f"Found {len(html_files)} HTML files. Starting analysis...")
    print("-" * 50)

    broken_links = []
    total_links_checked = 0
    
    # Cache for anchors to avoid re-parsing the same file multiple times
    anchor_cache = {}

    for source_file in html_files:
        parser = LinkParser()
        with open(source_file, 'r', encoding='utf-8', errors='ignore') as f:
            parser.feed(f.read())

        source_rel = os.path.relpath(source_file, base_dir)
        
        for href in parser.links:
            # Skip external links and mailto/tel
            if href.startswith(("http", "mailto:", "tel:", "javascript:")):
                continue
            
            total_links_checked += 1
            
            # Split href into path and anchor
            parsed_href = urlparse(href)
            path = unquote(parsed_href.path)
            anchor = parsed_href.fragment

            # Calculate absolute path of target
            if not path: # Link to an anchor in the same file
                target_file = source_file
            else:
                source_dir = os.path.dirname(source_file)
                target_file = os.path.abspath(os.path.join(source_dir, path))

            # 1. Check if file exists
            if not os.path.exists(target_file):
                broken_links.append({
                    "source": source_rel,
                    "target": href,
                    "reason": "File not found"
                })
                continue

            # 2. Check if anchor exists in target file
            if anchor:
                if target_file not in anchor_cache:
                    anchor_cache[target_file] = get_file_anchors(target_file)
                
                if anchor not in anchor_cache[target_file]:
                    broken_links.append({
                        "source": source_rel,
                        "target": href,
                        "reason": f"Anchor '#{anchor}' not found in target"
                    })

    print(f"Analysis complete.")
    print(f"Total links checked: {total_links_checked}")
    print(f"Broken links found: {len(broken_links)}")
    print("-" * 50)

    if broken_links:
        print("BROKEN LINKS REPORT:")
        for bl in broken_links:
            print(f"Source: {bl['source']}")
            print(f"  -> Target: {bl['target']}")
            print(f"  -> Reason: {bl['reason']}")
            print("")
    else:
        print("All internal links are valid! Great job.")

if __name__ == "__main__":
    check_links()
