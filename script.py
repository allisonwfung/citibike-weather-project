import io
import zipfile
from pathlib import Path
from datetime import datetime, timedelta

import requests
import pandas as pd

def fetch_openmeteo_data(lat: float, lon: float, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches historical hourly weather data from the Open-Meteo Archive API."""
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,relative_humidity_2m,cloud_cover,precipitation",
        "timezone": "America/New_York",
        "temperature_unit": "fahrenheit" 
    }
    
    print(f"Requesting weather data from {start_date} to {end_date}...")
    response = requests.get(url, params=params)
    
    response.raise_for_status() 
    
    df = pd.DataFrame(response.json()["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    return df

def fetch_previous_day_forecast(lat: float, lon: float, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches what GFS forecasted 24 hours before each hour actually occurred."""
    url = "https://previous-runs-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m_previous_day1",
        "models": "gfs_seamless",
        "timezone": "America/New_York",
        "temperature_unit": "fahrenheit"
    }
    print(f"Requesting previous-day forecasts from {start_date} to {end_date}...")
    response = requests.get(url, params=params)
    response.raise_for_status()

    df = pd.DataFrame(response.json()["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    return df

def fetch_noaa_daily_high(station_id: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches official daily max temperature from a NOAA GHCN-Daily station."""
    url = "https://www.ncei.noaa.gov/access/services/data/v1"
    params = {
        "dataset": "daily-summaries",
        "stations": station_id,
        "startDate": start_date,
        "endDate": end_date,
        "dataTypes": "TMAX",
        "units": "standard",
        "format": "json",
    }
    print(f"Requesting NOAA daily highs from {start_date} to {end_date}...")
    response = requests.get(url, params=params)
    response.raise_for_status()

    df = pd.DataFrame(response.json())
    df["DATE"] = pd.to_datetime(df["DATE"])
    df["TMAX"] = pd.to_numeric(df["TMAX"])
    return df

def fetch_citibike_month(year_month: str) -> pd.DataFrame:
    """Downloads and extracts a specific month of Citi Bike trip data from S3."""
    url = f"https://s3.amazonaws.com/tripdata/{year_month}-citibike-tripdata.zip"
    print(f"Downloading Citi Bike data for {year_month}...")
    
    response = requests.get(url)
    response.raise_for_status()
    
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        csv_filename = [name for name in z.namelist() if name.endswith('.csv') and not name.split('/')[-1].startswith('.')][0]
        print(f"Extracting {csv_filename}...")
        
        with z.open(csv_filename) as f:
            return pd.read_csv(f, parse_dates=['started_at', 'ended_at'], low_memory=False)

def main():
    LAT = 40.7829
    LON = -73.9654
    NOAA_STATION = "USW00094728"
    
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=3*365)).strftime('%Y-%m-%d')

    df_actual = fetch_openmeteo_data(LAT, LON, start_date, end_date)
    df_actual.to_parquet(output_dir / "raw_central_park_weather.parquet", engine="pyarrow", compression="snappy")
    print(f"Success! {len(df_actual)} weather rows saved.")

    df_forecast = fetch_previous_day_forecast(LAT, LON, start_date, end_date)
    df_forecast.to_parquet(output_dir / "raw_forecast_previous_day1.parquet", engine="pyarrow", compression="snappy")
    print(f"Success! {len(df_forecast)} forecast rows saved.")

    df_noaa = fetch_noaa_daily_high(NOAA_STATION, start_date, end_date)
    df_noaa.to_parquet(output_dir / "raw_noaa_daily_high.parquet", engine="pyarrow", compression="snappy")
    print(f"Success! {len(df_noaa)} NOAA rows saved.")

    target_months = ["202601", "202607"] 
    for month in target_months:
        output_path = output_dir / f"raw_citibike_{month}.parquet"
        
        if not output_path.exists():
            df = fetch_citibike_month(month)
            df.to_parquet(output_path, engine="pyarrow", compression="snappy")
            print(f"Success! {month} saved to {output_path}")
        else:
            print(f"File {month} already exists. Skipping.")

if __name__ == "__main__":
    main()


