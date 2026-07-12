# 🚀 Celebal Technologies Data Engineering Internship

## 📌 Overview

This repository contains the weekly assignments and projects completed during my **Data Engineering Internship at Celebal Technologies**.

Over the course of eight weeks, the assignments progressed from foundational data analysis with Python and SQL to cloud data pipelines, Apache Spark, Delta Lake, and finally an end-to-end E-Commerce Analytics System.

The internship provided hands-on experience with the complete data engineering lifecycle:

**Data Generation → Data Cleaning → Transformation → Storage → Processing → Analytics → Reporting**

---

## 🛠️ Technologies & Tools

- Python
- Pandas
- NumPy
- SQL
- SQLite
- Azure Data Factory
- Azure Blob Storage
- Apache Spark
- PySpark
- Databricks
- Delta Lake
- Faker
- Git & GitHub
- Google Colab

---

# 📚 Weekly Assignments

| Week | Project | Key Technologies |
|------|---------|------------------|
| Week 1 | Shopping Data Exploration & Cleaning | Python, Pandas, NumPy |
| Week 2 | SQL Data Analysis | SQL, Relational Databases |
| Week 3 | Advanced SQL Analytics | CTEs, Subqueries, Window Functions |
| Week 4 | Azure Data Pipeline | Azure Data Factory, Blob Storage |
| Week 5 | Spark Data Processing | Apache Spark, PySpark |
| Week 6 | Advanced Spark & Performance | Spark, Parquet, DAG |
| Week 7 | Delta Lake MERGE Implementation | Databricks, Delta Lake |
| Week 8 | E-Commerce Order Analytics System | Python, Pandas, SQLite, SQL |

---

# 📊 Week 1 — Shopping Data Exploration & Cleaning

## Objective

Perform exploratory data analysis, data cleaning, feature engineering, visualization, and derive meaningful insights from a shopping dataset.

## Key Tasks

- Loaded CSV data using Pandas
- Explored dataset structure and data types
- Identified and handled missing values
- Removed duplicate records
- Converted price-related columns to numeric format
- Created derived features such as:
  - Price difference
  - Popularity metric
- Performed univariate and bivariate analysis
- Conducted category-level analysis
- Created visualizations using histograms, bar charts, and boxplots
- Documented key business insights

## Skills Gained

`Python` `Pandas` `NumPy` `EDA` `Data Cleaning` `Feature Engineering` `Data Visualization`

---

# 🗄️ Week 2 — SQL-Based Data Analysis

## Objective

Analyze sales data using SQL filtering, aggregation, joins, and business queries.

## Key Tasks

- Created relational database tables
- Implemented primary and foreign key relationships
- Created indexes for query optimization
- Loaded and validated data
- Applied `WHERE` filters
- Used aggregate functions:
  - `COUNT()`
  - `SUM()`
  - `AVG()`
  - `MIN()`
  - `MAX()`
- Used `GROUP BY` and `ORDER BY`
- Implemented `INNER JOIN` and `LEFT JOIN`
- Used `CASE` statements
- Worked with transactions
- Solved business-oriented SQL problems

## Skills Gained

`SQL` `Database Design` `Filtering` `Aggregation` `Joins` `Indexes` `Transactions`

---

# 📈 Week 3 — Advanced SQL Analytics

## Objective

Use advanced SQL concepts to analyze sales data from the Superstore dataset.

## Key Tasks

- Loaded Superstore data into a staging table
- Created customers, orders, and products tables
- Used subqueries for:
  - Above-average sales
  - Highest-value orders
- Used CTEs for intermediate aggregations
- Calculated customer-level sales metrics
- Applied window functions:
  - `ROW_NUMBER()`
  - `RANK()`
  - `DENSE_RANK()`
- Combined joins, CTEs, and window functions
- Identified:
  - Top customers
  - Bottom customers
  - Single-order customers
  - Above-average customers
- Generated customer sales rankings and business insights

## Skills Gained

`Advanced SQL` `Subqueries` `CTEs` `Window Functions` `Customer Analytics`

---

# ☁️ Week 4 — Azure Data Pipeline using ADF

## Objective

Understand Azure cloud fundamentals and build an end-to-end data pipeline using Azure Storage and Azure Data Factory.

## Pipeline Architecture

