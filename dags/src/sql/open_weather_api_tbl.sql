-- Drop the table if it exists in the 'open_weather' schema
DROP TABLE open_weather.open_weather_api_tbl;

-- Create the 'open_weather_api_tbl' table in the 'open_weather' schema
-- This table is designed to store weather data from the OpenWeather API
CREATE TABLE open_weather.open_weather_api_tbl (
    id              INT,                         -- City ID
    main            VARCHAR,                     -- Main weather condition 
    description     VARCHAR,                     -- Detailed weather description
    icon            VARCHAR,                     -- Icon ID for weather representation
    base            VARCHAR,                     -- Internal parameter 
    visibility      INT,                         -- Visibility in meters
    dt              INT,                         -- Time of data calculation
    timezone        INT,                         -- Shift in seconds from UTC
    name            VARCHAR,                     -- City name
    cod             INT,                         -- Internal parameter for response code
    coord_lon       DOUBLE PRECISION,            -- Longitude of the location
    coord_lat       DOUBLE PRECISION,            -- Latitude of the location
    main_temp       DOUBLE PRECISION,            -- Current temperature
    main_feels_like DOUBLE PRECISION,            -- Temperature perceived by humans
    main_temp_min   DOUBLE PRECISION,            -- Minimum temperature at the moment
    main_temp_max   DOUBLE PRECISION,            -- Maximum temperature at the moment
    main_pressure   INT,                         -- Atmospheric pressure 
    main_humidity   INT,                         -- Humidity percentage
    main_sea_level  INT,                         -- Sea level pressure 
    main_grnd_level INT,                         -- Ground level pressure 
    wind_speed      DOUBLE PRECISION,            -- Wind speed 
    wind_deg        INT,                         -- Wind direction 
    wind_gust       DOUBLE PRECISION,            -- Wind gust 
    clouds_all      INT,                         -- Cloudiness percentage
    sys_country     VARCHAR,                     -- Country code 
    sys_sunrise     INT,                         -- Sunrise time 
    sys_sunset      INT,                         -- Sunset time 
    sys_type        DOUBLE PRECISION,            -- Internal parameter
    sys_id          DOUBLE PRECISION,            -- Internal parameter
    date_time       TIMESTAMP                    -- Timestamp when the record was inserted
);

-- View all data in the new table 
SELECT * FROM open_weather.open_weather_api_tbl;

-- Delete all data from the table 
DELETE FROM open_weather.open_weather_api_tbl;

-- View data from a table with the same name in the 'public' schema 
SELECT * FROM public.open_weather_api_tbl;