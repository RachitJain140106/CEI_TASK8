# Databricks notebook source
gold_tables = [
    "inventory_snapshot",
    "low_stock_alert",
    "product_movement",
    "sales_summary",
    "sales_trend",
    "supplier_performance"
]

print("===== GOLD LAYER SUMMARY =====")

for table in gold_tables:
    df = spark.table(f"workspace.gold.{table}")
    print(f"{table}: {df.count()} rows")

# COMMAND ----------

from pyspark.sql.functions import (
    sum as spark_sum,
    round,
    avg
)

inventory_snapshot = spark.table("workspace.gold.inventory_snapshot")
low_stock = spark.table("workspace.gold.low_stock_alert")
sales_summary = spark.table("workspace.gold.sales_summary")
supplier_performance = spark.table("workspace.gold.supplier_performance")

total_inventory_value = (
    inventory_snapshot
    .agg(round(spark_sum("inventory_value"), 2))
    .first()[0]
)

total_revenue = (
    sales_summary
    .agg(round(spark_sum("total_revenue"), 2))
    .first()[0]
)

total_units_sold = (
    sales_summary
    .agg(spark_sum("total_units_sold"))
    .first()[0]
)

average_delay = (
    supplier_performance
    .agg(round(avg("avg_delay_days"), 2))
    .first()[0]
)

print("===== BUSINESS KPI SUMMARY =====")
print("Total Revenue:", total_revenue)
print("Total Units Sold:", total_units_sold)
print("Total Inventory Value:", total_inventory_value)
print("Low Stock Alerts:", low_stock.count())
print("Average Delivery Duration:", average_delay)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VOLUME IF NOT EXISTS workspace.iasp.powerbi_exports;

# COMMAND ----------

export_path = "/Volumes/workspace/iasp/powerbi_exports"

for table in gold_tables:

    df = spark.table(f"workspace.gold.{table}")

    (
        df
        .coalesce(1)
        .write
        .mode("overwrite")
        .option("header", "true")
        .csv(f"{export_path}/{table}")
    )

    print(f"{table} exported")

# COMMAND ----------

display(dbutils.fs.ls(export_path))

# COMMAND ----------

for table in gold_tables:
    print(f"\n--- {table} ---")
    
    files = dbutils.fs.ls(
        f"/Volumes/workspace/iasp/powerbi_exports/{table}"
    )
    
    for file in files:
        print(file.name, file.size)

# COMMAND ----------

