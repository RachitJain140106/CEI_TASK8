# Databricks notebook source
# MAGIC %md
# MAGIC # Gold Layer - Sales and Product Movement Analytics
# MAGIC
# MAGIC This notebook creates business-ready datasets from validated transaction data.
# MAGIC
# MAGIC ### Gold tables
# MAGIC 1. Product Movement - Stock inflow and outflow by product
# MAGIC 2. Sales Summary - Units sold and revenue by product
# MAGIC 3. Sales Trend - Monthly revenue trend

# COMMAND ----------

from pyspark.sql.functions import (
    col, when, sum as spark_sum,
    year, month, round
)

transactions = spark.table("workspace.silver.transactions")

products = (
    spark.table("workspace.silver.products")
    .filter(col("current_flag") == "Y")
)

print("Transactions:", transactions.count())
print("Current products:", products.count())

# COMMAND ----------

product_movement = (
    transactions
    .groupBy("product_id")
    .agg(
        spark_sum(
            when(
                col("transaction_type") == "IN",
                col("quantity")
            ).otherwise(0)
        ).alias("total_stock_in"),

        spark_sum(
            when(
                col("transaction_type") == "OUT",
                col("quantity")
            ).otherwise(0)
        ).alias("total_stock_out")
    )
    .withColumn(
        "net_movement",
        col("total_stock_in") - col("total_stock_out")
    )
    .join(
        products.select(
            "product_id",
            "product_name",
            "category"
        ),
        "product_id",
        "left"
    )
)

# COMMAND ----------

sales_transactions = (
    transactions
    .filter(col("transaction_type") == "OUT")
)

# COMMAND ----------

sales_summary = (
    sales_transactions
    .groupBy("product_id")
    .agg(
        spark_sum("quantity").alias("total_units_sold"),

        round(
            spark_sum("total_price"),
            2
        ).alias("total_revenue")
    )
    .join(
        products.select(
            "product_id",
            "product_name",
            "category",
            "brand"
        ),
        "product_id",
        "left"
    )
)

# COMMAND ----------

sales_trend = (
    sales_transactions
    .groupBy(
        year("transaction_timestamp").alias("year"),
        month("transaction_timestamp").alias("month")
    )
    .agg(
        round(
            spark_sum("total_price"),
            2
        ).alias("monthly_revenue")
    )
    .orderBy("year", "month")
)

# COMMAND ----------

(
    product_movement.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.gold.product_movement")
)

(
    sales_summary.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.gold.sales_summary")
)

(
    sales_trend.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.gold.sales_trend")
)

print("Gold product_movement created")
print("Gold sales_summary created")
print("Gold sales_trend created")

# COMMAND ----------

total_revenue = (
    sales_summary
    .agg(
        round(
            spark_sum("total_revenue"),
            2
        ).alias("total_revenue")
    )
)

total_units = (
    sales_summary
    .agg(
        spark_sum("total_units_sold")
        .alias("total_units_sold")
    )
)

display(total_revenue)
display(total_units)

# COMMAND ----------

