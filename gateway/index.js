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
  const { message } = req.body;

  const response = await client.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1000,
    messages: [{ role: 'user', content: message }]
  });

  res.json({ reply: response.content[0].text });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Gateway running on http://localhost:${PORT}`);
});