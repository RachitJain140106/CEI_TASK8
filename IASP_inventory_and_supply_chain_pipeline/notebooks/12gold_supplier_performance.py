# Databricks notebook source
# MAGIC %md
# MAGIC # Gold Layer - Supplier Performance
# MAGIC
# MAGIC This notebook evaluates supplier performance using shipment data.
# MAGIC
# MAGIC ### Metrics
# MAGIC - Total shipments
# MAGIC - Delivered shipments
# MAGIC - Average delivery duration
# MAGIC - Delayed shipments
# MAGIC - Performance category
# MAGIC
# MAGIC Shipments without a valid delivery date are included in shipment counts but excluded from average delivery calculations.

# COMMAND ----------

from pyspark.sql.functions import (
    col, count, avg, sum as spark_sum,
    when, round
)

shipments = spark.table("workspace.silver.shipments")
suppliers = spark.table("workspace.silver.suppliers")

print("Shipments:", shipments.count())
print("Valid suppliers:", suppliers.count())

# COMMAND ----------

shipment_metrics = (
    shipments
    .groupBy("supplier_id")
    .agg(
        count("*").alias("total_shipments"),

        spark_sum(
            when(
                col("shipment_status") == "DELIVERED", 1
            ).otherwise(0)
        ).alias("delivered_shipments"),

        spark_sum(
            when(
                col("shipment_status") == "DELAYED", 1
            ).otherwise(0)
        ).alias("delayed_shipments"),

        round(
            avg("delay_days"),
            2
        ).alias("avg_delay_days")
    )
)

# COMMAND ----------

supplier_performance = (
    shipment_metrics.alias("m")
    .join(
        suppliers.alias("s"),
        col("m.supplier_id") == col("s.supplier_id"),
        "left"
    )
    .select(
        col("m.supplier_id"),
        col("s.supplier_name"),
        col("s.country"),
        col("s.rating"),
        col("m.total_shipments"),
        col("m.delivered_shipments"),
        col("m.delayed_shipments"),
        col("m.avg_delay_days")
    )
)

# COMMAND ----------

bronze_supplier_names = (
    spark.table("workspace.bronze.suppliers")
    .select(
        "supplier_id",
        "supplier_name"
    )
    .dropDuplicates(["supplier_id"])
)

# COMMAND ----------

supplier_performance = (
    shipment_metrics
    .join(
        bronze_supplier_names,
        "supplier_id",
        "left"
    )
)

# COMMAND ----------

supplier_performance = (
    supplier_performance
    .withColumn(
        "performance_category",
        when(
            col("avg_delay_days") <= 3,
            "EXCELLENT"
        )
        .when(
            col("avg_delay_days") <= 7,
            "GOOD"
        )
        .otherwise("NEEDS IMPROVEMENT")
    )
)

# COMMAND ----------

display(
    supplier_performance
    .orderBy("avg_delay_days")
)

# COMMAND ----------

(
    supplier_performance.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.gold.supplier_performance")
)

print("Gold supplier_performance created successfully")

# COMMAND ----------

display(
    spark.sql("SHOW TABLES IN workspace.gold")
)

# COMMAND ----------

