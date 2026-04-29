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
            <div>
                <span class="vote-label">A:</span>
                <span class="vote-count vote-a">0</span>
            </div>
            <div>
                <span class="vote-label">B:</span>
                <span class="vote-count vote-b">0</span>
            </div>
            <div>
                <span class="vote-label">C:</span>
                <span class="vote-count vote-c">0</span>
            </div>
            <div>
                <span class="vote-label">D:</span>
                <span class="vote-count vote-d">0</span>
            </div>
        </div>
        <button class="toggle-details" onclick="toggleVoteDetails()">
            Show Details (or press V)
        </button>
    `;
    return container;
}

/**
 * Inject vote display component into all question slides
 * This runs once on page load to automatically add the component
 */
function injectVoteDisplays() {
    const questionSlides = document.querySelectorAll('[data-question-slide="true"]');
    questionSlides.forEach(slide => {
        // Only inject if not already present
        if (!slide.querySelector('.vote-display')) {
            const voteDisplay = createVoteDisplayComponent();
            slide.appendChild(voteDisplay);
        }
    });
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
const SERVER_URL = 'http://localhost:8000';
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
    try {
        const response = await fetch(`${SERVER_URL}/new-question`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title: questionTitle })
        });
        
        const data = await response.json();
        console.log('New question set:', data);
        
        // Reset vote display
        updateVoteDisplay({ total: 0, A: 0, B: 0, C: 0, D: 0 });
        
    } catch (error) {
        console.error('Error notifying new question:', error);
    }
}

/**
 * Poll server for vote results
 */
async function pollResults() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
        
        const response = await fetch(`${SERVER_URL}/results`, {
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
    const voteDisplay = slide.querySelector('.vote-display');
    
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
    const detailedVotes = slide.querySelector('.detailed-votes');
    const button = slide.querySelector('.toggle-details');
    
    if (detailedVotes) {
        detailedVotes.classList.toggle('hidden');
        
        if (button) {
            if (detailedVotes.classList.contains('hidden')) {
                button.textContent = 'Show Details (or press V)';
            } else {
                button.textContent = 'Hide Details (or press V)';
            }
        }
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
function onSlideChanged(event) {
    const slide = event.currentSlide;
    const isQuestion = slide.hasAttribute('data-question-slide');
    
    // Stop polling from previous slide
    stopPolling();
    
    if (isQuestion) {
        // This is a question slide
        isQuestionSlide = true;
        const questionTitle = getQuestionTitle(slide);
        
        console.log('Entered question slide:', questionTitle);
        
        // Notify server about new question
        notifyNewQuestion(questionTitle);
        
        // Start polling for results
        startPolling();
        
        // Ensure details are hidden initially
        const detailedVotes = slide.querySelector('.detailed-votes');
        const button = slide.querySelector('.toggle-details');
        if (detailedVotes) {
            detailedVotes.classList.add('hidden');
        }
        if (button) {
            button.textContent = 'Show Details (or press V)';
        }
        
    } else {
        isQuestionSlide = false;
        console.log('Left question slide');
    }
}

/**
 * Handle keyboard events
 * @param {KeyboardEvent} event - Keyboard event
 */
function onKeyPress(event) {
    // Check for 'V' key press
    if (event.key === 'v' || event.key === 'V') {
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

// Make toggle function globally accessible for onclick handlers
window.toggleVoteDetails = toggleVoteDetails;

console.log('Voting system initialized');
console.log('Press V on question slides to toggle detailed vote counts');
