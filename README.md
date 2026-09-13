# 🚲 NYC Citi Bike vs. Weather

**Live Dashboard:** https://citibike-weather-project.streamlit.app/
### Project Overview
An end-to-end ELT data pipeline and interactive web application analyzing how daily temperature and rainfall metrics impact riders across New York City.

### Tech Stack
* **Core Languages:** Python (for data extraction and web application) and SQL (for data transformation).
* **Python Libraries:** `pandas`, `requests`, and `pyarrow` for in-memory data extraction from Open-Meteo and AWS S3.
* **Database Engine:** DuckDB
* **dbt (Data Build Tool):** Manages the SQL transformations, staging models, and fact tables.
* **Streamlit & Altair:** Interactive front-end visualization and charting framework.
* 
### Data
* **Citi Bike Trip Data:** Monthly trip logs extracted directly from AWS S3 via the Citi Bike public data program.
* **Weather Data:** Historical hourly weather metrics and 24-hour predictive forecasts acquired via API calls from Open-Meteo.

### Code Structure
```text
├── data/                              
├── bike_project/                       
│   ├── dbt_project.yml
│   └── models/
│       ├── _sources.yml               
│       ├── stg_citibike.sql            
│       ├── stg_weather.sql             
│       └── fct_citibike_weather_impact.sql 
├── ingest_data.py                     
├── app.py                              
├── requirements.txt                   
└── README.md
```

### Installation and Setup
To replicate this project locally:
   ```bash
   pip install -r requirements.txt
   python script.py
   cd bike_project
   dbt build
   cd ..
   streamlit run app.py
   ```
   
   
### A Quick Note on the Data
If you look at the Python script, you'll notice it pulls three different weather datasets (historical hourly, 24-hour forecasts, and NOAA daily highs). Right now, the dashboard only uses the historical data to show how weather affects bike rides. I decided to pull the extra data anyway just for the practice of working with different API endpoints. They are saved as Parquet files in the pipeline so I can use them later when I dive into forecasting and machine learning!
