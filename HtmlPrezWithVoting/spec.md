# Overview

The goal of the project is to create a presentation using HTML and Reveal.js with not only static content, but also a test at the end of the lesson. This test uses ABCD multiple choice questions and the audience can vote. The number of votes can be seen real-time (in this phase, noone can see the ratio of answers so that it does not influence the voters) and after the presenter chooses so, the number of votes can be seen for the individual answers.

Votes are collected by a REST API of a small Node.js server running on the presenters notebook. The presentation is polling it. Audience smartphones vote on the current question via a simple webpage served by the same server. The URL of the server is shown to the audience via a QR code. Everytime the presenter proceeds to a new question, the vote counters are reset.

Functions of the server:
- Serve the voting webpage for the audience. This is a single HTML page with maybe some embedded javascript.
- Reset the vote counters, send title of the next question. Called when the presenter proceeds to a next question. Parallel questions do not need to be supported as the server is running on the presenter's notebook. No need to support parallel presentations. Before resetting the vote counters, the server saves the previous counter values with the title of the previous question into a CSV file (with timestamp) for backup.
- Serve a REST API endpoint which delivers a QR code containing the URL of the server for the audience (using the tunneling service).
- When the server starts, it initializes the tunneling server and when it is shut down, it deactivates the tunnel.

Functions of the tunnel
- This is a free tunneling service which is running as long as the Node.js web server is running.

Functions of the presentation, implemented in javascript inside the presentations template.
- Fetch the QR code from the Node.js server running on localhost and display it in a presentation slide.
- Notify the server about a new test question when entering a new question slide. The title of the question slide is sent as the title of the question. (If the slide does not have a title, the server receives an "untitled question" title.)
- In the question slide template, first only the number of total votes is displayed. After a hotkey is pressed of a small icon is clicked, the counter of the A-B-C-D answers are are shown. This is a small dedicated control inside the slides which can be reused in all slides.

# Implementation details

## Technical Stack & Libraries

1. **Node.js Web Framework**: Express.js will be used for the server.
   - Answer: Express.js (standard choice for Node.js web servers)

2. **Tunneling Service**: Which free tunneling service should I use?
   - ngrok (requires account but stable)
   - localtunnel (npm-based, no account needed)
   - cloudflared (Cloudflare Tunnel, no account needed)
   - Other preference?
   - Answer: localtunnel

3. **QR Code Generation**: Any library preference? (qrcode npm package, node-qrcode, etc.)
   - Answer: No preference, choose the one easiest to integrate.

4. **Reveal.js**: Should I use a specific version or template? Should I download it locally or use CDN?
   - Answer: use CDN

## Functionality Details

5. **Voting Page UI**: Any styling preferences? (Minimal/modern/specific color scheme?)
   - Answer: use minimal design which light background

6. **Polling Frequency**: How often should the presentation poll for vote updates? (1 second, 2 seconds?)
   - Answer: 1 second

7. **Results Reveal**: What hotkey should trigger showing individual answer counts? (Space, R, specific key?)
   - Answer: V as "votes"

8. **Question Detection**: How should the system identify question slides?
   - Data attribute (e.g., `data-question-slide`)?
   - Specific CSS class?
   - Any slide with certain content pattern?
   - Answer: Use a simple data attribute for this.

9. **Answer Format**: Should the ABCD answers be:
   - Hardcoded in slide content?
   - Configured via data attributes?
   - Any specific HTML structure?
   - Answer: The answers are hardcoded in the slide content. The implemenation does not need to know about it.

## Configuration & Deployment

10. **Port Configuration**: Any preference for the server port? (default 5000, 8000, configurable?)
    - Answer: 8000, but keep it configurable as the servers command line parameter.

11. **CSV Format**: Should the CSV include: timestamp, question title, A/B/C/D counts, total votes? Any other columns?
    - Answer: This is fine, no further columns needed.

12. **Security**: Do you need any authentication/rate limiting for votes to prevent spam?
    - Answer: Yes, add command-line configurable limit, the server should stop receiving votes after 500 votes.

13. **Starting the System**: Should there be a startup script, or should users manually start the Node.js server then open the presentation?
    - Answer: a batch file should be there to start the server and open the browser.

# Implementation plan

## Phase 1: Node.js Server Backend

### 1.1 Project Structure
Create the following files:
- `server.js` - Main Express server application
- `package.json` - Node.js dependencies (express, localtunnel, qrcode, cors)
- `votes.csv` - CSV file for storing vote history (auto-created)
- `start.bat` - Startup script for Windows

### 1.2 Server Core Functionality
- Initialize Express application with configurable port (default: 8000)
- Add command-line arguments:
  - `--port` - Server port
  - `--max-votes` - Maximum votes limit (default: 500)
- Implement vote storage with in-memory counters (A, B, C, D)
- Track current question title and total vote count
- Add vote limit enforcement (stop accepting after max reached)

