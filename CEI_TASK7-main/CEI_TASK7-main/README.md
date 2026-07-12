# Week 7 Assignment – Data Exploration and Cleaning using Pandas

## Overview

This project demonstrates basic data exploration and data cleaning using **Python**, **Pandas**, and **Databricks**. The Sample Superstore dataset was analyzed to understand its structure, clean the data, and perform basic transformations.

## Objectives

- Load a CSV dataset into a Pandas DataFrame.
- Explore the dataset using various Pandas functions.
- Identify and handle missing values.
- Filter rows and select required columns.
- Remove duplicate records.
- Create a derived column (`total_amount`).
- Save the cleaned dataset as a new CSV file.
- Demonstrate Spark DataFrame integration in Databricks.

## Technologies Used

- Python
- Pandas
- Apache Spark
- Databricks Community Edition

## Dataset

- **Dataset:** Sample Superstore
- **Format:** CSV

## Steps Performed

1. Imported the required Python libraries.
2. Loaded the dataset into a Pandas DataFrame.
3. Explored the data using:
   - `head()`
   - `tail()`
   - `shape`
   - `columns`
   - `dtypes`
   - `info()`
   - `describe()`
4. Checked for missing values and verified data quality.
5. Filtered rows based on different conditions.
6. Selected relevant columns for analysis.
7. Checked and removed duplicate records.
8. Created derived columns (`Price` and `total_amount`).
9. Saved the cleaned dataset as a new CSV file.
10. Converted the cleaned dataset into a Spark DataFrame for Databricks integration.

## Output Files

- `Week7_Pandas_Data_Exploration.ipynb`
- `cleaned_superstore.csv`

## Learning Outcomes

- Gained hands-on experience with Pandas DataFrames.
- Learned basic data exploration and cleaning techniques.
- Performed filtering, column selection, and duplicate removal.
- Created derived columns using existing data.
- Learned how Pandas integrates with Apache Spark in Databricks.
