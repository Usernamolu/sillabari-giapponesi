/**
 * UTILITIES CONDIVISE
 * Funzioni helper per performance, sicurezza e accessibilità
 */

/**
 * Audio Manager Singleton - Previene memory leak
 */
const AudioManager = {
    current: null,
    play(src) {
        // Valida path audio
        if (!src || !src.match(/^assets\/audio\/[\w-]+\.mp3$/)) {
            console.warn('Path audio non valido:', src);
            return Promise.reject(new Error('Invalid audio path'));
        }

        // Ferma audio corrente se esiste
        if (this.current) {
            this.current.pause();
            this.current = null;
        }

        // Crea e riproduce nuovo audio
        this.current = new Audio(src);
        return this.current.play().catch(err => {
            console.error('Errore riproduzione audio:', err);
            throw err;
        });
    }
};

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

        console.log(`✓ Stile "${id}" caricato`);
    }
};

/**
 * localStorage Safe Wrapper - Error handling
 */
const safeStorage = {
    get(key) {
        try {
            return localStorage.getItem(key);
        } catch(e) {
            console.warn('localStorage non disponibile:', e);
            return null;
        }
    },
    set(key, value) {
        try {
            localStorage.setItem(key, value);
            return true;
        } catch(e) {
            console.warn('localStorage non disponibile:', e);
            return false;
        }
    }
};

/**
 * Sanitizzazione TEI - Rimuove script e handler
 */
function sanitizeTEI(text) {
    return text
        .replace(/<script[^>]*>.*?<\/script>/gi, '')
        .replace(/on\w+\s*=\s*["'][^"']*["']/gi, '');
}

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

// Esporta utilities
window.AudioManager = AudioManager;
window.StyleManager = StyleManager;
window.safeStorage = safeStorage;
window.sanitizeTEI = sanitizeTEI;
window.debounce = debounce;

console.log('🛠️ Utilities caricate');
