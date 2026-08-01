<?php
/**
 * Presentation Voting API
 *
 * Single-file REST API replacing the Node.js/localtunnel server.
 * State is persisted in data/state.json (with file locking).
 * Vote history is appended to data/votes.csv on each new-question call.
 *
 * Endpoints (all via query param ?action=...):
 *   GET  ?action=status       - Current question, voting_open flag, counts
 *   GET  ?action=results      - Full vote counts (total + A/B/C/D)
 *   POST ?action=vote         - Submit a vote; body: {"vote":"A"}
 *   POST ?action=new-question - Reset counters, save CSV; body: {"title":"..."}
 */

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

define('STATE_FILE', __DIR__ . '/data/state.json');
define('CSV_FILE',   __DIR__ . '/data/votes.csv');
define('MAX_VOTES',  500);

// ---------------------------------------------------------------------------
// CORS – allow any origin so presentation.html works from file:// or localhost
// ---------------------------------------------------------------------------

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

// ---------------------------------------------------------------------------
// Error handlers – ensures any PHP error is returned as JSON, not empty 500
// ---------------------------------------------------------------------------

set_error_handler(function ($errno, $errstr, $errfile, $errline) {
    http_response_code(500);
    echo json_encode(['success' => false,
        'error' => "PHP error ($errno): $errstr in $errfile:$errline"]);
    exit;
});

register_shutdown_function(function () {
    $e = error_get_last();
    if ($e && in_array($e['type'], [E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR], true)) {
        http_response_code(500);
        echo json_encode(['success' => false,
            'error' => "PHP fatal: {$e['message']} in {$e['file']}:{$e['line']}"]);
    }
});

/**
 * Return a default empty state array.
 */
function defaultState() {
    return [
        'question'    => 'Waiting for first question...',
        'A'           => 0,
        'B'           => 0,
        'C'           => 0,
        'D'           => 0,
        'total'       => 0,
        'max_votes'   => MAX_VOTES,
        'voting_open' => true,
    ];
}

/**
 * Read state from JSON file. Returns default state if file missing/corrupt.
 * $fp must be an already-opened, flock()ed file handle.
 */
function readState($fp) {
    rewind($fp);
    $raw = stream_get_contents($fp);
    if ($raw === false || $raw === '') {
        return defaultState();
    }
    $data = json_decode($raw, true);
    if (!is_array($data)) {
        return defaultState();
    }
    return $data;
}

/**
 * Write state back to the file handle (truncate + write).
 */
function writeState($fp, $state) {
    rewind($fp);
    ftruncate($fp, 0);
    fwrite($fp, json_encode($state, JSON_PRETTY_PRINT));
    // Flush userspace buffer to the OS before releasing the lock,
    // so concurrent readers always see the updated data.
    fflush($fp);
}

/**
 * Open the state file for reading+writing, acquiring an exclusive lock.
 * Creates the file (and its directory) if necessary.
 * Returns the file handle, or exits with a 500 error on failure.
 */
function openStateLocked() {
    $dir = dirname(STATE_FILE);
    if (!is_dir($dir)) {
        $made = mkdir($dir, 0775, true);
        if (!$made && !is_dir($dir)) {
            jsonError(500, 'Cannot create data directory "' . $dir . '". ' .
                'Create it manually on the server and make it writable by the web server process.');
        }
    }
    // Suppress the PHP warning so we can report it ourselves
    $fp = @fopen(STATE_FILE, 'c+');
    if ($fp === false) {
        $err = error_get_last();
        $reason = $err ? $err['message'] : 'unknown reason';
        jsonError(500, 'Cannot open state file "' . STATE_FILE . '": ' . $reason . '. ' .
            'Make the data/ directory writable by the web server process (e.g. chmod 775 data/).');
    }
    if (!flock($fp, LOCK_EX)) {
        fclose($fp);
        jsonError(500, 'Cannot lock state file.');
    }
    return $fp;
}

// ---------------------------------------------------------------------------
// Helpers: CSV logging
// ---------------------------------------------------------------------------

function appendToCsv($state) {
    $needHeader = !file_exists(CSV_FILE) || filesize(CSV_FILE) === 0;
    $fp = fopen(CSV_FILE, 'a');
    if ($fp === false) {
        return; // Non-fatal – log failure silently
    }
    flock($fp, LOCK_EX);
    if ($needHeader) {
        fputcsv($fp, ['timestamp', 'question_title', 'votes_A', 'votes_B', 'votes_C', 'votes_D', 'total_votes']);
    }
    fputcsv($fp, [
        date('c'),
        $state['question'],
        $state['A'],
        $state['B'],
        $state['C'],
        $state['D'],
        $state['total'],
    ]);
    flock($fp, LOCK_UN);
    fclose($fp);
}

