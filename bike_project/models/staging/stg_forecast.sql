SELECT
    CAST(time AS TIMESTAMP) AS forecast_timestamp,
    CAST(time AS DATE) AS forecast_date,
    temperature_2m_previous_day1 AS forecast_temp_previous_day1
FROM {{ source('raw_weather', 'central_park_forecast_previous_day1') }}