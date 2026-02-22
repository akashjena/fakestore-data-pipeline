\# FakeStore Data Engineering Pipeline



\## Overview



This project implements a simple medallion-style data pipeline using data from [https://fakestoreapi.com/](https://fakestoreapi.com/products).



The pipeline follows a Bronze → Silver → Gold architecture using Delta Lake in Databricks.



---



\## Part 1 – The Pipeline



\### 1. Fetch (Bronze Layer)



\* Data was fetched from the `/products` endpoint.

\* The JSON data was stored as raw data.

\* The raw JSON was converted into a Delta table (`bronze\_products`).



\### 2. Store



\* Data is stored in Delta format.

\* Bronze layer preserves the raw structure.

\* Silver layer applies structural cleansing.

\* Gold layer produces business-level metrics.



\### 3. Transform



Silver Layer:



\* Flattened nested `rating`  into atomic columns.

\* Standardized column names.

\* Selected analytical fields.



Gold Layer:



\* Aggregated metrics by product category:



&nbsp; \* Average price

&nbsp; \* Average rating

&nbsp; \* Total rating count

&nbsp; \* Product count



\### Example Business Metric:



Top product categories by average rating.



---



\## How to Run



1\. Upload the JSON file from FakeStore API into Databricks.

2\. Run the notebook `fakestore\_pipeline.py`.

3\. Execute cells sequentially.

4\. Visualizations can be viewed directly in Databricks.



---



\## Assumptions \& Shortcuts



\* Used Databricks Community Edition.

\* Used a single dataset (`/products`) to keep scope focused.

\* API data was manually downloaded due to API restrictions.

\* No incremental ingestion implemented.



---



\## Improvements With More Time



\* Automate API ingestion using scheduled job.

\* Implement incremental load strategy.

\* Add data quality checks (null checks, range validation).

\* Partition Delta tables for performance.

\* Add orchestration (Airflow / Databricks Jobs).



---



\## Part 2 – Infrastructure Thinking



\### Daily Production Setup



\* Scheduled Databricks Job (daily trigger).

\* Raw data stored in cloud storage (S3/ADLS).

\* Delta tables maintained in Lakehouse.



\### Monitoring



\* Monitor record counts per run.

\* Track schema changes.

\* Alert on ingestion failures.



\### ML Extension Possibility



Features that could be extracted:



\* Average product rating

\* Category-level price behavior

\* Popularity score (rating\_count)



Feature Storage:



\* Store features in a curated Gold feature table.

\* Serve via Feature Store (if scaling to ML use case).



Pipeline Changes for ML:



\* Add feature engineering layer.

\* Maintain feature freshness.

\* Implement training data snapshot versioning.



---



\## Tech Stack



\* Databricks Community Edition

\* PySpark

\* Delta Lake

\* FakeStore API




