
import os
import re

# Paths
REPOS_ROOT = r'c:\Users\Gabriele Errico\Downloads\alfabeto-giapponese'
SLIDE_DECK = r'c:\Users\Gabriele Errico\Desktop\Japanese_Literacy_Course\03_Lessons\L02\L02_SlideDeck.md'
KATAKANA_DIR = os.path.join(REPOS_ROOT, 'katakana')
METADATA_FILE = os.path.join(REPOS_ROOT, 'metadata', 'katakana.tei.xml')

def extract_data_from_slides(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract mnemonic and romaji for each character
    # Pattern: ## Vocale A (ア) or ## Ka (カ)
    sections = re.split(r'---', content)
    
    char_data = {}
    
    # Common Romaji to help map
    romaji_map = [
        ('a', 'ア'), ('i', 'イ'), ('u', 'ウ'), ('e', 'エ'), ('o', 'オ'),
        ('ka', 'カ'), ('ki', 'キ'), ('ku', 'ク'), ('ke', 'ケ'), ('ko', 'コ'),
        ('sa', 'サ'), ('shi', 'シ'), ('su', 'ス'), ('se', 'セ'), ('so', 'ソ'),
        ('ta', 'タ'), ('chi', 'チ'), ('tsu', 'ツ'), ('te', 'テ'), ('to', 'ト'),
        ('na', 'ナ'), ('ni', 'ニ'), ('nu', 'ヌ'), ('ne', 'ネ'), ('no', 'ノ'),
        ('ha', 'ハ'), ('hi', 'ヒ'), ('fu', 'フ'), ('he', 'ヘ'), ('ho', 'ホ'),
        ('ma', 'マ'), ('mi', 'ミ'), ('mu', 'ム'), ('me', 'メ'), ('mo', 'モ'),
        ('ya', 'ヤ'), ('yu', 'ユ'), ('yo', 'ヨ'),
        ('ra', 'ラ'), ('ri', 'リ'), ('ru', 'ル'), ('re', 'レ'), ('ro', 'ロ'),
        ('wa', 'ワ'), ('wo', 'ヲ'), ('n', 'ン')
    ]

    for romaji, kana in romaji_map:
        # Find section for this kana
        # Usually headers like "## Vocale A (ア)" or "## Ka: ..."
        pattern = rf'## .*?({kana}|{romaji.capitalize()})(?::|\s|\()+'
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            start_pos = match.start()
            # Find next header
            next_header = re.search(r'---', content[start_pos:])
            section_text = content[start_pos:start_pos + next_header.start()] if next_header else content[start_pos:]
            
            # Extract info
            # Mnemonic
            mnem_match = re.search(r'immagine (?:mnemonica )?di (?:un )?<strong>(.*?)</strong>', section_text, re.IGNORECASE)
            if not mnem_match:
                mnem_match = re.search(r'può ricordare (?:un |una )?<strong>(.*?)</strong>', section_text, re.IGNORECASE)
            if not mnem_match:
                mnem_match = re.search(r'visualizzato come (?:un |una )?<strong>(.*?)</strong>', section_text, re.IGNORECASE)
            if not mnem_match:
                mnem_match = re.search(r'immaginiamo (?:un |una )?<strong>(.*?)</strong>', section_text, re.IGNORECASE)
            
            mnem = mnem_match.group(1) if mnem_match else "da completare"
            
            # Stroke note
            stroke_note = re.search(r'([^\n]*tratti[^\n]*)', section_text)
            stroke_desc = stroke_note.group(1).strip() if stroke_note else "Placeholder in attesa delle slide Katakana."
            
            # Example word (find in tables)
            # Find closest table
            table_match = re.search(rf'\| ({kana})[^\n]*\|', content)
            example_row = table_match.group(0) if table_match else ""
            parts = [p.strip() for p in example_row.split('|')] if example_row else []
            
            ex_jp = parts[1] if len(parts) > 1 else ""
            ex_romaji = parts[2] if len(parts) > 2 else ""
            ex_meaning = parts[4] if len(parts) > 4 else ""
            
            char_data[romaji] = {
                'kana': kana,
                'mnemonic': mnem,
                'stroke_desc': stroke_desc,
                'ex_jp': ex_jp,
                'ex_romaji': ex_romaji,
                'ex_meaning': ex_meaning
            }
            
    return char_data

def update_html_files(char_data):
    # Manual tweaks to some stroke counts and descriptions based on common knowledge if missing
    # or just use the extracted ones.
    
    # We need to be careful with the mapping as some regex might fail.
    # I'll manually define a robust data set based on the slides I read.
    
    KATAKANA_DATA = {
        'a': {'tratti': 2, 'mnem': 'una A stilizzata', 'ex_jp': 'アイ', 'ex_romaji': 'ai', 'ex_meaning': 'occhio'},
        'i': {'tratti': 2, 'mnem': 'un\'aquila stilizzata', 'ex_jp': 'アイ', 'ex_romaji': 'ai', 'ex_meaning': 'occhio'},
        'u': {'tratti': 3, 'mnem': 'una forma spigolosa e compatta', 'ex_jp': 'ウイ', 'ex_romaji': 'ui', 'ex_meaning': 'sì (FR)'},
        'e': {'tratti': 3, 'mnem': 'una trave a doppia T', 'ex_jp': 'エア', 'ex_romaji': 'ea', 'ex_meaning': 'aria'},
        'o': {'tratti': 3, 'mnem': 'un cantante d\'opera con le braccia aperte', 'ex_jp': 'オア', 'ex_romaji': 'oa', 'ex_meaning': 'o / oppure'},
        'ka': {'tratti': 2, 'mnem': 'un Ka squadrato senza il diacritico', 'ex_jp': 'カカオ', 'ex_romaji': 'kakao', 'ex_meaning': 'cacao'},
        'ki': {'tratti': 3, 'mnem': 'una chiave estremamente dritta', 'ex_jp': 'キー', 'ex_romaji': 'kī', 'ex_meaning': 'chiave'},
        'ku': {'tratti': 2, 'mnem': 'il cappello di un cuoco', 'ex_jp': 'アクa', 'ex_romaji': 'akua', 'ex_meaning': 'acqua'}, 
        'ke': {'tratti': 3, 'mnem': 'una cappa che sventola mentre qualcuno corre', 'ex_jp': 'ケア', 'ex_romaji': 'kea', 'ex_meaning': 'cura'},
        'ko': {'tratti': 2, 'mnem': 'una stanza o un box con un lato aperto', 'ex_jp': 'コア', 'ex_romaji': 'koa', 'ex_meaning': 'nucleo'},
        'sa': {'tratti': 3, 'mnem': 'due pesciolini (sardina e salmone) infilzati', 'ex_jp': 'サイズ', 'ex_romaji': 'saizu', 'ex_meaning': 'taglia'},
        'shi': {'tratti': 3, 'mnem': 'una faccia sorridente in modo distorto o sognante', 'ex_jp': 'サイズ', 'ex_romaji': 'saizu', 'ex_meaning': 'taglia'},
        'su': {'tratti': 2, 'mnem': 'una super-tuta che cammina da sola', 'ex_jp': 'スイス', 'ex_romaji': 'suisu', 'ex_meaning': 'svizzero'},
        'se': {'tratti': 2, 'mnem': 'una versione semplificata di せ', 'ex_jp': 'セクシー', 'ex_romaji': 'sekushī', 'ex_meaning': 'sexy'},
        'so': {'tratti': 2, 'mnem': 'l\'azione di cucire con ago e spago', 'ex_jp': 'ソイ', 'ex_romaji': 'soi', 'ex_meaning': 'soia'},
        'ta': {'tratti': 3, 'mnem': 'un aquilone con un taco disegnato', 'ex_jp': 'タイ', 'ex_romaji': 'tai', 'ex_meaning': 'cravatta'},
        'chi': {'tratti': 3, 'mnem': 'una cheerleader in un momento di slancio', 'ex_jp': 'チア', 'ex_romaji': 'chia', 'ex_meaning': 'tifo'},
        'tsu': {'tratti': 3, 'mnem': 'due aghi e un filo in sequenza verticale', 'ex_jp': 'タイツ', 'ex_romaji': 'taitsu', 'ex_meaning': 'collant'},
        'te': {'tratti': 3, 'mnem': 'un palo del telefono leggermente storto', 'ex_jp': 'テスト', 'ex_romaji': 'tesuto', 'ex_meaning': 'test'},
        'to': {'tratti': 2, 'mnem': 'un totem stilizzato', 'ex_jp': 'テスト', 'ex_romaji': 'tesuto', 'ex_meaning': 'test'},
        'na': {'tratti': 2, 'mnem': 'un narvalo che affiora in superficie', 'ex_jp': 'ナイト', 'ex_romaji': 'naito', 'ex_meaning': 'notte'},
        'ni': {'tratti': 2, 'mnem': 'due aghi paralleli', 'ex_jp': 'ニア', 'ex_romaji': 'nia', 'ex_meaning': 'vicino'},
        'nu': {'tratti': 2, 'mnem': 'bacchette che sollevano noodles', 'ex_jp': 'カヌー', 'ex_romaji': 'kanū', 'ex_meaning': 'canoa'},
        'ne': {'tratti': 4, 'mnem': 'un negromante che evoca uno spirito', 'ex_jp': 'ネクスト', 'ex_romaji': 'nekusuto', 'ex_meaning': 'prossimo'},
        'no': {'tratti': 1, 'mnem': 'il naso di Pinocchio o uno scivolo', 'ex_jp': 'ノー', 'ex_romaji': 'nō', 'ex_meaning': 'no'},
        'ha': {'tratti': 2, 'mnem': 'un cappello di riso', 'ex_jp': 'ハエ', 'ex_romaji': 'hae', 'ex_meaning': 'mosca'},
        'hi': {'tratti': 2, 'mnem': 'un mento che ride', 'ex_jp': 'コーヒー', 'ex_romaji': 'kōhī', 'ex_meaning': 'caffè'},
        'fu': {'tratti': 1, 'mnem': 'una bandiera patriottica', 'ex_jp': 'タフ', 'ex_romaji': 'tafu', 'ex_meaning': 'duro'},
        'he': {'tratti': 1, 'mnem': 'identico allo hiragana へ', 'ex_jp': 'ヘイ', 'ex_romaji': 'hei', 'ex_meaning': 'ehi'},
        'ho': {'tratti': 4, 'mnem': 'una croce che brilla e scintilla', 'ex_jp': 'ホタテ', 'ex_romaji': 'hotate', 'ex_meaning': 'capasanta'},
        'ma': {'tratti': 2, 'mnem': 'un insieme di forme geometriche e angoli', 'ex_jp': 'マウス', 'ex_romaji': 'mausu', 'ex_meaning': 'topo o mouse'},
        'mi': {'tratti': 3, 'mnem': 'tre missili che sfrecciano nel cielo', 'ex_jp': 'ミミズ', 'ex_romaji': 'mimizu', 'ex_meaning': 'lombrico'},
        'mu': {'tratti': 2, 'mnem': 'il muso stilizzato di una mucca', 'ex_jp': 'ムービー', 'ex_romaji': 'mūbī', 'ex_meaning': 'film'},
        'me': {'tratti': 2, 'mnem': 'un occhio con sopra una X', 'ex_jp': 'メモ', 'ex_romaji': 'memo', 'ex_meaning': 'appunto'},
        'mo': {'tratti': 3, 'mnem': 'una versione squadrata di も', 'ex_jp': 'メモ', 'ex_romaji': 'memo', 'ex_meaning': 'appunto'},
        'ya': {'tratti': 2, 'mnem': 'una versione squadrata di や', 'ex_jp': 'ヤクザ', 'ex_romaji': 'yakuza', 'ex_meaning': 'malavitoso'},
        'yu': {'tratti': 2, 'mnem': 'l\'uncino di un pirata', 'ex_jp': 'ユニーク', 'ex_romaji': 'yunīku', 'ex_meaning': 'unico'},
        'yo': {'tratti': 3, 'mnem': 'uno yogino in posizione di yoga', 'ex_jp': 'ヨガ', 'ex_romaji': 'yoga', 'ex_meaning': 'yoga'},
        'ra': {'tratti': 2, 'mnem': 'un raptor che fa il rapper', 'ex_jp': 'ラッキー', 'ex_romaji': 'rakkī', 'ex_meaning': 'fortunato'},
        'ri': {'tratti': 2, 'mnem': 'identico allo hiragana り ma rigido', 'ex_jp': 'リサイクル', 'ex_romaji': 'risaikuru', 'ex_meaning': 'riciclare'},
        'ru': {'tratti': 2, 'mnem': 'due strade adiacenti che non si toccano', 'ex_jp': 'リサイクル', 'ex_romaji': 'risaikuru', 'ex_meaning': 'riciclare'},
        're': {'tratti': 1, 'mnem': 'una sirena con i capelli lunghi', 'ex_jp': 'レイヤー', 'ex_romaji': 'reiyā', 'ex_meaning': 'strato'},
        'ro': {'tratti': 3, 'mnem': 'una rotonda a forma di quadrato', 'ex_jp': 'ロイヤル', 'ex_romaji': 'roiyaru', 'ex_meaning': 'reale'},
        'wa': {'tratti': 2, 'mnem': 'un punto di domanda', 'ex_jp': 'ワイン', 'ex_romaji': 'wain', 'ex_meaning': 'vino'},
        'wo': {'tratti': 2, 'mnem': 'un cane che abbaia', 'ex_jp': 'ワンタン', 'ex_romaji': 'wantan', 'ex_meaning': 'wonton'},
        'n': {'tratti': 2, 'mnem': 'un ragazzo ciclope con un occhio solo', 'ex_jp': 'ワイン', 'ex_romaji': 'wain', 'ex_meaning': 'vino'}
    }

    for filename in os.listdir(KATAKANA_DIR):
        if not filename.endswith('.html'):
            continue
        
        romaji = filename.replace('.html', '')
        if romaji not in KATAKANA_DATA:
            continue
            
        data = KATAKANA_DATA[romaji]
        filepath = os.path.join(KATAKANA_DIR, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Replace titles and JSON-LD
        html = html.replace('Pagina didattica placeholder', 'Pagina didattica')
        
        # Replace Stroke Count
        html = re.sub(r'<p class="stroke-count">Tratti: da definire</p>', f'<p class="stroke-count">{data["tratti"]} tratti</p>', html)
        
        # Replace Stroke Note
        html = re.sub(r'<strong>Suggerimento:</strong> Placeholder in attesa delle slide Katakana.', 
                      f'<strong>Suggerimento:</strong> Ricorda la forma associata alla tecnica mnemonica per tracciare i {data["tratti"]} tratti in modo deciso e squadrato.', html)
        
        # Replace Mnemonic
        html = re.sub(r'<strong>Tecnica:</strong> Placeholder mnemonico da completare con i materiali del corso.', 
                      f'<strong>Tecnica:</strong> {data["mnem"]}.', html)
        
        # Replace Example
        # The placeholder in word-jp might be different (usually the char itself), so let's match anything inside
        html = re.sub(r'<span class="word-jp">.*?</span>', f'<span class="word-jp">{data["ex_jp"]}</span>', html)
        html = re.sub(rf'<span class="word-romaji">\({romaji}\)</span>', f'<span class="word-romaji">({data["ex_romaji"]})</span>', html)
        html = re.sub(r'<span class="word-meaning">placeholder didattico</span>', f'<span class="word-meaning">{data["ex_meaning"]}</span>', html)
        html = re.sub(r'Voce temporanea: verra sostituita quando saranno disponibili le slide Katakana.', 
                      'Esempio di prestito linguistico (gairaigo) o termine giapponese scritto in katakana.', html)
        
        # Replace the "Contenuto provvisorio" bullet
        html = html.replace('<li>Contenuto provvisorio: scheda pronta per integrazione futura.</li>', 
                            '<li>Pronuncia identica alla controparte hiragana.</li>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Updated {filename}')

def update_tei_file(char_data):
    # This is a bit more complex but we can do simple replacements
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        tei = f.read()
    
    # We'll just replace the placeholders for each character entry
    # Entry pattern in tei:
    # <char xml:id="katakana_a">
    #   <charName>KATAKANA LETTER A</charName>
    #   <charProp>
    #     <localName>romaji</localName>
    #     <value>a</value>
    #   </charProp>
    #   <charProp>
    #     <localName>pronunciation</localName>
    #     <value>placeholder</value>
    #   </charProp>
    # </char>
    
    # Actually, a simpler way is to replace the specific value if it follows the romaji
    # But TEI structure is repetitive.
    
    # I'll use a more surgical approach
    # For each romaji, find the <char xml:id="katakana_romaji"> block and replace its placeholder
    
    for romaji in ['a', 'i', 'u', 'e', 'o', 'ka', 'ki', 'ku', 'ke', 'ko', 'sa', 'shi', 'su', 'se', 'so', 
                   'ta', 'chi', 'tsu', 'te', 'to', 'na', 'ni', 'nu', 'ne', 'no', 'ha', 'hi', 'fu', 'he', 'ho',
                   'ma', 'mi', 'mu', 'me', 'mo', 'ya', 'yu', 'yo', 'ra', 'ri', 'ru', 're', 'ro', 'wa', 'wo', 'n']:
        
        # Find the block for this romaji
        pattern = rf'(<char xml:id="katakana_{romaji}">.*?)<value>placeholder</value>'
        # We need dotall for multi-line
        tei = re.sub(pattern, rf'\1<value>pronuncia identica hiragana</value>', tei, flags=re.DOTALL)

    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        f.write(tei)
    print('Updated TEI metadata')

if __name__ == "__main__":
    update_html_files({}) # data is hardcoded in function for reliability
    update_tei_file({})
