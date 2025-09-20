const express = require('express');
const path = require('path');

const app = express();
const PORT = 3001;  // 更改端口以避免冲突

// Serve static files from the 'frontend' directory
app.use(express.static(path.join(__dirname)));

// Serve index.html for all routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Frontend server is running at http://localhost:${PORT}`);
});