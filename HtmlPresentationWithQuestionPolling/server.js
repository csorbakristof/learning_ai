const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const ngrok = require('ngrok');
const QRCode = require('qrcode');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

const PORT = 3000;

// In-memory vote storage
const votes = {
  question1: { A: 0, B: 0, C: 0, D: 0 },
  question2: { A: 0, B: 0, C: 0 },
  question3: { A: 0, B: 0, C: 0, D: 0 }
};

// Track voter sessions to prevent duplicate voting
const voterSessions = new Set();

// Serve static files from public directory
app.use(express.static('public'));
app.use(express.json());

// API endpoint to get current vote counts
app.get('/api/votes', (req, res) => {
  res.json(votes);
});

// API endpoint to submit a vote
app.post('/api/vote', (req, res) => {
  const { questionId, answer, sessionId } = req.body;
  
  // Check if this session has already voted
  const voteKey = `${sessionId}-${questionId}`;
  if (voterSessions.has(voteKey)) {
    return res.status(400).json({ error: 'Already voted for this question' });
  }
  
  // Validate question and answer
  if (!votes[questionId] || !votes[questionId].hasOwnProperty(answer)) {
    return res.status(400).json({ error: 'Invalid question or answer' });
  }
  
  // Record the vote
  votes[questionId][answer]++;
  voterSessions.add(voteKey);
  
  // Broadcast updated votes to all connected clients
  io.emit('voteUpdate', { questionId, votes: votes[questionId] });
  
  res.json({ success: true, votes: votes[questionId] });
});

// API endpoint to reset votes (for presenter)
app.post('/api/reset', (req, res) => {
  Object.keys(votes).forEach(key => {
    Object.keys(votes[key]).forEach(answer => {
      votes[key][answer] = 0;
    });
  });
  voterSessions.clear();
  io.emit('votesReset');
  res.json({ success: true });
});

// API endpoint to get QR code
app.get('/api/qrcode', async (req, res) => {
  try {
    const url = req.query.url;
    const qrCodeDataURL = await QRCode.toDataURL(url, {
      width: 300,
      margin: 2
    });
    res.json({ qrCode: qrCodeDataURL });
  } catch (error) {
    res.status(500).json({ error: 'Failed to generate QR code' });
  }
});

// Socket.io connection handling
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  
  // Send current vote counts to newly connected client
  socket.emit('initialVotes', votes);
  
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

// Start the server
server.listen(PORT, async () => {
  console.log(`\n✅ Local server running on http://localhost:${PORT}`);
  console.log('📊 Presentation: http://localhost:${PORT}');
  console.log('📱 Voting page: http://localhost:${PORT}/vote.html\n');
  
  try {
    // Start ngrok tunnel
    console.log('🌐 Starting ngrok tunnel...');
    const url = await ngrok.connect({
      addr: PORT,
      authtoken_from_env: true // Set NGROK_AUTHTOKEN env variable for stable URLs
    });
    
    console.log(`\n✨ Public URL: ${url}`);
    console.log(`📱 Voting URL: ${url}/vote.html`);
    console.log('\n🎯 Share this URL with your audience!\n');
    
    // Store the public URL for QR code generation
    global.publicUrl = url;
    
  } catch (error) {
    console.error('⚠️  Failed to start ngrok:', error.message);
    console.log('💡 Install ngrok and optionally set NGROK_AUTHTOKEN environment variable');
    console.log('   Presentation will work locally, but no public access available.\n');
    global.publicUrl = `http://localhost:${PORT}`;
  }
});

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n🛑 Shutting down...');
  await ngrok.kill();
  process.exit(0);
});
