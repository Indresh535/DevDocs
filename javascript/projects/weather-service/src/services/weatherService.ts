// # Fetch weather data and insert into DB
import axios from "axios";
import { connectDB } from "../config/db";
import sql from "mssql";

interface WeatherData {
  location: string;
  country: string;
  temperature: number;
  humidity: number;
  condition: string;
  wind_speed: number;
  timestamp: Date;
}

const fetchWeatherData = async (location: string): Promise<WeatherData | null> => {
  try {
    const response = await axios.get(process.env.API_URL as string, {
      params: { key: process.env.API_KEY as string, q: location, aqi: "no" },
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
    console.error(` Error fetching data for ${location}:`, error.message);
    return null;
  }
};

const insertWeatherData = async (data: WeatherData) => {
  try {
    const pool = await connectDB();
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
  } catch (error: any) {
    console.error("Database insert error:", error);
  }
};

export const processWeather = async () => {
  const locations = ["10001", "london"];
  for (const location of locations) {
    const weatherData = await fetchWeatherData(location);
    if (weatherData) {
      await insertWeatherData(weatherData);
    }
  }
};
