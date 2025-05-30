# Patient Data Streaming Pipeline

## Overview

This project implements a real-time **Patient Data Streaming Pipeline** using Databricks' Delta Live Tables (DLT) and **Autoloader**. The pipeline processes streaming healthcare data in three layers: **Raw Data Layer** (formerly Bronze), **Silver Layer**, and **Gold Layer**. The goal is to ingest, transform, clean, and aggregate patient records for analytics and reporting, enabling real-time insights into patient health data.

## Pipeline Layers

1. **Raw Data Layer(Bronze Data)**:
   - **Autoloader** is used to ingest raw data automatically from the `raw_data` folder. New patient data files (in CSV format) are continuously monitored and ingested into the Delta Lake as soon as they arrive.
   - Minimal transformations such as schema enforcement and null handling are applied.
   - Data is stored in Delta Lake tables for further processing.

2. **Silver Layer**:
   - Data cleaning and transformations are applied, including handling missing values, standardizing formats, and resolving inconsistencies.
   - The Silver Layer also includes joining the raw patient data with diagnosis mapping files.

3. **Gold Layer**:
   - Final aggregation, windowing, and data quality checks are performed.
   - The Gold layer provides rich, refined data, optimized for analytics, such as average patient metrics, diagnosis-specific summaries, and time-series trends.
   - Data quality checks ensure that records meet the required criteria.

## Features

- **Real-time data ingestion with Autoloader**: The **Databricks Autoloader** is used to continuously monitor the raw data directory and automatically ingest new patient data files into the pipeline.
- **Delta Live Tables (DLT)**: Automatically handles the transformation and data quality checks as the data flows from the Raw Data layer to the Silver and Gold layers.
- **Data quality checks**: Ensure the integrity of the data before it reaches the final analytical layer.
- **Aggregations and windowing**: Perform advanced calculations like rolling averages and real-time patient monitoring.

## Setup and Installation

1. **Databricks Environment**:
   - Ensure you have access to a Databricks workspace with Delta Live Tables enabled.
   - Clone this repository and upload the necessary files to your Databricks workspace.

2. **Data Ingestion Using Autoloader**:
   - The **Autoloader** automatically monitors the directory `dbfs:/FileStore/shashank/raw_data/` for new patient data files.
   - The new files are ingested into the `patient.raw_patients_daily` Delta table using the following Autoloader configuration:

     ```python
     from pyspark.sql.functions import *

     # Define the raw data input path
     raw_patient_data_path = "dbfs:/FileStore/rkuturu/raw_data/"

     # Autoloader to detect new files
     df_patients = (spark.readStream.format("cloudFiles")
                    .option("cloudFiles.format", "csv")
                    .option("header", "true")
                    .option("inferSchema", "true")
                    .load(raw_patient_data_path))

     # Cast 'admission_date' to date type and write to Delta table
     df_patients_transformed = df_patients.withColumn("admission_date", df_patients["admission_date"].cast("date"))

     df_patients_transformed.writeStream \
         .format("delta") \
         .outputMode("append") \
         .option("mergeSchema", "true") \
         .option("checkpointLocation", "dbfs:/checkpoints/raw_patients_daily") \
         .table("patient.raw_patients_daily")
     ```

3. **Delta Live Tables Configuration**:
   - Set up the DLT pipeline in Databricks by creating a new DLT notebook. Follow the steps outlined in the `dlt_pipeline_notebook.sql` file for the transformations and quality checks.
   - Define the Raw, Silver, and Gold tables in your DLT pipeline.

4. **Automating the Process**:
   - **Autoloader** will automatically detect new files and process them into the Raw Data layer.
   - Use **Delta Live Tables (DLT)** to transform the data from the Raw Data layer into Silver and Gold layers.
   - You can also schedule Databricks Jobs to ensure the pipeline runs continuously.

## Data Structure

### Files

- **patients_daily_file_*.csv:**
  - Contains synthetic daily records of patients, including patient information such as ID, name, age, gender, admission date, and diagnosis code.
  
- **diagnosis_mapping.csv:**
  - Contains mappings of diagnosis codes to human-readable diagnosis descriptions.

### Table Definitions

- **Raw Data Table**:
  - Contains raw patient data ingested using **Autoloader** and stored in Delta format.

- **Silver Table**:
  - Cleaned and transformed data with all inconsistencies and missing values addressed.
  
- **Gold Table**:
  - Aggregated, windowed, and validated data, optimized for analytics and reporting.

## Future Enhancements

- Implement a more complex data generation mechanism for simulating different healthcare scenarios.
- Add more advanced machine learning models for real-time patient risk prediction based on ingested data.
- Implement dashboarding for live monitoring and alerts.
