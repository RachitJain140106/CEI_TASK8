import pandas as pd
import numpy as np
import random
import os

from faker import Faker
from datetime import datetime, timedelta

# -----------------------------
# Configuration
# -----------------------------

NUM_CUSTOMERS = 500
NUM_PRODUCTS = 500
NUM_ORDERS = 500
NUM_ORDER_ITEMS = 1000

random.seed(42)
np.random.seed(42)
Faker.seed(42)

fake = Faker("en_IN")

# Create raw data folder
os.makedirs("data/raw", exist_ok=True)

# -----------------------------
# Generate Customers
# -----------------------------

customer_types = ["REGULAR", "PREMIUM", "VIP"]

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    customers.append({

        "customer_id": customer_id,

        "customer_name": fake.name(),

        "email": fake.email(),

        "registration_date": fake.date_between(
            start_date="-2y",
            end_date="today"
        ),

        "customer_type": random.choice(customer_types)

    })

customers_df = pd.DataFrame(customers)

# Introduce 2% invalid emails

invalid_count = int(0.02 * NUM_CUSTOMERS)

invalid_indices = random.sample(
    list(customers_df.index),
    invalid_count
)

for idx in invalid_indices:

    email = customers_df.loc[idx, "email"]

    if random.random() < 0.5:
        customers_df.loc[idx, "email"] = email.replace("@", "")
    else:
        customers_df.loc[idx, "email"] = email.split("@")[0] + "@"

# -----------------------------
# Generate Products
# -----------------------------

catalog = {

    "Electronics": [
        "Laptop",
        "Keyboard",
        "Mouse",
        "Monitor",
        "Headphones",
        "Camera"
    ],

    "Books": [
        "Novel",
        "Biography",
        "Dictionary",
        "Magazine",
        "Comics"
    ],

    "Clothing": [
        "T-Shirt",
        "Jeans",
        "Shoes",
        "Jacket",
        "Hoodie"
    ],

    "Home": [
        "Chair",
        "Table",
        "Lamp",
        "Curtains",
        "Sofa"
    ]

}

products = []

for product_id in range(1, NUM_PRODUCTS + 1):

    category = random.choice(list(catalog.keys()))

    product_name = random.choice(catalog[category])

    products.append({

        "product_id": product_id,

        "product_name": product_name,

        "category": category,

        "subcategory": category,

        "cost_price": round(
            random.uniform(100, 5000),
            2
        )

    })

products_df = pd.DataFrame(products)

# Introduce mixed case & extra spaces

dirty_count = int(0.05 * NUM_PRODUCTS)

dirty_indices = random.sample(
    list(products_df.index),
    dirty_count
)

for idx in dirty_indices:

    name = products_df.loc[idx, "product_name"]

    option = random.randint(1, 4)

    if option == 1:
        name = " " + name

    elif option == 2:
        name = name + " "

    elif option == 3:
        name = name.upper()

    else:
        name = name.lower()

    products_df.loc[idx, "product_name"] = name


# -----------------------------
# Generate Orders
# -----------------------------

order_status = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]

regions = [
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST"
]

orders = []

for order_id in range(1, NUM_ORDERS + 1):

    customer_id = random.randint(1, NUM_CUSTOMERS)

    # 5% NULL customer_id
    if random.random() < 0.05:
        customer_id = None

    order_date = fake.date_time_between(
        start_date="-1y",
        end_date="now"
    )

    # 5% wrong date format
    if random.random() < 0.05:
        order_date = order_date.strftime("%d-%m-%Y %H:%M:%S")
    else:
        order_date = order_date.strftime("%Y-%m-%d %H:%M:%S")

    orders.append({

        "order_id": order_id,

        "customer_id": customer_id,

        "order_date": order_date,

        "status": random.choice(order_status),

        "region_code": random.choice(regions)

    })

orders_df = pd.DataFrame(orders)

# -----------------------------
# Generate Order Items
# -----------------------------

order_items = []

for item_id in range(1, NUM_ORDER_ITEMS + 1):

    quantity = random.randint(1, 5)

    # 3% negative quantity
    if random.random() < 0.03:
        quantity = -quantity

    order_items.append({

        "item_id": item_id,

        "order_id": random.randint(1, NUM_ORDERS),

        "product_id": random.randint(1, NUM_PRODUCTS),

        "quantity": quantity,

        "unit_price": round(
            random.uniform(200, 10000),
            2
        ),

        "discount_percent": random.randint(0, 100)

    })

order_items_df = pd.DataFrame(order_items)

# -----------------------------
# Save CSV Files
# -----------------------------

customers_df.to_csv(
    "data/raw/customers.csv",
    index=False
)

products_df.to_csv(
    "data/raw/products.csv",
    index=False
)

orders_df.to_csv(
    "data/raw/orders.csv",
    index=False
)

order_items_df.to_csv(
    "data/raw/order_items.csv",
    index=False
)

print("=" * 50)
print("DATA GENERATION COMPLETED")
print("=" * 50)

print(f"Customers     : {customers_df.shape}")
print(f"Products      : {products_df.shape}")
print(f"Orders        : {orders_df.shape}")
print(f"Order Items   : {order_items_df.shape}")

print("\nCSV files saved inside data/raw/")

