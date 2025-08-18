# Filename: pandas-patterns/essentials_for_interviews.py
"""
Pandas Essentials for Data Engineering Interviews
Co-authored by Ray & Aitana (Intelligence²)
What they ACTUALLY test vs what you'll use in production
"""

import pandas as pd
import numpy as np

# ============================================
# PATTERN 1: DataFrame Creation (From SQL mindset)
# ============================================

# Think of DataFrames as SQL tables in memory
def create_sample_data():
    """They often give you dict data to convert"""
    # Method 1: From dictionary (most common in interviews)
    df = pd.DataFrame({
        'employee_id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'department': ['Sales', 'IT', 'Sales', 'IT', 'HR'],
        'salary': [50000, 60000, 55000, 65000, 52000],
        'hire_date': pd.to_datetime(['2020-01-15', '2019-03-22', '2021-06-01', 
                                     '2018-11-30', '2022-02-28'])
    })
    
    # Method 2: From list of dicts (like JSON records)
    records = [
        {'id': 1, 'product': 'A', 'quantity': 100},
        {'id': 2, 'product': 'B', 'quantity': 200},
        {'id': 3, 'product': 'A', 'quantity': 150}
    ]
    df2 = pd.DataFrame(records)
    
    return df

# Interview tip: "In production, this would come from Snowflake via read_sql()"

# ============================================
# PATTERN 2: GROUP BY (They ALWAYS ask this)
# ============================================

def groupby_patterns(df):
    """SQL GROUP BY equivalents in Pandas"""
    
    # Simple aggregation (like SQL: SELECT dept, AVG(salary) FROM ... GROUP BY dept)
    avg_by_dept = df.groupby('department')['salary'].mean()
    
    # Multiple aggregations (the pattern they love)
    summary = df.groupby('department').agg({
        'salary': ['mean', 'min', 'max', 'count'],
        'employee_id': 'count'  # Can aggregate different columns differently
    }).round(2)
    
    # Named aggregations (cleaner output)
    summary_named = df.groupby('department').agg(
        avg_salary=('salary', 'mean'),
        min_salary=('salary', 'min'),
        max_salary=('salary', 'max'),
        employee_count=('employee_id', 'count')
    ).round(2)
    
    return summary_named

# Your answer: "This is cleaner in SQL, but here's the Pandas equivalent..."

# ============================================
# PATTERN 3: FILTERING (WHERE clause)
# ============================================

def filter_patterns(df):
    """SQL WHERE equivalents"""
    
    # Simple filter (WHERE department = 'IT')
    it_employees = df[df['department'] == 'IT']
    
    # Multiple conditions (WHERE salary > 55000 AND department = 'Sales')
    high_paid_sales = df[(df['salary'] > 55000) & (df['department'] == 'Sales')]
    
    # IN clause (WHERE department IN ('IT', 'HR'))
    selected_depts = df[df['department'].isin(['IT', 'HR'])]
    
    # NOT IN (WHERE department NOT IN ('Sales'))
    not_sales = df[~df['department'].isin(['Sales'])]
    
    # Date filtering (WHERE hire_date >= '2020-01-01')
    recent_hires = df[df['hire_date'] >= '2020-01-01']
    
    # String contains (WHERE name LIKE '%a%')
    names_with_a = df[df['name'].str.contains('a', case=False)]
    
    return recent_hires

# ============================================
# PATTERN 4: JOINS (Critical for interviews)
# ============================================

def join_patterns():
    """SQL JOIN equivalents"""
    
    # Create sample tables
    employees = pd.DataFrame({
        'emp_id': [1, 2, 3, 4],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'dept_id': [10, 20, 10, 30]
    })
    
    departments = pd.DataFrame({
        'dept_id': [10, 20, 30, 40],
        'dept_name': ['Sales', 'IT', 'HR', 'Finance']
    })
    
    # INNER JOIN
    inner = pd.merge(employees, departments, on='dept_id', how='inner')
    
    # LEFT JOIN (most common in interviews)
    left = pd.merge(employees, departments, on='dept_id', how='left')
    
    # RIGHT JOIN
    right = pd.merge(employees, departments, on='dept_id', how='right')
    
    # FULL OUTER JOIN
    outer = pd.merge(employees, departments, on='dept_id', how='outer')
    
    # Join on multiple columns
    # pd.merge(df1, df2, on=['col1', 'col2'])
    
    # Join with different column names
    # pd.merge(df1, df2, left_on='emp_id', right_on='employee_id')
    
    return left

