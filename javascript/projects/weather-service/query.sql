ALTER LOGIN sa ENABLE;
ALTER LOGIN sa WITH PASSWORD = 'NewSecurePassword';-- Then, set a new password:
ALTER LOGIN sa WITH CHECK_POLICY = OFF; -- Ensure sa login is active:


SELECT * FROM  WeatherData

SELECT * FROM  StatusLog

SELECT * FROM  ErrorLog

SELECT @@SERVERNAME AS ServerName;

USE [testdb]
GO
/****** Object:  StoredProcedure [dbo].[UpsertWeatherData]    Script Date: 31-03-2025 23:54:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Indresh>
-- Create date: <Create Date,30-March-2025,>
-- Description:	<Description,Insert new weather data if the location does not exist,Update the existing record if the location exists but with new data.>
-- =============================================
ALTER   PROCEDURE [dbo].[UpsertWeatherData]
    @location NVARCHAR(100),
    @country NVARCHAR(100),
    @temperature FLOAT,
    @humidity INT,
    @condition NVARCHAR(255),
    @wind_speed FLOAT,
    @timestamp DATETIME
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    IF EXISTS (SELECT 1 FROM WeatherData WHERE LocationName = @location)
    BEGIN
        -- Update existing record if data has changed
        UPDATE WeatherData
        SET 
            Temperature = @temperature,
            Humidity = @humidity,
            Condition = @condition,
            WindSpeed = @wind_speed,
            TimeStamp = @timestamp,
			LastUpdatedDate = GETDATE()
        WHERE LocationName = @location;
    END
    ELSE
    BEGIN
        -- Insert new record
        INSERT INTO WeatherData (LocationName, CountryName, Temperature, Humidity, Condition, WindSpeed, TimeStamp, LastUpdatedDate)
        VALUES (@location, @country, @temperature, @humidity, @condition, @wind_speed, @timestamp, GETDATE());
    END
END
