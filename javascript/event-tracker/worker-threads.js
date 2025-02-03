// worker.js - Worker Thread
const { parentPort } = require('worker_threads');

function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

parentPort.on('message', (num) => {
    const result = fibonacci(num);
    parentPort.postMessage(result);
});

// workerThreads.js - Main file
const { Worker } = require('worker_threads');

function runWorker(num) {
    return new Promise((resolve, reject) => {
        const worker = new Worker('./worker.js');
        worker.postMessage(num);
        worker.on('message', resolve);
        worker.on('error', reject);
        worker.on('exit', (code) => {
            if (code !== 0) reject(new Error(`Worker stopped with exit code ${code}`));
        });
    });
}

async function main() {
    console.time('WorkerThreads');
    const results = await Promise.all([runWorker(40), runWorker(40)]);
    console.timeEnd('WorkerThreads');
    console.log('Results:', results);
}

main();