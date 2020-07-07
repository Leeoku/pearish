import express from 'express';
import path from 'path';

const app = express();

app.post('api/auth', (req, res) => {
  res.status(400).json({error: {global: "Invalid credentials"}});
});

app.get('/*', (req,res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(6969, () => console.log('Running on localhost:6969'));
