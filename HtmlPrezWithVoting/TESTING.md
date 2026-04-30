# Testing Guide - Presentation Voting System

This document provides a comprehensive testing checklist and procedures for the Presentation Voting System.

## Prerequisites for Testing

- Node.js installed
- Internet connection (for localtunnel)
- Two devices recommended:
  - One for presenting (laptop/desktop)
  - One for voting (smartphone/tablet)
- Modern web browser (Chrome, Firefox, Edge, Safari)

## Quick Test (5 minutes)

1. **Start the system**:
   ```bash
   ./start.bat  # Windows
   # or
   node server.js  # Manual start
   ```

2. **Verify server startup**:
   - [ ] Server console shows "Server starting..."
   - [ ] Port 8000 is used (or custom port if specified)
   - [ ] Localtunnel URL is displayed
   - [ ] No error messages

3. **Test presentation**:
   - [ ] Browser opens automatically (if using start.bat)
   - [ ] Presentation loads at http://localhost:8000/presentation.html
   - [ ] Navigate through slides with arrow keys
   - [ ] QR code displays on slide 2

4. **Test voting**:
   - [ ] Open http://localhost:8000/ in another browser/device
   - [ ] Question title displays
   - [ ] A/B/C/D buttons are clickable
   - [ ] Vote is recorded successfully

5. **Test real-time updates**:
   - [ ] Navigate to question slide in presentation
   - [ ] Submit vote from voting page
   - [ ] Total vote count updates within 1-2 seconds in presentation
   - [ ] Press 'V' key to show detailed breakdown
   - [ ] Correct answer is highlighted in green with checkmark (✓)
   - [ ] "Correct Answer: [letter]" indicator appears at bottom

## Complete Testing Checklist

### Phase 1: Server Backend Tests

#### 1.1 Server Startup
- [ ] Server starts without errors
- [ ] Port configuration works (`--port 3000`)
- [ ] Max votes configuration works (`--max-votes 100`)
- [ ] Localtunnel initializes and provides URL
- [ ] Console output is clear and informative

#### 1.2 REST API Endpoints

