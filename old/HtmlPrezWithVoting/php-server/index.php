<?php
/**
 * Audience Voting Page
 *
 * This page is what audience members open on their smartphones.
 * It polls api.php?action=status every 2 seconds to track the current question,
 * and POSTs to api.php?action=vote when the user picks an answer.
 *
 * Both api.php and this file live in the same directory on the web server,
 * so all fetch() calls use relative URLs.
 */
?>
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
            fetch('api.php?action=status')
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

            fetch('api.php?action=vote', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
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

        // Load question on page open, then poll every 2 seconds
        updateQuestion();
        setInterval(updateQuestion, 2000);
    </script>
</body>
</html>
