const express = require('express');
const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());

// Route
app.get('/', (req, res) => {
  res.send('Hello from Simple Node.js Server!');
});

// Start Server
app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});
