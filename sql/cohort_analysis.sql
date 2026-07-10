-- =====================================================
-- COHORT ANALYSIS & CUSTOMER SEGMENTATION
-- E-Commerce Analytics System
-- =====================================================

--------------------------------------------------------
-- 1. Customer Cohorts (First Purchase Month)
--------------------------------------------------------

WITH FirstPurchase AS
(
    SELECT
        customer_id,
        MIN(DATE(order_date)) AS first_purchase_date
    FROM orders
    GROUP BY customer_id
)

SELECT
    customer_id,
    strftime('%Y-%m', first_purchase_date) AS cohort_month
FROM FirstPurchase
ORDER BY cohort_month;



--------------------------------------------------------
-- 2. Monthly Retention Analysis
--------------------------------------------------------

WITH FirstPurchase AS
(
    SELECT
        customer_id,
        MIN(DATE(order_date)) AS first_purchase_date
    FROM orders
    GROUP BY customer_id
),

CustomerOrders AS
(
    SELECT
        o.customer_id,
        strftime('%Y-%m', fp.first_purchase_date) AS cohort_month,
        strftime('%Y-%m', o.order_date) AS order_month
    FROM orders o
    JOIN FirstPurchase fp
        ON o.customer_id = fp.customer_id
)

SELECT
    cohort_month,
    order_month,
    COUNT(DISTINCT customer_id) AS retained_customers
FROM CustomerOrders
GROUP BY
    cohort_month,
    order_month
ORDER BY
    cohort_month,
    order_month;



--------------------------------------------------------
-- 3. Repeat vs One-Time Customers
--------------------------------------------------------

SELECT
    customer_id,

    COUNT(order_id) AS total_orders,

    CASE

        WHEN COUNT(order_id)=1
            THEN 'One-Time'

        ELSE 'Repeat'

    END AS customer_type

FROM orders

GROUP BY customer_id;



--------------------------------------------------------
-- 4. Purchase Frequency Segmentation
--------------------------------------------------------

SELECT

customer_id,

COUNT(order_id) total_orders,

CASE

WHEN COUNT(order_id)=1
THEN 'One-Time'

WHEN COUNT(order_id) BETWEEN 2 AND 5
THEN 'Occasional'

ELSE 'Loyal'

END purchase_segment

FROM orders

GROUP BY customer_id;



--------------------------------------------------------
-- 5. Spend Tier Segmentation
--------------------------------------------------------

WITH CustomerSpend AS

(

SELECT

o.customer_id,

SUM(

oi.quantity*

oi.unit_price*

(1-oi.discount_percent/100.0)

) total_spend

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY o.customer_id

)

SELECT

customer_id,

ROUND(total_spend,2) total_spend,

CASE

WHEN total_spend<5000
THEN 'Low'

WHEN total_spend BETWEEN 5000 AND 10000
THEN 'Medium'

ELSE 'High'

END spend_tier

FROM CustomerSpend;



--------------------------------------------------------
-- 6. RFM Analysis
--------------------------------------------------------

WITH CustomerMetrics AS

(

SELECT

o.customer_id,

MAX(DATE(order_date)) last_order,

COUNT(DISTINCT o.order_id) frequency,

SUM(

oi.quantity*

oi.unit_price*

(1-oi.discount_percent/100.0)

) monetary

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY o.customer_id

)

SELECT

customer_id,

last_order,

frequency,

ROUND(monetary,2) monetary

FROM CustomerMetrics;



--------------------------------------------------------
-- 7. NTILE Customer Segmentation
--------------------------------------------------------

WITH LifetimeValue AS

(

SELECT

o.customer_id,

SUM(

oi.quantity*

oi.unit_price*

(1-oi.discount_percent/100.0)

) total_value

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY o.customer_id

)

SELECT

customer_id,

ROUND(total_value,2) total_value,

NTILE(4)

OVER(

ORDER BY total_value DESC

)

quartile,

CASE

WHEN NTILE(4)

OVER(

ORDER BY total_value DESC

)=1 THEN 'Platinum'

WHEN NTILE(4)

OVER(

ORDER BY total_value DESC

)=2 THEN 'Gold'

WHEN NTILE(4)

OVER(

ORDER BY total_value DESC

)=3 THEN 'Silver'

ELSE 'Bronze'

END quartile_label

FROM LifetimeValue;



--------------------------------------------------------
-- 8. Year-over-Year Revenue
--------------------------------------------------------

WITH RevenueByMonth AS

(

SELECT

strftime('%Y',order_date) year,

strftime('%m',order_date) month,

SUM(

oi.quantity*

oi.unit_price*

(1-oi.discount_percent/100.0)

) revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY

year,

month

)

SELECT

year,

month,

ROUND(revenue,2) revenue,

LAG(revenue)

OVER(

PARTITION BY month

ORDER BY year

)

previous_year,

ROUND(

100.0*

(

revenue-

LAG(revenue)

OVER(

PARTITION BY month

ORDER BY year

)

)

/

LAG(revenue)

OVER(

PARTITION BY month

ORDER BY year

),

2

)

yoy_growth

FROM RevenueByMonth;



--------------------------------------------------------
-- 9. First Purchased Category vs Last Purchased Category
--------------------------------------------------------

WITH PurchaseHistory AS

(

SELECT

o.customer_id,

p.category,

o.order_date,

ROW_NUMBER()

OVER(

PARTITION BY o.customer_id

ORDER BY o.order_date

)

first_order,

ROW_NUMBER()

OVER(

PARTITION BY o.customer_id

ORDER BY o.order_date DESC

)

last_order

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

JOIN products p

ON oi.product_id=p.product_id

)

SELECT

f.customer_id,

f.category first_category,

l.category last_category,

CASE

WHEN f.category=l.category

THEN 'No'

ELSE 'Yes'

END category_shift

FROM PurchaseHistory f

JOIN PurchaseHistory l

ON f.customer_id=l.customer_id

WHERE

f.first_order=1

AND

l.last_order=1;



--------------------------------------------------------
-- 10. Frequently Bought Together
--------------------------------------------------------

SELECT

oi1.product_id product_a,

oi2.product_id product_b,

COUNT(*) times_bought_together

FROM order_items oi1

JOIN order_items oi2

ON oi1.order_id=oi2.order_id

WHERE

oi1.product_id<oi2.product_id

GROUP BY

oi1.product_id,

oi2.product_id

ORDER BY

times_bought_together DESC

LIMIT 20;