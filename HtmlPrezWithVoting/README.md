# Presentation Voting System

A real-time audience voting system for HTML presentations using Reveal.js.

## Phase 1 Complete ✓ - Server Backend
## Phase 2 Complete ✓ - Reveal.js Presentation
## Phase 3 Complete ✓ - Startup Script

The complete voting system is now implemented with the following features:

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

### Phase 2 - Presentation Features

- **Reveal.js Integration**: Loaded via CDN (no local files needed)
- **Interactive Slides**: Example presentation with title, content, and question slides
- **QR Code Display**: Dedicated slide showing voting URL for audience
- **Question Slides**: 
  - Marked with `data-question-slide="true"` attribute
  - Optional `data-question-title` for custom titles
  - Auto-detects question title from `<h2>` element
- **Vote Display Component**:
  - Shows total votes in real-time
  - Toggle detailed breakdown with 'V' key or button
  - Updates every 1 second via polling
  - Positioned at bottom-right of slides
- **Automatic Question Management**:
  - Detects slide changes
  - Notifies server when entering question slides
  - Resets votes automatically for each new question
  - Starts/stops polling based on slide type
- **Keyboard Controls**: Press 'V' to show/hide detailed vote counts

### Phase 3 - Startup Automation

- **start.bat**: Windows batch file for easy startup
  - Checks Node.js installation
  - Automatically installs dependencies if needed
  - Starts server in background
  - Opens presentation in default browser
  - Shows helpful instructions
  - One-click launch solution

### Installation

1. Install Node.js (if not already installed):
   - Download from https://nodejs.org/

2. Install npm dependencies:
   ```bash
   npm install
   ```
   
   Or simply run `start.bat` - it will install dependencies automatically!

### Usage

**Easy Way (Windows):**
Simply double-click `start.bat` in Windows Explorer!

The script will:
- Check Node.js installation
- Install dependencies if needed
- Start the server
- Open the presentation in your browser

**Manual Way:**

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
├── server.js              # Main Express server
├── package.json           # Node.js dependencies
├── presentation.html      # Reveal.js presentation with voting
├── start.bat              # Windows startup script
├── votes.csv             # Vote history (auto-created)
└── README.md             # This file
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

### Next Steps (Optional Enhancements)

- Additional themes and styling options
- Support for more question types
- Admin dashboard for monitoring votes
- Export results to different formats
- Multi-language support

## Using the Presentation

### Quick Start with start.bat

**For Windows users**, the easiest way to start the system:

1. **Double-click `start.bat`** in Windows Explorer
2. The script will:
   - ✓ Check if Node.js is installed
   - ✓ Install dependencies automatically (if not installed)
   - ✓ Start the server
   - ✓ Open the presentation in your browser
3. Follow the on-screen instructions

That's it! The presentation will open automatically.

### Manual Start

If you prefer to start manually or are on Mac/Linux:

1. **Start the server**:
   ```bash
   node server.js
   ```

2. **Open the presentation**:
   - Navigate to http://localhost:8000/presentation.html
   - Or the server will show you the URL in the console

3. **Show QR code to audience**:
   - Navigate to the QR code slide (slide 2)
   - Audience scans and opens voting page on their phones

4. **Navigate through slides**:
   - Use arrow keys or space bar
   - When you reach a question slide, voting starts automatically

5. **View vote results**:
   - Total votes update in real-time
   - Press **V** key to show/hide detailed breakdown (A, B, C, D counts)
   - Or click the "Show Details" button

6. **Move to next question**:
   - Simply navigate to the next question slide
   - Votes reset automatically and previous results are saved to CSV

### Creating Your Own Presentation

To create your own presentation with voting:

1. **Copy presentation.html** as a template

2. **Add regular slides** (without voting):
   ```html
   <section>
       <h2>Your Content</h2>
       <p>Regular slide content</p>
   </section>
   ```

3. **Add question slides** (with voting):
   ```html
   <section class="question-slide" data-question-slide="true" data-question-title="Custom Title">
       <h2>Your Question?</h2>
       <ul>
           <li><strong>A)</strong> Option A</li>
           <li><strong>B)</strong> Option B</li>
           <li><strong>C)</strong> Option C</li>
           <li><strong>D)</strong> Option D</li>
       </ul>
       
       <!-- Copy this vote display component -->
       <div class="vote-display">
           <h4>Live Votes</h4>
           <div class="total-votes">
               Total: <span class="vote-total">0</span>
           </div>
           <div class="detailed-votes hidden">
               <div><span class="vote-label">A:</span><span class="vote-count vote-a">0</span></div>
               <div><span class="vote-label">B:</span><span class="vote-count vote-b">0</span></div>
               <div><span class="vote-label">C:</span><span class="vote-count vote-c">0</span></div>
               <div><span class="vote-label">D:</span><span class="vote-count vote-d">0</span></div>
           </div>
           <button class="toggle-details" onclick="toggleVoteDetails()">
               Show Details (or press V)
           </button>
       </div>
   </section>
   ```

4. **Customize the QR code slide** (keep it or remove it):
   ```html
   <section>
       <h2>Join the Voting!</h2>
       <div class="qr-code-container">
           <img id="qrCodeImage" src="/qr-code" alt="QR Code for Voting">
           <h3>Scan with your smartphone</h3>
       </div>
   </section>
   ```

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

### Testing the Complete System

1. **Start the server**:
   ```bash
   node server.js
   ```

2. **Open presentation** in your browser:
   - Go to http://localhost:8000/presentation.html

3. **Open voting page** on another device (or browser tab):
   - Go to http://localhost:8000/ (or scan QR code from slide 2)

4. **Navigate to a question slide** in the presentation:
   - Watch vote counter initialize to 0

5. **Submit votes** from the voting page:
   - Click A, B, C, or D
   - Watch total votes update in presentation (every 1 second)

6. **Press V key** in presentation:
   - See detailed breakdown of A, B, C, D votes

7. **Navigate to next question slide**:
   - Previous votes should be saved to votes.csv
   - Vote counters reset to 0

8. **Check votes.csv**:
   - Verify previous question data was saved

### Troubleshooting

**Problem**: start.bat shows "Node.js is not installed"
- **Solution**: Install Node.js from https://nodejs.org/ and restart

**Problem**: start.bat fails with npm install error
- **Solution**: Open command prompt, navigate to folder, run `npm install` manually to see detailed error

**Problem**: Localtunnel fails to start
- **Solution**: Check internet connection, try restarting server

**Problem**: Port already in use
- **Solution**: Use `--port` option to specify different port

**Problem**: npm install fails
- **Solution**: Ensure Node.js is installed and up to date

**Problem**: QR code doesn't display
- **Solution**: Wait for tunnel to initialize (can take 5-10 seconds)

**Problem**: How do I stop the server when using start.bat?
- **Solution**: Press Ctrl+C in the command window that opened

**Problem**: Browser doesn't open automatically
- **Solution**: Manually open http://localhost:8000/presentation.html

### Development Notes

- Server automatically saves votes before shutdown (Ctrl+C)
- Each question's votes are logged to CSV when moving to next question
- localStorage prevents users from voting multiple times per question
- Vote limit prevents spam and abuse
