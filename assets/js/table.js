/**
 * JavaScript per le tabelle Kana interattive
 */

document.addEventListener('DOMContentLoaded', function() {
    initTableInteractions();
    initKeyboardNavigation();
});

/**
 * Interazioni con le celle della tabella + Accessibilità
 * Usa event delegation per migliori performance
 */
function initTableInteractions() {
    const cells = document.querySelectorAll('.kana-cell:not(.empty)');

    // Setup ARIA labels per accessibilità
    cells.forEach(cell => {
        const kana = cell.querySelector('.kana')?.textContent || '';
        const romaji = cell.querySelector('.romaji')?.textContent || '';
        cell.setAttribute('role', 'button');
        cell.setAttribute('aria-label', `Carattere ${kana} pronunciato ${romaji}`);
        cell.setAttribute('tabindex', '0');
    });

    // Event delegation sulla tabella per performance
    const table = document.querySelector('.unified-kana-table, .kana-table');
    if (!table) return;

    // Hover con event delegation
    table.addEventListener('mouseover', function(e) {
        const cell = e.target.closest('.kana-cell:not(.empty)');
        if (cell) {
            highlightRelated(cell);
        }
    });

    table.addEventListener('mouseout', function(e) {
        const cell = e.target.closest('.kana-cell:not(.empty)');
        if (cell) {
            clearHighlights();
        }
    });

    // Click con feedback - event delegation
    table.addEventListener('click', function(e) {
        const link = e.target.closest('.kana-cell a');
        if (link && !link.classList.contains('is-disabled')) {
            const cell = link.closest('.kana-cell');
            if (cell) {
                // Animazione di click
                cell.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    cell.style.transform = '';
                }, 100);
            }
        }
    });
}

/**
 * Evidenzia caratteri correlati (stessa riga/colonna)
 */
function highlightRelated(cell) {
    const table = cell.closest('table');
    const row = cell.parentElement;
    const cellIndex = Array.from(row.children).indexOf(cell);

    // Evidenzia riga
    row.classList.add('row-highlighted');

    // Evidenzia colonna
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(r => {
        const c = r.children[cellIndex];
        if (c) {
            c.classList.add('col-highlighted');
        }
    });
}

/**
 * Rimuovi evidenziazioni
 */
function clearHighlights() {
    document.querySelectorAll('.row-highlighted').forEach(el => {
        el.classList.remove('row-highlighted');
    });
    document.querySelectorAll('.col-highlighted').forEach(el => {
        el.classList.remove('col-highlighted');
    });
}

/**
 * Navigazione con tastiera + debouncing
 */
function initKeyboardNavigation() {
    let currentIndex = 0;
    const cells = Array.from(document.querySelectorAll('.kana-cell:not(.empty) a:not(.is-disabled)'));

    // Debounced focus per performance
    const debouncedFocus = debounce(focusCell, 100);

    document.addEventListener('keydown', function(e) {
        if (!cells.length) return;

        switch(e.key) {
            case 'ArrowRight':
                e.preventDefault();
                currentIndex = (currentIndex + 1) % cells.length;
                debouncedFocus(currentIndex);
                break;

            case 'ArrowLeft':
                e.preventDefault();
                currentIndex = (currentIndex - 1 + cells.length) % cells.length;
                debouncedFocus(currentIndex);
                break;

            case 'ArrowDown':
                e.preventDefault();
                currentIndex = Math.min(currentIndex + 5, cells.length - 1);
                debouncedFocus(currentIndex);
                break;

            case 'ArrowUp':
                e.preventDefault();
                currentIndex = Math.max(currentIndex - 5, 0);
                debouncedFocus(currentIndex);
                break;

            case 'Enter':
                if (document.activeElement.classList.contains('kana-cell')) {
                    cells[currentIndex].click();
                }
                break;
        }
    });
}

/**
 * Metti focus sulla cella corrente
 */
function focusCell(index) {
    const cells = document.querySelectorAll('.kana-cell:not(.empty)');
    if (cells[index]) {
        cells[index].scrollIntoView({ behavior: 'smooth', block: 'center' });
        cells[index].focus();

        // Effetto visivo temporaneo
        cells[index].style.boxShadow = '0 0 20px rgba(196, 30, 58, 0.6)';
        setTimeout(() => {
            cells[index].style.boxShadow = '';
        }, 500);
    }
}

/**
 * Modalità quiz (randomizza visualizzazione)
 */
function toggleQuizMode() {
    const romajiElements = document.querySelectorAll('.romaji, .ita');
    const isHidden = romajiElements[0].style.display === 'none';

    romajiElements.forEach(el => {
        el.style.display = isHidden ? '' : 'none';
    });

    console.log(isHidden ? '👀 Pronuncia mostrata' : '❓ Modalità quiz attivata');
}

// Esponi la funzione globally per poterla chiamare
window.toggleQuizMode = toggleQuizMode;

// Aggiungi stili con StyleManager
StyleManager.inject('table-highlights', `
    .row-highlighted {
        background: rgba(255, 183, 197, 0.2) !important;
    }
    .col-highlighted {
        background: rgba(135, 206, 235, 0.2) !important;
    }
    .kana-cell:focus {
        outline: 3px solid #c41e3a;
        outline-offset: 2px;
    }
`);

console.log('📊 Tabella interattiva caricata! Usa le frecce per navigare.');
