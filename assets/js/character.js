/**
 * JavaScript per le pagine dei singoli caratteri
 */

document.addEventListener('DOMContentLoaded', function () {
    initNavigationShortcuts();
    initTEIToggle();
});

/**
 * Scorciatoie da tastiera per navigazione
 */
function initNavigationShortcuts() {
    document.addEventListener('keydown', function (e) {
        // Alt + Freccia sinistra = carattere precedente
        if (e.altKey && e.key === 'ArrowLeft') {
            e.preventDefault();
            const prevLink = document.querySelector('a[rel="prev"]');
            if (prevLink) prevLink.click();
        }

        // Alt + Freccia destra = carattere successivo
        if (e.altKey && e.key === 'ArrowRight') {
            e.preventDefault();
            const nextLink = document.querySelector('a[rel="next"]');
            if (nextLink) nextLink.click();
        }

        // Alt + H = torna alla tabella
        if (e.altKey && e.key === 'h') {
            e.preventDefault();
            window.location.href = 'index.html';
        }
    });
}

/**
 * Toggle sezione TEI
 */
function initTEIToggle() {
    const teiDetails = document.querySelector('.tei-section details');
    if (!teiDetails) return;

    teiDetails.addEventListener('toggle', function () {
        if (this.open) {
            console.log('📄 Metadati TEI visualizzati');
            this.querySelector('pre').style.animation = 'fadeIn 0.3s ease';
        }
    });
}

/**
 * Copia codice TEI negli appunti (con sanitizzazione)
 */
function copyTEICode() {
    const code = document.querySelector('.tei-code code');
    if (!code) return;

    // Sanitizza il contenuto prima di copiare
    const text = code.textContent;
    const sanitized = sanitizeTEI ? sanitizeTEI(text) : text;

    navigator.clipboard.writeText(sanitized).then(() => {
        console.log('📋 Codice TEI copiato!');
        showNotification('Codice TEI copiato negli appunti!');
    }).catch(err => {
        console.error('Errore copia:', err);
    });
}

/**
 * Notifica temporanea
 */
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: #4CAF50;
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 2500);
}

// Esponi funzione globalmente
window.copyTEICode = copyTEICode;

// Aggiungi stili necessari con StyleManager
StyleManager.inject('character-base-styles', `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { transform: translateX(400px); }
        to { transform: translateX(0); }
    }

    @keyframes slideOut {
        from { transform: translateX(0); }
        to { transform: translateX(400px); }
    }
`);

console.log('🎌 Pagina carattere caricata! Usa Alt+← e Alt+→ per navigare.');