// ---------------------------------------------------------------------------
// Helpers: HTTP responses
// ---------------------------------------------------------------------------

function jsonResponse($data, $code = 200) {
    http_response_code($code);
    echo json_encode($data);
    exit;
}

function jsonError($code, $message) {
    http_response_code($code);
    echo json_encode(['success' => false, 'error' => $message]);
    exit;
}

function getRequestBody() {
    $raw = file_get_contents('php://input');
    if (!$raw) {
        return [];
    }
    $data = json_decode($raw, true);
    return is_array($data) ? $data : [];
}

// ---------------------------------------------------------------------------
// Routing
// ---------------------------------------------------------------------------

$action = isset($_GET['action']) ? $_GET['action'] : '';
$method = $_SERVER['REQUEST_METHOD'];

switch ($action) {

    // -----------------------------------------------------------------------
    // GET ?action=status
    // -----------------------------------------------------------------------
    case 'status':
        if ($method !== 'GET') {
            jsonError(405, 'Method not allowed.');
        }
        $fp    = openStateLocked();
        $state = readState($fp);
        flock($fp, LOCK_UN);
        fclose($fp);

        jsonResponse([
            'question'    => $state['question'],
            'voting_open' => $state['voting_open'],
            'total_votes' => $state['total'],
            'max_votes'   => $state['max_votes'],
        ]);
        break;

    // -----------------------------------------------------------------------
    // GET ?action=results
    // -----------------------------------------------------------------------
    case 'results':
        if ($method !== 'GET') {
            jsonError(405, 'Method not allowed.');
        }
        $fp    = openStateLocked();
        $state = readState($fp);
        flock($fp, LOCK_UN);
        fclose($fp);

        jsonResponse([
            'total'       => $state['total'],
            'A'           => $state['A'],
            'B'           => $state['B'],
            'C'           => $state['C'],
            'D'           => $state['D'],
            'question'    => $state['question'],
            'voting_open' => $state['voting_open'],
        ]);
        break;

    // -----------------------------------------------------------------------
    // POST ?action=vote
    // Body: {"vote": "A"}   (A / B / C / D)
    // -----------------------------------------------------------------------
    case 'vote':
        if ($method !== 'POST') {
            jsonError(405, 'Method not allowed.');
        }
        $body = getRequestBody();
        $vote = isset($body['vote']) ? strtoupper(trim($body['vote'])) : '';

        if (!in_array($vote, ['A', 'B', 'C', 'D'], true)) {
            jsonError(400, 'Invalid vote. Must be A, B, C, or D.');
        }

        $fp    = openStateLocked();
        $state = readState($fp);

        if ($state['total'] >= $state['max_votes']) {
            flock($fp, LOCK_UN);
            fclose($fp);
            jsonResponse(['success' => false, 'error' => 'Vote limit reached for this question.']);
        }

        $state[$vote]++;
        $state['total']++;
        $state['voting_open'] = ($state['total'] < $state['max_votes']);

        writeState($fp, $state);
        flock($fp, LOCK_UN);
        fclose($fp);

        jsonResponse(['success' => true, 'total' => $state['total']]);
        break;

    // -----------------------------------------------------------------------
    // POST ?action=new-question
    // Body: {"title": "Question title"}
    // -----------------------------------------------------------------------
    case 'new-question':
        if ($method !== 'POST') {
            jsonError(405, 'Method not allowed.');
        }
        $body  = getRequestBody();
        $title = isset($body['title']) ? trim($body['title']) : 'Untitled question';

        $fp    = openStateLocked();
        $state = readState($fp);

        // Save previous question results to CSV (if there were any votes)
        if ($state['total'] > 0) {
            appendToCsv($state);
        }

        // Reset for the new question
        $state['question']    = $title;
        $state['A']           = 0;
        $state['B']           = 0;
        $state['C']           = 0;
        $state['D']           = 0;
        $state['total']       = 0;
        $state['voting_open'] = true;

        writeState($fp, $state);
        flock($fp, LOCK_UN);
        fclose($fp);

        jsonResponse(['success' => true, 'question' => $title]);
        break;

    // -----------------------------------------------------------------------
    // Unknown action
    // -----------------------------------------------------------------------
    default:
        jsonError(404, 'Unknown action. Valid actions: status, results, vote, new-question.');
}
