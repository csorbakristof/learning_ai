/**
 * Interactive Voting System for Reveal.js Presentations
 * 
 * This script manages real-time audience voting integration with Reveal.js.
 * It handles vote display components, server communication, and animations.
 */

// ============================================
// COMPONENT CREATION
// ============================================

/**
 * Creates a reusable vote display component
 * @returns {HTMLElement} The vote display component
 */
function createVoteDisplayComponent() {
    const container = document.createElement('div');
    container.className = 'vote-display';
    container.innerHTML = `
        <h4>Live Votes</h4>
        <div class="total-votes">
            Total: <span class="vote-total">0</span>
        </div>
        <div class="detailed-votes hidden">
            <div data-option="A">
                <span class="vote-label">A:</span>
                <span class="vote-count vote-a">0</span>
            </div>
            <div data-option="B">
                <span class="vote-label">B:</span>
                <span class="vote-count vote-b">0</span>
            </div>
            <div data-option="C">
                <span class="vote-label">C:</span>
                <span class="vote-count vote-c">0</span>
            </div>
            <div data-option="D">
                <span class="vote-label">D:</span>
                <span class="vote-count vote-d">0</span>
            </div>
            <div class="correct-answer-indicator" style="display:none;">
                Correct Answer: <span class="correct-answer-letter"></span>
            </div>
        </div>
        <button class="toggle-details" onclick="toggleVoteDetails()">
            Details (D)
        </button>
    `;
    return container;
}

/**
 * Inject vote display component into all question slides
 * This runs once on page load to automatically add the component
 */
function injectVoteDisplays() {
    // Create a single global vote display outside the slides container
    // This ensures position:fixed works correctly (not affected by Reveal's transforms)
    if (!document.querySelector('.vote-display')) {
        const voteDisplay = createVoteDisplayComponent();
        voteDisplay.style.display = 'none'; // Hidden by default
        document.body.appendChild(voteDisplay);
    }
}

// ============================================
// INITIALIZATION
// ============================================

// Inject vote displays before Reveal initializes
injectVoteDisplays();

// Initialize Reveal.js
Reveal.initialize({
    hash: true,
    center: true,
    transition: 'slide',
    slideNumber: true,
    showNotes: false
});

// ============================================
// VOTING SYSTEM STATE
// ============================================

let currentSlide = null;
let pollingInterval = null;
let isQuestionSlide = false;
let previousVoteCount = 0; // Track previous vote count for animation
let qrOverlayVisible = false; // Track QR overlay visibility
let qrOverlayElement = null; // Reference to QR overlay element
// SERVER_URL is set via window.PHP_SERVER_URL in presentation.html.
// It points to the directory on the PHP server that contains api.php and index.php.
const SERVER_URL = (window.PHP_SERVER_URL || '').replace(/\/+$/, '');
const POLL_INTERVAL = 1000; // 1 second

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Get question title from slide
 * @param {HTMLElement} slide - The slide element
 * @returns {string} The question title
 */
function getQuestionTitle(slide) {
    // Check for data-question-title attribute
    const customTitle = slide.getAttribute('data-question-title');
    if (customTitle) {
        return customTitle;
    }
    
    // Otherwise use h2 content
    const h2 = slide.querySelector('h2');
    if (h2) {
        return h2.textContent.trim();
    }
    
    return 'Untitled question';
}

// ============================================
// SERVER COMMUNICATION
// ============================================

/**
 * Notify server about new question
 * @param {string} questionTitle - The title of the new question
 */
async function notifyNewQuestion(questionTitle) {
    const url = `${SERVER_URL}/api.php?action=new-question`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title: questionTitle })
        });

        const text = await response.text();
        if (!response.ok) {
            console.error(`new-question HTTP ${response.status} from ${url}:`, text);
            return;
        }
        const data = JSON.parse(text);
        if (data.success) {
            console.log('New question confirmed by server:', data);
        } else {
            console.error('Server rejected new-question:', data);
        }

    } catch (error) {
        console.error('Error notifying new question (URL was: ' + url + '):', error);
    }
}

/**
 * Poll server for vote results
 */
async function pollResults() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
        
        const response = await fetch(`${SERVER_URL}/api.php?action=results`, {
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }
        
        const data = await response.json();
        updateVoteDisplay(data);
        
    } catch (error) {
        if (error.name === 'AbortError') {
            console.warn('Polling timeout - server may be slow');
        } else {
            console.error('Error polling results:', error.message);
            // Show error in console but don't disrupt presentation
        }
    }
}

// ============================================
// VOTE DISPLAY MANAGEMENT
// ============================================

/**
 * Update vote display with current counts
 * @param {Object} results - Vote results object {total, A, B, C, D}
 */
