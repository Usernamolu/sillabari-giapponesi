# Sillabari Giapponesi - Hiragana + Katakana (DH Project)

Prototipo web didattico open-source progettato per gli studenti e gli appassionati di lingua giapponese. Il progetto nasce in ambiente accademico per il corso di Digital Humanities (UniPV, 2025-2026) con un focus specifico sullo studio interattivo di Hiragana e Katakana.

🌐 **Accesso Diretto**: L'applicazione è consultabile online da qualsiasi dispositivo (Desktop e Mobile) al seguente indirizzo ufficiale:
**[https://usernamolu.github.io/sillabari-giapponesi/](https://usernamolu.github.io/sillabari-giapponesi/)**

## Stato del progetto
Questo progetto è in divenire. 

La piattaforma offre attualmente:
- Tabelle `gojuon` esplorabili in homepage sia per Hiragana che Katakana.
- Pagine didattiche per l'Hiragana complete (46/46 caratteri base).
- Pagine didattiche per il Katakana complete (46/46 caratteri base).
- Metadati accademici TEI-XML strutturati disponibili nella cartella `metadata/`.
- Pagina referenziale `metodologia.html` inclusa.

## Funzionalità (Aprile 2026)
- Tabelle `gojuon` interattive (effetti hover, focus e navigazione via tastiera).
- Schede didattiche per singolo carattere fornite di informazioni ausiliarie (tratti, pronuncia mnemonica).
- Cross-link continui tra Sillabario Hiragana e corrispettivo Katakana.
- Configurazione Vanilla (HTML, CSS, JS) ultraveloce priva di dipendenze complesse.
- Metadati semantici (TEI e Schema.org) integrati.

## Workflow locale (utente finale)
Obiettivo: scaricare il progetto e farlo funzionare subito in locale, in modo stabile.

### 1) Scarica il progetto
Opzione A (Git):
```bash
git clone git@github.com:Usernamolu/sillabari-giapponesi.git
cd sillabari-giapponesi
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

Alternativa con Node (npm):
```bash
npx http-server .
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
sillabari-giapponesi/
  index.html
  metodologia.html
  assets/
    css/
    js/
  hiragana/
    ...46 pagine carattere...
  katakana/
    ...46 pagine carattere...
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
