import express from 'express';
const app = express();
const PORT = 3000;

import child_process from 'child_process';
const spawn = child_process.spawn;

import fs from 'fs';

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

// API to run python script on call
app.get('/runPython', (req, res) => {
  let data1;
  const pythonScript = spawn('python', ['api_scripts/run_api_scripts.py']);
  pythonScript.stdout.on('data', function(data){
    data1 = data.toString()
  });

  pythonScript.on('close', (code) => {
    console.log("code", code)
    res.send(data1);
  });
});

const myDataPath = './api_json_output/';
app.get('/jsonData/:id', (req, res) => {
    let id = req.params.id;
    let path = myDataPath + id + '.json';

    if (fs.existsSync(path)) {
        res.json(JSON.parse(fs.readFileSync(path)));
    } else {
        res.sendStatus(404);
    }
});

// Running server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
