# Overview

We are creating a HTML and Reveal.js based presentation with questions at the end which will be answered by the audience via their smartphones. The presentation will show interactive statistics about the answers received.

I do not want to use any kind of server service which has to be started separately. I want the presentation contain the server functions.

I was suggested to use a tunneling service to provide access to the audience. They will scan a QR code, access a public tunnel towards my presentation notebook and access the webserver operated by the presentation (HTML+JavaScript) itself. The audience will get a very simple multiple choice page where they can vote for the answer.

## Technology

### Chosen Architecture: Node.js Server + ngrok Tunnel

The presentation runs on a **Node.js-based local web server** on the presenter's laptop, with **ngrok** providing public HTTPS access for the audience.

### Core Technology Stack

**Presentation Layer:**
- **Reveal.js**: HTML presentation framework with plugin support and mobile compatibility
- **HTML5 + CSS3**: Presentation content and responsive voting interface
- **Chart.js**: Real-time vote visualization (bar charts, updating automatically)
- **Socket.io Client**: Receives live vote updates from server

**Server Layer:**
- **Node.js**: JavaScript runtime for the local server
- **Express.js**: Minimal web server for serving presentation and handling API requests
- **Socket.io Server**: Real-time bidirectional WebSocket communication
- **In-memory storage**: Votes stored in JavaScript Map/Object (no database needed)

**Public Access:**
- **ngrok**: Secure tunnel providing public HTTPS URL
  - Command: `ngrok http 3000`
  - Free tier available, stable URLs with paid tier
  - Automatic HTTPS certificates
  - Example URL: `https://abc123.ngrok.io`

**Utilities:**
- **qrcode.js**: Client-side QR code generation for the tunnel URL
- **UUID/nanoid**: Generate unique session IDs for vote tracking

### Architecture Diagram

```
┌─────────────────────────────────────┐
│   Presenter's Laptop                │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  Web Browser                  │ │
│  │  http://localhost:3000        │ │
│  │  ┌─────────────────────────┐  │ │
│  │  │  Reveal.js Presentation │  │ │
│  │  │  • Slides               │  │ │
│  │  │  • QR Code Display      │  │ │
│  │  │  • Live Vote Charts     │  │ │
│  │  │  • Socket.io Client     │  │ │
│  │  └─────────────────────────┘  │ │
│  └───────────────────────────────┘ │
│             ↕ WebSocket             │
│             (localhost)             │
│  ┌───────────────────────────────┐ │
│  │  Node.js Server (Express)     │ │
│  │  • GET  /          → slides   │ │
│  │  • GET  /vote      → form     │ │
│  │  • POST /api/vote  → submit   │ │
│  │  • Socket.io broadcasts       │ │
│  │  • In-memory vote storage     │ │
│  │  Port: 3000                   │ │
│  └───────────────────────────────┘ │
│             ↕ HTTP                  │
│  ┌───────────────────────────────┐ │
│  │  ngrok Process                │ │
│  │  ngrok http 3000              │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
              ↕ HTTPS Tunnel
       ┌──────────────────────┐
       │  ngrok Cloud Service │
       │  https://abc.ngrok.io│
       └──────────────────────┘
              ↕ HTTPS
┌─────────────────────────────────────┐
│    Audience Smartphones (any WiFi)  │
│  ┌───────────────────────────────┐ │
│  │  1. Scan QR Code on screen    │ │
│  │  2. Opens: https://abc.ngrok  │ │
│  │            .io/vote            │ │
│  │                                │ │
│  │  ┌─────────────────────────┐  │ │
│  │  │ Vote for your answer:   │  │ │
│  │  │ ○ Answer A              │  │ │
│  │  │ ○ Answer B              │  │ │
│  │  │ ○ Answer C              │  │ │
│  │  │ ○ Answer D              │  │ │

**1. Server Startup:**
```
1. Run: node server.js
2. Express server starts on localhost:3000
3. Script automatically starts ngrok tunnel
4. ngrok returns public URL (e.g., https://abc123.ngrok.io)
5. Server stores tunnel URL for QR code generation
6. Open browser to http://localhost:3000
```

**2. Presentation Flow:**
```
1. Presenter navigates to question slide
2. JavaScript generates QR code with URL: https://abc123.ngrok.io/vote?q=1
3. Audience scans QR code with smartphones
```

**3. Voting Flow:**
```
Audience Device:
  1. Scan QR → opens /vote?q=1 in browser
  2. Display simple form with answer options
  3. User selects answer → clicks Submit
  4. POST to /api/vote { question: 1, answer: 'B', sessionId: '...' }

Server:
  5. Validate vote (check session hasn't voted yet)
  6. Store vote in memory: votes.get(questionId).set(sessionId, answer)
  7. Broadcast via Socket.io: emit('voteUpdate', { questionId, counts })

Presentation:
  8. Socket.io client receives 'voteUpdate' event
  9. Chart.js updates bar chart with new vote counts
  10. Display updates in real-time (no page refresh)
```

**4. Vote Display:**
- Chart shows vote distribution: A: 12 | B: 8 | C: 15 | D: 5
- Updates smoothly as each vote comes in
- Percentages calculated and displayed

### Project File Structure
```
presentation/
├── server.js                 # Express + Socket.io server with ngrok integration
├── package.json              # Node.js dependencies
├── package-lock.json
├── public/                   # Static files served by Express
│   ├── index.html           # Reveal.js presentation
│   ├── vote.html            # Mobile voting page
│   ├── css/
│   │   ├── reveal.css       # Reveal.js styles
│   │   ├── theme.css        # Custom presentation theme
│   │   └── vote.css         # Mobile-optimized voting interface
│   ├── js/
│   │   ├── presentation.js  # Custom presentation logic + Socket.io client
│   │   ├── voting.js        # Vote submission logic
│   │   └── qrcode.min.js    # QR code generation library
│   └── lib/                 # External libraries
│       ├── reveal.js
│       ├── chart.js
│       └── socket.io.js     # Socket.io client
├── .gitignore
└── README.md
```

### Key NPM Dependencies
```json
{
  "dependencies": {
    "express": "^4.18.0",
    "socket.io": "^4.6.0",
    "ngrok": "^5.0.0",
    "uuid": "^9.0.0"
  }
}
```
### Recommended Tech Stack Summary
- **Frontend**: Reveal.js + Chart.js + Socket.io client
- **Backend**: Node.js + Express + Socket.io server (or Python + Flask alternative)
- **Packaging**: Electron (optional, for standalone app)
- **Tunnel**: ngrok
- **QR Code**: qrcode.js
- **Storage**: In-memory JavaScript object/Map

### Security Considerations
- Rate limiting on vote endpoint (prevent spam)
- Session-based voting (one vote per session/device)
- CORS configuration for tunnel access
- No sensitive data storage
- Optional: Simple PIN/code for presentation control endpoints

## Steps of the implementation

First create a demo presentation using the above technologies about the use of the SOLID principles, 5 slides all together. Add 3 questions and multiple choice answers at the end.

