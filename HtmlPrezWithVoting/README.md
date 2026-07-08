# Presentation Voting System

Interactive Reveal.js presentation with live audience voting backed by a small PHP API.

## Status

The current implementation is based on:

- `sweep_questions.html` for the presentation content
- `voting-system.js` for Reveal.js integration and polling
- `php-server/` for the audience voting page and JSON API

This README documents that PHP-based setup. Older Node.js and `start.bat` instructions are no longer applicable.

## Project Structure

```text
HtmlPrezWithVoting/
├── sweep_questions.html      # Reveal.js presentation
├── presentation.css          # Presentation and vote display styling
├── voting-system.js          # Voting integration, polling, QR overlay, keyboard shortcuts
├── php-server/
│   ├── index.php             # Audience voting page
│   ├── api.php               # Voting API
│   └── data/
│       ├── state.json        # Current vote state (created/updated at runtime)
│       └── votes.csv         # Vote history log
├── TESTING.md                # Test notes
├── questions.md              # Question source material
├── spec.md                   # Specification
└── README.md                 # This file
```

## System Requirements

- PHP 7.4+ or PHP 8.x with a web server, or PHP's built-in development server for local testing
- A writable `php-server/data/` directory on the host running PHP
- A modern browser for the presentation and for audience devices
- Internet access while presenting if you rely on CDN-hosted Reveal.js and `qrcodejs`

Node.js, npm, Express, and localtunnel are not required by the current version.

## What The System Does

- Displays a Reveal.js slide deck with question slides
- Resets vote counts automatically when the presenter enters a new question slide
- Polls the PHP API once per second for live results
- Shows a floating vote panel on question slides
- Lets the presenter toggle detailed counts with `D`
- Lets the presenter toggle a large QR overlay with `Q`
- Generates QR codes client-side from the configured voting URL
- Saves completed question results into `php-server/data/votes.csv`

## Architecture

### Presentation side

- `sweep_questions.html` loads Reveal.js from CDN
- `window.PHP_SERVER_URL` defines the base URL of the deployed PHP voting server
- `voting-system.js` calls:
  - `GET {PHP_SERVER_URL}/api.php?action=results`
  - `POST {PHP_SERVER_URL}/api.php?action=new-question`
- The presentation can be opened from a local file or another host because `api.php` sends permissive CORS headers

### Audience side

- Audience members open the PHP server URL itself, which serves `php-server/index.php`
- That page polls `api.php?action=status` every 2 seconds
- Votes are submitted to `api.php?action=vote`
- A `localStorage` key prevents repeat voting for the same question in the same browser

### Persistence

- Current counters are stored in `php-server/data/state.json`
- Finished question results are appended to `php-server/data/votes.csv`
- Writes use file locking in `api.php` to reduce concurrent write issues

## Configuration

Set the voting backend URL in `sweep_questions.html`:

```html
<script>
    window.PHP_SERVER_URL = 'https://example.com/vote';
</script>
```

This URL must point to the directory that contains both `index.php` and `api.php`.

Example:

- If the deployed audience page is `https://example.com/vote/index.php`
- Then `window.PHP_SERVER_URL` should be `https://example.com/vote`

## Running Locally

### Option 1: Local PHP backend + local presentation file

1. Start the PHP server from `php-server/`:

```bash
php -S localhost:8080
```

2. In `sweep_questions.html`, set:

```html
<script>
    window.PHP_SERVER_URL = 'http://localhost:8080';
</script>
```

3. Open `sweep_questions.html` in a browser.

4. Open `http://localhost:8080/` on a phone or a second browser window to vote.

### Option 2: Deploy the PHP backend remotely

1. Upload the contents of `php-server/` to a PHP-capable web host.
2. Make sure the `data/` directory is writable by the web server process.
3. Set `window.PHP_SERVER_URL` in `sweep_questions.html` to that deployed URL.
4. Open `sweep_questions.html` locally or host it on any static server.

## Presentation Behavior

Question slides are recognized by the `data-question-slide="true"` attribute.

When the presenter lands on a question slide:

