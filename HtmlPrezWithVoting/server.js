#!/usr/bin/env node
/**
 * Presentation Voting Server
 * A Node.js/Express server to handle real-time audience voting for presentations
 */

const express = require('express');
const cors = require('cors');
const localtunnel = require('localtunnel');
const QRCode = require('qrcode');
const fs = require('fs');
const path = require('path');

// Parse command-line arguments
const args = process.argv.slice(2);
let port = 8000;
let maxVotes = 500;

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--port' && args[i + 1]) {
        port = parseInt(args[i + 1]);
        i++;
    } else if (args[i] === '--max-votes' && args[i + 1]) {
        maxVotes = parseInt(args[i + 1]);
        i++;
    }
}

// Initialize Express app
const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('.')); // Serve static files from current directory

// Global state
let voteCounts = { A: 0, B: 0, C: 0, D: 0 };
let totalVotes = 0;
let currentQuestion = "Waiting for first question...";
let tunnelUrl = null;
let tunnel = null;
const csvFilename = 'votes.csv';

// HTML template for voting page
const VOTING_PAGE_HTML = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vote</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #f5f5f5;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            padding: 30px;
            max-width: 500px;
            width: 100%;
        }
        
        h1 {
            font-size: 24px;
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .question {
            font-size: 16px;
            color: #666;
            margin-bottom: 30px;
            text-align: center;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 8px;
        }
        
        .buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        button {
            font-size: 32px;
            font-weight: bold;
            padding: 40px;
            border: 2px solid #ddd;
            border-radius: 12px;
            background: white;
            color: #333;
            cursor: pointer;
            transition: all 0.2s;
            touch-action: manipulation;
        }
        
        button:hover {
            transform: scale(1.05);
            border-color: #4CAF50;
            background: #f0f8f0;
        }
        
        button:active {
            transform: scale(0.98);
        }
        
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .message {
            text-align: center;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 16px;
            display: none;
        }
        
        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .message.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #999;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Cast Your Vote</h1>
        <div class="question" id="question">Loading question...</div>
        <div class="buttons">
            <button onclick="vote('A')" id="btnA">A</button>
            <button onclick="vote('B')" id="btnB">B</button>
            <button onclick="vote('C')" id="btnC">C</button>
            <button onclick="vote('D')" id="btnD">D</button>
        </div>
        <div class="message" id="message"></div>
        <div class="footer">Choose your answer by clicking a button</div>
    </div>

    <script>
        const STORAGE_KEY = 'voted_question';
        
        function updateQuestion() {
            fetch('/status')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('question').textContent = data.question;
                    
                    // Check if we've already voted for this question
                    const votedQuestion = localStorage.getItem(STORAGE_KEY);
                    if (votedQuestion === data.question) {
                        showMessage('You have already voted for this question', 'info');
                        disableButtons();
                    } else {
                        enableButtons();
                        hideMessage();
                    }
                    
                    if (!data.voting_open) {
                        showMessage('Voting limit reached for this question', 'error');
                        disableButtons();
                    }
                })
                .catch(err => {
                    console.error('Error fetching status:', err);
                });
        }
        
        function vote(answer) {
            const currentQuestion = document.getElementById('question').textContent;
            
            fetch('/vote', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ vote: answer })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showMessage('✓ Vote recorded successfully!', 'success');
                    localStorage.setItem(STORAGE_KEY, currentQuestion);
                    disableButtons();
                } else {
                    showMessage(data.error || 'Failed to record vote', 'error');
                    if (data.error && data.error.includes('limit')) {
                        disableButtons();
                    }
                }
            })
            .catch(err => {
                showMessage('Network error. Please try again.', 'error');
                console.error('Error voting:', err);
            });
        }
        
        function showMessage(text, type) {
            const msg = document.getElementById('message');
            msg.textContent = text;
            msg.className = 'message ' + type;
            msg.style.display = 'block';
        }
        
        function hideMessage() {
            document.getElementById('message').style.display = 'none';
        }
        
        function disableButtons() {
            document.querySelectorAll('button').forEach(btn => btn.disabled = true);
        }
        
        function enableButtons() {
            document.querySelectorAll('button').forEach(btn => btn.disabled = false);
        }
        
        // Update question on page load
        updateQuestion();
        
        // Poll for question changes every 2 seconds
        setInterval(updateQuestion, 2000);
    </script>
</body>
</html>
`;

/**
 * Save current vote counts to CSV file
 */
function saveVotesToCSV(questionTitle) {
    const fileExists = fs.existsSync(csvFilename);
    
    // Create header row if file doesn't exist
    let csvContent = '';
    if (!fileExists) {
        csvContent = 'timestamp,question_title,votes_A,votes_B,votes_C,votes_D,total_votes\n';
    }
    
    // Add vote data
    const timestamp = new Date().toISOString();
    csvContent += `"${timestamp}","${questionTitle.replace(/"/g, '""')}",${voteCounts.A},${voteCounts.B},${voteCounts.C},${voteCounts.D},${totalVotes}\n`;
    
    fs.appendFileSync(csvFilename, csvContent, 'utf8');
    console.log(`✓ Saved votes to ${csvFilename}: ${questionTitle} -> Total: ${totalVotes}`);
}

/**
 * Initialize localtunnel
 */
