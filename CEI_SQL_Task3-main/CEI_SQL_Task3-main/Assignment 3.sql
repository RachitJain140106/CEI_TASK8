CREATE DATABASE superstore_db;
USE superstore_db;
SELECT *
FROM superstore_raw
LIMIT 10;
-- ------------------------
-- Creating Tables --
-- ------------------------
# CUSTOMER TABLE
CREATE TABLE customers AS
SELECT DISTINCT
    `Customer ID` AS customer_id,
    `Customer Name` AS customer_name,
    Segment
FROM superstore_raw;
SELECT * FROM customers LIMIT 5;

# ORDERS TABLE
CREATE TABLE orders AS
SELECT DISTINCT
    `Order ID` AS order_id,
    `Order Date` AS order_date,
    `Ship Date` AS ship_date,
    `Ship Mode` AS ship_mode,
    `Customer ID` AS customer_id,
    Sales,
    Quantity,
    Discount,
    Profit
FROM superstore_raw;
SELECT * FROM orders LIMIT 5;




# PRODUCT TABLE

CREATE TABLE products AS
SELECT DISTINCT
    `Product ID` AS product_id,
    `Product Name` AS product_name,
    Category,
    `Sub-Category` AS sub_category
FROM superstore_raw;
SELECT * FROM products LIMIT 5;

# 1. Find all orders where sales are greater than the average sales. (Subquery)  
SELECT *
FROM orders
WHERE Sales >
(
    SELECT AVG(Sales)
    FROM orders
);

# 2.Find the highest sales order for each customer. (Subquery)
SELECT *
FROM orders o
WHERE Sales = (
    SELECT MAX(o2.Sales)
    FROM orders o2
    WHERE o2.customer_id = o.customer_id
);
# 3.Calculate total sales for each customer. (CTE)
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(Sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT *
FROM customer_sales; 
# 4.Find customers whose total sales are above average. (CTE + Subquery)
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(Sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT *
FROM customer_sales
WHERE total_sales >
(
    SELECT AVG(total_sales)
    FROM customer_sales
); 
# 5.Rank all customers based on total sales. (Window Function) 
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(Sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT
    customer_id,
    total_sales,
    RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM customer_sales; 
# 6.Assign row numbers to each order within a customer. (Window Function + PARTITION BY)
SELECT
    customer_id,
    order_id,
    Sales,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY Sales DESC
    ) AS row_num
FROM orders;  
# 7.Display top 3 customers based on total sales. (Window Function)
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(Sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT *
FROM (
    SELECT
        customer_id,
        total_sales,
        RANK() OVER (ORDER BY total_sales DESC) AS rank_no
    FROM customer_sales
) t
WHERE rank_no <= 3;

# FINAL COMBINED QUERY
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(Sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT
    c.customer_name,
    cs.total_sales,
    RANK() OVER (
        ORDER BY cs.total_sales DESC
    ) AS customer_rank
FROM customer_sales cs
JOIN customers c
ON cs.customer_id = c.customer_id
ORDER BY customer_rank;

-- ---------------------------------------
-- Mini Project: Customer Sales Insights 
-- ---------------------------------------
# 1.Who are the top 5 customers?  
WITH customer_sales AS (
    SELECT
        c.customer_name,
        SUM(o.Sales) AS total_sales
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_name
)

SELECT *
FROM customer_sales
ORDER BY total_sales DESC
LIMIT 5;
# 2. Who are the bottom 5 customers? 
WITH customer_sales AS (
    SELECT
        c.customer_name,
        SUM(o.Sales) AS total_sales
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_name
)

SELECT *
FROM customer_sales
ORDER BY total_sales ASC
LIMIT 5; 
# 3. Which customers made only one order?  
SELECT
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_name
HAVING COUNT(DISTINCT o.order_id) = 1;
# 4. Which customers have above-average sales?  
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(Sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT
    c.customer_name,
    cs.total_sales
FROM customer_sales cs
JOIN customers c
    ON cs.customer_id = c.customer_id
WHERE cs.total_sales >
(
    SELECT AVG(total_sales)
    FROM customer_sales
);
# 5. What is the highest order value per customer? 
SELECT
    c.customer_name,
    MAX(o.Sales) AS highest_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_name
ORDER BY highest_order_value DESC;