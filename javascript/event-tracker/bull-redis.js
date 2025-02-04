
// Redis + Bull Setup and Implementation
// Install Redis and start the server: https://redis.io/docs/getting-started/installation/
// Install dependencies: npm install bull ioredis

const Queue = require('bull');
const fibonacciQueue = new Queue('fibonacci');
const { BullAdapter } = require('bull-board');
const { router } = require('bull-board');

const app = express();



function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Process jobs
fibonacciQueue.process(async (job) => {
    return fibonacci(job.data.number);
});

// Adding jobs to the queue
async function addJobs() {
    console.time('Redis-Bull');
    const job1 = await fibonacciQueue.add({ number: 40 });
    const job2 = await fibonacciQueue.add({ number: 40 });
    
    job1.finished().then(result => console.log('Job 1 result:', result));
    job2.finished().then(result => console.log('Job 2 result:', result));
    
    console.timeEnd('Redis-Bull');
}

addJobs();