```text
CSV Dataset
     │
     ▼
Azure Blob Storage
     │
     ▼
Azure Data Factory
     │
     ├── Get Metadata
     │
     └── Copy Data
     │
     ▼
Destination Storage
```

## Key Tasks

- Created an Azure Resource Group
- Created an Azure Storage Account
- Created Blob Containers
- Uploaded the Superstore dataset
- Created an Azure Data Factory instance
- Configured Linked Services
- Created source and destination datasets
- Used the Get Metadata activity
- Built a Copy Data pipeline
- Executed pipelines using Debug and Trigger
- Monitored pipeline execution
- Configured IAM roles
- Implemented an end-to-end:

**Blob Storage → Azure Data Factory → Destination**

## Skills Gained

`Microsoft Azure` `Azure Data Factory` `Blob Storage` `ETL Pipelines` `IAM` `Cloud Computing`

---

# ⚡ Week 5 — Spark Data Processing

## Objective

Understand Apache Spark fundamentals and perform data cleaning, transformation, filtering, and aggregation using Spark DataFrames.

## Key Tasks

- Studied limitations of MapReduce
- Understood Spark's in-memory processing model
- Created Spark sessions
- Loaded CSV data into Spark DataFrames
- Explored schemas and column types
- Removed duplicate records
- Handled null values
- Applied filtering conditions
- Renamed columns
- Cast data types
- Used aggregation functions
- Applied `groupBy()`
- Learned about wide transformations and shuffle operations
- Built a complete Spark data processing pipeline

## Pipeline

```text
Load Data
    ↓
Clean Data
    ↓
Filter Data
    ↓
Transform Data
    ↓
Aggregate Data
    ↓
Generate Results
```

## Skills Gained

`Apache Spark` `PySpark` `DataFrames` `Transformations` `Aggregations` `Distributed Processing`

---

# 🔥 Week 6 — Advanced Spark & Performance Optimization

## Objective

Understand Spark architecture and build efficient data processing pipelines using optimized schemas and file formats.

## Key Concepts

### Spark Architecture

```text
Driver
   │
   ▼
Cluster Manager
   │
   ▼
Executors
   │
   ▼
Tasks
```

## Key Tasks

- Studied Spark architecture
- Understood:
  - Driver
  - Cluster Manager
  - Executors
- Learned Lazy Evaluation
- Explored DAG and lineage graphs
- Compared transformations and actions
- Defined explicit schemas using `StructType`
- Read CSV and Parquet files
- Performed column selection and filtering
- Renamed and cast columns
- Created derived columns
- Studied narrow and wide transformations
- Understood shuffle operations
- Learned Predicate Pushdown
- Compared CSV and Parquet performance
- Used `.explain()` to inspect execution plans
- Followed Spark best practices such as avoiding `.collect()` on large datasets
- Built an optimized pipeline:

```text
Read
 ↓
Clean
 ↓
Filter
 ↓
Transform
 ↓
Aggregate
 ↓
Write to Parquet
```

## Skills Gained

`Spark Architecture` `Lazy Evaluation` `DAG` `Parquet` `Predicate Pushdown` `Performance Optimization`

---

# 🧱 Week 7 — Delta Lake MERGE Implementation

## Objective

Perform incremental data processing and implement update/insert operations using Delta Lake.

## Key Tasks

- Loaded datasets into Delta tables
- Performed data cleaning
- Handled null values
- Removed duplicates
- Created incremental datasets
- Implemented Delta Lake `MERGE`
- Updated existing records
- Inserted new records
- Validated row counts
- Checked duplicate records
- Displayed and analyzed the final dataset

## Data Flow

```text
Customer Master Data
        │
        ▼
    Delta Table
        ▲
        │
Incremental Data
        │
        ▼
   MERGE Operation
        │
        ├── MATCHED → UPDATE
        │
        └── NOT MATCHED → INSERT
        │
        ▼
 Updated Delta Table
```

## Skills Gained

`Delta Lake` `Databricks` `MERGE` `Incremental Processing` `Data Validation`

---

# 🛒 Week 8 — E-Commerce Order Analytics System

## Objective

Design and develop an end-to-end E-Commerce Order Analytics System combining Python and SQL, from realistic dataset generation to business reporting.

## System Architecture

