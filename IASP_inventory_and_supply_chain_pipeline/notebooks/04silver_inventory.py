# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Layer - Inventory
# MAGIC
# MAGIC This notebook cleans and validates inventory data from the Bronze layer.
# MAGIC
# MAGIC ### Main transformations
# MAGIC - Remove ingestion metadata
# MAGIC - Validate primary and foreign keys
# MAGIC - Validate stock quantities
# MAGIC - Calculate available stock
# MAGIC - Separate invalid records into a quarantine table
# MAGIC - Store trusted records in the Silver layer

# COMMAND ----------

from pyspark.sql.functions import col, trim, upper, to_date, when, lit

inventory_df = spark.table("workspace.bronze.inventory")

print("Total Bronze records:", inventory_df.count())
inventory_df.printSchema()

# COMMAND ----------

clean_inventory = (
    inventory_df
    .drop("ingestion_timestamp", "source_file")
    .withColumn("inventory_id", upper(trim(col("inventory_id"))))
    .withColumn("product_id", upper(trim(col("product_id"))))
    .withColumn("warehouse_id", upper(trim(col("warehouse_id"))))
    .withColumn("last_restock_date", to_date(col("last_restock_date")))
    .withColumn("last_updated", to_date(col("last_updated")))
)

# COMMAND ----------

inventory_with_stock = (
    clean_inventory
    .withColumn(
        "available_stock",
        col("stock_quantity")
        - col("reserved_quantity")
        - col("damaged_quantity")
    )
)

# COMMAND ----------

inventory_checked = (
    inventory_with_stock
    .withColumn(
        "rejection_reason",
        when(
            col("inventory_id").isNull(),
            lit("MISSING_INVENTORY_ID")
        )
        .when(
            col("product_id").isNull(),
            lit("MISSING_PRODUCT_ID")
        )
        .when(
            col("warehouse_id").isNull(),
            lit("MISSING_WAREHOUSE_ID")
        )
        .when(
            col("stock_quantity") < 0,
            lit("NEGATIVE_STOCK_QUANTITY")
        )
        .when(
            col("reserved_quantity") < 0,
            lit("NEGATIVE_RESERVED_QUANTITY")
        )
        .when(
            col("damaged_quantity") < 0,
            lit("NEGATIVE_DAMAGED_QUANTITY")
        )
        .when(
            col("available_stock") < 0,
            lit("NEGATIVE_AVAILABLE_STOCK")
        )
        .otherwise(lit(None))
    )
)

# COMMAND ----------

valid_inventory = (
    inventory_checked
    .filter(col("rejection_reason").isNull())
    .drop("rejection_reason")
)

quarantine_inventory = (
    inventory_checked
    .filter(col("rejection_reason").isNotNull())
)

# COMMAND ----------

bronze_count = inventory_df.count()
valid_count = valid_inventory.count()
quarantine_count = quarantine_inventory.count()

print("Bronze records:", bronze_count)
print("Valid Silver records:", valid_count)
print("Quarantined records:", quarantine_count)
print("Reconciliation check:", valid_count + quarantine_count)

# COMMAND ----------

display(
    quarantine_inventory
    .groupBy("rejection_reason")
    .count()
    .orderBy(col("count").desc())
)

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.quarantine")

(
    valid_inventory.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.silver.inventory")
)

(
    quarantine_inventory.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.quarantine.inventory")
)

print("Silver inventory table created")
print("Quarantine inventory table created")

# COMMAND ----------

print(
    "Silver inventory:",
    spark.table("workspace.silver.inventory").count()
)

print(
    "Quarantine inventory:",
    spark.table("workspace.quarantine.inventory").count()
)

display(
    spark.table("workspace.silver.inventory").limit(10)
)

# COMMAND ----------

