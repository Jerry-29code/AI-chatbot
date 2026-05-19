const express = require('express');
const dotenv = require('dotenv');

dotenv.config({ path: '../.env' });

const app = express();
app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Gateway is running' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Gateway running on http://localhost:${PORT}`);
});