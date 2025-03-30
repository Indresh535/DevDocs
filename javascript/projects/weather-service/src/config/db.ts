// SQL Server connection setup

import "dotenv/config";
import sql from "mssql";

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

export const connectDB = async () => {
  try {
    const pool = await sql.connect(dbConfig);
    console.log("Connected to SQL Server");
    return pool;
  } catch (error: any) {
    console.error("Database connection error:", error);
    throw error;
  }
};


// API_URL=https://api.weatherapi.com/v1/current.json
// API_KEY=796cc2653c1d4c7597d134220252903
// DB_USER=sa
// DB_PASSWORD=admin
// DB_SERVER=DELL
// DB_DATABASE=testdb