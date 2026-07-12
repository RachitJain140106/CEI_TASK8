# CEI_TASK_6
# Week 6 
## Objective

The objective of this assignment was to understand Apache Spark architecture and perform efficient data processing using PySpark. The tasks included reading data from different file formats, applying transformations and filtering, handling schemas and null values, and building a simple data processing pipeline.

## Technologies Used

- Apache Spark
- PySpark
- Google Colab
- Python

## Tasks Performed

- Understood Spark Architecture (Driver, Cluster Manager, Executors)
- Learned Lazy Evaluation and DAG execution
- Read data from CSV and Parquet files
- Selected and filtered required records
- Renamed columns and changed data types
- Added new calculated columns
- Handled null values
- Compared CSV and Parquet formats
- Built a simple data pipeline (Read → Transform → Filter → Write)
- Saved processed data as CSV

## Brief Insights

- Spark executes transformations lazily, which helps optimize performance.
- The DAG (Lineage Graph) allows Spark to recover lost data efficiently if a node fails.
- Parquet performs better than CSV because it stores data in a columnar format and supports Predicate Pushdown.
- Transformations are executed only when an action is called.
- Using `show()` is preferred over `collect()` when working with large datasets to avoid memory issues.

## Outcome

Successfully implemented basic Spark data processing operations and understood key performance optimization concepts such as Lazy Evaluation, DAG execution, Shuffle, and efficient file formats.
