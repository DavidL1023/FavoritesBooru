import express from 'express';
const app = express();
const PORT = 3000;

import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Open website on port 3000
app.use(express.static(__dirname));
app.get('/', function(req, res) {
  res.sendFile(__dirname + '/index.html');
});

import open, {openApp, apps} from 'open';
await open('http://localhost:3000');

// API
app.get('/runPython', (req, res) => {
  res.status(200).send('wow!')
});

// Running server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
