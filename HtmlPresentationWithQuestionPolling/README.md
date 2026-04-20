# SOLID Principles - Interactive Presentation

An interactive presentation about SOLID principles with live audience polling using Node.js, Reveal.js, and ngrok.

## Features

- 📊 **5 slides** covering all SOLID principles with code examples
- 🎯 **3 interactive questions** with multiple-choice answers
- 📱 **Mobile-friendly voting** via QR code
- 📈 **Real-time vote visualization** using Chart.js
- 🌐 **Public access** via ngrok tunnel
- 🔄 **Live updates** with Socket.io WebSockets

## Technology Stack

- **Node.js** + **Express.js** - Local web server
- **Socket.io** - Real-time bidirectional communication
- **Reveal.js** - HTML presentation framework
- **Chart.js** - Interactive vote charts
- **ngrok** - Public HTTPS tunnel
- **QRCode.js** - QR code generation

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. (Optional) Configure ngrok

For a stable public URL, sign up at [ngrok.com](https://ngrok.com) and set your auth token:

```bash
# Windows PowerShell
$env:NGROK_AUTHTOKEN="your_token_here"

# Windows CMD
set NGROK_AUTHTOKEN=your_token_here

# Linux/Mac
export NGROK_AUTHTOKEN=your_token_here
```

**Note:** ngrok will work without authentication, but you'll get a random URL each time.

### 3. Start the Server

```bash
npm start
```

The server will:
1. Start on `http://localhost:3000`
2. Launch an ngrok tunnel
3. Display the public URL in the console
4. Generate QR codes automatically

## Usage

### For Presenters

1. Open `http://localhost:3000` in your browser
2. Navigate through slides using arrow keys or space
3. When you reach question slides, QR codes will appear automatically
4. Watch real-time vote updates on the charts
5. Use the **Reset Votes** button (bottom-right) to clear all votes between sessions

### For Audience

1. Scan the QR code displayed on the presentation
2. You'll be directed to the voting page
3. Select your answer for each question
4. Votes are submitted immediately and counted in real-time
5. Each device can vote once per question (tracked by session ID)

## Project Structure

```
HtmlPresentationWithQuestionPolling/
├── server.js                 # Node.js server with Express & Socket.io
├── package.json              # Dependencies
├── README.md                 # This file
├── public/
│   ├── index.html           # Reveal.js presentation
│   ├── vote.html            # Mobile voting page
│   ├── styles.css           # Custom CSS
│   └── presentation.js      # Client-side logic & charts
```

## API Endpoints

- `GET /` - Presentation page
- `GET /vote.html` - Voting page
- `GET /api/votes` - Get current vote counts
- `POST /api/vote` - Submit a vote
- `POST /api/reset` - Reset all votes (presenter only)
- `GET /api/qrcode?url=<url>` - Generate QR code

## Questions Included

1. **Question 1:** Which SOLID principle states that "a class should have only one reason to change"?
   - Correct answer: B) Single Responsibility Principle

2. **Question 2:** What is the main benefit of following the Dependency Inversion Principle?
   - Correct answer: B) Better testability and flexibility

3. **Question 3:** Which principle is violated when a subclass cannot properly replace its parent class?
   - Correct answer: C) Liskov Substitution Principle

## Troubleshooting

### ngrok fails to start
- Install ngrok: `npm install ngrok`
- Or download from [ngrok.com](https://ngrok.com/download)
- The presentation will still work locally without ngrok

### Votes not updating in real-time
- Check browser console for errors
- Ensure Socket.io is connecting (check server logs)
- Try refreshing both presentation and voting pages

### QR codes not appearing
- Check that the server has internet access
- Verify the QRCode library is installed: `npm install qrcode`

## Development

To run in development mode with auto-reload:

```bash
npm run dev
```

This uses `nodemon` to restart the server when files change.

## License

MIT
