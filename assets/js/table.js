/**
 * JavaScript per le tabelle Kana interattive
 */

document.addEventListener('DOMContentLoaded', function() {
    initTableInteractions();
    initKeyboardNavigation();
});

/**
 * Interazioni con le celle della tabella + accessibilita
 */
function initTableInteractions() {
    const cells = document.querySelectorAll('.kana-cell:not(.empty)');

    cells.forEach(cell => {
        const link = cell.querySelector('a');
        const kana = cell.querySelector('.kana')?.textContent || '';
        const romaji = cell.querySelector('.romaji')?.textContent || '';
        if (link && !link.classList.contains('is-disabled')) {
            cell.setAttribute('role', 'button');
            cell.setAttribute('aria-label', `Carattere ${kana} pronunciato ${romaji}`);
            cell.setAttribute('tabindex', '0');
        }
    });

    const table = document.querySelector('.unified-kana-table, .kana-table');
    if (!table) return;

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

    table.addEventListener('click', function(e) {
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
}

/**
 * Evidenzia caratteri correlati (stessa riga/colonna)
 */
function highlightRelated(cell) {
    const table = cell.closest('table');
    const row = cell.parentElement;
    const cellIndex = Array.from(row.children).indexOf(cell);

    row.classList.add('row-highlighted');

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

        cells[index].style.boxShadow = '0 0 20px rgba(196, 30, 58, 0.6)';
        setTimeout(() => {
            cells[index].style.boxShadow = '';
        }, 500);
    }
}

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