async function startLocaltunnel() {
    try {
        console.log('Starting localtunnel...');
        tunnel = await localtunnel({ port: port });
        tunnelUrl = tunnel.url;
        console.log(`✓ Tunnel URL: ${tunnelUrl}`);
        
        tunnel.on('close', () => {
            console.log('Tunnel closed');
        });
        
        return tunnelUrl;
    } catch (error) {
        console.error('ERROR starting localtunnel:', error.message);
        console.log('Server will run on localhost only.');
        tunnelUrl = `http://localhost:${port}`;
        return tunnelUrl;
    }
}

/**
 * Stop localtunnel
 */
function stopLocaltunnel() {
    if (tunnel) {
        console.log('Stopping localtunnel...');
        tunnel.close();
        console.log('Localtunnel stopped.');
    }
}

// ============================================================================
// REST API ENDPOINTS
// ============================================================================

/**
 * GET / - Serve the voting page to audience
 */
app.get('/', (req, res) => {
    res.send(VOTING_PAGE_HTML);
});

/**
 * POST /vote - Handle vote submission from audience
 */
app.post('/vote', (req, res) => {
    const vote = req.body.vote ? req.body.vote.toUpperCase() : '';
    
    // Validate vote
    if (!['A', 'B', 'C', 'D'].includes(vote)) {
        return res.json({ success: false, error: 'Invalid vote. Must be A, B, C, or D.' });
    }
    
    // Check if vote limit reached
    if (totalVotes >= maxVotes) {
        return res.json({ success: false, error: 'Vote limit reached for this question.' });
    }
    
    // Record vote
    voteCounts[vote]++;
    totalVotes++;
    
    console.log(`Vote received: ${vote} | Total: ${totalVotes} | Counts: A=${voteCounts.A} B=${voteCounts.B} C=${voteCounts.C} D=${voteCounts.D}`);
    
    res.json({ success: true, total: totalVotes });
});

/**
 * GET /results - Get current vote counts for presentation display
 */
app.get('/results', (req, res) => {
    res.json({
        total: totalVotes,
        A: voteCounts.A,
        B: voteCounts.B,
        C: voteCounts.C,
        D: voteCounts.D,
        question: currentQuestion,
        voting_open: totalVotes < maxVotes
    });
});

/**
 * POST /new-question - Reset votes for a new question and save previous results
 */
app.post('/new-question', (req, res) => {
    const newTitle = req.body.title || 'Untitled question';
    
    // Save previous question results to CSV (if there were any votes)
    if (totalVotes > 0) {
        saveVotesToCSV(currentQuestion);
    }
    
    // Reset for new question
    voteCounts = { A: 0, B: 0, C: 0, D: 0 };
    totalVotes = 0;
    currentQuestion = newTitle;
    
    console.log('\n=== New Question ===');
    console.log(`Title: ${newTitle}`);
    console.log('Vote counters reset.');
    
    res.json({ success: true, question: currentQuestion });
});

/**
 * GET /qr-code - Generate and return QR code image with tunnel URL
 */
app.get('/qr-code', async (req, res) => {
    if (!tunnelUrl) {
        return res.status(500).json({ error: 'Tunnel URL not available' });
    }
    
    try {
        // Generate QR code as PNG buffer
        const qrCodeBuffer = await QRCode.toBuffer(tunnelUrl, {
            errorCorrectionLevel: 'M',
            type: 'png',
            width: 300,
            margin: 2
        });
        
        res.type('png');
        res.send(qrCodeBuffer);
    } catch (error) {
        console.error('Error generating QR code:', error);
        res.status(500).json({ error: 'Failed to generate QR code' });
    }
});

/**
 * GET /status - Check voting status
 */
app.get('/status', (req, res) => {
    res.json({
        question: currentQuestion,
        voting_open: totalVotes < maxVotes,
        total_votes: totalVotes,
        max_votes: maxVotes
    });
});

// ============================================================================
// SERVER STARTUP AND SHUTDOWN
// ============================================================================

/**
 * Graceful shutdown handler
 */
function gracefulShutdown() {
    console.log('\n\nShutting down server...');
    
    // Save current votes if any
    if (totalVotes > 0) {
        saveVotesToCSV(currentQuestion);
    }
    
    // Stop tunnel
    stopLocaltunnel();
    
    console.log('Goodbye!');
    process.exit(0);
}

// Register shutdown handlers
process.on('SIGINT', gracefulShutdown);
process.on('SIGTERM', gracefulShutdown);

/**
 * Start the server
 */
async function startServer() {
    console.log('='.repeat(60));
    console.log('  PRESENTATION VOTING SERVER');
    console.log('='.repeat(60));
    console.log(`Port: ${port}`);
    console.log(`Max votes per question: ${maxVotes}`);
    console.log(`CSV file: ${csvFilename}`);
    console.log('='.repeat(60));
    
    // Start localtunnel
    await startLocaltunnel();
    
    // Start Express server
    app.listen(port, () => {
        console.log('\n✓ Server starting...');
        console.log(`✓ Presentation URL: http://localhost:${port}/presentation.html`);
        console.log(`✓ Voting URL: ${tunnelUrl}`);
        console.log('\nPress Ctrl+C to stop the server\n');
    });
}

// Start the server
startServer().catch(error => {
    console.error('Failed to start server:', error);
    process.exit(1);
});
