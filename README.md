# 🚲 NYC Citi Bike vs. Weather Elasticity

**Live Dashboard:** [Insert Streamlit Link Here]

### Project Overview
An end-to-end ELT data pipeline and interactive web application analyzing how daily temperature and rainfall metrics impact riders across New York City.

### Tech Stack
* **Python:** Data extraction from APIs (Open-Meteo) and AWS S3 in-memory processing (`pandas`, `requests`, `pyarrow`).
* **DuckDB & Parquet:** Local analytical database engine and columnar data storage.
* **dbt (Data Build Tool):** SQL transformations, staging models, and fact tables.
* **Streamlit & Altair:** Interactive front-end visualization and charting.

### Data
* **Citi Bike Trip Data:** Monthly trip logs extracted directly from AWS S3 via the Citi Bike public data program.
* **Weather Data:** Historical hourly weather metrics and 24-hour predictive forecasts acquired via API calls from Open-Meteo.

### Pipeline Architecture
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
   
   
