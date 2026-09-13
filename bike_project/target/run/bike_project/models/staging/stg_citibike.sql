
  
    
    

    create  table
      "bike"."main"."stg_citibike__dbt_tmp"
  
    as (
      SELECT
    CAST(started_at AS TIMESTAMP) AS started_at,
    CAST(ended_at AS TIMESTAMP) AS ended_at,
    date_trunc('hour', CAST(started_at AS TIMESTAMP)) AS trip_hour,
    
    rideable_type,
    member_casual,
    
    epoch(CAST(ended_at AS TIMESTAMP) - CAST(started_at AS TIMESTAMP)) / 60.0 AS duration_minutes

FROM '../data/raw_citibike_*.parquet'
WHERE started_at IS NOT NULL 
  AND ended_at IS NOT NULL
  AND (epoch(CAST(ended_at AS TIMESTAMP) - CAST(started_at AS TIMESTAMP)) / 60.0) > 1 
  AND (epoch(CAST(ended_at AS TIMESTAMP) - CAST(started_at AS TIMESTAMP)) / 60.0) < 1440
    );
  
  