-- =====================================================
-- AGGREGATION QUERIES
-- E-Commerce Analytics System
-- =====================================================

--------------------------------------------------------
-- 1. Total Revenue Per Customer
--------------------------------------------------------

SELECT
    c.customer_id,
    c.customer_name,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_revenue DESC;


--------------------------------------------------------
-- 2. Total Revenue Per Category
--------------------------------------------------------

SELECT
    p.category,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_revenue
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.category
ORDER BY
    total_revenue DESC;


--------------------------------------------------------
-- 3. Total Revenue Per Month
--------------------------------------------------------

SELECT
    strftime('%Y-%m', o.order_date) AS order_month,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS monthly_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    order_month
ORDER BY
    order_month;


--------------------------------------------------------
-- 4. Top 10 Products by Quantity Sold
--------------------------------------------------------

SELECT
    p.product_id,
    p.product_name,
    SUM(oi.quantity) AS total_quantity
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY
    total_quantity DESC
LIMIT 10;


--------------------------------------------------------
-- 5. Top 10 Products by Revenue
--------------------------------------------------------

SELECT
    p.product_id,
    p.product_name,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS revenue
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY
    revenue DESC
LIMIT 10;


--------------------------------------------------------
-- 6. Average Order Value (AOV) by Customer Type
--------------------------------------------------------

WITH OrderTotals AS
(
    SELECT
        o.order_id,
        o.customer_id,
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) AS order_value
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.order_id,
        o.customer_id
)

SELECT
    c.customer_type,
    ROUND(
        AVG(OrderTotals.order_value),
        2
    ) AS average_order_value
FROM OrderTotals
JOIN customers c
    ON OrderTotals.customer_id = c.customer_id
GROUP BY
    c.customer_type
ORDER BY
    average_order_value DESC;