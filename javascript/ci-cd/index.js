const express = require('express');
const app = express();
const PORT = 3001;

// Middleware to parse JSON
app.use(express.json());

// In-memory "database"
let items = [
  { id: 1, name: "Item 1" },
  { id: 2, name: "Item 2" },
  { id: 3, name: "Item 3" },
  { id: 4, name: "Item 4" },
  { id: 5, name: "Item 5" },
  { id: 6, name: "Item 6" }
];

// GET all items
app.get('/api/items', (req, res) => {
  res.json(items);
});

// POST new item
app.post('/api/items', (req, res) => {
  const newItem = {
    id: items.length + 1,
    name: req.body.name
  };
  items.push(newItem);
  res.status(201).json(newItem);
});

// PUT update item
app.put('/api/items/:id', (req, res) => {
  const itemId = parseInt(req.params.id);
  const item = items.find(i => i.id === itemId);

  if (!item) {
    return res.status(404).json({ message: 'Item not found' });
  }

  item.name = req.body.name;
  res.json(item);
});

// DELETE item
app.delete('/api/items/:id', (req, res) => {
  const itemId = parseInt(req.params.id);
  items = items.filter(i => i.id !== itemId);
  res.json({ message: 'Item deleted successfully' });
});

// Default route
app.get('/', (req, res) => {
  res.send('Hello from Simple Node.js Server with CRUD API!');
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running at http://localhost:${PORT}`);
});
