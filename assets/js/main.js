/**
 * ALFABETO GIAPPONESE INTERATTIVO
 * JavaScript principale
 * Gabriele Errico - UniPV 2025-2026
 */

// Inizializzazione al caricamento della pagina
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎌 Alfabeto Giapponese caricato!');

    // Smooth scroll per i link interni
    initSmoothScroll();

    // Animazioni al scroll
    initScrollAnimations();

    // Statistiche visita
    trackVisit();
});

/**
 * Smooth scroll per i link di navigazione interna
 */
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            // Ignora i link vuoti o solo "#"
            if (href === '#' || href === '') return;

            e.preventDefault();

            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                // Aggiorna URL senza reload
                history.pushState(null, null, href);
            }
        });
    });
}

/**
 * Animazioni al scroll (fade in)
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Osserva tutte le card
    const cards = document.querySelectorAll('.system-card, .path-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

/**
 * Traccia visite con safeStorage
 */
function trackVisit() {
    const visits = safeStorage.get('jp-visits') || 0;
    const newVisits = parseInt(visits) + 1;
    safeStorage.set('jp-visits', newVisits);

    if (newVisits === 1) {
        console.log('👋 Benvenuto per la prima volta!');
    } else {
        console.log(`🎉 Questa è la tua visita numero ${newVisits}!`);
    }
}

/**
 * Aggiungi classe per animazione fade-in con StyleManager
 */
StyleManager.inject('main-animations', `
    .fade-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
`);

/**
 * Easter egg: Konami Code
 */
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', function(e) {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);

    if (konamiCode.join(',') === konamiSequence.join(',')) {
        activateEasterEgg();
    }
});

function activateEasterEgg() {
    console.log('🎮 Konami Code attivato!');
    document.body.style.transition = 'all 2s ease';
    document.body.style.transform = 'rotate(360deg)';

    setTimeout(() => {
        document.body.style.transform = 'none';
        alert('🌸 がんばって! (Ganbatte! - Buona fortuna con lo studio!)');
    }, 2000);
}

/**
 * Funzione utility: formatta data in giapponese
 */
function getJapaneseDate() {
    const date = new Date();
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();

    return `${year}年${month}月${day}日`;
}

// Mostra data in console
console.log(`📅 Oggi: ${getJapaneseDate()}`);
