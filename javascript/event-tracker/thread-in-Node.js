const fs = require('fs');
const os = require('os');
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');


console.info("My CPU as Threads",os.cpus().length);

console.info("My CPU as Threads",os.cpus());
// Simulate a non-blocking I/O operation (e.g., reading a file)
function readFileNonBlocking() {
  fs.readFile('tests/sample.txt', 'utf-8', (err, data) => {
    if (err) {
      console.error('Error reading file:', err);
    } else {
      console.log('Non-blocking I/O - File data:', data);
    }
  });
}

// Simulate a blocking operation (e.g., a long computation)
function blockingOperation() {
  let sum = 0;
  console.log('Starting blocking operation...');
  for (let i = 0; i < 1e9; i++) {
    sum += i;
  }
  console.log('Blocking operation finished.');
  console.log('Sum:', sum);
}

// Simulate a CPU-intensive task using Worker Threads
function cpuIntensiveTask() {
  return new Promise((resolve, reject) => {
    const worker = new Worker(__filename, {
      workerData: 'CPU intensive task started...'
    });
    worker.on('message', (result) => {
      console.log('Worker Result:', result);
      resolve();
    });
    worker.on('error', reject);
    worker.on('exit', (code) => {
      if (code !== 0) reject(new Error(`Worker stopped with exit code ${code}`));
    });
  });
}

// Worker thread code for CPU-intensive tasks
if (!isMainThread) {
  console.log('Worker thread:', workerData);
  let sum = 0;
  for (let i = 0; i < 1e8; i++) {
    sum += i;
  }
  parentPort.postMessage(`Worker finished with sum: ${sum}`);
  return;
}
// Main thread execution
async function main() {
  console.log('Starting Node.js program...\n');
  
  // Non-blocking I/O example
  console.log('Running non-blocking I/O...');
  readFileNonBlocking();
  
  // Blocking operation (this will block the event loop)
  console.log('Running blocking operation...');
  blockingOperation();

  // Demonstrating event loop and callback-based concurrency
  setTimeout(() => {
    console.log('Event Loop: setTimeout callback executed!');
  }, 0);

  // Simulate a CPU-intensive task using worker threads
  await cpuIntensiveTask();
  
  console.log('\nNode.js program completed.');
}

main();



// Below is a Node.js program that demonstrates various core concepts in a single script: single-threaded nature, worker pool, blocking and non-blocking operations, event queue, event loop, callback-based concurrency, and multithreading using worker threads for CPU-intensive tasks.

// Overview:
// Single-Threaded: The main thread in Node.js executes asynchronously and handles I/O operations.
// Non-Blocking: I/O tasks like reading files or network requests do not block the execution of the program.
// Event Loop: The event loop is responsible for managing async callbacks and executing them after tasks are completed.
// Worker Threads: For CPU-bound tasks, we use worker_threads to handle processing in parallel.
// Blocking: We'll simulate a blocking operation that will prevent other tasks from being processed until it's done.

// Breakdown of the Code:
// Single Thread (Main Thread):

// Node.js runs on a single thread, and the event loop handles I/O and async tasks like file reading, HTTP requests, etc.
// The main thread executes the program and handles callbacks (like fs.readFile).
// Non-Blocking I/O:

// The readFileNonBlocking function is non-blocking. It asynchronously reads a file and returns control to the event loop before the operation is finished. The event loop continues to run other tasks while waiting for the file read.
// Blocking Operation:

// The blockingOperation function simulates a long-running CPU-bound task. This operation blocks the event loop, meaning that no other tasks (like setTimeout or I/O operations) can be processed until this function finishes.
// Event Loop:

// The setTimeout function is used to demonstrate the event loop. It places the callback function in the event queue, and Node.js will execute it as soon as the event loop is ready (after the current stack is cleared).
// Callback (Multithreaded CPU Task):

// We simulate a CPU-intensive task in the main thread and offload that work to a worker thread. Worker threads allow us to process data in parallel on separate threads, thus not blocking the main thread.
// Worker Pool (Worker Threads):

// In the cpuIntensiveTask function, we use worker_threads to handle CPU-heavy tasks. This demonstrates how we can use worker threads to perform parallel processing without blocking the main thread.
// Multithreading:

// In the worker thread, we simulate a CPU-bound task (looping to sum a large range of numbers). After completion, the result is sent back to the main thread using parentPort.postMessage.
// Key Concepts Demonstrated:
// Single-threaded Execution: The entire code execution in Node.js runs on a single thread unless offloaded to workers.
// Non-blocking I/O: The readFile operation doesn’t block the event loop, allowing other tasks to execute.
// Blocking Tasks: The blockingOperation simulates a task that blocks the event loop.
// Event Loop & Event Queue: The setTimeout is pushed to the event queue and will execute once the event loop is free.
// Worker Threads for Multithreading: The cpuIntensiveTask is offloaded to a worker thread to prevent blocking of the main thread and make use of multiple CPU cores.
// Output:
// Non-blocking I/O: The file read will finish after other operations, showcasing non-blocking I/O.
// Blocking: The blocking operation will delay other tasks, such as the setTimeout.
// Worker Threads: CPU-bound tasks are handled in parallel by the worker thread, allowing the main thread to remain responsive.
// Notes:
// Make sure to create a sample.txt file in the same directory as the script to test the non-blocking I/O operation.
// This script is designed to show how the event loop, blocking vs non-blocking operations, and worker threads interact in a real-time Node.js application.
// Let me know if you need further explanation or adjustments!