1. The floating vote display is shown.
2. Counts are reset visually to zero.
3. The presentation sends `new-question` to the backend using the slide title.
4. Polling starts and live results begin updating.

When the presenter leaves a question slide:

1. Polling stops.
2. The floating vote display is hidden.

Detailed vote counts are shown with `D`. When details are visible, the answer matching `data-correct-answer` is highlighted.

## Keyboard Shortcuts

- `D` toggles the detailed vote breakdown on question slides
- `Q` toggles a full-screen QR code overlay on any slide
- Standard Reveal.js shortcuts still apply for navigation, fullscreen, overview, and speaker tools

## Question Slide Markup

Example:

```html
<section
    class="question-slide"
    data-question-slide="true"
    data-question-title="Your question title"
    data-correct-answer="B">
    <h2>Your question?</h2>
    <ul>
        <li><strong>A)</strong> Option A</li>
        <li><strong>B)</strong> Option B</li>
        <li><strong>C)</strong> Option C</li>
        <li><strong>D)</strong> Option D</li>
    </ul>
</section>
```

Notes:

- `data-question-slide="true"` marks the slide as vote-enabled
- `data-question-title` overrides the title stored in the backend
- If `data-question-title` is missing, the first `h2` text is used
- `data-correct-answer` can be `A`, `B`, `C`, or `D`
- The vote display is injected automatically by JavaScript; do not copy it into every slide

## API Reference

The backend is routed through `php-server/api.php?action=...`.

### `GET ?action=status`

Returns a compact status object for the audience page.

Example response:

```json
{
  "question": "Current question",
  "voting_open": true,
  "total_votes": 12,
  "max_votes": 500
}
```

### `GET ?action=results`

Returns full counts for the presentation overlay.

Example response:

```json
{
  "total": 12,
  "A": 3,
  "B": 4,
  "C": 2,
  "D": 3,
  "question": "Current question",
  "voting_open": true
}
```

### `POST ?action=vote`

Body:

```json
{ "vote": "A" }
```

Successful response:

```json
{ "success": true, "total": 13 }
```

### `POST ?action=new-question`

Body:

```json
{ "title": "Question title" }
```

Successful response:

```json
{ "success": true, "question": "Question title" }
```

## Vote Limits and Storage

- `api.php` currently uses `MAX_VOTES = 500`
- Once the total reaches that limit, `voting_open` becomes `false`
- On each `new-question` call, the previous question is appended to `votes.csv` if it received any votes
- The current question is not appended to CSV until the next question begins

## Troubleshooting

### QR code or voting URL is wrong

- Check `window.PHP_SERVER_URL` in `sweep_questions.html`
- It must point to the PHP server directory, not directly to `api.php`

### Votes are not being saved

- Verify that `php-server/data/` exists
- Verify that the PHP process can write to `php-server/data/state.json` and `php-server/data/votes.csv`

### Presentation loads but live counts do not update

- Open browser developer tools and check failed requests to `api.php`
- Confirm the configured `PHP_SERVER_URL` is reachable from the presentation machine
- Confirm the PHP host allows `GET`, `POST`, and `OPTIONS`

### The audience page says the user already voted

- The audience page stores the last-voted question in `localStorage`
- Test with a private browsing window or clear site storage for the voting page

### The QR code overlay shows a placeholder or error

- The configured URL may still contain a placeholder value
- The QR code library is loaded from CDN, so offline environments may block generation unless assets are cached or vendored locally

## Customization

- Edit `sweep_questions.html` to change slides and question metadata
- Edit `presentation.css` to change styling
- Edit `voting-system.js` to change polling, keyboard behavior, or overlay behavior
- Edit `php-server/index.php` to change the audience voting page
- Edit `php-server/api.php` to change API behavior, vote limits, or storage format

## Development Notes

- The current implementation uses client-side QR generation through `qrcodejs`
- The `D` key is intentionally used instead of `V`
- The vote display is global and fixed-position, not embedded inside each question slide

## References

- Reveal.js: https://revealjs.com/
- PHP manual: https://www.php.net/docs.php
