/**
 * UTILITIES CONDIVISE
 * Funzioni helper per performance
 */

/**
 * Style Manager - Previene duplicazione stili
 */
const StyleManager = {
    injected: new Set(),
    inject(id, css) {
        if (this.injected.has(id)) return;

        const style = document.createElement('style');
        style.id = `style-${id}`;
        style.innerHTML = css;
        document.head.appendChild(style);
        this.injected.add(id);
    }
};

/**
 * Debounce - Throttling funzioni
 */
function debounce(fn, ms) {
    let timer;
    return function(...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), ms);
    };
}

window.StyleManager = StyleManager;
window.debounce = debounce;
