# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Layer - Products Dimension
# MAGIC
# MAGIC This notebook cleans and transforms the Bronze products data.
# MAGIC
# MAGIC Since multiple versions of each product are available, the product history is preserved using Slowly Changing Dimension Type 2 (SCD Type 2).
# MAGIC
# MAGIC ### Main transformations
# MAGIC - Remove ingestion metadata
# MAGIC - Standardize text fields
# MAGIC - Validate product records
# MAGIC - Preserve historical product versions
# MAGIC - Generate start date, end date, and current flag

# COMMAND ----------

products_df = spark.table("workspace.bronze.products")

print("Total rows:", products_df.count())
print("Total columns:", len(products_df.columns))

products_df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import count

product_counts = (
    products_df
    .groupBy("product_id")
    .agg(count("*").alias("number_of_versions"))
    .orderBy("product_id")
)

display(product_counts.limit(20))

# COMMAND ----------

print(
    "Unique products:",
    products_df.select("product_id").distinct().count()
)

# COMMAND ----------

from pyspark.sql.functions import col, trim, upper, to_timestamp

clean_products = (
    products_df
    .drop("ingestion_timestamp", "source_file")
    .filter(col("product_id").isNotNull())
    .withColumn("product_id", upper(trim(col("product_id"))))
    .withColumn("product_name", trim(col("product_name")))
    .withColumn("category", upper(trim(col("category"))))
    .withColumn("brand", upper(trim(col("brand"))))
    .withColumn("currency", upper(trim(col("currency"))))
    .withColumn("product_status", upper(trim(col("product_status"))))
    .withColumn("last_updated", to_timestamp(col("last_updated")))
)

# COMMAND ----------

valid_products = (
    clean_products
    .filter(col("cost_price") >= 0)
    .filter(col("selling_price") >= 0)
    .filter(col("last_updated").isNotNull())
)

# COMMAND ----------

from pyspark.sql.window import Window
from pyspark.sql.functions import lead, row_number, when, lit, date_sub

product_window = (
    Window
    .partitionBy("product_id")
    .orderBy("last_updated")
)

latest_window = (
    Window
    .partitionBy("product_id")
    .orderBy(col("last_updated").desc())
)

silver_products = (
    valid_products
    .withColumn(
        "start_date",
        col("last_updated").cast("date")
    )
    .withColumn(
        "next_start_date",
        lead(col("last_updated").cast("date")).over(product_window)
    )
    .withColumn(
        "end_date",
        when(
            col("next_start_date").isNotNull(),
            date_sub(col("next_start_date"), 1)
        )
    )
    .withColumn(
        "version_rank",
        row_number().over(latest_window)
    )
    .withColumn(
        "current_flag",
        when(col("version_rank") == 1, lit("Y"))
        .otherwise(lit("N"))
    )
    .drop("next_start_date", "version_rank")
)

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.silver")

(
    silver_products.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.silver.products")
)

print("Silver products table created successfully")

# COMMAND ----------

silver_df = spark.table("workspace.silver.products")

print("Total historical records:", silver_df.count())

print(
    "Unique products:",
    silver_df.select("product_id").distinct().count()
)

print(
    "Current records:",
    silver_df.filter(col("current_flag") == "Y").count()
)

# COMMAND ----------

display(
    silver_df
    .filter(col("product_id") == "P1000")
    .orderBy("start_date")
)

# COMMAND ----------

