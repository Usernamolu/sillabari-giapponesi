import os
import re

def update_html_with_favicons(root_dir):
    favicon_tags_root = """    <link rel="icon" type="image/png" href="assets/favicons/favicon-96x96.png" sizes="96x96" />
    <link rel="shortcut icon" href="assets/favicons/favicon.ico" />
    <link rel="apple-touch-icon" sizes="180x180" href="assets/favicons/apple-touch-icon.png" />
    <link rel="manifest" href="site.webmanifest" />"""

    favicon_tags_sub = """    <link rel="icon" type="image/png" href="../assets/favicons/favicon-96x96.png" sizes="96x96" />
    <link rel="shortcut icon" href="../assets/favicons/favicon.ico" />
    <link rel="apple-touch-icon" sizes="180x180" href="../assets/favicons/apple-touch-icon.png" />
    <link rel="manifest" href="../site.webmanifest" />"""

    for root, dirs, files in os.walk(root_dir):
        # Skip assets and scratch directories
        if any(x in root for x in ['assets', 'scratch', '.git']):
            continue

        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                is_root = (root == root_dir)
                tags = favicon_tags_root if is_root else favicon_tags_sub

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check if already has favicons to avoid duplication
                if 'rel="icon"' in content or 'rel="shortcut icon"' in content:
                    continue

                # Insert after <meta charset> or <title>
                if '<head>' in content:
                    new_content = re.sub(r'(<head>.*?\n)', f'\\1{tags}\n', content, flags=re.DOTALL | re.IGNORECASE)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {file_path}")

if __name__ == "__main__":
    update_html_with_favicons(r"c:\Users\Gabriele Errico\Downloads\alfabeto-giapponese")
