# Databricks notebook source
# MAGIC %md
# MAGIC # IASP - Inventory and Supply Chain Data Pipeline
# MAGIC
# MAGIC This project builds an end-to-end data pipeline for inventory and supply chain analytics.
# MAGIC
# MAGIC ### Pipeline
# MAGIC Raw CSV → Bronze → Silver → Gold → Power BI
# MAGIC
# MAGIC ### Technologies
# MAGIC - Azure Data Lake Storage Gen2
# MAGIC - Databricks
# MAGIC - Apache Spark / PySpark
# MAGIC - Delta Lake
# MAGIC - Power BI

# COMMAND ----------

# Source location in the Databricks managed volume
raw_path = "/Volumes/workspace/iasp/raw_files"
print("Raw data path:", raw_path)

# COMMAND ----------

files = dbutils.fs.ls(raw_path)
for file in files:
    print(file.name)

# COMMAND ----------

datasets = [
    "products",
    "inventory",
    "suppliers",
    "warehouses",
    "transactions",
    "shipments"
]
print("Number of source datasets:", len(datasets))

# COMMAND ----------

for dataset in datasets:
    file_path = f"{raw_path}/{dataset}.csv"
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(file_path)
    )
    print(f"{dataset}: {df.count()} rows, {len(df.columns)} columns")

# COMMAND ----------

