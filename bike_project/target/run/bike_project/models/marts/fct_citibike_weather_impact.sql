
  
    
    

    create  table
      "bike"."main"."fct_citibike_weather_impact__dbt_tmp"
  
    as (
      WITH raw_citibike AS (
    SELECT * FROM "bike"."main"."stg_citibike"
),
hourly_citibike AS (
    SELECT
        trip_hour,
        COUNT(*) AS total_rides,
        COUNT(CASE WHEN member_casual = 'member' THEN 1 END) AS member_rides,
        COUNT(CASE WHEN member_casual = 'casual' THEN 1 END) AS casual_rides,
        COUNT(CASE WHEN rideable_type = 'electric_bike' THEN 1 END) AS electric_rides,
        COUNT(CASE WHEN rideable_type = 'classic_bike' THEN 1 END) AS classic_rides,
        ROUND(AVG(duration_minutes), 2) AS avg_duration_minutes
    FROM raw_citibike
    GROUP BY trip_hour
),

weather AS (
    SELECT * FROM "bike"."main"."stg_weather"
)

SELECT
    w.weather_timestamp AS hour_timestamp,
    w.weather_date,
    w.hour_of_day,
    w.temp_f,
    w.humidity,
    w.cloud_cover,
    w.precipitation,
    (w.precipitation > 0.05) AS is_raining,
    (w.temp_f < 32.0) AS is_freezing,
    COALESCE(c.total_rides, 0) AS total_rides,
    COALESCE(c.member_rides, 0) AS member_rides,
    COALESCE(c.casual_rides, 0) AS casual_rides,
    COALESCE(c.electric_rides, 0) AS electric_rides,
    COALESCE(c.classic_rides, 0) AS classic_rides,
    c.avg_duration_minutes
FROM weather w
LEFT JOIN hourly_citibike c
    ON w.weather_timestamp = c.trip_hour
    );
  
  