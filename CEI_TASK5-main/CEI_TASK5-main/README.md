# Celebal Technologies Internship - Week 5

## Apache Spark Data Cleaning, Transformation and Aggregation

### Objective
To understand Spark fundamentals and perform data cleaning, transformation, filtering, aggregation, and schema modifications using PySpark DataFrames.

---

## Technologies Used

- Apache Spark
- PySpark
- Python

---

## Brief Insights

### Q1. MapReduce vs Spark
Traditional MapReduce relies on disk-based processing, making it slower for modern big data workloads. Spark uses in-memory computing, resulting in significantly faster execution.

### Q2. In-Memory Computing
Spark stores intermediate data in RAM, reducing disk I/O and improving the performance of iterative machine learning and analytics tasks.

### Q3. Duplicate Removal
Used `dropDuplicates()` to remove repeated records and maintain data quality.

### Q4. Filtering and Aggregation
Applied filters and grouped data to calculate average sales by product category.

### Q5. Handling Null Values
Used `.na.fill()` and `.na.drop()` to manage missing values and improve dataset reliability.

### Q6. Grouping and Counting
Used `groupBy()` and `count()` to analyze record distribution across cities.

### Q7. DataFrame Immutability
Spark DataFrames are immutable, meaning every transformation creates a new DataFrame.

### Q8. Conditional Filtering
Filtered records using multiple conditions to extract specific user segments.

### Q9. Null Handling Before Aggregation
Cleaning null values before aggregations ensures accurate calculations and meaningful insights.

### Q10. Schema Modification
Converted timestamp columns to proper data types and renamed columns for better readability.

### Q11. Shuffle and Wide Transformations
Grouping operations trigger shuffle processes where data is redistributed across partitions for computation.

### Q12. Removing Invalid Records
Filtered out records containing null emails or empty usernames to improve data quality.

### Q13. Multiple Aggregations
Used `.agg()` to calculate multiple statistics such as minimum, maximum, and average values in a single operation.

### Q14. Schema Inference Risks
Inconsistent date formats may lead to incorrect schema detection when using `inferSchema=true`.

### Q15. End-to-End Processing Pipeline
Built a complete pipeline combining duplicate removal, null handling, and revenue aggregation.

---

## Key Learning Outcomes

- Understanding Spark architecture and advantages over MapReduce
- Working with Spark DataFrames
- Performing data cleaning and preprocessing
- Applying filtering and aggregation operations
- Handling schema transformations
- Understanding shuffle operations and DataFrame immutability
- Building complete data processing workflows using PySpark

---

## Conclusion

This assignment provided hands-on experience with Spark DataFrames and core data engineering concepts including data cleaning, transformation, aggregation, and schema management. The exercises demonstrated how Spark efficiently processes large datasets using distributed and in-memory computing techniques.
