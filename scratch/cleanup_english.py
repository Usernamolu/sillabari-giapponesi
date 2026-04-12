
import os
import re

REPOS_ROOT = r'c:\Users\Gabriele Errico\Downloads\alfabeto-giapponese'
DIRECTORIES = [os.path.join(REPOS_ROOT, 'hiragana'), os.path.join(REPOS_ROOT, 'katakana')]

def cleanup_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Target <p class="mnemonic-text"> or similar sections
    # Find the technique section
    pattern = r'(<strong>Tecnica:</strong>.*?)(</p>)'
    
    def replacer(match):
        text = match.group(1)
        # Remove (em something /em) or (something)
        # We want to be careful not to remove important hints if they are in Italian.
        # But the user said "eliminerei questa spiegazione in inglese".
        
        # Specifically targeting common English patterns or just anything in parentheses within technique
        # Since technique is usually a single sentence, removing parentheses is generally safe if they contain English.
        
        # Remove (<em>...</em>)
        text = re.sub(r'\s*\(\s*<em>.*?</em>\s*\)', '', text)
        # Remove (...) if it contains common english words or is just 1-2 words
        # but let's be more specific as per user request
        text = re.sub(r'\s*\((exotic bird|eagle|chef hat|kite|paddy hat|What\?|Woof woof!|sew)\)', '', text, flags=re.IGNORECASE)
        # Generic removal of parentheses with only latin chars and spaces (English-like)
        # avoiding those that might be Italian (though Italian also uses latin chars)
        # But in this project, parentheses in technique are almost exclusively English translations.
        text = re.sub(r'\s*\([a-zA-Z\s\?!\']+\)', '', text)
        
        return text + match.group(2)

    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if __name__ == "__main__":
    count = 0
    for d in DIRECTORIES:
        if not os.path.exists(d): continue
        for filename in os.listdir(d):
            if filename.endswith('.html'):
                if cleanup_file(os.path.join(d, filename)):
                    print(f"Cleaned {filename}")
                    count += 1
    print(f"Total files cleaned: {count}")