function updateVoteDisplay(results) {
    const slide = Reveal.getCurrentSlide();
    const voteDisplay = document.querySelector('.vote-display');
    
    if (!voteDisplay) return;
    
    // Update total with animation
    const totalSpan = voteDisplay.querySelector('.vote-total');
    if (totalSpan) {
        const newTotal = results.total || 0;
        const oldTotal = parseInt(totalSpan.textContent) || 0;
        
        if (newTotal !== oldTotal) {
            // Add animation class
            const totalContainer = voteDisplay.querySelector('.total-votes');
            if (totalContainer) {
                totalContainer.classList.add('updated');
                setTimeout(() => totalContainer.classList.remove('updated'), 500);
            }
        }
        
        totalSpan.textContent = newTotal;
    }
    
    // Update individual counts with animation
    const voteElements = {
        A: voteDisplay.querySelector('.vote-a'),
        B: voteDisplay.querySelector('.vote-b'),
        C: voteDisplay.querySelector('.vote-c'),
        D: voteDisplay.querySelector('.vote-d')
    };
    
    ['A', 'B', 'C', 'D'].forEach(letter => {
        const element = voteElements[letter];
        if (element) {
            const newCount = results[letter] || 0;
            const oldCount = parseInt(element.textContent) || 0;
            
            if (newCount !== oldCount) {
                // Add animation class
                element.classList.add('updated');
                setTimeout(() => element.classList.remove('updated'), 400);
            }
            
            element.textContent = newCount;
        }
    });
}

/**
 * Toggle visibility of detailed vote breakdown
 */
function toggleVoteDetails() {
    const slide = Reveal.getCurrentSlide();
    const voteDisplay = document.querySelector('.vote-display');
    
    if (!voteDisplay) return;
    
    const detailedVotes = voteDisplay.querySelector('.detailed-votes');
    const button = voteDisplay.querySelector('.toggle-details');
    
    if (detailedVotes) {
        const isCurrentlyHidden = detailedVotes.classList.contains('hidden');
        detailedVotes.classList.toggle('hidden');
        
        if (button) {
            if (detailedVotes.classList.contains('hidden')) {
                button.textContent = 'Details (D)';
            } else {
                button.textContent = 'Hide (D)';
                // When showing details, highlight correct answer
                highlightCorrectAnswer(slide);
            }
        }
    }
}

/**
 * Highlight the correct answer in the vote display
 * @param {HTMLElement} slide - The current slide element
 */
function highlightCorrectAnswer(slide) {
    const correctAnswer = slide.getAttribute('data-correct-answer');
    
    if (!correctAnswer) return; // No correct answer specified
    
    const voteDisplay = document.querySelector('.vote-display');
    if (!voteDisplay) return;
    
    // Remove any existing highlighting
    voteDisplay.querySelectorAll('.correct-answer').forEach(el => {
        el.classList.remove('correct-answer');
    });
    
    // Highlight the correct answer row
    const correctRow = voteDisplay.querySelector(`[data-option="${correctAnswer}"]`);
    if (correctRow) {
        correctRow.classList.add('correct-answer');
    }
    
    // Show correct answer indicator
    const indicator = voteDisplay.querySelector('.correct-answer-indicator');
    const indicatorLetter = voteDisplay.querySelector('.correct-answer-letter');
    if (indicator && indicatorLetter) {
        indicatorLetter.textContent = correctAnswer;
        indicator.style.display = 'block';
    }
}

// ============================================
// POLLING MANAGEMENT
// ============================================

/**
 * Start polling for vote results
 */
function startPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
    }
    
    // Poll immediately
    pollResults();
    
    // Then poll every second
    pollingInterval = setInterval(pollResults, POLL_INTERVAL);
    console.log('Started polling for results');
}

/**
 * Stop polling for vote results
 */
function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
        console.log('Stopped polling for results');
    }
}

// ============================================
// EVENT HANDLERS
// ============================================

/**
 * Handle slide change events
 * @param {Object} event - Reveal.js slide change event
 */
