# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Layer - Raw Data Ingestion
# MAGIC
# MAGIC The Bronze layer ingests the source CSV files into Delta tables.
# MAGIC
# MAGIC The source data is preserved without applying business-level cleaning.  
# MAGIC Two metadata columns are added for traceability:
# MAGIC
# MAGIC - `ingestion_timestamp`
# MAGIC - `source_file`

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, input_file_name
raw_path = "/Volumes/workspace/iasp/raw_files"
datasets = [
    "products",
    "inventory",
    "suppliers",
    "warehouses",
    "transactions",
    "shipments"
]
print("Bronze ingestion setup completed")

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.bronze")

# COMMAND ----------

display(spark.sql("SHOW SCHEMAS IN workspace"))

# COMMAND ----------

for dataset in datasets:
    
    file_path = f"{raw_path}/{dataset}.csv"
    
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(file_path)
    )
    
    bronze_df = (
        df
        .withColumn("ingestion_timestamp", current_timestamp())
        .withColumn("source_file", df["_metadata.file_path"])
    )
    
    table_name = f"workspace.bronze.{dataset}"
    
    (
        bronze_df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable(table_name)
    )
    
    print(f"{dataset} loaded successfully")

# COMMAND ----------

for dataset in datasets:
    table_name = f"workspace.bronze.{dataset}"
    df = spark.table(table_name)

    print(
        f"{dataset}: "
        f"{df.count()} rows, "
        f"{len(df.columns)} columns"
    )

# COMMAND ----------

display(spark.table("workspace.bronze.products").limit(10))

# COMMAND ----------

print("===== BRONZE LAYER - RAW DATA INGESTION =====")

bronze_tables = [
    "products",
    "inventory",
    "suppliers",
    "warehouses",
    "transactions",
    "shipments"
]

for table in bronze_tables:
    count = spark.table(f"workspace.bronze.{table}").count()
    print(f"{table:<15} : {count} records")

# COMMAND ----------

