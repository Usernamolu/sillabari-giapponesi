import re

def improve_index():
    filepath = r"c:\Users\Gabriele Errico\Downloads\alfabeto-giapponese\index.html"
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add skip link
    if '<a href="#main-content" class="skip-link"' not in content:
        content = content.replace('<body>', '<body>\n    <a href="#main-content" class="skip-link">Vai al contenuto principale</a>')
    
    # Add id to main
    content = content.replace('<main>', '<main id="main-content">')

    # 2. Add scope to table headers
    # Column headers
    content = content.replace('<th>a</th>', '<th scope="col">a</th>')
    content = content.replace('<th>i</th>', '<th scope="col">i</th>')
    content = content.replace('<th>u</th>', '<th scope="col">u</th>')
    content = content.replace('<th>e</th>', '<th scope="col">e</th>')
    content = content.replace('<th>o</th>', '<th scope="col">o</th>')

    # Row labels headers
    content = re.sub(r'<th class="row-label">([^<]+)</th>', r'<th class="row-label" scope="row">\1</th>', content)

    # 3. Add lang="ja" and aria-label to links
    # Pattern: <a href="hiragana/a.html">\n\s+<span class="kana">あ</span>\n\s+<span class="romaji">a</span>\n\s+</a>
    # We want to transform to:
    # <a href="hiragana/a.html" aria-label="Scheda didattica Hiragana あ (a)">
    #     <span class="kana" lang="ja">あ</span>
    #     <span class="romaji">a</span>
    # </a>

    def replacer(match):
        path = match.group(1)
        kana = match.group(2)
        romaji = match.group(3)
        type_kana = "Hiragana" if "hiragana/" in path else "Katakana"
        return f'<a href="{path}" aria-label="Scheda didattica {type_kana} {kana} ({romaji})">\n                                    <span class="kana" lang="ja">{kana}</span>\n                                    <span class="romaji">{romaji}</span>\n                                </a>'

    link_pattern = re.compile(r'<a href="([^"]+)">\s+<span class="kana">([^<]+)</span>\s+<span class="romaji">([^<]+)</span>\s+</a>')
    content = link_pattern.sub(replacer, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    improve_index()
