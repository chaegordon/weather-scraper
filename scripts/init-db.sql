-- init-db.sql is a script that initializes the database schema and creates the necessary tables and views.

-- Create the weather_data table to store weather data
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,                 -- Auto-incrementing primary key
    frequency VARCHAR(50),                 -- Frequency of data (minutely, hourly, daily)
    timestamp TIMESTAMP,                   -- Timestamp of data
    scraped_at TIMESTAMP,                  -- Timestamp of when data was scraped
    cloud_base FLOAT,                      -- Cloud base (floating-point value)
    cloud_ceiling FLOAT,                   -- Cloud ceiling (floating-point value)
    cloud_cover INTEGER,                   -- Cloud cover (integer value)
    dew_point FLOAT,                       -- Dew point temperature (floating-point value)
    freezing_rain_intensity INTEGER,       -- Intensity of freezing rain (integer value)
    humidity INTEGER,                      -- Humidity percentage (integer value)
    precipitation_probability INTEGER,     -- Precipitation probability (integer value)
    pressure_surface_level FLOAT,          -- Pressure at surface level (floating-point value)
    rain_intensity INTEGER,                -- Rain intensity (integer value)
    sleet_intensity INTEGER,               -- Sleet intensity (integer value)
    snow_intensity INTEGER,                -- Snow intensity (integer value)
    temperature FLOAT,                     -- Temperature (floating-point value)
    temperature_apparent FLOAT,            -- Apparent temperature (floating-point value)
    uv_health_concern INTEGER,             -- UV health concern (integer value)
    uv_index INTEGER,                      -- UV index (integer value)
    visibility INTEGER,                    -- Visibility (integer value)
    weather_code INTEGER,                  -- Weather code (integer value)
    wind_direction FLOAT,                  -- Wind direction (floating-point value)
    wind_gust FLOAT,                       -- Wind gust speed (floating-point value)
    wind_speed FLOAT,                      -- Wind speed (floating-point value)
    latitude FLOAT,                        -- Latitude (floating-point value)
    longitude FLOAT                        -- Longitude (floating-point value)
);
-- Create indexes to improve query performance
CREATE INDEX idx_weather_data_timestamp ON weather_data(timestamp);
CREATE INDEX idx_weather_data_scraped_at ON weather_data(scraped_at);

-- Create minutely_weather materialized view
CREATE MATERIALIZED VIEW minutely_weather AS
WITH ranked_minutely AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY timestamp ORDER BY scraped_at DESC) AS rn
    FROM weather_data
    WHERE frequency = 'minutely'
)
SELECT *
FROM ranked_minutely
WHERE rn = 1;

-- Create hourly_weather materialized view
CREATE MATERIALIZED VIEW hourly_weather AS
WITH ranked_hourly AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY timestamp ORDER BY scraped_at DESC) AS rn
    FROM weather_data
    WHERE frequency = 'hourly'
)
SELECT *
FROM ranked_hourly
WHERE rn = 1;

-- Create daily_weather materialized view
CREATE MATERIALIZED VIEW daily_weather AS
WITH ranked_daily AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY timestamp ORDER BY scraped_at DESC) AS rn
    FROM weather_data
    WHERE frequency = 'daily'
)
SELECT *
FROM ranked_daily
WHERE rn = 1;

CREATE MATERIALIZED VIEW realtime_weather AS
SELECT *
FROM weather_data
WHERE frequency = 'realtime';

-- Create unique indexes on materialized views
CREATE UNIQUE INDEX minutely_weather_unique_idx ON minutely_weather(id);
CREATE UNIQUE INDEX hourly_weather_unique_idx ON hourly_weather(id);
CREATE UNIQUE INDEX daily_weather_unique_idx ON daily_weather(id);
CREATE UNIQUE INDEX realtime_weather_unique_idx ON realtime_weather(id);