### 1.3 Localtunnel Integration
- Use localtunnel npm package programmatically
- Start localtunnel when server starts
- Get tunnel URL from localtunnel API
- Store tunnel URL for QR code generation
- Gracefully shutdown tunnel on server exit

### 1.4 REST API Endpoints
- `GET /` - Serve the voting page (HTML)
- `POST /vote` - Submit a vote (A/B/C/D), returns success/error
- `GET /results` - Get current vote counts (JSON: total, A, B, C, D)
- `POST /new-question` - Reset votes, save to CSV, set new question title
- `GET /qr-code` - Return QR code PNG image with tunnel URL
- `GET /status` - Check if voting is open (not at max limit)

### 1.5 CSV Logging
- Format: `timestamp, question_title, votes_A, votes_B, votes_C, votes_D, total_votes`
- Append to `votes.csv` when new question starts (saves previous question data)
- Use ISO timestamp format

## Phase 2: Voting Webpage

### 2.1 HTML Structure (`/` endpoint serves this)
- Minimal, light background design
- Large, touch-friendly A/B/C/D buttons
- Display current question title at top
- Show feedback after voting (success/already voted/limit reached)
- Responsive design for mobile devices

### 2.2 Client-Side Logic
- Prevent multiple votes (use localStorage to track voted state)
- AJAX POST to `/vote` endpoint
- Display error messages if vote fails
- Simple, clean CSS with light colors

## Phase 3: Reveal.js Presentation

### 3.1 Base Template
- Create `presentation.html` with Reveal.js CDN links
- Include custom JavaScript for voting integration
- Add example slides including:
  - Title slide
  - Content slides
  - QR code slide
  - Multiple question slides

### 3.2 QR Code Slide
- Dedicated slide that displays QR code
- Fetch QR code image from `http://localhost:8000/qr-code`
- Display with appropriate size and instructions

### 3.3 Question Slides
- Add `data-question-slide="true"` attribute to question slides
- Add optional `data-question-title="..."` for custom title (otherwise use `<h2>` content)
- Include vote display component:
  - Total votes counter (always visible)
  - Individual A/B/C/D counts (hidden until 'V' pressed)
  - Small icon/button to toggle detailed view

### 3.4 Voting Integration JavaScript
- Detect slide changes using Reveal.js events
- When entering question slide:
  - Extract question title
  - POST to `/new-question` with title
  - Start polling `/results` every 1 second
- When leaving question slide:
  - Stop polling
- Handle 'V' key press (globally or per-slide):
  - Toggle visibility of detailed vote breakdown
- Update vote display in real-time from polling

### 3.5 Vote Display Component
- Reusable HTML structure to embed in question slides:
```html
<div class="vote-display">
  <div class="total-votes">Total votes: <span id="total">0</span></div>
  <div class="detailed-votes" style="display:none;">
    <div>A: <span id="votes-a">0</span></div>
    <div>B: <span id="votes-b">0</span></div>
    <div>C: <span id="votes-c">0</span></div>
    <div>D: <span id="votes-d">0</span></div>
  </div>
  <button class="toggle-details">Show Details</button>
</div>
```

## Phase 4: Integration & Testing

### 4.1 Startup Script (`start.bat`)
- Check if Node.js is installed
- Install npm dependencies if needed (npm install)
- Start Node.js server in background
- Wait 2-3 seconds for server to initialize
- Open default browser to `http://localhost:8000/presentation.html`
- Display instructions to presenter

### 4.2 Documentation
- Create `README.md` with:
  - Prerequisites (Node.js only)
  - Installation instructions (npm install)
  - How to start the system
  - How to use in presentation
  - Troubleshooting common issues

### 4.3 Testing Checklist
- Server starts and initializes localtunnel
- QR code displays in presentation
- Mobile devices can access voting page via tunnel
- Votes register correctly
- Vote limit enforcement works
- CSV logging captures data correctly
- Polling updates vote display in real-time
- 'V' key toggles detailed view
- Multiple question slides work sequentially
- Server shutdown closes tunnel properly

## Phase 5: Polish & Deployment

### 5.1 Error Handling
- Handle localtunnel failures gracefully
- Validate vote inputs (only A/B/C/D accepted)
- Handle network errors in polling
- Add try-catch blocks for file operations

### 5.2 UI/UX Improvements
- Add CSS animations for vote updates
- Improve mobile responsiveness
- Add visual feedback for button clicks
- Style the presentation consistently

### 5.3 Configuration File (Optional)
- Create `config.json` for default settings
- Allow override via command-line args

## Implementation Order

1. **Start with server.js** - Core Express app with endpoints (without tunnel first)
2. **Add voting page HTML** - Test voting locally
3. **Implement CSV logging** - Verify data saves correctly
4. **Add localtunnel integration** - Test remote access
5. **Create presentation.html** - Basic Reveal.js setup
6. **Add voting JavaScript** - Integration with server
7. **Create start.bat** - Automation script
8. **Testing and refinement** - Full end-to-end testing
9. **Documentation** - README.md