**GET /**
- [ ] Returns voting page HTML
- [ ] Page loads without errors
- [ ] Mobile-responsive design works

**POST /vote**
- [ ] Accepts valid votes (A, B, C, D)
- [ ] Rejects invalid votes (X, Y, Z, 1, 2)
- [ ] Returns success message for valid votes
- [ ] Returns error for invalid votes
- [ ] Enforces vote limit (stops at max_votes)
- [ ] Increments vote counters correctly

**GET /results**
- [ ] Returns JSON with current vote counts
- [ ] Includes total, A, B, C, D counts
- [ ] Includes current question title
- [ ] Includes voting_open status

**POST /new-question**
- [ ] Accepts new question title
- [ ] Saves previous question votes to CSV
- [ ] Resets vote counters to zero
- [ ] Updates current question title

**GET /qr-code**
- [ ] Generates QR code image (PNG)
- [ ] QR code contains correct tunnel URL
- [ ] Image displays properly in browsers

**GET /status**
- [ ] Returns current question
- [ ] Returns voting_open status
- [ ] Returns total_votes count
- [ ] Returns max_votes limit

#### 1.3 CSV Logging
- [ ] votes.csv file is created on first save
- [ ] CSV header row is correct
- [ ] Vote data is appended correctly
- [ ] Timestamp is in ISO format
- [ ] Question title is properly escaped (handles quotes)
- [ ] All vote counts (A, B, C, D) are saved
- [ ] Total votes is saved

#### 1.4 Vote Limiting
- [ ] Stops accepting votes at max_votes limit
- [ ] Returns appropriate error message when limit reached
- [ ] Voting page shows "limit reached" message
- [ ] Presentation shows voting_open status

#### 1.5 Graceful Shutdown
- [ ] Ctrl+C triggers shutdown handler
- [ ] Saves pending votes to CSV before exit
- [ ] Closes localtunnel connection
- [ ] Shows "Goodbye!" message
- [ ] Process exits cleanly

### Phase 2: Presentation Tests

#### 2.1 Reveal.js Integration
- [ ] Presentation loads from CDN
- [ ] Slides render correctly
- [ ] Navigation works (arrow keys, space)
- [ ] Slide transitions are smooth
- [ ] Slide numbers display

#### 2.2 QR Code Slide
- [ ] QR code image loads
- [ ] QR code is scannable with smartphone
- [ ] Scanning opens voting page
- [ ] Instructions are clear

#### 2.3 Question Slides
- [ ] Question slides detected by data attribute
- [ ] Question title extracted correctly
- [ ] Custom titles (data-question-title) work
- [ ] Default titles (from h2) work
- [ ] Vote display component renders

#### 2.4 Vote Display Component
- [ ] Total votes show initially
- [ ] Total updates in real-time (every 1 second)
- [ ] Detailed votes hidden by default
- [ ] "Show Details" button works
- [ ] 'V' key toggles details
- [ ] Individual vote counts (A, B, C, D) display correctly
- [ ] Vote counts update in real-time

#### 2.5 Slide Navigation
- [ ] Entering question slide triggers new-question
- [ ] Vote counters reset to zero
- [ ] Previous votes saved to CSV
- [ ] Polling starts automatically
- [ ] Leaving question slide stops polling
- [ ] Multiple question slides work sequentially

#### 2.6 Keyboard Controls
- [ ] 'D' key works only on question slides
- [ ] Toggles detailed view correctly
- [ ] Correct answer is highlighted when showing details (green background + checkmark)
- [ ] Correct answer indicator appears at bottom of details
- [ ] Doesn't interfere with Reveal.js navigation
- [ ] Button and key press do the same action

### Phase 3: Integration Tests

#### 3.1 End-to-End Flow
1. [ ] Start server with start.bat
2. [ ] Browser opens to presentation
3. [ ] Navigate to QR code slide
4. [ ] Scan QR code with phone
5. [ ] Phone opens voting page
6. [ ] Navigate to question slide
7. [ ] Vote counters reset
8. [ ] Submit vote from phone
9. [ ] Vote appears in presentation within 1 second
10. [ ] Press 'V' to see breakdown
11. [ ] Navigate to next question
12. [ ] Previous votes saved to CSV
13. [ ] Counters reset for new question
14. [ ] Stop server with Ctrl+C
15. [ ] Final votes saved to CSV
16. [ ] Tunnel closes

#### 3.2 Multiple Voters
- [ ] Multiple devices can vote simultaneously
- [ ] Each device can only vote once per question (localStorage)
- [ ] Vote counts are accurate with multiple voters
- [ ] No race conditions or lost votes

#### 3.3 Edge Cases
- [ ] Empty question title handled
- [ ] Special characters in question title
- [ ] Very long question titles
- [ ] Rapid slide navigation
- [ ] Server restart (votes reset)
- [ ] Network interruption recovery

### Phase 4: Mobile Device Testing

#### 4.1 Mobile Voting Page
- [ ] Loads correctly on iOS Safari
- [ ] Loads correctly on Android Chrome
- [ ] Loads correctly on other mobile browsers
- [ ] Touch targets are large enough
- [ ] No horizontal scrolling needed
- [ ] Buttons easy to tap
- [ ] Text is readable

#### 4.2 Mobile Network
- [ ] Works over WiFi
- [ ] Works over cellular data
- [ ] Tunnel URL accessible from outside network
- [ ] No CORS errors

### Phase 5: Performance Tests

#### 5.1 Server Performance
- [ ] Handles 10 simultaneous voters
- [ ] Handles 50 simultaneous voters
- [ ] Handles 100+ simultaneous voters
- [ ] Response time < 100ms for /vote
- [ ] Response time < 50ms for /results
- [ ] No memory leaks over time

#### 5.2 Presentation Performance
- [ ] Polling doesn't slow down slides
- [ ] Vote updates are smooth
- [ ] No UI freezing or lag
- [ ] Works with 10+ question slides

### Phase 6: Browser Compatibility

#### 6.1 Desktop Browsers
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Edge (latest)
- [ ] Safari (latest)

#### 6.2 Mobile Browsers
- [ ] iOS Safari
- [ ] Android Chrome
- [ ] Firefox Mobile
- [ ] Samsung Internet

### Phase 7: Error Handling Tests

#### 7.1 Server Errors
- [ ] Invalid vote format handled gracefully
- [ ] Missing request body handled
- [ ] Localtunnel failure doesn't crash server
- [ ] File write errors logged appropriately
- [ ] Port already in use shows clear error

#### 7.2 Client Errors
- [ ] Server unreachable shows error message
- [ ] Network timeout handled gracefully
- [ ] Invalid JSON response handled
- [ ] QR code load failure shows placeholder

## Test Scenarios

### Scenario 1: Basic Presentation Flow

**Setup**: Start fresh server

**Steps**:
1. Start server
2. Open presentation
3. Navigate to question slide 1
4. Open voting page in new tab
5. Vote for option A
6. Verify vote shows in presentation
7. Press 'V' to see breakdown
8. Navigate to question slide 2
9. Vote for option C
10. Navigate to question slide 3
11. Vote for option B
12. Stop server

**Expected Results**:
- All votes recorded correctly
- votes.csv contains 3 rows of data
- Total votes for each question is 1

### Scenario 2: Multiple Voters

**Setup**: Start fresh server, prepare 3 devices

**Steps**:
1. Start server
2. Open presentation
3. Share tunnel URL with 3 test devices
4. Navigate to question slide
5. Have all 3 devices vote (different options)
6. Wait 2 seconds
7. Press 'V' to see breakdown

**Expected Results**:
- Total shows 3 votes
- Individual counts match votes (e.g., A:1, B:1, C:1, D:0)
- All votes registered within 2 seconds

### Scenario 3: Vote Limit Test

**Setup**: Start server with `--max-votes 5`

**Steps**:
1. Navigate to question slide
2. Submit 5 votes from different devices
3. Attempt 6th vote
4. Check presentation status

**Expected Results**:
- First 5 votes accepted
- 6th vote rejected with error message
- Voting page shows "limit reached"
- Total shows 5 votes

### Scenario 4: Quick Slide Navigation

**Setup**: Start fresh server

**Steps**:
1. Navigate to question 1 (wait 1 second)
2. Navigate to question 2 (wait 1 second)
3. Navigate to question 3 (wait 1 second)
4. Navigate back to question 1
5. Check votes.csv

**Expected Results**:
- All questions logged to CSV
- No duplicate entries
- Vote counts are zero for each

## Automated Testing Commands

Test REST API with curl:

```bash
# Test voting
curl -X POST http://localhost:8000/vote \
  -H "Content-Type: application/json" \
  -d '{"vote":"A"}'

# Test results
curl http://localhost:8000/results

# Test new question
curl -X POST http://localhost:8000/new-question \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Question"}'

# Test status
curl http://localhost:8000/status
```

## Known Limitations

1. **Single presentation**: Only one presentation can run at a time per server
2. **In-memory storage**: Vote counts reset on server restart
3. **LocalStorage limitation**: Users can vote again by clearing browser storage
4. **Tunnel stability**: Localtunnel may occasionally disconnect
5. **Network delay**: Vote updates have ~1 second delay

## Troubleshooting Test Issues

### Issue: QR Code doesn't load
- Wait 10 seconds for tunnel to initialize
- Check console for tunnel URL
- Try refreshing the page

### Issue: Votes not updating in presentation
- Check browser console for errors
- Verify polling is active (console log)
- Check server is responding (/results endpoint)

### Issue: Cannot vote multiple times for testing
- Clear browser localStorage
- Use incognito/private browsing mode
- Use different browsers/devices

### Issue: Server won't start
- Check port 8000 is not in use
- Verify Node.js is installed
- Check npm dependencies are installed

## Test Report Template

After testing, document results:

```
Test Date: [DATE]
Tester: [NAME]
Server Version: 1.0.0
Node.js Version: [VERSION]

✓ Passed: [NUMBER]
✗ Failed: [NUMBER]
⊘ Skipped: [NUMBER]

Failed Tests:
- [Test name]: [Reason]
- [Test name]: [Reason]

Notes:
- [Any observations]
- [Performance issues]
- [Suggestions]
```

## Continuous Testing

For ongoing development:

1. **Before each demo**: Run Quick Test (5 min)
2. **After code changes**: Run Complete Testing Checklist
3. **Before release**: Run all Test Scenarios
4. **Weekly**: Performance testing with 50+ voters

## Success Criteria

The system is ready for production use when:
- [ ] All Complete Testing Checklist items pass
- [ ] All Test Scenarios execute successfully
- [ ] No critical or high-severity bugs
- [ ] Performance meets requirements (100+ voters)
- [ ] Mobile devices work reliably
- [ ] Documentation is complete
