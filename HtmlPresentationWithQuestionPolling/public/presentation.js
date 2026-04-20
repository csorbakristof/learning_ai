// Initialize Reveal.js
Reveal.initialize({
  hash: true,
  transition: 'slide',
  plugins: [],
  width: 1280,
  height: 720,
  margin: 0.1,
  center: true
});

// Connect to Socket.io
const socket = io();

// Store chart instances
const charts = {};

// Question configuration
const questionConfig = {
  question1: {
    labels: ['A) Open/Closed', 'B) Single Resp.', 'C) Liskov Sub.', 'D) Dependency Inv.'],
    answers: ['A', 'B', 'C', 'D']
  },
  question2: {
    labels: ['A) Faster execution', 'B) Better testability', 'C) Reduced memory'],
    answers: ['A', 'B', 'C']
  },
  question3: {
    labels: ['A) Interface Seg.', 'B) Open/Closed', 'C) Liskov Sub.', 'D) Single Resp.'],
    answers: ['A', 'B', 'C', 'D']
  }
};

// Initialize charts for each question
function initializeChart(questionId) {
  const canvas = document.getElementById(`chart-${questionId}`);
  if (!canvas) return;

  const config = questionConfig[questionId];
  const ctx = canvas.getContext('2d');
  
  charts[questionId] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: config.labels,
      datasets: [{
        label: 'Votes',
        data: config.answers.map(() => 0),
        backgroundColor: [
          'rgba(255, 99, 132, 0.7)',
          'rgba(54, 162, 235, 0.7)',
          'rgba(255, 206, 86, 0.7)',
          'rgba(75, 192, 192, 0.7)'
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)'
        ],
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1,
            color: '#fff',
            font: {
              size: 14
            }
          },
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        },
        x: {
          ticks: {
            color: '#fff',
            font: {
              size: 14
            }
          },
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        }
      },
      plugins: {
        legend: {
          display: false
        }
      },
      animation: {
        duration: 500
      }
    }
  });
}

// Update chart with new vote data
function updateChart(questionId, votes) {
  if (!charts[questionId]) return;
  
  const config = questionConfig[questionId];
  const data = config.answers.map(answer => votes[answer] || 0);
  
  charts[questionId].data.datasets[0].data = data;
  charts[questionId].update();
}

// Generate QR code for voting URL
async function generateQRCode(questionId) {
  const container = document.getElementById(`qr-container-${questionId.replace('question', '')}`);
  if (!container) return;

  try {
    // Get the public URL from the server
    const votingUrl = window.location.origin + '/vote.html';
    
    // Generate QR code
    const response = await fetch(`/api/qrcode?url=${encodeURIComponent(votingUrl)}`);
    const data = await response.json();
    
    if (data.qrCode) {
      container.innerHTML = `
        <img src="${data.qrCode}" alt="QR Code" />
        <p>Scan to vote</p>
      `;
    }
  } catch (error) {
    console.error('Failed to generate QR code:', error);
    container.innerHTML = '<p style="color: #333;">QR code unavailable</p>';
  }
}

// Initialize all question slides
function initializeQuestions() {
  Object.keys(questionConfig).forEach(questionId => {
    initializeChart(questionId);
    generateQRCode(questionId);
  });
}

// Socket.io event handlers
socket.on('initialVotes', (votes) => {
  console.log('Received initial votes:', votes);
  Object.keys(votes).forEach(questionId => {
    updateChart(questionId, votes[questionId]);
  });
});

socket.on('voteUpdate', (data) => {
  console.log('Vote update:', data);
  updateChart(data.questionId, data.votes);
});

socket.on('votesReset', () => {
  console.log('Votes reset');
  Object.keys(questionConfig).forEach(questionId => {
    const config = questionConfig[questionId];
    const emptyVotes = {};
    config.answers.forEach(answer => emptyVotes[answer] = 0);
    updateChart(questionId, emptyVotes);
  });
});

// Fetch initial vote counts
async function fetchInitialVotes() {
  try {
    const response = await fetch('/api/votes');
    const votes = await response.json();
    Object.keys(votes).forEach(questionId => {
      updateChart(questionId, votes[questionId]);
    });
  } catch (error) {
    console.error('Failed to fetch initial votes:', error);
  }
}

// Add reset button for presenter
function addResetButton() {
  const resetBtn = document.createElement('button');
  resetBtn.className = 'reset-button';
  resetBtn.textContent = '🔄 Reset Votes';
  resetBtn.addEventListener('click', async () => {
    if (confirm('Are you sure you want to reset all votes?')) {
      try {
        await fetch('/api/reset', { method: 'POST' });
        alert('Votes reset successfully!');
      } catch (error) {
        console.error('Failed to reset votes:', error);
        alert('Failed to reset votes');
      }
    }
  });
  document.body.appendChild(resetBtn);
}

// Initialize when Reveal.js is ready
Reveal.addEventListener('ready', () => {
  console.log('Presentation ready');
  initializeQuestions();
  fetchInitialVotes();
  addResetButton();
});

// Update charts when navigating to question slides
Reveal.addEventListener('slidechanged', (event) => {
  const questionId = event.currentSlide.dataset.question;
  if (questionId && charts[questionId]) {
    // Force chart update when slide is shown
    charts[questionId].update();
  }
});
