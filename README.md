# NYC Citi Bike vs. Weather Elasticity

**Live Dashboard:** [URL will go here]

An end-to-end ELT data pipeline and interactive web application analyzing how daily temperature and rainfall metrics impact rider behavior across New York City.

**Tech Stack**
* **Python:** Data extraction from APIs (Open-Meteo, NOAA) and AWS S3.
* **DuckDB & Parquet:** Local analytical database engine and columnar data storage.
* **dbt (Data Build Tool):** SQL transformations, staging models, and fact tables.
* **Streamlit & Altair:** Interactive front-end visualization and charting.

**Architecture Highlights**
* **In-Memory Processing:** Bypasses slow disk I/O by unzipping massive S3 Citi Bike payloads directly in RAM using `io.BytesIO`.
* **dbt Best Practices:** Enforces strict 1:1 row integrity in the staging layer (`stg_`) and isolates heavy aggregations, `COALESCE` logic, and table joins in the downstream marts layer (`fct_`).

**Local Setup**
1. Install dependencies: `pip install -r requirements.txt`
2. Ingest raw data: `python ingest_data.py`
3. Build database: `cd bike_project && dbt build`
4. Launch app: `streamlit run app.py`
