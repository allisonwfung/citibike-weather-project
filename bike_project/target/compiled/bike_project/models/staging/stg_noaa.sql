SELECT
    CAST(DATE AS DATE) AS weather_date,
    TMAX AS official_high_temp
FROM '../data/raw_noaa_daily_high.parquet'