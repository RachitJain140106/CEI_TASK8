# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Layer - Suppliers
# MAGIC
# MAGIC This notebook cleans and validates supplier master data.
# MAGIC
# MAGIC ### Main transformations
# MAGIC - Standardize supplier information
# MAGIC - Validate email addresses
# MAGIC - Validate supplier ratings
# MAGIC - Validate lead time and contract dates
# MAGIC - Separate invalid records into quarantine

# COMMAND ----------

from pyspark.sql.functions import (
    col, trim, upper, lower, to_date,
    when, lit
)

suppliers_df = spark.table("workspace.bronze.suppliers")

print("Bronze supplier records:", suppliers_df.count())
suppliers_df.printSchema()

# COMMAND ----------

clean_suppliers = (
    suppliers_df
    .drop("ingestion_timestamp", "source_file")
    .withColumn("supplier_id", upper(trim(col("supplier_id"))))
    .withColumn("supplier_name", trim(col("supplier_name")))
    .withColumn("country", upper(trim(col("country"))))
    .withColumn("region", upper(trim(col("region"))))
    .withColumn("contact_name", trim(col("contact_name")))
    .withColumn("contact_email", lower(trim(col("contact_email"))))
    .withColumn("contract_start_date", to_date(col("contract_start_date")))
    .withColumn("contract_end_date", to_date(col("contract_end_date")))
)

# COMMAND ----------

email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

suppliers_checked = (
    clean_suppliers
    .withColumn(
        "rejection_reason",
        when(
            col("supplier_id").isNull(),
            lit("MISSING_SUPPLIER_ID")
        )
        .when(
            col("supplier_name").isNull(),
            lit("MISSING_SUPPLIER_NAME")
        )
        .when(
            col("contact_email").isNotNull() &
            (~col("contact_email").rlike(email_pattern)),
            lit("INVALID_EMAIL")
        )
        .when(
            ~col("rating").between(1, 5),
            lit("INVALID_RATING")
        )
        .when(
            col("lead_time_days") < 0,
            lit("INVALID_LEAD_TIME")
        )
        .when(
            col("contract_end_date").isNotNull() &
            (col("contract_end_date") < col("contract_start_date")),
            lit("INVALID_CONTRACT_DATES")
        )
        .otherwise(lit(None))
    )
)

# COMMAND ----------

valid_suppliers = (
    suppliers_checked
    .filter(col("rejection_reason").isNull())
    .drop("rejection_reason")
)

quarantine_suppliers = (
    suppliers_checked
    .filter(col("rejection_reason").isNotNull())
)

# COMMAND ----------

bronze_count = suppliers_df.count()
valid_count = valid_suppliers.count()
quarantine_count = quarantine_suppliers.count()

print("Bronze records:", bronze_count)
print("Valid Silver records:", valid_count)
print("Quarantined records:", quarantine_count)
print("Reconciliation:", valid_count + quarantine_count)

# COMMAND ----------

(
    valid_suppliers.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.silver.suppliers")
)

(
    quarantine_suppliers.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.quarantine.suppliers")
)

print("Silver suppliers table created")
print("Quarantine suppliers table created")

# COMMAND ----------

display(
    spark.table("workspace.silver.suppliers")
)

# COMMAND ----------

