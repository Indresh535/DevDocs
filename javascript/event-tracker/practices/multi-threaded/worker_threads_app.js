// This implementation uses Worker Threads to run tasks in parallel.

const { Worker, isMainThread, parentPort, workerData } = require("worker_threads");
const os = require("os");
const express = require("express");
const client = require("prom-client");

const app = express();
const PORT = 3001;
const NUM_WORKERS = os.cpus().length;

// Prometheus Metrics
const jobCounter = new client.Counter({
  name: "worker_total_jobs_processed",
  help: "Total number of jobs processed by workers"
});

const activeThreads = new client.Gauge({
  name: "worker_active_threads",
  help: "Number of active worker threads"
});

const cpuUsage = new client.Gauge({
  name: "worker_cpu_usage_percent",
  help: "CPU usage in percentage"
});

client.collectDefaultMetrics();

if (isMainThread) {
  console.log(`Main Thread: Spawning ${NUM_WORKERS} workers...`);
  const workers = [];

  for (let i = 0; i < NUM_WORKERS; i++) {
    const worker = new Worker(__filename, { workerData: { id: i } });
    workers.push(worker);
  }

  setInterval(() => {
    cpuUsage.set(os.loadavg()[0] / os.cpus().length * 100);
    activeThreads.set(workers.length);
  }, 2000);

  app.get("/metrics", async (req, res) => {
    res.set("Content-Type", client.register.contentType);
    res.end(await client.register.metrics());
  });

  app.listen(PORT, () => {
    console.log(`Worker Thread Server running on http://localhost:${PORT}`);
  });
} else {
  function fibonacci(n) {
    return n < 2 ? n : fibonacci(n - 1) + fibonacci(n - 2);
  }

  console.log(`Worker ${workerData.id} started.`);
  setInterval(() => {
    fibonacci(30);
    jobCounter.inc();
  }, 1000);
}
