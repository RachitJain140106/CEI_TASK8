# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Layer - Warehouses
# MAGIC
# MAGIC This notebook cleans and validates warehouse master data.
# MAGIC
# MAGIC ### Main transformations
# MAGIC - Standardize warehouse information
# MAGIC - Validate warehouse capacity
# MAGIC - Validate primary keys
# MAGIC - Separate invalid records into quarantine

# COMMAND ----------

from pyspark.sql.functions import col, trim, upper, when, lit

warehouses_df = spark.table("workspace.bronze.warehouses")

print("Bronze warehouse records:", warehouses_df.count())
warehouses_df.printSchema()

# COMMAND ----------

print(warehouses_df.columns)
display(warehouses_df.limit(10))

# COMMAND ----------

clean_warehouses = (
    warehouses_df
    .drop("ingestion_timestamp", "source_file")
    .withColumn("warehouse_id", upper(trim(col("warehouse_id"))))
    .withColumn("warehouse_name", trim(col("warehouse_name")))
    .withColumn("location_city", upper(trim(col("location_city"))))
    .withColumn("location_state", upper(trim(col("location_state"))))
    .withColumn("country", upper(trim(col("country"))))
    .withColumn("warehouse_type", upper(trim(col("warehouse_type"))))
    .withColumn("manager_name", trim(col("manager_name")))
    .withColumn("operational_status", upper(trim(col("operational_status"))))
)

# COMMAND ----------

warehouses_checked = (
    clean_warehouses
    .withColumn(
        "rejection_reason",
        when(
            col("warehouse_id").isNull(),
            lit("MISSING_WAREHOUSE_ID")
        )
        .when(
            col("warehouse_name").isNull(),
            lit("MISSING_WAREHOUSE_NAME")
        )
        .when(
            col("capacity") <= 0,
            lit("INVALID_CAPACITY")
        )
        .when(
            ~col("operational_status").isin("ACTIVE", "INACTIVE"),
            lit("INVALID_OPERATIONAL_STATUS")
        )
        .otherwise(lit(None))
    )
)

# COMMAND ----------

valid_warehouses = (
    warehouses_checked
    .filter(col("rejection_reason").isNull())
    .drop("rejection_reason")
)

quarantine_warehouses = (
    warehouses_checked
    .filter(col("rejection_reason").isNotNull())
)

# COMMAND ----------

bronze_count = warehouses_df.count()
valid_count = valid_warehouses.count()
quarantine_count = quarantine_warehouses.count()

print("Bronze records:", bronze_count)
print("Valid Silver records:", valid_count)
print("Quarantined records:", quarantine_count)
print("Reconciliation:", valid_count + quarantine_count)

# COMMAND ----------

(
    valid_warehouses.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.silver.warehouses")
)

(
    quarantine_warehouses.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.quarantine.warehouses")
)

print("Silver warehouses table created")
print("Quarantine warehouses table created")

# COMMAND ----------

display(
    spark.table("workspace.silver.warehouses")
)

# COMMAND ----------

