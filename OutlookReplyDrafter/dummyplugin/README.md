# Dummy Outlook Plugin

A minimal Outlook add-in that adds a button to compose a "Hello World!" email.

## Features

- Adds a button to Outlook's compose window
- When clicked, drafts an email with subject "Hello World from Dummy Plugin" and body "Hello world!"
- Does not send the email automatically - just drafts it

## Setup Instructions

1. **Install dependencies:**
   ```powershell
   cd dummyplugin
   npm install
   ```

2. **Start the local server:**
   ```powershell
   npm start
   ```
   This will start a server on http://localhost:3001

3. **Install the add-in in Outlook Desktop:**
   - Open Outlook Desktop
   - Go to File > Options > Trust Center > Trust Center Settings > Add-ins
   - Click "Manage Add-ins" (opens browser)
   - Click "Upload Custom Add-in" > "Add from file..."
   - Select the `manifest.xml` file from this folder
   - Restart Outlook

4. **Test the plugin:**
   - Create a new email in Outlook
   - You should see the "Dummy Hello World Plugin" panel on the right
   - Click "Draft Hello World Email" button
   - The email subject and body will be populated with "Hello World" content

## Files

- `manifest.xml` - Outlook add-in manifest file
- `compose.html` - HTML interface for the plugin
- `compose.js` - JavaScript functionality
- `package.json` - Node.js dependencies and scripts

## Notes

- The plugin only works in compose mode (when creating new emails)
- Requires an active internet connection for Office.js library
- Runs on port 3001 to avoid conflicts with the main project (port 3000)
