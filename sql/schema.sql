-- =====================================================
-- DATABASE SCHEMA
-- E-Commerce Analytics System
-- =====================================================

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

--------------------------------------------------------
-- Customers
--------------------------------------------------------

CREATE TABLE customers (

    customer_id INTEGER PRIMARY KEY,

    customer_name TEXT NOT NULL,

    email TEXT NOT NULL,

    registration_date DATE,

    customer_type TEXT NOT NULL

);

--------------------------------------------------------
-- Products
--------------------------------------------------------

CREATE TABLE products (

    product_id INTEGER PRIMARY KEY,

    product_name TEXT NOT NULL,

    category TEXT NOT NULL,

    subcategory TEXT,

    cost_price REAL NOT NULL

);

--------------------------------------------------------
-- Orders
--------------------------------------------------------

CREATE TABLE orders (

    order_id INTEGER PRIMARY KEY,

    customer_id INTEGER,

    order_date DATETIME NOT NULL,

    status TEXT NOT NULL,

    region_code TEXT NOT NULL,

    FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)

);

--------------------------------------------------------
-- Order Items
--------------------------------------------------------

CREATE TABLE order_items (

    item_id INTEGER PRIMARY KEY,

    order_id INTEGER NOT NULL,

    product_id INTEGER NOT NULL,

    quantity INTEGER NOT NULL,

    unit_price REAL NOT NULL,

    discount_percent REAL NOT NULL,

    FOREIGN KEY(order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY(product_id)
        REFERENCES products(product_id)

);