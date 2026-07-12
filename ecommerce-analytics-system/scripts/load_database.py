import os
import sqlite3
import pandas as pd

# =====================================================
# Configuration
# =====================================================

DATABASE = "database/ecommerce.db"
SCHEMA_FILE = "sql/schema.sql"

# Create database folder if it doesn't exist
os.makedirs("database", exist_ok=True)

# =====================================================
# Load Cleaned CSV Files
# =====================================================

customers = pd.read_csv("data/cleaned/customers_clean.csv")
products = pd.read_csv("data/cleaned/products_clean.csv")
orders = pd.read_csv("data/cleaned/orders_clean.csv")
order_items = pd.read_csv("data/cleaned/order_items_clean.csv")

print("✅ Cleaned CSV files loaded successfully.")

# =====================================================
# Connect to SQLite
# =====================================================

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

print("✅ Connected to SQLite database.")

# Enable Foreign Key Constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# =====================================================
# Create Database Schema
# =====================================================

with open(SCHEMA_FILE, "r") as file:
    schema = file.read()

cursor.executescript(schema)

print("✅ Database schema created successfully.")

# =====================================================
# Load Data into Tables
# =====================================================

customers.to_sql(
    "customers",
    connection,
    if_exists="append",
    index=False
)

products.to_sql(
    "products",
    connection,
    if_exists="append",
    index=False
)

orders.to_sql(
    "orders",
    connection,
    if_exists="append",
    index=False
)

order_items.to_sql(
    "order_items",
    connection,
    if_exists="append",
    index=False
)

print("✅ Data inserted successfully.")

# =====================================================
# Verify Row Counts
# =====================================================

print("\n==============================")
print("TABLE ROW COUNTS")
print("==============================")

tables = [
    "customers",
    "products",
    "orders",
    "order_items"
]

for table in tables:

    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]

    print(f"{table:<15} : {count}")

# =====================================================
# Verify Foreign Key Relationships
# =====================================================

print("\n==============================")
print("FOREIGN KEY CHECK")
print("==============================")

cursor.execute("""
SELECT COUNT(*)
FROM orders o
LEFT JOIN customers c
ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
""")

invalid_orders = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM order_items oi
LEFT JOIN orders o
ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;
""")

invalid_order_items = cursor.fetchone()[0]

print(f"Orders with invalid customer_id : {invalid_orders}")
print(f"Order Items with invalid order_id : {invalid_order_items}")

# =====================================================
# Commit & Close
# =====================================================

connection.commit()
connection.close()

print("\n✅ SQLite database created successfully!")
print(f"Database Location : {DATABASE}")