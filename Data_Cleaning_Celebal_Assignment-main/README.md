# Data_Cleaning_Celebal_Assignment
As a CEI intern this is my first project and it includes handling missing values, removing duplicates, performing basic data operations, normalization (1NF, 2NF, 3NF), and creating a cleaned dataset using Python and Pandas
# Basic Data Exploration and Cleaning using Pandas
In this assignment, I worked with a CSV dataset and performed different data cleaning operations such as:
- Exploring the dataset
- Handling missing values
- Filtering data
- Removing duplicate values
- Creating a derived column
- Applying normalization concepts (1NF, 2NF, 3NF)
- Saving the cleaned dataset

---

## Tools and Technologies Used
- Python
- Pandas
- Google Colab
- GitHub

---

## Files Included

| File Name | Description |
|------------|-------------|
| `Assignment.ipynb` | Contains complete Python code |
| `Combined_dataset.csv` | Original dataset |
| `clean_dataset.csv` | Cleaned dataset after processing |

---

## Steps Performed

### 1. Loading Dataset
Loaded the CSV dataset using Pandas.

### 2. Data Exploration
Explored the dataset using:
- `head()`
- `tail()`
- `shape`
- `columns`
- `dtypes`

### 3. Handling Missing Values
Checked missing values and filled them where required.

### 4. Basic Operations
Performed:
- Row filtering
- Column selection

### 5. Removing Duplicates
Removed duplicate rows using:
```python
drop_duplicates()
```

### 6. Normalization
Applied:
- 1NF
- 2NF
- 3NF

### 7. Derived Column
Created a new column:
```python
total_amount = initial_price * ratings_count
```

### 8. Saving Final Dataset
Saved the final cleaned dataset as a CSV file.

---

## Conclusion
This project helped me understand the basics of data cleaning and preprocessing using Pandas. I learned how to work with datasets, handle missing values, remove duplicates, and perform simple transformations on data.

---

## Author
Rachit Jain
