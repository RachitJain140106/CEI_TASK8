import pandas as pd
import os
import re

# -----------------------------
# Create cleaned folder
# -----------------------------

os.makedirs("data/cleaned", exist_ok=True)

# -----------------------------
# Load Raw CSV Files
# -----------------------------

customers_df = pd.read_csv("data/raw/customers.csv")

products_df = pd.read_csv("data/raw/products.csv")

orders_df = pd.read_csv("data/raw/orders.csv")

order_items_df = pd.read_csv("data/raw/order_items.csv")

print("Raw datasets loaded successfully.\n")

issues = {
    "invalid_emails": 0,
    "duplicate_customers": 0,
    "duplicate_products": 0,
    "duplicate_orders": 0,
    "duplicate_order_items": 0,
    "null_customer_ids": 0,
    "fixed_dates": 0,
    "invalid_order_references": 0,
    "negative_quantities": 0
}

def validate_emails(df):

    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    invalid_ids = []

    for _, row in df.iterrows():

        email = str(row["email"])

        if re.match(pattern, email) is None:
            invalid_ids.append(row["customer_id"])

    return invalid_ids


def clean_customers():

    global customers_df

    before = len(customers_df)

    customers_df.drop_duplicates(inplace=True)

    issues["duplicate_customers"] = before - len(customers_df)

    invalid = validate_emails(customers_df)

    issues["invalid_emails"] = len(invalid)

    for cid in invalid:

        customers_df.loc[
            customers_df.customer_id == cid,
            "email"
        ] = f"user{cid}@example.com"

    customers_df["registration_date"] = pd.to_datetime(
        customers_df["registration_date"]
    )

    print("Customers cleaned.")

def clean_products():

    global products_df

    before = len(products_df)

    products_df.drop_duplicates(inplace=True)

    issues["duplicate_products"] = before - len(products_df)

    products_df["product_name"] = (

        products_df["product_name"]

        .str.strip()

        .str.title()

    )

    print("Products cleaned.")

# -----------------------------
# Clean Orders
# -----------------------------

def clean_orders():

    global orders_df

    # Remove duplicate orders
    before = len(orders_df)

    orders_df.drop_duplicates(inplace=True)

    issues["duplicate_orders"] = before - len(orders_df)

    # Count NULL customer IDs
    issues["null_customer_ids"] = orders_df["customer_id"].isna().sum()

    # Remove rows with NULL customer_id
    orders_df = orders_df.dropna(subset=["customer_id"])

    # Convert customer_id to integer
    orders_df["customer_id"] = orders_df["customer_id"].astype(int)

    # Fix mixed date formats
    fixed_dates = []

    for date in orders_df["order_date"]:

        try:
            parsed = pd.to_datetime(date, format="%Y-%m-%d %H:%M:%S")

        except:

            parsed = pd.to_datetime(date, format="%d-%m-%Y %H:%M:%S")

            issues["fixed_dates"] += 1

        fixed_dates.append(parsed)

    orders_df["order_date"] = fixed_dates

    print("Orders cleaned.")

# -----------------------------
# Clean Order Items
# -----------------------------

def clean_order_items():

    global order_items_df

    before = len(order_items_df)

    order_items_df.drop_duplicates(inplace=True)

    issues["duplicate_order_items"] = before - len(order_items_df)

    # Count negative quantities
    issues["negative_quantities"] = (
        order_items_df["quantity"] < 0
    ).sum()

    # Remove negative quantities
    order_items_df = order_items_df[
        order_items_df["quantity"] > 0
    ]

    print("Order Items cleaned.")

# -----------------------------
# Referential Integrity
# -----------------------------

def check_referential_integrity():

    global order_items_df

    valid_orders = set(
        orders_df["order_id"]
    )

    invalid = order_items_df[
        ~order_items_df["order_id"].isin(valid_orders)
    ]

    issues["invalid_order_references"] = len(invalid)

    order_items_df = order_items_df[
        order_items_df["order_id"].isin(valid_orders)
    ]

    print("Referential integrity checked.")

# -----------------------------
# Save Cleaned Data
# -----------------------------

def save_cleaned_data():

    customers_df.to_csv(
        "data/cleaned/customers_clean.csv",
        index=False
    )

    products_df.to_csv(
        "data/cleaned/products_clean.csv",
        index=False
    )

    orders_df.to_csv(
        "data/cleaned/orders_clean.csv",
        index=False
    )

    order_items_df.to_csv(
        "data/cleaned/order_items_clean.csv",
        index=False
    )

    print("Cleaned CSV files saved.")

# -----------------------------
# Cleaning Report
# -----------------------------

def print_report():

    print("\n" + "="*50)
    print("DATA CLEANING REPORT")
    print("="*50)

    for key, value in issues.items():
        print(f"{key:30} : {value}")



# -----------------------------
# Execute Cleaning
# -----------------------------

if __name__ == "__main__":

    clean_customers()

    clean_products()

    clean_orders()

    clean_order_items()

    check_referential_integrity()

    save_cleaned_data()

    print_report()

    print("\nCleaning completed successfully!")