async function onSlideChanged(event) {
    const slide = event.currentSlide;
    const isQuestion = slide.hasAttribute('data-question-slide');
    
    console.log('onSlideChanged fired — isQuestion:', isQuestion, '| slide:', slide.id || slide.className || '(no id/class)');

    // Get the global vote display
    const voteDisplay = document.querySelector('.vote-display');
    
    // Stop polling from previous slide
    stopPolling();
    
    if (isQuestion) {
        // This is a question slide
        isQuestionSlide = true;
        const questionTitle = getQuestionTitle(slide);
        
        console.log('Entering question slide:', questionTitle);
        
        // Show the vote display and reset counters immediately (optimistic reset)
        if (voteDisplay) {
            voteDisplay.style.display = 'block';
        }
        updateVoteDisplay({ total: 0, A: 0, B: 0, C: 0, D: 0 });

        // Hide details panel on new question
        const detailedVotes = voteDisplay ? voteDisplay.querySelector('.detailed-votes') : null;
        const button = voteDisplay ? voteDisplay.querySelector('.toggle-details') : null;
        if (detailedVotes) detailedVotes.classList.add('hidden');
        if (button) button.textContent = 'Details (D)';

        // Tell the server to reset, then start polling
        await notifyNewQuestion(questionTitle);
        startPolling();
        
    } else {
        isQuestionSlide = false;
        console.log('Left question slide');
        
        // Hide the vote display
        if (voteDisplay) {
            voteDisplay.style.display = 'none';
        }
    }
}

/**
 * Create QR code overlay element
 */
function createQROverlay() {
    if (qrOverlayElement) return; // Already created
    
    const overlay = document.createElement('div');
    overlay.className = 'qr-overlay';
    overlay.innerHTML = `
        <div class="qr-code-container">
            <div id="qrcode-overlay"></div>
            <h3>Scan to Vote!</h3>
            <p id="votingUrlOverlay" style="font-size:14px; color:#666; word-break:break-all;"></p>
            <p class="close-hint">Press Q to close</p>
        </div>
    `;
    
    document.body.appendChild(overlay);
    qrOverlayElement = overlay;
    
    // Generate QR code for overlay
    const url = window.PHP_SERVER_URL || '';
    if (url && url.indexOf('YOUR-SERVER') === -1) {
        const qrElement = overlay.querySelector('#qrcode-overlay');
        if (qrElement) {
            new QRCode(qrElement, {
                text: url,
                width: 512,
                height: 512,
                correctLevel: QRCode.CorrectLevel.M
            });
        }
        const urlLabel = overlay.querySelector('#votingUrlOverlay');
        if (urlLabel) {
            urlLabel.textContent = url;
        }
    }
}

/**
 * Toggle QR code overlay visibility
 */
function toggleQROverlay() {
    if (!qrOverlayElement) {
        createQROverlay();
    }
    
    qrOverlayVisible = !qrOverlayVisible;
    
    if (qrOverlayVisible) {
        qrOverlayElement.classList.add('visible');
    } else {
        qrOverlayElement.classList.remove('visible');
    }
}

/**
 * Handle keyboard events
 * @param {KeyboardEvent} event - Keyboard event
 */
function onKeyPress(event) {
    // Check for 'Q' key press (QR overlay)
    if (event.key === 'q' || event.key === 'Q') {
        toggleQROverlay();
        event.preventDefault();
        return;
    }
    
    // Check for 'D' key press (Details)
    if (event.key === 'd' || event.key === 'D') {
        if (isQuestionSlide) {
            toggleVoteDetails();
            event.preventDefault();
        }
    }
}

// ============================================
// EVENT REGISTRATION
// ============================================

// Register event listeners
Reveal.on('slidechanged', onSlideChanged);
document.addEventListener('keydown', onKeyPress);

// Handle initial slide if it's a question
Reveal.on('ready', () => {
    const initialSlide = Reveal.getCurrentSlide();
    if (initialSlide.hasAttribute('data-question-slide')) {
        onSlideChanged({ currentSlide: initialSlide });
    }
});

/**
 * Initialize QR code on the main slide (for the QR code slide)
 */
function initializeMainQRCode() {
    const url = window.PHP_SERVER_URL || '';
    const el = document.getElementById('qrcode');
    const lbl = document.getElementById('votingUrl');
    
    if (!url || url.indexOf('YOUR-SERVER') !== -1) {
        if (el) el.innerHTML = '<p style="color:#c00;">Set PHP_SERVER_URL in sweep_questions.html</p>';
        return;
    }
    
    if (el) {
        new QRCode(el, {
            text: url,
            width: 256,
            height: 256,
            correctLevel: QRCode.CorrectLevel.M
        });
    }
    
    if (lbl) lbl.textContent = url;
}

// ============================================
// INITIALIZATION ON PAGE LOAD
// ============================================

// Make toggle functions globally accessible for onclick handlers
window.toggleVoteDetails = toggleVoteDetails;
window.toggleQROverlay = toggleQROverlay;

// Initialize QR codes when page is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        createQROverlay();
        initializeMainQRCode();
    });
} else {
    createQROverlay();
    initializeMainQRCode();
}

console.log('Voting system initialized');
console.log('Press Q on any slide to show/hide QR code');
console.log('Press D on question slides to toggle detailed vote counts');
