SELECT
    CAST(time AS TIMESTAMP) AS weather_timestamp,
    CAST(time AS DATE) AS weather_date,
    EXTRACT(HOUR FROM CAST(time AS TIMESTAMP)) AS hour_of_day,
    temperature_2m AS temp_f,
    relative_humidity_2m AS humidity,
    cloud_cover,
    precipitation
FROM {{ source('raw_weather', 'central_park_hourly') }}