```text
Data Generation
      │
      ▼
Raw CSV Files
      │
      ▼
Pandas Data Cleaning
      │
      ▼
Cleaned Datasets
      │
      ▼
SQLite Database
      │
      ▼
SQL Analytics
      │
      ▼
CLI Reporting Tool
      │
      ▼
Business Reports
```

## Data Generation

Generated four interconnected datasets:

- Customers
- Products
- Orders
- Order Items

Intentional data quality issues were introduced, including:

- Missing customer IDs
- Invalid emails
- Incorrect date formats
- Mixed-case product names
- Extra spaces
- Negative quantities

## Data Cleaning

Used Pandas to:

- Handle missing values
- Remove duplicates
- Normalize product names
- Validate email addresses
- Fix date formats
- Validate referential integrity
- Export cleaned datasets

## Database Design

Created a SQLite database with:

- Primary Keys
- Foreign Keys
- NOT NULL constraints
- Referential integrity validation

## SQL Analytics

Implemented:

- Revenue per customer
- Revenue per category
- Monthly revenue
- Top products
- Average Order Value
- Customer Lifetime Value
- Running totals
- Moving averages
- Customer ranking
- Product ranking
- Customer order-gap analysis
- Cohort analysis
- Retention analysis
- RFM-style customer segmentation
- Spend-tier segmentation
- Purchase-frequency segmentation
- Year-over-Year analysis
- Frequently bought-together analysis

### Advanced SQL Concepts

- `JOIN`
- `CTE`
- `RANK()`
- `DENSE_RANK()`
- `LAG()`
- `NTILE()`
- `SUM() OVER()`
- `AVG() OVER()`

## CLI Reporting Tool

Developed a Python command-line reporting tool supporting:

```bash
python scripts/report_cli.py --report revenue
```

```bash
python scripts/report_cli.py --report top_customers
```

```bash
python scripts/report_cli.py --report retention
```

## Edge Case Testing

Validated:

- Invalid order references
- Discount percentages greater than 100
- Zero quantities
- Future order dates
- Empty results
- Database connection errors

## Skills Gained

`Python` `Pandas` `SQLite` `Advanced SQL` `Data Modeling` `CLI Development` `Cohort Analysis` `Customer Segmentation`

---

# 🧠 Key Learning Outcomes

Throughout these eight weeks, I gained practical experience in:

- Data cleaning and preprocessing
- Exploratory Data Analysis
- Relational database design
- Basic and advanced SQL
- Subqueries and CTEs
- SQL window functions
- Cloud data engineering using Azure
- Building ETL pipelines with Azure Data Factory
- Distributed data processing with Apache Spark
- Spark architecture and performance optimization
- Optimized file formats such as Parquet
- Incremental processing using Delta Lake
- End-to-end analytics system development
- Data validation and edge-case handling
- Technical documentation and GitHub project organization

---

# 📈 Learning Progression

```text
Week 1
Python & Pandas
      │
      ▼
Week 2
SQL Fundamentals
      │
      ▼
Week 3
Advanced SQL
      │
      ▼
Week 4
Azure Data Engineering
      │
      ▼
Week 5
Apache Spark Fundamentals
      │
      ▼
Week 6
Advanced Spark & Optimization
      │
      ▼
Week 7
Delta Lake & Incremental Processing
      │
      ▼
Week 8
End-to-End Data Analytics System
```

---

# 📁 Suggested Repository Structure

```text
Celebal-Technologies-Data-Engineering-Internship/
│
├── Week-1-Shopping-Data-Analysis/
├── Week-2-SQL-Data-Analysis/
├── Week-3-Advanced-SQL-Analytics/
├── Week-4-Azure-Data-Pipeline/
├── Week-5-Spark-Fundamentals/
├── Week-6-Advanced-Spark/
├── Week-7-Delta-Lake/
├── Week-8-Ecommerce-Analytics/
│
├── README.md
└── LICENSE
```

---

# 👨‍💻 Author

**Rachit Jain**

B.Tech — Artificial Intelligence & Data Science  
Jaipur Engineering College & Research Centre (JECRC)

---

## ⭐ Acknowledgement

I would like to thank **Celebal Technologies** for providing a structured learning experience and hands-on assignments covering modern data engineering technologies and real-world data processing workflows.

---

> This repository documents my learning journey through Python, SQL, Azure, Apache Spark, Delta Lake, and end-to-end data engineering.
