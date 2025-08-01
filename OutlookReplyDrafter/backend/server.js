// --- backend/server.js ---
const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const path = require("path");
const { OpenAI } = require("openai");
require("dotenv").config();

const app = express();
app.use(bodyParser.json());

// Enable CORS for Outlook add-in and VBA macros
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*'); // Allow all origins for local development
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
  if (req.method === 'OPTIONS') {
    res.sendStatus(200);
  } else {
    next();
  }
});

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

function loadContextFiles() {
  const workflow = fs.readFileSync(path.join(__dirname, "context", "workflows.md"), "utf-8");
  const customer = fs.readFileSync(path.join(__dirname, "context", "customer-info.md"), "utf-8");
  return `# Workflow Info\n${workflow}\n\n# Customer Info\n${customer}`;
}

app.post("/analyze-email", async (req, res) => {
  const { subject, sender, body } = req.body;
  const context = loadContextFiles();

  const prompt = `${context}\n\nEmail from ${sender}:
Subject: ${subject}

Body:
${body}

Classify the email as one of:
- NO_ACTION
- EASY_REPLY
- TASK_REQUIRED

If EASY_REPLY, suggest a reply draft.
If TASK_REQUIRED, describe actions and suggest a reply.`;

  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [{ role: "user", content: prompt }],
    });
    res.json({ response: completion.choices[0].message.content });
  } catch (error) {
    console.error('OpenAI API Error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.post("/compose-email", async (req, res) => {
  const { draft } = req.body;
  const context = loadContextFiles();

  const prompt = `${context}\n\nYou are helping write a professional email. Improve or rewrite the following draft:\n\n${draft}`;

  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [{ role: "user", content: prompt }],
    });
    res.json({ response: completion.choices[0].message.content });
  } catch (error) {
    console.error('OpenAI API Error:', error);
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`API running on http://localhost:${PORT}`));
