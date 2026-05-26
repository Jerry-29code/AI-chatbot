const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const express = require('express');
const dotenv = require('dotenv');
const Anthropic = require('@anthropic-ai/sdk');

dotenv.config({ path: '../.env' });

const app = express();
app.use(express.json());

const client = new Anthropic.default({ apiKey: process.env.ANTHROPIC_API_KEY });

app.get('/', (req, res) => {
  res.json({ message: 'Gateway is running' });
});

app.post('/chat', async (req, res) => {
  try {
    const { message } = req.body;

    // Step 1: Search for relevant chunks
    const searchRes = await fetch(`http://127.0.0.1:8000/search?q=${encodeURIComponent(message)}`);
    const searchData = await searchRes.json();
    const context = searchData.results.join('\n\n');

    // Step 2: Build grounded prompt
    const prompt = context.length > 0
      ? `You are a helpful assistant. Answer the question using ONLY the context below.\n\nContext:\n${context}\n\nQuestion: ${message}`
      : `You are a helpful assistant. Answer the following question: ${message}`;

    // Step 3: Call Claude
    const response = await client.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1000,
      messages: [{ role: 'user', content: prompt }]
    });

    res.json({ reply: response.content[0].text });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Gateway running on http://localhost:${PORT}`);
});