# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Layer - Transactions
# MAGIC
# MAGIC This notebook cleans and validates transaction data.
# MAGIC
# MAGIC ### Main transformations
# MAGIC - Standardize transaction fields
# MAGIC - Validate quantities and prices
# MAGIC - Recalculate total price
# MAGIC - Preserve valid transaction types
# MAGIC - Quarantine invalid records

# COMMAND ----------

from pyspark.sql.functions import (
    col, trim, upper, to_timestamp,
    when, lit, round
)

transactions_df = spark.table("workspace.bronze.transactions")

print("Bronze transaction records:", transactions_df.count())
transactions_df.printSchema()

# COMMAND ----------

clean_transactions = (
    transactions_df
    .drop("ingestion_timestamp", "source_file")
    .withColumn("transaction_id", upper(trim(col("transaction_id"))))
    .withColumn("product_id", upper(trim(col("product_id"))))
    .withColumn("warehouse_id", upper(trim(col("warehouse_id"))))
    .withColumn("supplier_id", upper(trim(col("supplier_id"))))
    .withColumn("transaction_type", upper(trim(col("transaction_type"))))
    .withColumn("channel", upper(trim(col("channel"))))
    .withColumn(
        "transaction_timestamp",
        to_timestamp(col("transaction_timestamp"))
    )
)

# COMMAND ----------

transactions_with_total = (
    clean_transactions
    .withColumn(
        "calculated_total_price",
        round(col("quantity") * col("unit_price"), 2)
    )
)

# COMMAND ----------

valid_transaction_types = [
    "IN",
    "OUT",
    "RETURN",
    "TRANSFER"
]

transactions_checked = (
    transactions_with_total
    .withColumn(
        "rejection_reason",
        when(
            col("transaction_id").isNull(),
            lit("MISSING_TRANSACTION_ID")
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
            col("quantity") <= 0,
            lit("INVALID_QUANTITY")
        )
        .when(
            col("unit_price") < 0,
            lit("INVALID_UNIT_PRICE")
        )
        .when(
            ~col("transaction_type").isin(valid_transaction_types),
            lit("INVALID_TRANSACTION_TYPE")
        )
        .otherwise(lit(None))
    )
)

# COMMAND ----------

valid_transactions = (
    transactions_checked
    .filter(col("rejection_reason").isNull())
    .drop("rejection_reason", "total_price")
    .withColumnRenamed(
        "calculated_total_price",
        "total_price"
    )
)

quarantine_transactions = (
    transactions_checked
    .filter(col("rejection_reason").isNotNull())
)

# COMMAND ----------

bronze_count = transactions_df.count()
valid_count = valid_transactions.count()
quarantine_count = quarantine_transactions.count()

print("Bronze records:", bronze_count)
print("Valid Silver records:", valid_count)
print("Quarantined records:", quarantine_count)
print("Reconciliation:", valid_count + quarantine_count)

# COMMAND ----------

display(
    valid_transactions
    .groupBy("transaction_type")
    .count()
    .orderBy("transaction_type")
)

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.quarantine")

print("Quarantine schema is ready")

# COMMAND ----------

(
    valid_transactions.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.silver.transactions")
)

(
    quarantine_transactions.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.quarantine.transactions")
)

print("Silver transactions table created")
print("Quarantine transactions table created")

# COMMAND ----------

print(
    "Silver transactions:",
    spark.table("workspace.silver.transactions").count()
)

print(
    "Quarantine transactions:",
    spark.table("workspace.quarantine.transactions").count()
)

display(
    spark.table("workspace.silver.transactions").limit(10)
)

# COMMAND ----------