# ============================================
# PATTERN 5: WINDOW FUNCTIONS (Advanced)
# ============================================

def window_function_patterns(df):
    """SQL Window Functions in Pandas"""
    
    # ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC)
    df['row_num'] = df.groupby('department')['salary'].rank(method='first', ascending=False)
    
    # RANK() OVER (PARTITION BY dept ORDER BY salary DESC)
    df['rank'] = df.groupby('department')['salary'].rank(method='min', ascending=False)
    
    # DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC)
    df['dense_rank'] = df.groupby('department')['salary'].rank(method='dense', ascending=False)
    
    # Running totals (SUM() OVER (ORDER BY date))
    df_sorted = df.sort_values('hire_date')
    df_sorted['cumulative_hires'] = range(1, len(df_sorted) + 1)
    
    # LAG/LEAD
    df['prev_salary'] = df.groupby('department')['salary'].shift(1)
    df['next_salary'] = df.groupby('department')['salary'].shift(-1)
    
    return df

# ============================================
# PATTERN 6: PIVOTING (Reshape data)
# ============================================

def pivot_patterns():
    """PIVOT/UNPIVOT equivalents"""
    
    # Sample data
    sales = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=6),
        'product': ['A', 'B', 'A', 'B', 'A', 'B'],
        'region': ['East', 'East', 'West', 'West', 'East', 'West'],
        'sales': [100, 200, 150, 250, 120, 230]
    })
    
    # PIVOT (rows to columns)
    pivoted = sales.pivot_table(
        index='date',
        columns='product',
        values='sales',
        aggfunc='sum',
        fill_value=0
    )
    
    # UNPIVOT (columns to rows) - melt
    melted = pivoted.reset_index().melt(
        id_vars=['date'],
        var_name='product',
        value_name='sales'
    )
    
    return pivoted

# ============================================
# PATTERN 7: HANDLING NULLS
# ============================================

def null_handling_patterns(df):
    """NULL handling strategies"""
    
    # Check for nulls
    null_counts = df.isnull().sum()
    
    # Drop rows with ANY null
    no_nulls = df.dropna()
    
    # Drop rows where specific column is null
    no_null_salary = df.dropna(subset=['salary'])
    
    # Fill nulls with value
    df['salary'].fillna(df['salary'].mean(), inplace=True)
    
    # Forward fill (use previous value)
    df['department'].fillna(method='ffill', inplace=True)
    
    # Backward fill
    df['department'].fillna(method='bfill', inplace=True)
    
    return df

# ============================================
# THE INTERVIEW HACK: Escape to SQL
# ============================================

def escape_to_sql_pattern():
    """When Pandas gets complex, pivot to SQL"""
    
    response = """
    # Your answer when it gets too complex:
    
    "In production, I'd handle this in Snowflake with:
    
    WITH ranked_data AS (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) as rn
        FROM employees
    )
    SELECT * FROM ranked_data WHERE rn <= 3
    
    But here's the Pandas equivalent..."
    
    # Then show the Pandas version (even if it's messier)
    """
    return response

# ============================================
# COMMON INTERVIEW QUESTIONS & ANSWERS
# ============================================

"""
Q: "How do you handle large datasets in Pandas?"
A: "I try to push filtering and aggregation to the database level using SQL,
   only bringing aggregated results into Pandas. For truly large datasets,
   I'd use PySpark or process in chunks."

Q: "Pandas vs SQL - when to use which?"
A: "SQL for data extraction, filtering, and joins. Pandas for complex
   statistical analysis, time series, and when I need Python's ecosystem.
   But honestly, 80% of transformations are cleaner in SQL/dbt."

Q: "How do you optimize Pandas operations?"
A: "Use vectorized operations, avoid loops, leverage categorical dtypes
   for string columns, and use query() method for complex filters.
   But the best optimization is often moving the logic to the warehouse."

Q: "Show me how to deduplicate data"
A: df.drop_duplicates(subset=['customer_id'], keep='last')
   "But in production, I'd use ROW_NUMBER() in SQL for more control"

REMEMBER: You're not becoming a Pandas expert. You're learning enough
to pass their gates. Your SQL expertise is your real value.
"""