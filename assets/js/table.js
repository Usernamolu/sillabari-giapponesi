/**
 * JavaScript per le tabelle Kana interattive
 */

document.addEventListener('DOMContentLoaded', function () {
    initTableInteractions();
    initKeyboardNavigation();
    initPrintButtons();
});

/**
 * Pulsanti di stampa (listener JS: la CSP blocca gli handler inline)
 */
function initPrintButtons() {
    document.querySelectorAll('.btn-download').forEach(btn => {
        btn.addEventListener('click', () => window.print());
    });
}

/**
 * Interazioni con le celle della tabella
 */
function initTableInteractions() {
    const tables = document.querySelectorAll('.unified-kana-table, .kana-table');
    if (!tables.length) return;

    tables.forEach(table => {
        table.addEventListener('mouseover', function (e) {
            const cell = e.target.closest('.kana-cell:not(.empty)');
            if (cell) {
                highlightRelated(cell);
            }
        });

        table.addEventListener('mouseout', function (e) {
            const cell = e.target.closest('.kana-cell:not(.empty)');
            if (cell) {
                clearHighlights();
            }
        });

        table.addEventListener('click', function (e) {
            const link = e.target.closest('.kana-cell a');
            if (link && !link.classList.contains('is-disabled')) {
                const cell = link.closest('.kana-cell');
                if (cell) {
                    cell.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        cell.style.transform = '';
                    }, 100);
                }
            }
        });
    });
}

/**
 * Evidenzia caratteri correlati (stessa riga/colonna)
 */
function highlightRelated(cell) {
    const table = cell.closest('table');
    const row = cell.parentElement;
    const cellIndex = Array.from(row.children).indexOf(cell);

    // Le celle hanno uno sfondo proprio: evidenzia le celle, non il <tr>
    Array.from(row.children).forEach(c => c.classList.add('row-highlighted'));

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
 * Navigazione con tastiera: attiva solo quando il focus è su una cella,
 * così le frecce continuano a scorrere la pagina altrove.
 */
function initKeyboardNavigation() {
    document.addEventListener('keydown', function (e) {
        if (e.altKey || e.ctrlKey || e.metaKey) return;

        const link = document.activeElement && document.activeElement.closest &&
            document.activeElement.closest('.kana-cell a:not(.is-disabled)');
        if (!link) return;

        const target = findNeighbour(link, e.key);
        if (target === undefined) return;

        e.preventDefault();
        if (target) focusCell(target);
    });
}

/**
 * Trova il link della cella adiacente nella stessa tabella
 * (restituisce undefined se il tasto non è una freccia)
 */
function findNeighbour(link, key) {
    const cell = link.closest('.kana-cell');
    const table = cell.closest('table');
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    const rowIndex = rows.indexOf(cell.parentElement);
    const colIndex = Array.from(cell.parentElement.children).indexOf(cell);
    const linkAt = (r, c) => {
        const td = rows[r] && rows[r].children[c];
        return td ? td.querySelector('a:not(.is-disabled)') : null;
    };

    switch (key) {
        case 'ArrowRight':
        case 'ArrowLeft': {
            const links = Array.from(table.querySelectorAll('.kana-cell a:not(.is-disabled)'));
            const i = links.indexOf(link) + (key === 'ArrowRight' ? 1 : -1);
            return links[i] || null;
        }
        case 'ArrowDown':
        case 'ArrowUp': {
            const step = key === 'ArrowDown' ? 1 : -1;
            for (let r = rowIndex + step; r >= 0 && r < rows.length; r += step) {
                const next = linkAt(r, colIndex);
                if (next) return next;
            }
            return null;
        }
        default:
            return undefined;
    }
}

/**
 * Sposta il focus sulla cella e la evidenzia brevemente
 */
function focusCell(link) {
    const cell = link.closest('.kana-cell');
    link.focus({ preventScroll: true });
    cell.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    cell.style.boxShadow = '0 0 20px rgba(196, 30, 58, 0.6)';
    setTimeout(() => {
        cell.style.boxShadow = '';
    }, 500);
}

StyleManager.inject('table-highlights', `
    .row-highlighted:not(:hover) {
        background: rgba(255, 183, 197, 0.2) !important;
    }
    .col-highlighted:not(:hover) {
        background: rgba(135, 206, 235, 0.2) !important;
    }
`);


