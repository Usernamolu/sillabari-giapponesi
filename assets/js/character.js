/**
 * JavaScript per le pagine dei singoli caratteri
 */

document.addEventListener('DOMContentLoaded', function() {
    initStrokeOrderReplay();
    initQuizButtons();
    initAudioPlayback();
    initNavigationShortcuts();
    initTEIToggle();
});

/**
 * Replay animazione stroke order
 */
function initStrokeOrderReplay() {
    const replayBtn = document.querySelector('.replay-btn');
    if (!replayBtn) return;

    replayBtn.addEventListener('click', function() {
        const svgContainer = document.querySelector('.stroke-order-display svg');
        if (!svgContainer) return;

        // Reset animazione
        const animations = svgContainer.querySelectorAll('animate, animateTransform');
        animations.forEach(anim => {
            anim.beginElement();
        });

        // Feedback visivo
        this.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            this.style.transform = '';
        }, 600);
    });
}

/**
 * Gestione pulsanti quiz
 */
function initQuizButtons() {
    const quizButtons = document.querySelectorAll('.quiz-option');

    quizButtons.forEach(button => {
        button.addEventListener('click', function() {
            const isCorrect = this.dataset.correct === 'true';

            // Disabilita tutti i pulsanti
            quizButtons.forEach(btn => btn.disabled = true);

            if (isCorrect) {
                this.classList.add('correct');
                this.innerHTML = '✓ ' + this.innerHTML;
                showFeedback('Corretto! 🎉', 'success');
            } else {
                this.classList.add('wrong');
                this.innerHTML = '✗ ' + this.innerHTML;

                // Mostra risposta corretta
                const correctBtn = Array.from(quizButtons).find(btn => btn.dataset.correct === 'true');
                if (correctBtn) {
                    setTimeout(() => {
                        correctBtn.classList.add('correct');
                        correctBtn.innerHTML = '✓ ' + correctBtn.innerHTML;
                    }, 500);
                }
                showFeedback('Riprova! 💪', 'error');
            }
        });
    });
}

/**
 * Feedback visivo per quiz
 */
function showFeedback(message, type) {
    const feedback = document.createElement('div');
    feedback.className = `quiz-feedback ${type}`;
    feedback.textContent = message;

    const quizSection = document.querySelector('.practice');
    if (quizSection) {
        quizSection.appendChild(feedback);

        setTimeout(() => {
            feedback.style.opacity = '0';
            setTimeout(() => feedback.remove(), 300);
        }, 2000);
    }
}

/**
 * Audio playback con AudioManager
 */
function initAudioPlayback() {
    const audioButtons = document.querySelectorAll('.play-audio');

    audioButtons.forEach(button => {
        button.addEventListener('click', function() {
            const audioSrc = this.dataset.audio;
            if (!audioSrc) {
                console.log('🎵 Audio non ancora disponibile');
                return;
            }

            // Usa AudioManager per prevenire memory leak
            AudioManager.play(audioSrc).then(() => {
                // Animazione durante riproduzione
                this.classList.add('playing');

                if (AudioManager.current) {
                    AudioManager.current.addEventListener('ended', () => {
                        this.classList.remove('playing');
                    });
                }
            }).catch(err => {
                console.error('Errore riproduzione audio:', err);
            });
        });
    });
}

/**
 * Scorciatoie da tastiera per navigazione
 */
function initNavigationShortcuts() {
    document.addEventListener('keydown', function(e) {
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

    teiDetails.addEventListener('toggle', function() {
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
    const sanitized = sanitizeTEI(text);

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

// Aggiungi stili con StyleManager (previene duplicati)
StyleManager.inject('character-styles', `
    .quiz-option.correct {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
        color: white !important;
        border-color: #4CAF50 !important;
    }

    .quiz-option.wrong {
        background: linear-gradient(135deg, #f44336 0%, #da190b 100%) !important;
        color: white !important;
        border-color: #f44336 !important;
    }

    .quiz-option:disabled {
        cursor: not-allowed;
        opacity: 0.7;
    }

    .quiz-feedback {
        margin-top: 1rem;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        animation: fadeIn 0.3s ease;
    }

    .quiz-feedback.success {
        background: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }

    .quiz-feedback.error {
        background: #f8d7da;
        color: #721c24;
        border: 2px solid #f5c6cb;
    }

    .play-audio.playing {
        animation: pulse 0.5s ease infinite;
    }

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

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
`);

console.log('🎌 Pagina carattere caricata! Usa Alt+← e Alt+→ per navigare.');
