import os
import re

# Data mapping for stroke order suggestions (Italian)
# Key format: "syllabary/romaji" (e.g., "hiragana/ka")

STROKE_SUGGESTIONS = {
    # HIRAGANA
    "hiragana/a": "inizia con un tratto curvo orizzontale, aggiungi la croce verticale e infine il grande arco che completa il carattere.",
    "hiragana/i": "traccia prima il segno a sinistra (leggermente curvo verso l'interno) con un piccolo uncino finale, poi il segno a destra, più corto.",
    "hiragana/u": "inizia con un piccolo tratto curvo in alto, poi disegna una grande curva a forma di C aperta verso sinistra in basso.",
    "hiragana/e": "traccia il piccolo segno in alto, poi il tratto complesso che sembra una 'z' e termina con una curva morbida.",
    "hiragana/o": "traccia il segno orizzontale, poi il verticale che curva ampiamente inclinandosi, e infine aggiungi il segno a goccia in alto a destra.",
    "hiragana/ka": "traccia il tratto lungo che curva con l'uncino, poi il tratto verticale che lo incrocia e infine il segno corto a destra.",
    "hiragana/ki": "traccia i due tratti orizzontali paralleli, incrociali con il tratto verticale curvo e aggiungi la base separata.",
    "hiragana/ku": "disegna un unico segno a punta (come un 'becco') aperto verso sinistra.",
    "hiragana/ke": "traccia il tratto verticale a sinistra, poi il breve tratto orizzontale al centro e infine il verticale lungo a destra.",
    "hiragana/ko": "disegna i due brevi tratti orizzontali paralleli, curvi leggermente uno verso l'altro.",
    "hiragana/sa": "traccia il tratto orizzontale, incrocialo con l'obliquo e aggiungi la base separata in basso.",
    "hiragana/shi": "traccia un unico segno verticale che curva dolcemente verso l'alto a destra, come un amo.",
    "hiragana/su": "traccia il tratto orizzontale, poi il verticale che forma un'asola circolare a metà altezza.",
    "hiragana/se": "traccia il lungo tratto orizzontale, poi il piccolo verticale a destra e infine il verticale a sinistra che curva.",
    "hiragana/so": "traccia un unico segno a zig-zag che termina con una curva ampia verso destra.",
    "hiragana/ta": "forma una croce con i primi due tratti, poi aggiungi a destra i due piccoli segni paralleli.",
    "hiragana/chi": "traccia l'orizzontale corto, poi il verticale che scende e forma una grande curva a sinistra.",
    "hiragana/tsu": "disegna un'unica grande curva orizzontale che scende verso il basso a destra.",
    "hiragana/te": "traccia il tratto orizzontale che piega e scende in un'ampia curva verso sinistra.",
    "hiragana/to": "traccia il piccolo segno obliquo in alto e collegalo a un'ampia curva aperta verso sinistra.",
    "hiragana/na": "forma la croce iniziale, aggiungi il piccolo segno a destra e conclude con l'asola in basso.",
    "hiragana/ni": "traccia il verticale a sinistra e i due segni paralleli a destra (simili a quelli di KO).",
    "hiragana/nu": "traccia i due tratti incrociati e termina con l'asola complessa in basso a destra.",
    "hiragana/ne": "traccia il verticale a sinistra e il tratto articolato che termina con l'asola finale.",
    "hiragana/no": "disegna un unico tratto circolare che ruota quasi su se stesso senza chiudersi.",
    "hiragana/ha": "traccia il verticale a sinistra, l'orizzontale e il verticale che chiude con l'asola.",
    "hiragana/hi": "traccia un unico grande segno a forma di 'coppa' larga con base morbida.",
    "hiragana/fu": "inizia dal punto in alto, traccia il corpo centrale e infine i due punti ai lati.",
    "hiragana/he": "un unico tratto a forma di montagna stilizzata (punta in alto).",
    "hiragana/ho": "simile a HA, ma con due tratti orizzontali paralleli in alto.",
    "hiragana/ma": "traccia i due orizzontali paralleli e il verticale che chiude con l'asola.",
    "hiragana/mi": "traccia il segno diagonale che fa un'asola e scende, poi incrocialo con l'ultimo tratto.",
    "hiragana/mu": "traccia l'orizzontale, il verticale con l'asola, aggiungi il punto in alto e il piccolo tratto finale.",
    "hiragana/me": "traccia i due tratti incrociati (simile a NU ma senza l'asola finale).",
    "hiragana/mo": "traccia il gancio verticale e incrocialo con i due tratti orizzontali.",
    "hiragana/ya": "traccia il gancio principale a destra, il piccolo tratto e il tratto lungo obliquo.",
    "hiragana/yu": "traccia il corpo ovale con asola e incrocialo con il verticale lungo a destra.",
    "hiragana/yo": "un tratto orizzontale corto e un verticale che termina con l'asola.",
    "hiragana/ra": "traccia il punto in alto e l'ampia curva aperta sottostante.",
    "hiragana/ri": "due tratti verticali: il sinistro è più corto e leggermente ricurvo.",
    "hiragana/ru": "un unico tratto che zig-zagga e chiude con un'asola circolare.",
    "hiragana/re": "traccia il verticale a sinistra e il tratto articolato che piega verso l'esterno.",
    "hiragana/ro": "un solo tratto identico a RU ma senza l'asola finale.",
    "hiragana/wa": "un verticale a sinistra e un tratto unico che forma un'ampia curva interna.",
    "hiragana/wo": "traccia l'orizzontale, l'obliquo centrale e l'ampia curva aperta finale.",
    "hiragana/n": "un solo tratto fluido e dinamico che ricorda una 'n' corsiva.",

    # KATAKANA
    "katakana/a": "traccia l'orizzontale che curva a sinistra e il tratto verticale leggermente curvo.",
    "katakana/i": "traccia l'obliquo che scende a sinistra e il tratto verticale dritto.",
    "katakana/u": "traccia il piccolo segno verticale sopra e il gancio orizzontale-verticale sotto.",
    "katakana/e": "traccia i tre tratti: l'orizzontale superiore, il verticale e la base orizzontale.",
    "katakana/o": "traccia l'orizzontale lungo, il verticale con uncino e l'obliquo a sinistra.",
    "katakana/ka": "traccia il gancio orizzontale e l'obliquo che lo incrocia nettamente.",
    "katakana/ki": "due tratti orizzontali paralleli e un obliquo lungo che li interseca.",
    "katakana/ku": "un piccolo obliquo in alto e un segno ricurvo che parte da metà.",
    "katakana/ke": "traccia l'obliquo a sinistra, l'orizzontale centrale e il verticale che scende.",
    "katakana/ko": "due tratti che formano un angolo retto superiore e una base orizzontale.",
    "katakana/sa": "traccia l'orizzontale lungo e due tratti verticali brevi che lo incrociano.",
    "katakana/shi": "traccia i due piccoli segni paralleli e il segno lungo che sale dal basso.",
    "katakana/su": "traccia l'orizzontale che curva a sinistra e l'obliquo che scende a destra.",
    "katakana/se": "due tratti collegati a L rovesciata e un tratto orizzontale di chiusura.",
    "katakana/so": "un piccolo segno in alto a sinistra e un tratto obliquo lungo verso il basso.",
    "katakana/ta": "un piccolo obliquo, un gancio angolato e un tratto corto interno.",
    "katakana/chi": "un obliquo in alto, un orizzontale e un verticale che curva a sinistra.",
    "katakana/tsu": "due piccoli segni quasi verticali e un tratto lungo che scende verso destra.",
    "katakana/te": "due tratti orizzontali paralleli e un verticale curvo finale.",
    "katakana/to": "un verticale corto e un tratto obliquo che lo tocca al centro.",
    "katakana/na": "un tratto orizzontale lungo incrociato da un obliquo corto a sinistra.",
    "katakana/ni": "due semplici tratti orizzontali (quello sotto è più lungo).",
    "katakana/nu": "due tratti obliqui che si incrociano nettamente a forma di X.",
    "katakana/ne": "quattro tratti: punto in alto, gancio angolato e due segni d'appoggio.",
    "katakana/no": "un unico tratto obliquo deciso che scende verso sinistra.",
    "katakana/ha": "due tratti obliqui che divergono simmetricamente verso il basso.",
    "katakana/hi": "un tratto orizzontale corto e un tratto a forma di cucchiaio o gancio.",
    "katakana/fu": "un unico segno angolato che scende dolcemente.",
    "katakana/he": "un unico tratto a forma di collina (identico al corrispondente hiragana).",
    "katakana/ho": "un orizzontale lungo con due verticali inseriti e un tratto a destra.",
    "katakana/ma": "un tratto orizzontale che curva e un piccolo tratto obliquo inverso.",
    "katakana/mi": "tre tratti obliqui paralleli che scendono verso destra.",
    "katakana/mu": "un gancio angolato accompagnato da un piccolo segno obliquo.",
    "katakana/me": "due tratti obliqui che si incrociano (uno lungo e uno corto).",
    "katakana/mo": "due orizzontali paralleli e un verticale con uncino finale a destra.",
    "katakana/ya": "un gancio orizzontale e un semplice tratto verticale che lo incrocia.",
    "katakana/yu": "un gancio angolato che delimita lo spazio e una base orizzontale.",
    "katakana/yo": "un tratto complesso che forma una sorta di 'E' rovesciata.",
    "katakana/ra": "un piccolo tratto orizzontale in alto sopra un gancio ricurvo.",
    "katakana/ri": "due tratti verticali: il sinistro è più corto del destro.",
    "katakana/ru": "due tratti obliqui paralleli che curvano in direzioni opposte alla base.",
    "katakana/re": "un unico tratto che scende e risale deciso verso destra.",
    "katakana/ro": "tre tratti che formano un perfetto perimetro quadrato.",
    "katakana/wa": "un verticale corto e un ampio tratto angolato orizzontale-verticale.",
    "katakana/wo": "due tratti orizzontali paralleli e un obliquo che parte dal primo.",
    "katakana/n": "un piccolo tratto obliquo e un segno lungo che sale dal basso verso destra.",
}

