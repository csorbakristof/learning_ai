# AI-Powered VBA Macro Setup Guide

## Overview
This guide sets up VBA macros that connect to the same backend server as the outlook-addin, providing AI-powered email analysis and composition assistance directly in Outlook.

## Prerequisites

### 1. Backend Server Setup
First, ensure your backend server is running:

```powershell
# Navigate to backend folder
cd "e:\_learning_ai\OutlookReplyDrafter\backend"

# Install dependencies (if not already done)
npm install

# Start the server
npm start
```

The server should be running on `http://localhost:5000`

### 2. OpenAI API Key
Ensure you have a `.env` file in the backend folder with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Outlook VBA Setup
1. **Enable macros** in Outlook Trust Center
2. **Enable Microsoft XML, v6.0 reference** (for HTTP requests):
   - In VBA Editor: Tools → References
   - Check "Microsoft XML, v6.0"
   - Click OK

## Installation Steps

### Step 1: Add the AI Macro Code
1. **Open Outlook** and press **Alt+F11** (VBA Editor)
2. **Right-click** on "Project1 (VbaProject.OTM)" → **Insert → Module**
3. **Copy the entire content** of `AIPoweredMacros.vba`
4. **Paste** into the new module
5. **Save** (Ctrl+S) and **close VBA Editor**

### Step 2: Add Macros to Ribbon
1. **File → Options → Customize Ribbon**
2. **"Choose commands from"** → **"Macros"**
3. **Add these macros** to your ribbon:
   - `AnalyzeEmailWithAI`
   - `ComposeEmailWithAI` 
   - `GenerateSmartReply`
   - `TestBackendConnection`

### Step 3: Test the Setup
1. **Click "TestBackendConnection"** button
2. **Should show:** "✅ Backend server is running"
3. **If error:** Check backend server is running on port 5000

## Available AI Features

### 🤖 **Analyze Email with AI**
- **Select an email** in your inbox
- **Click "AnalyzeEmailWithAI"** button  
- **AI analyzes** the email and categorizes it as:
  - NO_ACTION
  - EASY_REPLY  
  - TASK_REQUIRED
- **Auto-categorizes** and flags emails based on analysis

### ✍️ **Compose Email with AI**
- **Click "ComposeEmailWithAI"** button
- **Enter initial draft** or use the template
- **AI improves** your draft for clarity and professionalism
- **New email opens** with AI-enhanced content

### 💬 **Generate Smart Reply**
- **Select an email** to reply to
- **Click "GenerateSmartReply"** button
- **AI analyzes** the email and generates appropriate reply
- **Reply window opens** with AI-suggested content

## How It Works

### Backend Integration
- **Same backend** as the outlook-addin (port 5000)
- **Same AI models** and context files
- **HTTP requests** from VBA to Node.js backend
- **JSON communication** between VBA and server

### AI Processing Flow
1. **VBA extracts** email content (subject, sender, body)
2. **Sends HTTP POST** to backend `/analyze-email` or `/compose-email`
3. **Backend processes** with OpenAI GPT-4
4. **Returns AI response** as JSON
5. **VBA displays** results or creates new email

## Troubleshooting

### ❌ "Cannot connect to backend server"
**Solutions:**
- Check backend server is running: `npm start` in backend folder
- Verify server URL: should be `http://localhost:5000`
- Check firewall/antivirus blocking port 5000
- Try running Outlook as Administrator

### ❌ "HTTP request failed"
**Solutions:**
- Enable Microsoft XML reference in VBA (Tools → References)
- Check Windows proxy settings
- Verify JSON payload format
- Check backend server logs for errors

### ❌ "OpenAI API Error"
**Solutions:**
- Verify OpenAI API key in backend `.env` file
- Check OpenAI account has credits/usage allowance
- Verify internet connection
- Check backend server logs for specific error

### ❌ "Macro security warnings"
**Solutions:**
- Enable macros: File → Options → Trust Center → Macro Settings
- Add VBA project to trusted locations
- Consider digitally signing macros for enterprise use

## Advanced Configuration

### Customize Backend URL
If your backend runs on a different port, update the constant in VBA:
```vb
Const BACKEND_URL As String = "http://localhost:YOUR_PORT"
```

### Add More AI Features
You can extend the macros to use additional backend endpoints:
- Add new API endpoints in `server.js`
- Create corresponding VBA functions
- Add new ribbon buttons for new features

### Context Files Integration
The backend automatically loads context from:
- `backend/context/workflows.md`
- `backend/context/customer-info.md`

Modify these files to customize AI behavior for your specific needs.

## Security Considerations

- **VBA macros** have full system access
- **Backend server** runs locally (port 5000)
- **OpenAI API** sends email content to external service
- **Consider data privacy** when processing sensitive emails
- **Use HTTPS** in production environments

## Comparison: VBA vs Web Add-in

| Feature | VBA Macros | Web Add-in |
|---------|------------|------------|
| **Domain Policy** | ✅ Usually allowed | ❌ Often blocked |
| **AI Backend** | ✅ Full access | ✅ Full access |
| **Setup** | ✅ Copy/paste code | ❌ Complex sideloading |
| **Performance** | ✅ Native | ⚠️ Web overhead |
| **Customization** | ✅ Full VBA power | ⚠️ Limited to web APIs |

## Next Steps

1. **Test basic functionality** with simple emails
2. **Customize context files** for your specific workflow  
3. **Add more AI features** as needed
4. **Consider automation** (e.g., auto-analyze incoming emails)
5. **Share with team** by exporting VBA modules

The VBA approach gives you all the AI power of the web add-in while bypassing domain restrictions!
