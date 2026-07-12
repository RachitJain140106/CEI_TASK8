# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Layer - Data Quality Validation
# MAGIC
# MAGIC This notebook validates the Silver layer before business-level Gold tables are created.
# MAGIC
# MAGIC ### Checks performed
# MAGIC - Table row counts
# MAGIC - Primary key validation
# MAGIC - Duplicate checks
# MAGIC - Foreign key integrity
# MAGIC - Shipment status consistency
# MAGIC - Bronze, Silver, and Quarantine reconciliation

# COMMAND ----------

print("SILVER TABLES")
display(spark.sql("SHOW TABLES IN workspace.silver"))

print("QUARANTINE TABLES")
display(spark.sql("SHOW TABLES IN workspace.quarantine"))

# COMMAND ----------

primary_keys = {
    "inventory": "inventory_id",
    "transactions": "transaction_id",
    "suppliers": "supplier_id",
    "shipments": "shipment_id",
    "warehouses": "warehouse_id"
}

for table, key in primary_keys.items():

    df = spark.table(f"workspace.silver.{table}")

    duplicate_count = (
        df.groupBy(key)
        .count()
        .filter("count > 1")
        .count()
    )

    print(f"{table}: {duplicate_count} duplicate {key} values")

# COMMAND ----------

silver_tables = [
    "products",
    "inventory",
    "transactions",
    "suppliers",
    "shipments",
    "warehouses"
]

for table in silver_tables:
    count = spark.table(f"workspace.silver.{table}").count()
    print(f"{table}: {count} rows")

# COMMAND ----------

primary_keys = {
    "inventory": "inventory_id",
    "transactions": "transaction_id",
    "suppliers": "supplier_id",
    "shipments": "shipment_id",
    "warehouses": "warehouse_id"
}

for table, key in primary_keys.items():

    df = spark.table(f"workspace.silver.{table}")

    duplicate_count = (
        df.groupBy(key)
        .count()
        .filter("count > 1")
        .count()
    )

    print(f"{table}: {duplicate_count} duplicate {key} values")

# COMMAND ----------

from pyspark.sql.functions import col

current_products = (
    spark.table("workspace.silver.products")
    .filter(col("current_flag") == "Y")
)

duplicate_current_products = (
    current_products
    .groupBy("product_id")
    .count()
    .filter("count > 1")
    .count()
)

print(
    "Duplicate current product records:",
    duplicate_current_products
)

# COMMAND ----------

shipments = spark.table("workspace.silver.shipments")

delivered_without_date = (
    shipments
    .filter(
        (col("shipment_status") == "DELIVERED") &
        (col("delivery_date").isNull())
    )
)

print(
    "Delivered shipments without delivery date:",
    delivered_without_date.count()
)

# COMMAND ----------

products = (
    spark.table("workspace.silver.products")
    .filter(col("current_flag") == "Y")
    .select("product_id")
)

transactions = spark.table("workspace.silver.transactions")

orphan_transactions = (
    transactions
    .join(products, "product_id", "left_anti")
)

print(
    "Transactions with unknown product:",
    orphan_transactions.count()
)

# COMMAND ----------

inventory = spark.table("workspace.silver.inventory")

orphan_inventory_products = (
    inventory
    .join(products, "product_id", "left_anti")
)

print(
    "Inventory rows with unknown product:",
    orphan_inventory_products.count()
)

# COMMAND ----------

warehouses = (
    spark.table("workspace.silver.warehouses")
    .select("warehouse_id")
)

orphan_inventory_warehouses = (
    inventory
    .join(warehouses, "warehouse_id", "left_anti")
)

print(
    "Inventory rows with unknown warehouse:",
    orphan_inventory_warehouses.count()
)

# COMMAND ----------

all_supplier_keys = (
    spark.table("workspace.bronze.suppliers")
    .select("supplier_id")
    .distinct()
)

shipments = spark.table("workspace.silver.shipments")

orphan_shipments = (
    shipments
    .join(all_supplier_keys, "supplier_id", "left_anti")
)

print(
    "Shipments with unknown supplier:",
    orphan_shipments.count()
)

# COMMAND ----------

print("===== SILVER LAYER VALIDATION =====")
print("Current products:", current_products.count())
print("Inventory records:", inventory.count())
print("Transaction records:", transactions.count())
print("Supplier records:", spark.table("workspace.silver.suppliers").count())
print("Shipment records:", shipments.count())
print("Warehouse records:", warehouses.count())

print("\n===== INTEGRITY CHECKS =====")
print("Duplicate current products:", duplicate_current_products)
print("Unknown transaction products:", orphan_transactions.count())
print("Unknown inventory products:", orphan_inventory_products.count())
print("Unknown inventory warehouses:", orphan_inventory_warehouses.count())
print("Unknown shipment suppliers:", orphan_shipments.count())
print("Delivered shipments missing date:", delivered_without_date.count())

# COMMAND ----------

