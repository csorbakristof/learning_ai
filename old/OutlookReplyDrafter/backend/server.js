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

  const prompt = `${context}\n\nEmail feladója: ${sender}
Tárgy: ${subject}

Tartalom:
${body}

Kategorizáld az emailt az alábbiak egyikeként:
- NINCS_TEENDŐ
- KÖNNYŰ_VÁLASZ
- FELADAT_SZÜKSÉGES

Ha KÖNNYŰ_VÁLASZ, javasolj egy válasz tervezetet.
Ha FELADAT_SZÜKSÉGES, írd le a szükséges intézkedéseket és javasolj egy választ.

FONTOS: Válaszolj teljes egészében magyar nyelven. Minden elemzés, javaslat és válasz magyar nyelvű legyen.`;

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

  const prompt = `${context}\n\nSegítesz egy professzionális email megírásában. Javítsd vagy írd át az alábbi tervezetet:\n\n${draft}\n\nFONTOS: Válaszolj teljes egészében magyar nyelven. A javított email magyar nyelvű legyen.`;

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
