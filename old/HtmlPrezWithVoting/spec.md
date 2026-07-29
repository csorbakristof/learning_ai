# Overview

The goal of the project is to create a presentation using HTML and Reveal.js with not only static content, but also a test at the end of the lesson. This test uses ABCD multiple choice questions and the audience can vote. The number of votes can be seen real-time (in this phase, noone can see the ratio of answers so that it does not influence the voters) and after the presenter chooses so, the number of votes can be seen for the individual answers.

Votes are collected by a REST API of a self-hosted PHP server on a publicly accessible web server. The presentation polls the PHP server for results. Audience smartphones vote on the current question via a simple webpage served by the PHP server. The URL of the server is shown to the audience via a QR code. Everytime the presenter proceeds to a new question, the vote counters are reset.

Functions of the server:
- Serve the voting webpage for the audience. This is a single HTML page with embedded javascript.
- Reset the vote counters, receive title of the next question. Called when the presenter proceeds to a next question. Parallel questions do not need to be supported. No need to support parallel presentations. Before resetting the vote counters, the server saves the previous counter values with the title of the previous question into a CSV file (with timestamp) for backup.
- Serve REST API endpoints for voting and retrieving vote results.
- The PHP server is publicly accessible, so no tunneling is needed.

Functions of the presentation, implemented in javascript inside the presentations template.
- Display a QR code containing the URL of the PHP voting server in a presentation slide (the URL is configured in the presentation HTML).
- Notify the PHP server about a new test question when entering a new question slide. The title of the question slide is sent as the title of the question. (If the slide does not have a title, the server receives an "untitled question" title.)
- In the question slide template, first only the number of total votes is displayed. After a hotkey is pressed or a small icon is clicked, the counter of the A-B-C-D answers are shown. This is a small dedicated control inside the slides which can be reused in all slides.

# Implementation details

## Technical Stack & Libraries

1. **Server Backend**: PHP (hosted on publicly accessible web server)
   - Answer: PHP with minimal dependencies

2. **Tunneling Service**: Not needed - PHP server is directly accessible
   - Answer: N/A - using self-hosted public server

3. **QR Code Generation**: QR code is generated client-side or displayed statically
   - Answer: Use client-side JavaScript library (qrcodejs) or pre-generated QR code

4. **Reveal.js**: Should I use a specific version or template? Should I download it locally or use CDN?
   - Answer: use CDN

## Functionality Details

5. **Voting Page UI**: Any styling preferences? (Minimal/modern/specific color scheme?)
   - Answer: use minimal design which light background

6. **Polling Frequency**: How often should the presentation poll for vote updates? (1 second, 2 seconds?)
   - Answer: 1 second

7. **Results Reveal**: What hotkey should trigger showing individual answer counts? (Space, R, specific key?)
   - Answer: D as "details"

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

10. **Server URL Configuration**: The PHP server URL should be configurable in the presentation HTML
    - Answer: Set as a JavaScript variable in the presentation file

11. **CSV Format**: Should the CSV include: timestamp, question title, A/B/C/D counts, total votes? Any other columns?
    - Answer: This is fine, no further columns needed.

12. **Security**: Do you need any authentication/rate limiting for votes to prevent spam?
    - Answer: Yes, add configurable limit, the server should stop receiving votes after a certain threshold (e.g., 500 votes).

13. **Starting the System**: Should there be a startup script, or should users manually open the presentation?
    - Answer: A batch file can be provided to open the browser with the presentation.

# Implementation plan

## Phase 1: PHP Server Backend

### 1.1 Project Structure
Create the following files on the web server:
- `api.php` - Main REST API handler
- `index.php` - Voting webpage for audience
- `votes.csv` - CSV file for storing vote history (auto-created)
- Local files:
  - `sweep_questions.html` or similar - Reveal.js presentation
  - `start.bat` - Startup script for Windows (optional, opens browser)

### 1.2 Server Core Functionality
- PHP REST API with simple routing
- Vote storage with file-based or session-based counters (A, B, C, D)
- Track current question title and total vote count
- Add vote limit enforcement (stop accepting after max reached)

### 1.3 No Tunneling Needed
- PHP server is hosted on publicly accessible web server
- No tunnel setup or teardown required
- Server URL is fixed and configured in presentation

### 1.4 REST API Endpoints
- `GET /` or `GET /index.php` - Serve the voting page (HTML)
- `POST /api.php?action=vote` - Submit a vote (A/B/C/D), returns success/error
- `GET /api.php?action=results` - Get current vote counts (JSON: total, A, B, C, D)
- `POST /api.php?action=new-question` - Reset votes, save to CSV, set new question title
- `GET /api.php?action=status` - Check if voting is open (not at max limit)

### 1.5 CSV Logging
- Format: `timestamp, question_title, votes_A, votes_B, votes_C, votes_D, total_votes`
- Append to `votes.csv` when new question starts (saves previous question data)
- Use ISO timestamp format
- Ensure proper file permissions for PHP to write

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
- Create presentation HTML file (e.g., `sweep_questions.html`) with Reveal.js CDN links
- Include custom JavaScript for voting integration
- Configure PHP server URL in JavaScript variable
- Add example slides including:
  - Title slide
  - Content slides
  - QR code slide
  - Multiple question slides

### 3.2 QR Code Slide
- Dedicated slide that displays QR code
- QR code points to the PHP server URL (e.g., `http://avalon.aut.bme.hu/~kristof/vote`)
- Generate QR code client-side using qrcodejs library
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
  - POST to PHP server `/api.php?action=new-question` with title
  - Start polling `/api.php?action=results` every 1 second
- When leaving question slide:
  - Stop polling
- Handle 'D' key press (globally or per-slide):
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
- Open default browser to the presentation HTML file
- Display instructions to presenter
- (No server startup needed - PHP server is already running)

### 4.2 Documentation
- Create `README.md` with:
  - Prerequisites (modern web browser, PHP server access)
  - Installation instructions (upload PHP files to server)
  - How to configure the server URL in presentation
  - How to start the presentation
  - How to use in presentation
  - Troubleshooting common issues

### 4.3 Testing Checklist
- PHP server is accessible from public internet
- QR code displays in presentation with correct URL
- Mobile devices can access voting page via QR code URL
- Votes register correctly
- Vote limit enforcement works
- CSV logging captures data correctly on server
- Polling updates vote display in real-time
- 'D' key toggles detailed view
- Multiple question slides work sequentially
- CORS headers allow cross-origin requests from presentation

## Phase 5: Polish & Deployment

### 5.1 Error Handling
- Handle PHP server connection failures gracefully in presentation
- Validate vote inputs (only A/B/C/D accepted)
- Handle network errors in polling
- Add try-catch blocks for file operations in PHP
- Proper CORS headers for cross-origin requests

### 5.2 UI/UX Improvements
- Add CSS animations for vote updates
- Improve mobile responsiveness of voting page
- Add visual feedback for button clicks
- Style the presentation consistently

### 5.3 Configuration File (Optional)
- Create `config.php` for server-side settings
- Make server URL easily configurable in presentation HTML

## Implementation Order

1. **Start with api.php** - Core PHP REST API with endpoints
2. **Add voting page (index.php)** - Test voting locally and remotely
3. **Implement CSV logging** - Verify data saves correctly on server
4. **Test server accessibility** - Ensure public access works
5. **Create presentation HTML** - Basic Reveal.js setup with configured server URL
6. **Add voting JavaScript** - Integration with PHP server
7. **Create start.bat** - Browser launch script (optional)
8. **Testing and refinement** - Full end-to-end testing
9. **Documentation** - README.md

