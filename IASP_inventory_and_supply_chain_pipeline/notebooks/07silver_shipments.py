# Databricks notebook source
shipments_df = spark.table("workspace.bronze.shipments")

print("Total records:", shipments_df.count())
shipments_df.printSchema()

display(
    shipments_df
    .groupBy("shipment_status")
    .count()
)

# COMMAND ----------

display(
    shipments_df
    .groupBy("shipment_status")
    .count()
    .orderBy("shipment_status")
)

# COMMAND ----------

from pyspark.sql.functions import (
    col, trim, upper, when, lit, datediff
)

clean_shipments = (
    shipments_df
    .drop("ingestion_timestamp", "source_file")
    .withColumn("shipment_id", upper(trim(col("shipment_id"))))
    .withColumn("supplier_id", upper(trim(col("supplier_id"))))
    .withColumn("warehouse_id", upper(trim(col("warehouse_id"))))
    .withColumn("shipment_status", upper(trim(col("shipment_status"))))
)

# COMMAND ----------

shipments_with_duration = (
    clean_shipments
    .withColumn(
        "calculated_delay_days",
        when(
            col("delivery_date").isNotNull(),
            datediff(col("delivery_date"), col("shipment_date"))
        )
    )
)

# COMMAND ----------

shipments_checked = (
    shipments_with_duration
    .withColumn(
        "rejection_reason",
        when(
            col("shipment_id").isNull(),
            lit("MISSING_SHIPMENT_ID")
        )
        .when(
            col("supplier_id").isNull(),
            lit("MISSING_SUPPLIER_ID")
        )
        .when(
            col("warehouse_id").isNull(),
            lit("MISSING_WAREHOUSE_ID")
        )
        .when(
            col("shipment_date").isNull(),
            lit("MISSING_SHIPMENT_DATE")
        )
        .when(
            col("delivery_date").isNotNull()
            & (col("delivery_date") < col("shipment_date")),
            lit("DELIVERY_BEFORE_SHIPMENT")
        )
        .when(
            col("shipping_cost") < 0,
            lit("NEGATIVE_SHIPPING_COST")
        )
        .otherwise(lit(None))
    )
)

# COMMAND ----------

valid_shipments = (
    shipments_checked
    .filter(col("rejection_reason").isNull())
    .drop("rejection_reason", "delay_days")
    .withColumnRenamed(
        "calculated_delay_days",
        "delay_days"
    )
)

quarantine_shipments = (
    shipments_checked
    .filter(col("rejection_reason").isNotNull())
)

# COMMAND ----------

bronze_count = shipments_df.count()
valid_count = valid_shipments.count()
quarantine_count = quarantine_shipments.count()

print("Bronze records:", bronze_count)
print("Valid Silver records:", valid_count)
print("Quarantined records:", quarantine_count)
print("Reconciliation:", valid_count + quarantine_count)

# COMMAND ----------

(
    valid_shipments.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.silver.shipments")
)

(
    quarantine_shipments.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.quarantine.shipments")
)

print("Silver shipments table created")
print("Quarantine shipments table created")

# COMMAND ----------

display(
    spark.table("workspace.silver.shipments")
    .limit(10)
)

# COMMAND ----------

