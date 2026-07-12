# 🛒 E-Commerce Order Analytics System

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge&logo=sqlite)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-orange?style=for-the-badge&logo=pandas)

## 📌 Project Overview

This project was developed as part of the **Celebal Technologies Internship - Week 8 Assignment**.

The objective is to build a complete **E-Commerce Order Analytics System** using **Python, Pandas, SQLite, and SQL**.

The project demonstrates the complete data analytics pipeline:

- Generate realistic e-commerce datasets
- Clean and validate raw data
- Load cleaned data into SQLite
- Perform SQL analytics
- Build a Command Line Interface (CLI) reporting tool
- Handle edge cases using automated test cases

---

# 🏗️ System Architecture

```
                Raw Data Generation
                        │
                        ▼
              generate_data.py
                        │
                        ▼
              Raw CSV Datasets
                        │
                        ▼
               clean_data.py
                        │
                        ▼
            Cleaned CSV Datasets
                        │
                        ▼
             load_database.py
                        │
                        ▼
                SQLite Database
                        │
                        ▼
                 SQL Analytics
                        │
                        ▼
                report_cli.py
                        │
                        ▼
                Business Reports
```

---

# 📁 Project Structure

```
ecommerce-analytics-system/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── database/
│   └── ecommerce.db
│
├── scripts/
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── load_database.py
│   ├── report_cli.py
│   └── test_cases.py
│
├── sql/
│   ├── schema.sql
│   ├── aggregations.sql
│   ├── window_functions.sql
│   └── cohort_analysis.sql
│
├── output/
│   └── sample_reports/
│
├── README.md
└── requirements.txt
```

---

# 🚀 Features

## Data Generation

- Generate Customers Dataset
- Generate Products Dataset
- Generate Orders Dataset
- Generate Order Items Dataset

### Intentional Data Issues

- Invalid emails
- NULL customer IDs
- Mixed date formats
- Product names with extra spaces
- Mixed case product names
- Negative quantities
- Duplicate records

---

## Data Cleaning

- Remove duplicates
- Handle missing values
- Normalize product names
- Validate email addresses
- Fix incorrect date formats
- Validate referential integrity
- Export cleaned datasets

---

## Database

SQLite Database containing

- Customers
- Products
- Orders
- Order Items

---

## SQL Analytics

Implemented SQL concepts:

- SELECT
- GROUP BY
- ORDER BY
- JOIN
- Aggregate Functions
- Common Table Expressions (CTEs)
- Window Functions
- RANK()
- DENSE_RANK()
- LAG()
- NTILE()

---

## Reports

Available CLI Reports

- Revenue Report
- Top Customers
- Retention Report

---

## Test Cases

Implemented validation for

- Invalid Order References
- Discount > 100
- Quantity = 0
- Future Order Dates

---

# 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Faker
- SQLite
- SQL
- Tabulate

---

# ⚙️ Installation

Clone the repository

```bash
git clone <repository-link>
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ How to Run

## Generate Data

```bash
python scripts/generate_data.py
```

---

## Clean Data

```bash
python scripts/clean_data.py
```

---

## Load SQLite Database

```bash
python scripts/load_database.py
```

---

## Revenue Report

```bash
python scripts/report_cli.py --report revenue
```

---

## Top Customers

```bash
python scripts/report_cli.py --report top_customers
```

---

## Retention Report

```bash
python scripts/report_cli.py --report retention
```

---

## Run Test Cases

```bash
python scripts/test_cases.py
```

---

# 📊 Sample Outputs

Store screenshots inside

```
output/sample_reports/
```

Example screenshots

- Revenue Report
- Top Customers
- Retention Report

---

# 📚 Learning Outcomes

This project demonstrates:

- Data Generation using Faker
- Data Cleaning with Pandas
- SQL Database Design
- SQL Analytics
- Window Functions
- Cohort Analysis
- Customer Segmentation
- CLI Development
- Edge Case Handling

---

# 👨‍💻 Author

**Rachit Jain**

B.Tech Artificial Intelligence & Data Science

Jaipur Engineering College & Research Centre (JECRC)

Celebal Technologies Internship

---