def update_kana_page(filepath, syllabary, romaji):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    key = f"{syllabary}/{romaji}"
    suggestion = STROKE_SUGGESTIONS.get(key)
    if not suggestion:
        print(f"No suggestion for {key}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update stroke suggestion
    # Find <p class="stroke-note"> ... </p> and replace its content after <strong>Suggerimento:</strong>
    stroke_pattern = re.compile(r'(<p class="stroke-note">\s*<strong>Suggerimento:</strong>).*?(</p>)', re.DOTALL)
    content = stroke_pattern.sub(rf'\1 {suggestion}\2', content)

    # 2. Update footer
    footer_old = '<p class="footer-credit">Progetto Digital Humanities - Gabriele Errico - UniPV 2025-2026</p>'
    footer_new = '<p class="footer-credit">Progetto Digital Humanities - Gabriele Errico - UniPV 2025-2026 | <a href="../index.html#crediti">Fonti e Metodologia</a></p>'
    content = content.replace(footer_old, footer_new)

    # 3. Clean up Hiragana specific notes
    old_note = 'Esempio tratto dai mini quiz della lezione L01.'
    content = content.replace(old_note, 'Esempio didattico per la pratica dei kana.')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

def main():
    base_dir = r"c:\Users\Gabriele Errico\Downloads\alfabeto-giapponese"
    
    # Process Hiragana
    hiragana_dir = os.path.join(base_dir, "hiragana")
    for filename in os.listdir(hiragana_dir):
        if filename.endswith(".html"):
            romaji = filename[:-5]
            update_kana_page(os.path.join(hiragana_dir, filename), "hiragana", romaji)

    # Process Katakana
    katakana_dir = os.path.join(base_dir, "katakana")
    for filename in os.listdir(katakana_dir):
        if filename.endswith(".html"):
            romaji = filename[:-5]
            update_kana_page(os.path.join(katakana_dir, filename), "katakana", romaji)

if __name__ == "__main__":
    main()
