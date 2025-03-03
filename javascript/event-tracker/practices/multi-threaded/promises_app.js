// This implementation does not use Worker Threads but uses async/await with Promises instead.

const express = require("express");
const client = require("prom-client");
const os = require("os");

const app = express();
const PORT = 3002;

// Prometheus Metrics
const jobCounter = new client.Counter({
  name: "promise_total_jobs_processed",
  help: "Total number of jobs processed using Promises"
});

const cpuUsage = new client.Gauge({
  name: "promise_cpu_usage_percent",
  help: "CPU usage in percentage"
});

client.collectDefaultMetrics();

function fibonacci(n) {
  return new Promise((resolve) => {
    if (n < 2) resolve(n);
    else resolve(fibonacci(n - 1).then(a => fibonacci(n - 2).then(b => a + b)));
  });
}

async function runHeavyTask() {
  await fibonacci(30);
  jobCounter.inc();
}

setInterval(() => {
  runHeavyTask();
  cpuUsage.set(os.loadavg()[0] / os.cpus().length * 100);
}, 1000);

app.get("/metrics", async (req, res) => {
  res.set("Content-Type", client.register.contentType);
  res.end(await client.register.metrics());
});

app.listen(PORT, () => {
  console.log(`Promise Server running on http://localhost:${PORT}`);
});
