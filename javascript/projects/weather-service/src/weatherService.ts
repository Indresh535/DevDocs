import "dotenv/config";
import axios from "axios";
import sql from "mssql";

// SQL Server Configuration
const dbConfig = {
  user: process.env.DB_USER as string,
  password: process.env.DB_PASSWORD as string,
  server: process.env.DB_SERVER as string,
  database: process.env.DB_DATABASE as string,
  options: {
    encrypt: false,
    trustServerCertificate: true,
  },
};

// Function to Fetch Weather Data
const fetchWeatherData = async (location: string) => {
  try {
    const response = await axios.get(process.env.API_URL as string, {
      params: {
        key: process.env.API_KEY as string,
        q: location,
        aqi: "no",
      },
    });

    const data = response.data;
    return {
      location: data.location.name,
      country: data.location.country,
      temperature: data.current.temp_c,
      humidity: data.current.humidity,
      condition: data.current.condition.text,
      wind_speed: data.current.wind_kph,
      timestamp: new Date(),
    };
  } catch (error: any) {
    console.error(`Error fetching data for ${location}:`, error.message);
    return null;
  }
};

// Function to Insert Data into SQL Server
const insertWeatherData = async (data: any) => {
  try {
    const pool = await sql.connect(dbConfig);
    const query = `
      INSERT INTO WeatherData (location, country, temperature, humidity, condition, wind_speed, timestamp) 
      VALUES (@location, @country, @temperature, @humidity, @condition, @wind_speed, @timestamp)
    `;

    await pool
      .request()
      .input("location", sql.NVarChar, data.location)
      .input("country", sql.NVarChar, data.country)
      .input("temperature", sql.Float, data.temperature)
      .input("humidity", sql.Int, data.humidity)
      .input("condition", sql.NVarChar, data.condition)
      .input("wind_speed", sql.Float, data.wind_speed)
      .input("timestamp", sql.DateTime, data.timestamp)
      .query(query);

    console.log(`Inserted weather data for ${data.location}`);
  } catch (error) {
    console.error("Database insert error:", error);
  }
};

// Process Locations
const processLocations = async () => {
  const locations = ["10001", "london"]; // US ZIP and UK Postcode
  for (const location of locations) {
    const weatherData = await fetchWeatherData(location);
    if (weatherData) {
      await insertWeatherData(weatherData);
    }
  }
};

// Run the Service
const runService = async () => {
  console.log("Weather Service Started...");
  await processLocations();
};

runService();
