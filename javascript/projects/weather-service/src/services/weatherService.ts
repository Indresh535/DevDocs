// # Fetch weather data and insert into DB
import axios from "axios";
import { connectDB } from "../config/db";
import sql from "mssql";

interface WeatherData {
  LocationName: string;
  CountryName: string;
  Temperature: number;
  Humidity: number;
  Condition: string;
  WindSpeed: number;
  TimeStamp: Date;
}


const logStatus = async (locationsProcessed: number, recordsInserted: number, recordsUpdated: number, executionTime: number, status: string) => {
  try {
    const pool = await connectDB();
    await pool
      .request()
      .input("locationsProcessed", sql.Int, locationsProcessed)
      .input("recordsInserted", sql.Int, recordsInserted)
      .input("recordsUpdated", sql.Int, recordsUpdated)
      .input("executionTime", sql.Float, executionTime)
      .input("status", sql.NVarChar, status)
      .query(`
        INSERT INTO StatusLog (LocationsProcessed, RecordsInserted, RecordsUpdated, ExecutionTime, Status)
        VALUES (@locationsProcessed, @recordsInserted, @recordsUpdated, @executionTime, @status)
      `);

    console.log(`Status log updated: ${status}`);
  } catch (error: any) {
    console.error("Error logging status:", error);
  }
};

const logError = async (message: string, location: string) => {
  try {
    const pool = await connectDB();
    await pool
      .request()
      .input("ErrorMessage", sql.NVarChar, message)
      .input("Location", sql.NVarChar, location)
      .query("INSERT INTO ErrorLog (ErrorMessage, Location) VALUES (@ErrorMessage, @Location)");

    console.log(`Error logged: ${message}`);
  } catch (error: any) {
    console.error("Error logging to database:", error);
  }
};


const fetchWeatherData = async (location: string): Promise<WeatherData | null> => {
  try {
    const response = await axios.get(process.env.API_URL as string, {
      params: { key: process.env.API_KEY as string, q: location, aqi: "no" },
    });

    const data = response.data;
    return {
      LocationName: data.location.name,
      CountryName: data.location.country,
      Temperature: data.current.temp_c,
      Humidity: data.current.humidity,
      Condition: data.current.condition.text,
      WindSpeed: data.current.wind_kph,
      TimeStamp: new Date()
    };
  } catch (error: any) {
    console.error(` Error fetching data for ${location}:`, error.message);
    await logError(error.message, location);
    return null;
  }
};



const upsertWeatherData = async (data: WeatherData) => {
  try {
    const pool = await connectDB();
    await pool
      .request()
      .input("location", sql.NVarChar, data.LocationName) 
      .input("country", sql.NVarChar, data.CountryName)  
      .input("temperature", sql.Float, data.Temperature)
      .input("humidity", sql.Int, data.Humidity)
      .input("condition", sql.NVarChar, data.Condition)
      .input("wind_speed", sql.Float, data.WindSpeed)
      .input("timestamp", sql.DateTime, data.TimeStamp)
      .execute("UpsertWeatherData");

    console.log(`Weather data upserted for ${data.LocationName}`);
    return true;
  } catch (error: any) {
    console.error("Database upsert error:", error);
    await logError(error.message, data.LocationName);
    return false;
  }
};


export const processWeather = async () => {
  const locations = ["10001", "london"];

  let recordsInserted = 0;
  let recordsUpdated = 0;
  const startTime = Date.now();

  for (const location of locations) {
    const weatherData = await fetchWeatherData(location);
    if (weatherData) {
      const success = await upsertWeatherData(weatherData);
      if (success) recordsInserted++;
      else recordsUpdated++;
    }
  }

  const executionTime = (Date.now() - startTime) / 1000;
  await logStatus(locations.length, recordsInserted, recordsUpdated, executionTime, "Completed");

};
