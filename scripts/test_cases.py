import sqlite3
from datetime import datetime

DATABASE = "database/ecommerce.db"


def connect_db():
    return sqlite3.connect(DATABASE)


# -----------------------------------------------------
# Test 1
# Invalid Order References
# -----------------------------------------------------

def test_invalid_order_reference(conn):

    cursor = conn.cursor()

    query = """
    SELECT COUNT(*)
    FROM order_items oi
    LEFT JOIN orders o
    ON oi.order_id = o.order_id
    WHERE o.order_id IS NULL;
    """

    cursor.execute(query)

    count = cursor.fetchone()[0]

    print("\nTest 1 : Invalid Order References")

    if count == 0:
        print("PASS")
    else:
        print(f"FAIL ({count} invalid records found)")


# -----------------------------------------------------
# Test 2
# Discount >100
# -----------------------------------------------------

def test_discount(conn):

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM order_items

        WHERE discount_percent>100;

    """)

    count = cursor.fetchone()[0]

    print("\nTest 2 : Discount Greater Than 100")

    if count == 0:
        print("PASS")
    else:
        print(f"FAIL ({count} records found)")


# -----------------------------------------------------
# Test 3
# Quantity = 0
# -----------------------------------------------------

def test_quantity(conn):

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM order_items

        WHERE quantity=0;

    """)

    count = cursor.fetchone()[0]

    print("\nTest 3 : Quantity Equals Zero")

    if count == 0:
        print("PASS")
    else:
        print(f"FAIL ({count} records found)")


# -----------------------------------------------------
# Test 4
# Future Order Date
# -----------------------------------------------------

def test_future_dates(conn):

    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""

        SELECT COUNT(*)

        FROM orders

        WHERE order_date>?

    """, (today,))

    count = cursor.fetchone()[0]

    print("\nTest 4 : Future Order Dates")

    if count == 0:
        print("PASS")
    else:
        print(f"FAIL ({count} records found)")


# -----------------------------------------------------
# Main
# -----------------------------------------------------

def main():

    conn = connect_db()

    print("=" * 50)
    print("RUNNING TEST CASES")
    print("=" * 50)

    test_invalid_order_reference(conn)

    test_discount(conn)

    test_quantity(conn)

    test_future_dates(conn)

    conn.close()

    print("\nAll Tests Executed Successfully.")


if __name__ == "__main__":
    main()