SELECT
    CAST(DATE AS DATE) AS weather_date,
    TMAX AS official_high_temp
FROM {{ source('raw_weather', 'central_park_noaa_daily_high') }}