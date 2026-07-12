# Databricks notebook source
# MAGIC %md
# MAGIC # Gold Layer - Inventory Analytics
# MAGIC
# MAGIC This notebook creates business-ready inventory datasets.
# MAGIC
# MAGIC ### Gold tables
# MAGIC 1. Inventory Snapshot - Current stock position and inventory value
# MAGIC 2. Low Stock Alert - Products requiring replenishment

# COMMAND ----------

from pyspark.sql.functions import col, when, lit, round

inventory = spark.table("workspace.silver.inventory")

products = (
    spark.table("workspace.silver.products")
    .filter(col("current_flag") == "Y")
)

warehouses = spark.table("workspace.silver.warehouses")

print("Inventory:", inventory.count())
print("Current products:", products.count())
print("Warehouses:", warehouses.count())

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.gold")

# COMMAND ----------

inventory_snapshot = (
    inventory.alias("i")
    .join(
        products.alias("p"),
        col("i.product_id") == col("p.product_id"),
        "inner"
    )
    .join(
        warehouses.alias("w"),
        col("i.warehouse_id") == col("w.warehouse_id"),
        "inner"
    )
    .select(
        col("i.inventory_id"),
        col("i.product_id"),
        col("p.product_name"),
        col("p.category"),
        col("i.warehouse_id"),
        col("w.warehouse_name"),
        col("w.location_city"),
        col("i.stock_quantity"),
        col("i.reserved_quantity"),
        col("i.damaged_quantity"),
        col("i.available_stock"),
        col("p.selling_price"),
        round(
            col("i.available_stock") * col("p.selling_price"),
            2
        ).alias("inventory_value"),
        col("p.reorder_level")
    )
)

# COMMAND ----------

print("Inventory snapshot records:", inventory_snapshot.count())

display(inventory_snapshot.limit(10))

# COMMAND ----------

low_stock_alert = (
    inventory_snapshot
    .filter(col("available_stock") < col("reorder_level"))
    .withColumn(
        "alert_level",
        when(
            col("available_stock") == 0,
            lit("CRITICAL")
        )
        .when(
            col("available_stock") < col("reorder_level") * 0.25,
            lit("HIGH")
        )
        .otherwise(lit("MEDIUM"))
    )
)

# COMMAND ----------

display(
    low_stock_alert
    .groupBy("alert_level")
    .count()
    .orderBy("alert_level")
)

# COMMAND ----------

(
    inventory_snapshot.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.gold.inventory_snapshot")
)

(
    low_stock_alert.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.gold.low_stock_alert")
)

print("Gold inventory_snapshot created")
print("Gold low_stock_alert created")

# COMMAND ----------

from pyspark.sql.functions import sum as spark_sum

total_inventory_value = (
    inventory_snapshot
    .agg(
        round(
            spark_sum("inventory_value"),
            2
        ).alias("total_inventory_value")
    )
)

display(total_inventory_value)

print("Low stock records:", low_stock_alert.count())

# COMMAND ----------

