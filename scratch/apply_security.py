import os
import glob

directories = ['.', 'hiragana', 'katakana']
html_files = []

for d in directories:
    html_files.extend(glob.glob(os.path.join(d, '*.html')))

csp_tag = '    <meta http-equiv="Content-Security-Policy" content="default-src \'self\'; style-src \'self\' \'unsafe-inline\' https://fonts.googleapis.com; font-src https://fonts.gstatic.com;">\n'

modified_count = 0

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Add CSP tag
    if 'Content-Security-Policy' not in content:
        # insert after <meta charset="UTF-8">
        content = content.replace('<meta charset="UTF-8">\n', f'<meta charset="UTF-8">\n{csp_tag}')

    # 2. Fix target="_blank"
    if 'target="_blank"' in content and 'rel="noopener noreferrer"' not in content:
        content = content.replace('target="_blank"', 'target="_blank" rel="noopener noreferrer"')

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        modified_count += 1

print(f"Modificati {modified_count} file aggiungendo CSP metadata e rel=noopener.")
