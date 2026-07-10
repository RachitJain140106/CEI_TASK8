import sqlite3
import argparse
from tabulate import tabulate

DATABASE = "database/ecommerce.db"


# -----------------------------
# Database Connection
# -----------------------------
def connect_db():
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return None


# -----------------------------
# Revenue Report
# -----------------------------
def revenue_report(conn):

    query = """
    SELECT
        p.category,
        ROUND(
            SUM(
                oi.quantity *
                oi.unit_price *
                (1-oi.discount_percent/100.0)
            ),
            2
        ) AS Revenue

    FROM products p

    JOIN order_items oi

    ON p.product_id=oi.product_id

    GROUP BY p.category

    ORDER BY Revenue DESC;
    """

    cursor = conn.cursor()

    cursor.execute(query)

    rows = [
    (category, f"{revenue:,.2f}")
    for category, revenue in cursor.fetchall()
]

    if rows:
        print("\nRevenue Report\n")
        print(
            tabulate(
                rows,
                headers=["Category","Revenue"],
                tablefmt="grid"
            )
        )
    else:
        print("No data found.")


# -----------------------------
# Top Customers
# -----------------------------
def top_customers(conn):

    query = """
    SELECT

        c.customer_id,

        c.customer_name,

        ROUND(

            SUM(

                oi.quantity*
                oi.unit_price*
                (1-oi.discount_percent/100.0)

            ),

            2

        ) revenue

    FROM customers c

    JOIN orders o

    ON c.customer_id=o.customer_id

    JOIN order_items oi

    ON o.order_id=oi.order_id

    GROUP BY

    c.customer_id,
    c.customer_name

    ORDER BY revenue DESC

    LIMIT 10;
    """

    cursor = conn.cursor()

    cursor.execute(query)

    rows = [
    (customer_id, customer_name, f"{revenue:,.2f}")
    for customer_id, customer_name, revenue in cursor.fetchall()
]

    if rows:

        print("\nTop Customers\n")

        print(

            tabulate(

                rows,

                headers=[
                    "Customer ID",
                    "Customer Name",
                    "Revenue"
                ],

                tablefmt="grid"

            )

        )

    else:

        print("No data found.")


# -----------------------------
# Retention Report
# -----------------------------
def retention_report(conn):

    query = """

    WITH FirstPurchase AS
    (
        SELECT
            customer_id,
            MIN(DATE(order_date)) first_purchase
        FROM orders
        GROUP BY customer_id
    )

    SELECT

        strftime('%Y-%m',first_purchase)

        AS Cohort,

        COUNT(*) Customers

    FROM FirstPurchase

    GROUP BY Cohort

    ORDER BY Cohort;

    """

    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    if rows:

        print("\nRetention Report\n")

        print(

            tabulate(

                rows,

                headers=[
                    "Cohort",
                    "Customers"
                ],

                tablefmt="grid"

            )

        )

    else:

        print("No data found.")


# -----------------------------
# Main
# -----------------------------
def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(

        "--report",

        required=True,

        choices=[
            "revenue",
            "top_customers",
            "retention"
        ],

        help="Report Type"

    )

    args = parser.parse_args()

    conn = connect_db()

    if conn is None:
        return

    if args.report == "revenue":
        revenue_report(conn)

    elif args.report == "top_customers":
        top_customers(conn)

    elif args.report == "retention":
        retention_report(conn)

    conn.close()


if __name__ == "__main__":
    main()
