ALTER LOGIN sa ENABLE;
ALTER LOGIN sa WITH PASSWORD = 'NewSecurePassword';-- Then, set a new password:
ALTER LOGIN sa WITH CHECK_POLICY = OFF; -- Ensure sa login is active:


select * from  WeatherData

SELECT @@SERVERNAME AS ServerName;

CREATE TABLE WeatherData (
    id INT IDENTITY(1,1) PRIMARY KEY,
    location NVARCHAR(100),
    country NVARCHAR(100),
    temperature FLOAT,
    humidity INT,
    condition NVARCHAR(255),
    wind_speed FLOAT,
    timestamp DATETIME DEFAULT GETDATE()
);
