# Presentation Voting System

A real-time audience voting system for HTML presentations using Reveal.js.

## Phase 1 Complete ✓

The Node.js server backend is now implemented with the following features:

### Features Implemented

- **Express Web Server**: Configurable port (default: 8000)
- **REST API Endpoints**:
  - `GET /` - Voting page for audience
  - `POST /vote` - Submit votes (A/B/C/D)
  - `GET /results` - Get current vote counts
  - `POST /new-question` - Reset votes and set new question
  - `GET /qr-code` - Generate QR code with tunnel URL
  - `GET /status` - Check voting status
- **Localtunnel Integration**: Automatic public URL generation for remote access
- **Vote Limiting**: Configurable max votes per question (default: 500)
- **CSV Logging**: Automatic backup of all vote data with timestamps
- **Mobile-Friendly Voting Page**: Clean, responsive UI with light background
- **Graceful Shutdown**: Saves pending votes and closes tunnel on Ctrl+C

### Installation

1. Install Node.js (if not already installed):
   - Download from https://nodejs.org/

2. Install npm dependencies:
   ```bash
   npm install
   ```

### Usage

Start the server:
```bash
node server.js
```

Or use npm script:
```bash
npm start
```

#### Command-line Options

- `--port PORT` - Set server port (default: 8000)
- `--max-votes N` - Set maximum votes per question (default: 500)

Examples:
```bash
node server.js --port 8080 --max-votes 1000
node server.js --port 3000
```

### How It Works

1. Server starts and initializes a public tunnel via localtunnel
2. QR code is generated with the public URL
3. Audience scans QR code to access voting page on their smartphones
4. Votes are collected and counted in real-time
5. When presenter moves to new question, previous votes are saved to CSV
6. Vote counters reset for the new question
7. Presenter can view real-time vote counts in presentation

### REST API Documentation

#### GET /
Returns the voting page HTML for audience members.

#### POST /vote
Submit a vote.
- **Body**: `{ "vote": "A" }` (A, B, C, or D)
- **Response**: `{ "success": true, "total": 42 }`

#### GET /results
Get current vote counts.
- **Response**: 
  ```json
  {
    "total": 42,
    "A": 15,
    "B": 10,
    "C": 12,
    "D": 5,
    "question": "What is the capital of France?",
    "voting_open": true
  }
  ```

#### POST /new-question
Reset votes for a new question.
- **Body**: `{ "title": "Question title" }`
- **Response**: `{ "success": true, "question": "Question title" }`

#### GET /qr-code
Get QR code image (PNG) with tunnel URL.

#### GET /status
Check voting status.
- **Response**:
  ```json
  {
    "question": "Current question title",
    "voting_open": true,
    "total_votes": 42,
    "max_votes": 500
  }
  ```

### File Structure

```
HtmlPrezWithVoting/
├── server.js          # Main Express server
├── package.json       # Node.js dependencies
├── votes.csv         # Vote history (auto-created)
└── README.md         # This file
```

### CSV Format

Vote data is saved with the following columns:
- `timestamp` - ISO format timestamp
- `question_title` - Title of the question
- `votes_A` - Number of A votes
- `votes_B` - Number of B votes
- `votes_C` - Number of C votes
- `votes_D` - Number of D votes
- `total_votes` - Total number of votes

### Technical Details

- **Framework**: Express.js with CORS enabled
- **QR Code**: Generated using `qrcode` npm package
- **Tunneling**: Uses localtunnel for public URL
- **Vote Storage**: In-memory (resets on server restart)
- **Static Files**: Serves files from current directory

### Next Steps (Not Yet Implemented)

- **Phase 2**: Reveal.js presentation template
- **Phase 3**: JavaScript integration for real-time updates in slides
- **Phase 4**: Startup batch file for Windows
- **Phase 5**: Complete documentation and testing

### Testing the Server

1. Start the server:
   ```bash
   npm start
   ```

2. Open the voting page in browser:
   - Local: http://localhost:8000/
   - Remote: Use the tunnel URL shown in console

3. Test voting:
   - Click A, B, C, or D buttons
   - Verify votes are counted

4. Test results endpoint:
   ```bash
   curl http://localhost:8000/results
   ```

5. Test new question:
   ```bash
   curl -X POST http://localhost:8000/new-question \
     -H "Content-Type: application/json" \
     -d '{"title":"Test Question"}'
   ```

### Troubleshooting

**Problem**: Localtunnel fails to start
- **Solution**: Check internet connection, try restarting server

**Problem**: Port already in use
- **Solution**: Use `--port` option to specify different port

**Problem**: npm install fails
- **Solution**: Ensure Node.js is installed and up to date

**Problem**: QR code doesn't display
- **Solution**: Wait for tunnel to initialize (can take 5-10 seconds)

### Development Notes

- Server automatically saves votes before shutdown (Ctrl+C)
- Each question's votes are logged to CSV when moving to next question
- localStorage prevents users from voting multiple times per question
- Vote limit prevents spam and abuse
