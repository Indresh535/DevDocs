const { Worker, isMainThread, parentPort, workerData } = require("worker_threads");
const express = require("express");
const client = require("prom-client");
const os = require("os");

const app = express();
const PORT = 3001;
const NUM_WORKERS = os.cpus().length;
const workers = [];

// Prometheus Metrics
const jobCounter = new client.Counter({
  name: "total_jobs_processed",
  help: "Total number of jobs processed by workers"
});

const activeThreads = new client.Gauge({
  name: "active_threads",
  help: "Number of active worker threads"
});

const cpuUsage = new client.Gauge({
  name: "cpu_usage_percent",
  help: "CPU usage in percentage"
});

client.collectDefaultMetrics();

if (isMainThread) {
  console.log(`Main Thread: Spawning ${NUM_WORKERS} workers...`);

  for (let i = 0; i < NUM_WORKERS; i++) {
    const worker = new Worker(__filename, { workerData: { id: i } });
    workers.push(worker);
  }

  setInterval(() => {
    const cpuLoad = os.loadavg()[0] / os.cpus().length * 100;
    cpuUsage.set(cpuLoad);
    activeThreads.set(workers.length);
  }, 5000);

  app.get("/metrics", async (req, res) => {
    res.set("Content-Type", client.register.contentType);
    res.end(await client.register.metrics());
  });

  app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
} else {
  console.log(`Worker ${workerData.id} started.`);
  setInterval(() => {
    jobCounter.inc();
  }, 1000);
}
