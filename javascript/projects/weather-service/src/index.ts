// # Main entry point

import { processWeather } from "./services/weatherService";

const runService = async () => {
  console.log("🚀 Weather Service Started...");
  await processWeather();
};

runService();
