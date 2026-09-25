/**
 * JavaScript per le pagine dei singoli caratteri
 */

document.addEventListener('DOMContentLoaded', function () {
    initNavigationShortcuts();
});

/**
 * Scorciatoie da tastiera per navigazione
 * (se non c'è un link da seguire, il tasto mantiene il comportamento del browser)
 */
function initNavigationShortcuts() {
    document.addEventListener('keydown', function (e) {
        if (!e.altKey) return;

        let link = null;

        // Alt + Freccia sinistra/destra = carattere precedente/successivo
        if (e.key === 'ArrowLeft') link = document.querySelector('a[rel="prev"]');
        if (e.key === 'ArrowRight') link = document.querySelector('a[rel="next"]');

        // Alt + H = torna alla tabella (e.code: su macOS Alt+H produce "˙")
        if (e.code === 'KeyH') link = document.querySelector('.back-btn');

        if (link) {
            e.preventDefault();
            link.click();
        }
    });
}

console.log('🎌 Pagina carattere caricata! Usa Alt+← e Alt+→ per navigare, Alt+H per tornare alla tabella.');
