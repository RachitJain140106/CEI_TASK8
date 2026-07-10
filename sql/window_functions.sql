-- =====================================================
-- WINDOW FUNCTIONS & ADVANCED SQL
-- E-Commerce Analytics System
-- =====================================================


--------------------------------------------------------
-- 1. Rank Customers by Lifetime Value
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
    ) AS lifetime_value,

    RANK() OVER(

        ORDER BY
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) DESC

    ) AS customer_rank

FROM customers c

JOIN orders o
ON c.customer_id = o.customer_id

JOIN order_items oi
ON o.order_id = oi.order_id

GROUP BY
c.customer_id,
c.customer_name;



--------------------------------------------------------
-- 2. Dense Rank Products by Revenue
--------------------------------------------------------

SELECT

    p.category,

    p.product_name,

    ROUND(

        SUM(

            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)

        ),

        2

    ) AS total_revenue,

    DENSE_RANK() OVER(

        PARTITION BY p.category

        ORDER BY

        SUM(

            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)

        ) DESC

    ) AS rank_in_category

FROM products p

JOIN order_items oi

ON p.product_id = oi.product_id

GROUP BY

p.category,

p.product_name;



--------------------------------------------------------
-- 3. Running Total Revenue by Region
--------------------------------------------------------

WITH DailyRevenue AS

(

SELECT

o.region_code,

DATE(o.order_date) AS order_day,

SUM(

oi.quantity *

oi.unit_price *

(1-oi.discount_percent/100.0)

) daily_revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY

o.region_code,

DATE(o.order_date)

)

SELECT

region_code,

order_day,

ROUND(daily_revenue,2) daily_revenue,

ROUND(

SUM(daily_revenue)

OVER(

PARTITION BY region_code

ORDER BY order_day

),

2

) running_total

FROM DailyRevenue;



--------------------------------------------------------
-- 4. Moving Average Revenue
--------------------------------------------------------

WITH DailyRevenue AS

(

SELECT

DATE(o.order_date) order_day,

SUM(

oi.quantity *

oi.unit_price *

(1-oi.discount_percent/100.0)

) revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY

DATE(o.order_date)

)

SELECT

order_day,

ROUND(revenue,2) revenue,

ROUND(

AVG(revenue)

OVER(

ORDER BY order_day

ROWS BETWEEN 2 PRECEDING AND CURRENT ROW

),

2

) moving_average

FROM DailyRevenue;



--------------------------------------------------------
-- 5. Days Between Consecutive Orders
--------------------------------------------------------

SELECT

customer_id,

order_date,

LAG(order_date)

OVER(

PARTITION BY customer_id

ORDER BY order_date

)

AS previous_order_date,

ROUND(

JULIANDAY(order_date)

-

JULIANDAY(

LAG(order_date)

OVER(

PARTITION BY customer_id

ORDER BY order_date

)

),

2

)

AS days_gap

FROM orders;



--------------------------------------------------------
-- 6. Customers At Risk
--------------------------------------------------------

WITH CustomerGap AS

(

SELECT

customer_id,

AVG(

JULIANDAY(order_date)

-

JULIANDAY(

LAG(order_date)

OVER(

PARTITION BY customer_id

ORDER BY order_date

)

)

) avg_gap

FROM orders

GROUP BY customer_id

)

SELECT

customer_id,

ROUND(avg_gap,2) average_gap,

CASE

WHEN avg_gap>30

THEN 'At Risk'

ELSE 'Active'

END customer_status

FROM CustomerGap;



--------------------------------------------------------
-- 7. Monthly Revenue using CTE
--------------------------------------------------------

WITH MonthlyRevenue AS

(

SELECT

strftime('%Y-%m',o.order_date) month,

SUM(

oi.quantity*

oi.unit_price*

(1-oi.discount_percent/100.0)

) revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY month

)

SELECT

month,

ROUND(revenue,2) revenue

FROM MonthlyRevenue

ORDER BY month;