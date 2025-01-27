const express = require('express');
const { Worker } = require("worker_threads");
const app = express();
const port = process.env.PORT || 3001;

app.get('/non-blocking',(req, res) => {
    res.status(200).send("This page is non-blocking");
})

app.get('/blocking',(req,res) => {
    let counter = 0
    for(let i=0; i<1e9; i++){
        // Simulate a CPU-intensive task
        // This will block the main thread
        counter++;
    }
    res.status(200).send(`This page is blocking and result is ${counter}`);
})

app.get('/multithread-blocking',(req,res) => {
    const worker = new Worker("./threads/worker-threads.js");
    worker.on("message", (data) => {
        res.status(200).send(`results multithread-blocking is ${data}`);
    });
    worker.on("error", (msg) => {
        res.status(404).send(`An error multithread-blockin occurred: ${msg}`);
    });
})

app.listen(port, () => {
    console.log(`App listening on http://localhost:${port}`);
  });