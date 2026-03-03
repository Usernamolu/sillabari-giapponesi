# Alfabeto Giapponese - Hiragana + Katakana (DH Project)

Prototipo web didattico per il corso di Digital Humanities (UniPV, 2025-2026), con focus sui sillabari giapponesi.

## Stato del progetto
Questo progetto e in divenire.

Al momento:
- Tabelle Hiragana e Katakana presenti in homepage.
- Pagine didattiche Hiragana complete (46/46).
- Pagine Katakana complete come struttura tecnica (46/46) con contenuti placeholder in attesa delle slide.
- Metadati TEI disponibili in `metadata/hiragana.tei.xml` e `metadata/katakana.tei.xml`.
- Pagina `metodologia.html` disponibile come supporto.

## Cosa include oggi
- Tabelle `gojuon` interattive (hover, click, navigazione da tastiera).
- Pagine singolo carattere per Hiragana e Katakana.
- Cross-link Hiragana <-> Katakana.
- Base CSS/JS modulare in `assets/`.
- Metadati in formato TEI.

## Roadmap
- [x] Homepage con tabella Hiragana (`gojuon`)
- [x] Homepage con tabella Katakana (`gojuon`)
- [x] Pagine Hiragana complete
- [x] Pagine Katakana placeholder complete
- [x] Metadati TEI (Hiragana + Katakana)
- [ ] Sostituire i placeholder Katakana con contenuti da slide
- [ ] Rafforzare bibliografia e riferimenti linguistici
- [ ] Rifiniture UX/UI e validazione finale contenuti

## Workflow locale (utente finale)
Obiettivo: scaricare il progetto e farlo funzionare subito in locale, in modo stabile.

### 1) Scarica il progetto
Opzione A (Git):
```bash
git clone git@github.com:Usernamolu/alfabeto-giapponese.git
cd alfabeto-giapponese
```

Opzione B (ZIP):
1. Scarica il file ZIP da GitHub.
2. Estrai la cartella.
3. Apri un terminale nella cartella estratta.

### 2) Avvia un server locale (consigliato)
Usa un server locale invece di `file://` per evitare problemi di percorso e comportamento browser.

Con Python (raccomandato):
```bash
python -m http.server 8000
```
Se `python` non e disponibile:
```bash
py -m http.server 8000
```

Alternativa con Node:
```bash
npx serve .
```

### 3) Apri il progetto nel browser
- `http://localhost:8000/` (Python)
- oppure l'URL mostrato da `npx serve`

Pagina principale:
- `index.html`

## Uso ottimale consigliato
- Browser aggiornato (Chrome/Edge/Firefox).
- Connessione internet attiva per il font Google (`Noto Sans JP`).
- Mantieni invariata la struttura cartelle (`assets/`, `hiragana/`, `katakana/`, `metadata/`) per non rompere i link relativi.

## Struttura essenziale
```text
alfabeto-giapponese/
  index.html
  metodologia.html
  assets/
    css/
    js/
  hiragana/
    ...46 pagine carattere...
  katakana/
    ...46 pagine carattere (placeholder)...
  metadata/
    hiragana.tei.xml
    katakana.tei.xml
  Docs/
```

## Tecnologie
- HTML5
- CSS3
- JavaScript vanilla
- TEI XML (metadati)

## Troubleshooting rapido
- Pagina bianca o link rotti: usa `http://localhost...` e non `file://`.
- Caratteri strani: verifica encoding UTF-8.
- Font non caricato: verifica connessione internet.
