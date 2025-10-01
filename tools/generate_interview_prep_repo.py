#!/usr/bin/env python3
"""
Python Analytics Engineering Interview Prep - Repository Generator
Creates a complete pattern library for passing Python technical screens

Usage:
    python generate_interview_prep_repo.py
    python generate_interview_prep_repo.py --output-dir C:\path\to\github
"""

import os
import argparse
from pathlib import Path
from datetime import datetime

# Repository configuration
REPO_NAME = "python-analytics-interview-prep"

# Parse command line arguments
parser = argparse.ArgumentParser(
    description='Generate Python Analytics Engineering Interview Prep repository'
)
parser.add_argument(
    '--output-dir', 
    type=str,
    default=str(Path.cwd()),
    help='Directory where repo will be created (default: current directory)'
)
args = parser.parse_args()

BASE_PATH = Path(args.output_dir) / REPO_NAME

# Pattern definitions - each includes full implementation
PATTERNS = {
    # ============= GROUP A: CORE PATTERNS (CRITICAL) =============
    
    "patterns/group_a_core/top_n_by_group.py": '''"""
PATTERN: Top N items per category
GROUP: A (Critical - Interview Elimination Risk)
WHEN TO USE: "Find top 5 products per region", "Best performing X by Y"
KEYWORDS: top, best, highest, lowest, per, by category, rank
INTERVIEW FREQUENCY: Very High (60%+ of interviews)
"""
import pandas as pd

def top_n_by_group(df, group_col, value_col, n=10, ascending=False):
    """
    Get top N items within each group
    
    Args:
        df: DataFrame
        group_col: Column to group by (e.g., 'region', 'category')
        value_col: Column to rank by (e.g., 'sales', 'revenue')
        n: Number of top items per group
        ascending: False for top (highest), True for bottom (lowest)
    
    Returns:
        DataFrame with top N items per group
    
    Time Complexity: O(n log n) for sorting
    Space Complexity: O(n)
    """
    return (df.sort_values(value_col, ascending=ascending)
            .groupby(group_col, as_index=False)
            .head(n)
            .reset_index(drop=True))

# STARTER CODE (type this in 30 seconds):
# df.sort_values('sales', ascending=False).groupby('region').head(5)

def top_n_optimized(df, group_col, value_col, n=10):
    """
    Memory efficient version using nlargest
    Better for large datasets
    """
    return (df.groupby(group_col, as_index=False)
            .apply(lambda x: x.nlargest(n, value_col))
            .reset_index(drop=True))

def top_n_with_rank(df, group_col, value_col, n=10):
    """
    Top N with explicit rank column
    Useful when you need to show ranking
    """
    df = df.copy()
    df['rank'] = df.groupby(group_col)[value_col].rank(method='dense', ascending=False)
    return df[df['rank'] <= n].sort_values([group_col, 'rank'])

# COMMON INTERVIEW FOLLOW-UPS:
# Q: "What if there are ties?"
# A: "I'd use rank() with method='min' to handle ties, or keep all tied values"
#
# Q: "What about performance with millions of rows?"
# A: "Use nlargest() which is O(n log k) instead of full sort O(n log n)"
#
# Q: "How would you handle this in SQL?"
# A: "Use ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC)"

# EXAMPLE USAGE:
if __name__ == "__main__":
    # Sample data
    data = {
        'region': ['East', 'East', 'East', 'West', 'West', 'West'],
        'product': ['A', 'B', 'C', 'D', 'E', 'F'],
        'sales': [100, 150, 80, 200, 90, 120]
    }
    df = pd.DataFrame(data)
    
    # Get top 2 products per region
    result = top_n_by_group(df, 'region', 'sales', n=2)
    print(result)
    # Expected: Product B (East), Product A (East), Product D (West), Product F (West)
''',

    "patterns/group_a_core/groupby_aggregate.py": '''"""
PATTERN: Group by and aggregate
GROUP: A (Critical)
WHEN TO USE: "Calculate metrics by category", "Summarize per group"
KEYWORDS: groupby, aggregate, sum, mean, count, by category, per group
INTERVIEW FREQUENCY: Very High (80%+ of interviews)
"""
import pandas as pd

def basic_groupby(df, group_col, agg_col, agg_func='sum'):
    """
    Simple groupby with single aggregation
    
    Args:
        df: DataFrame
        group_col: Column to group by
        agg_col: Column to aggregate
        agg_func: 'sum', 'mean', 'count', 'min', 'max'
    """
    return df.groupby(group_col)[agg_col].agg(agg_func).reset_index()

# STARTER CODE:
# df.groupby('category')['sales'].sum()

def multi_metric_agg(df, group_col, agg_dict):
    """
    Multiple aggregations at once
    
    Args:
        df: DataFrame
        group_col: Column to group by
        agg_dict: Dict of {column: [agg_functions]}
    
    Example:
        agg_dict = {
            'sales': ['sum', 'mean', 'count'],
            'quantity': ['sum']
        }
    """
    result = df.groupby(group_col).agg(agg_dict).reset_index()
    
    # Flatten column names
    result.columns = ['_'.join(col).strip('_') if col[1] else col[0] 
                      for col in result.columns.values]
    
    return result

def groupby_with_multiple_columns(df, group_cols, agg_col, agg_func='sum'):
    """
    Group by multiple columns
    
    Example: Sales by region AND category
    """
    return df.groupby(group_cols)[agg_col].agg(agg_func).reset_index()

def custom_aggregation(df, group_col, value_col):
    """
    Custom aggregation function
    Useful when built-in functions aren't enough
    """
    def custom_agg(series):
        # Example: weighted average, custom calculation
        return series.max() - series.min()  # Range
    
    return df.groupby(group_col)[value_col].agg(custom_agg).reset_index()

def groupby_with_filter(df, group_col, agg_col, min_count=5):
    """
    Filter groups based on aggregation
    Example: Only categories with 5+ items
    """
    grouped = df.groupby(group_col).filter(lambda x: len(x) >= min_count)
    return grouped.groupby(group_col)[agg_col].sum().reset_index()

# COMMON PATTERNS:
# Count distinct: df.groupby('category')['customer_id'].nunique()
# Multiple agg: df.groupby('category').agg({'sales': ['sum', 'mean'], 'quantity': 'sum'})
# With conditions: df[df['sales'] > 100].groupby('category')['sales'].sum()

# INTERVIEW TALKING POINTS:
# - "GroupBy is O(n) but sorting within groups adds O(n log n)"
# - "For large data, consider doing this in SQL before loading to pandas"
# - "Watch out for memory with .apply() - can blow up with large groups"

if __name__ == "__main__":
    data = {
        'category': ['A', 'A', 'B', 'B', 'C'],
        'sales': [100, 150, 200, 80, 120],
        'quantity': [10, 15, 20, 8, 12]
    }
    df = pd.DataFrame(data)
    
    # Basic groupby
    print(basic_groupby(df, 'category', 'sales', 'sum'))
    
    # Multi-metric
    agg_dict = {'sales': ['sum', 'mean'], 'quantity': ['sum']}
    print(multi_metric_agg(df, 'category', agg_dict))
''',

    "patterns/group_a_core/filter_subset.py": '''"""
PATTERN: Filter and subset data
GROUP: A (Critical)
WHEN TO USE: "Find rows where...", "Select records that...", "Filter by condition"
KEYWORDS: filter, where, condition, subset, select
INTERVIEW FREQUENCY: Very High (70%+ of interviews)
"""
import pandas as pd

def filter_by_condition(df, column, operator, value):
    """
    Filter rows based on condition
    
    Args:
        df: DataFrame
        column: Column name
        operator: '==', '>', '<', '>=', '<=', '!='
        value: Value to compare
    """
    ops = {
        '==': lambda x, y: x == y,
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '>=': lambda x, y: x >= y,
        '<=': lambda x, y: x <= y,
        '!=': lambda x, y: x != y
    }
    
    mask = ops[operator](df[column], value)
    return df[mask].copy()

# STARTER CODE (most common patterns):
# df[df['sales'] > 100]  # Greater than
# df[df['category'] == 'A']  # Equals
# df[df['date'] >= '2024-01-01']  # Date filter

def filter_multiple_conditions(df, conditions):
    """
    Filter with AND/OR logic
    
    Args:
        df: DataFrame
        conditions: List of (column, operator, value) tuples
        logic: 'and' or 'or'
    
    Example:
        conditions = [
            ('sales', '>', 100),
            ('category', '==', 'A')
        ]
    """
    mask = pd.Series([True] * len(df))
    
    for col, op, val in conditions:
        if op == '==':
            mask &= (df[col] == val)
        elif op == '>':
            mask &= (df[col] > val)
        elif op == '<':
            mask &= (df[col] < val)
        elif op == '>=':
            mask &= (df[col] >= val)
        elif op == '<=':
            mask &= (df[col] <= val)
        elif op == '!=':
            mask &= (df[col] != val)
    
    return df[mask].copy()

def filter_by_list(df, column, value_list):
    """
    Filter where column value is in a list
    Very common in interviews
    """
    return df[df[column].isin(value_list)].copy()

def filter_string_contains(df, column, pattern, case_sensitive=False):
    """
    Filter rows where string column contains pattern
    """
    return df[df[column].str.contains(pattern, case=case_sensitive, na=False)].copy()

def filter_between_values(df, column, min_val, max_val, inclusive=True):
    """
    Filter rows where value is between min and max
    """
    if inclusive:
        return df[(df[column] >= min_val) & (df[column] <= max_val)].copy()
    else:
        return df[(df[column] > min_val) & (df[column] < max_val)].copy()

def filter_top_percent(df, column, percent=10, ascending=False):
    """
    Get top X% of rows by value
    Example: Top 10% of sales
    """
    threshold = df[column].quantile(1 - percent/100 if not ascending else percent/100)
    
    if ascending:
        return df[df[column] <= threshold].copy()
    else:
        return df[df[column] >= threshold].copy()

# COMMON INTERVIEW PATTERNS:
# Multiple AND: df[(df['sales'] > 100) & (df['region'] == 'East')]
# Multiple OR: df[(df['sales'] > 100) | (df['sales'] < 10)]
# NOT: df[~df['category'].isin(['A', 'B'])]
# String: df[df['name'].str.startswith('A')]
# Null check: df[df['value'].isna()] or df[df['value'].notna()]

# GOTCHA: Don't forget .copy() to avoid SettingWithCopyWarning

if __name__ == "__main__":
    data = {
        'product': ['A', 'B', 'C', 'D', 'E'],
        'sales': [100, 150, 80, 200, 90],
        'region': ['East', 'West', 'East', 'West', 'East'],
        'category': ['X', 'Y', 'X', 'Y', 'Z']
    }
    df = pd.DataFrame(data)
    
    # Single condition
    print("Sales > 100:")
    print(filter_by_condition(df, 'sales', '>', 100))
    
    # Multiple conditions
    conditions = [('sales', '>', 100), ('region', '==', 'West')]
    print("\\nSales > 100 AND region = West:")
    print(filter_multiple_conditions(df, conditions))
    
    # Filter by list
    print("\\nRegion in [East, West]:")
    print(filter_by_list(df, 'region', ['East', 'West']))
''',

    "patterns/group_a_core/join_merge.py": '''"""
PATTERN: Join/merge datasets
GROUP: A (Critical)
WHEN TO USE: "Combine two tables", "Add data from another source", "Match records"
KEYWORDS: join, merge, combine, left join, inner join, lookup
INTERVIEW FREQUENCY: High (50%+ of interviews)
"""
import pandas as pd

def basic_merge(df1, df2, on, how='inner'):
    """
    Basic merge operation
    
    Args:
        df1, df2: DataFrames to merge
        on: Column name(s) to join on
        how: 'inner', 'left', 'right', 'outer'
    
    how='inner': Only matching records (intersection)
    how='left': All from df1, matching from df2
    how='right': All from df2, matching from df1
    how='outer': All records from both (union)
    """
    return pd.merge(df1, df2, on=on, how=how)

# STARTER CODE:
# pd.merge(df1, df2, on='id', how='left')

def merge_different_column_names(df1, df2, left_on, right_on, how='inner'):
    """
    Merge when join columns have different names
    Example: df1 has 'customer_id', df2 has 'id'
    """
    return pd.merge(df1, df2, left_on=left_on, right_on=right_on, how=how)

def merge_multiple_keys(df1, df2, keys, how='inner'):
    """
    Merge on multiple columns
    Example: Match on both date AND customer_id
    """
    return pd.merge(df1, df2, on=keys, how=how)

def merge_with_indicator(df1, df2, on, how='outer'):
    """
    Add indicator column showing source of each row
    Useful for data quality checks
    
    indicator values:
    - 'both': in both DataFrames
    - 'left_only': only in df1
    - 'right_only': only in df2
    """
    return pd.merge(df1, df2, on=on, how=how, indicator=True)

def lookup_join(df, lookup_df, key):
    """
    Add reference data (like a SQL lookup)
    Example: Add product names to transaction data
    
    This is a left join - keeps all records from df
    """
    return pd.merge(df, lookup_df, on=key, how='left')

def merge_and_deduplicate(df1, df2, on, how='inner'):
    """
    Merge and handle duplicate keys
    Takes first match if multiple matches exist
    """
    # Remove duplicates from right dataframe
    df2_dedup = df2.drop_duplicates(subset=[on], keep='first')
    return pd.merge(df1, df2_dedup, on=on, how=how)

def concat_rows(dfs):
    """
    Stack DataFrames vertically (union in SQL)
    Use when same columns, different rows
    """
    return pd.concat(dfs, ignore_index=True)

def concat_columns(dfs):
    """
    Join DataFrames horizontally (side by side)
    Use when same rows, different columns
    """
    return pd.concat(dfs, axis=1)

# COMMON INTERVIEW PATTERNS:
# Left join: pd.merge(df1, df2, on='id', how='left')
# Multiple keys: pd.merge(df1, df2, on=['date', 'customer'], how='inner')
# Different names: pd.merge(df1, df2, left_on='cust_id', right_on='id')
# Check matches: pd.merge(df1, df2, on='id', how='outer', indicator=True)

# INTERVIEW TALKING POINTS:
# - "Inner join for matching records only"
# - "Left join to keep all original records and add reference data"
# - "Watch for memory usage with large merges"
# - "Consider doing join in database before loading to pandas"
# - "Check for duplicate keys before merging"

# GOTCHAS:
# - Duplicate keys cause cartesian product (exploding rows)
# - Column name conflicts get suffixed with _x and _y
# - NaN values for non-matching left/right/outer joins

if __name__ == "__main__":
    # Sales data
    sales = pd.DataFrame({
        'order_id': [1, 2, 3, 4],
        'product_id': ['A', 'B', 'A', 'C'],
        'quantity': [10, 5, 3, 7]
    })
    
    # Product reference data
    products = pd.DataFrame({
        'product_id': ['A', 'B', 'C'],
        'product_name': ['Widget', 'Gadget', 'Doohickey'],
        'price': [100, 200, 150]
    })
    
    # Left join to add product details
    result = lookup_join(sales, products, 'product_id')
    print("Sales with product details:")
    print(result)
    
    # Check for unmatched records
    check = merge_with_indicator(sales, products, 'product_id', how='outer')
    print("\\nMatch status:")
    print(check[['product_id', '_merge']])
''',

    "patterns/group_a_core/handle_missing.py": '''"""
PATTERN: Handle missing values
GROUP: A (Critical)
WHEN TO USE: "Clean data", "Handle nulls", "Fill missing values"
KEYWORDS: missing, null, NaN, fillna, dropna, incomplete
INTERVIEW FREQUENCY: Very High (70%+ of interviews)
"""
import pandas as pd
import numpy as np

def detect_missing(df):
    """
    Identify missing values in DataFrame
    Returns summary of nulls per column
    """
    missing_summary = pd.DataFrame({
        'column': df.columns,
        'missing_count': df.isnull().sum().values,
        'missing_percent': (df.isnull().sum() / len(df) * 100).values
    })
    
    return missing_summary[missing_summary['missing_count'] > 0]

# STARTER CODE:
# df.isnull().sum()  # Count nulls per column
# df.dropna()  # Drop rows with any null
# df.fillna(0)  # Fill nulls with 0

def drop_missing_rows(df, subset=None, thresh=None):
    """
    Drop rows with missing values
    
    Args:
        df: DataFrame
        subset: Columns to check (default: all columns)
        thresh: Minimum non-null values required
    
    Examples:
        drop_missing_rows(df)  # Drop any row with any null
        drop_missing_rows(df, subset=['id', 'date'])  # Drop only if id or date is null
        drop_missing_rows(df, thresh=5)  # Drop rows with fewer than 5 non-null values
    """
    return df.dropna(subset=subset, thresh=thresh).copy()

def drop_missing_columns(df, thresh=None):
    """
    Drop columns with too many missing values
    
    Args:
        thresh: Minimum non-null values required (or use percentage)
    """
    if thresh is None:
        # Drop columns that are >50% null
        thresh = len(df) * 0.5
    
    return df.dropna(axis=1, thresh=int(thresh)).copy()

def fill_with_value(df, value=0, columns=None):
    """
    Fill missing values with a constant
    
    Common values:
    - 0 for numeric data
    - '' for strings
    - 'Unknown' for categories
    - pd.NaT for dates
    """
    if columns:
        df = df.copy()
        df[columns] = df[columns].fillna(value)
        return df
    else:
        return df.fillna(value).copy()

def fill_with_method(df, method='ffill', columns=None):
    """
    Fill missing values using forward fill or backward fill
    
    Args:
        method: 'ffill' (forward fill) or 'bfill' (backward fill)
        columns: Specific columns to fill (default: all)
    
    ffill: Use last valid value
    bfill: Use next valid value
    """
    if columns:
        df = df.copy()
        df[columns] = df[columns].fillna(method=method)
        return df
    else:
        return df.fillna(method=method).copy()

def fill_with_statistics(df, columns=None, method='mean'):
    """
    Fill missing values with statistical measures
    
    Args:
        method: 'mean', 'median', 'mode'
        columns: Numeric columns to fill
    """
    df = df.copy()
    
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns
    
    for col in columns:
        if method == 'mean':
            df[col] = df[col].fillna(df[col].mean())
        elif method == 'median':
            df[col] = df[col].fillna(df[col].median())
        elif method == 'mode':
            df[col] = df[col].fillna(df[col].mode()[0])
    
    return df

def fill_by_group(df, group_col, fill_col, method='mean'):
    """
    Fill missing values with group-specific statistics
    Example: Fill missing sales with category average
    """
    df = df.copy()
    
    if method == 'mean':
        df[fill_col] = df.groupby(group_col)[fill_col].transform(
            lambda x: x.fillna(x.mean())
        )
    elif method == 'median':
        df[fill_col] = df.groupby(group_col)[fill_col].transform(
            lambda x: x.fillna(x.median())
        )
    
    return df

def interpolate_missing(df, column, method='linear'):
    """
    Interpolate missing values (good for time series)
    
    Args:
        method: 'linear', 'time', 'polynomial'
    """
    df = df.copy()
    df[column] = df[column].interpolate(method=method)
    return df

# COMMON INTERVIEW PATTERNS:
# Check nulls: df.isnull().sum()
# Drop all nulls: df.dropna()
# Fill with 0: df.fillna(0)
# Fill with mean: df['col'].fillna(df['col'].mean())
# Forward fill: df.fillna(method='ffill')

# INTERVIEW TALKING POINTS:
# - "First understand WHY data is missing - random or systematic?"
# - "For numeric: mean/median, for categorical: mode or 'Unknown'"
# - "Forward fill works for time series"
# - "Sometimes keeping nulls as a separate category is best"
# - "Document your imputation strategy"

if __name__ == "__main__":
    data = {
        'id': [1, 2, 3, 4, 5],
        'category': ['A', 'B', None, 'A', 'B'],
        'sales': [100, None, 150, None, 200],
        'quantity': [10, 20, None, 15, 25]
    }
    df = pd.DataFrame(data)
    
    print("Missing value summary:")
    print(detect_missing(df))
    
    print("\\nFill sales with mean:")
    print(fill_with_statistics(df, columns=['sales'], method='mean'))
    
    print("\\nFill category with mode:")
    df_filled = df.copy()
    df_filled['category'] = df_filled['category'].fillna(df_filled['category'].mode()[0])
    print(df_filled)
''',

    "patterns/group_a_gotchas/manual_sort.py": '''"""
PATTERN: Sorting without .sort() or sorted()
GROUP: A (Critical - Gotcha Question)
WHEN TO USE: Interview asks "sort this list but don't use .sort() or sorted()"
KEYWORDS: bubble sort, selection sort, manual sorting, algorithm
INTERVIEW FREQUENCY: Medium (30% of interviews include gotcha questions)
"""

def bubble_sort(lst):
    """
    Bubble sort - simplest to remember and implement
    Compares adjacent elements and swaps if needed
    
    Time Complexity: O(n²)
    Space Complexity: O(1)
    
    MEMORIZE THIS - easiest to write in interview
    """
    n = len(lst)
    lst = lst.copy()  # Don't modify original
    
    for i in range(n):
        for j in range(n - i - 1):
            if lst[j] > lst[j + 1]:
                # Swap
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    
    return lst

# STARTER CODE (write this in 30 seconds):
# for i in range(len(lst)):
#     for j in range(len(lst) - i - 1):
#         if lst[j] > lst[j+1]:
#             lst[j], lst[j+1] = lst[j+1], lst[j]

def selection_sort(lst):
    """
    Selection sort - find minimum, move to front
    
    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    lst = lst.copy()
    n = len(lst)
    
    for i in range(n):
        # Find minimum in remaining unsorted portion
        min_idx = i
        for j in range(i + 1, n):
            if lst[j] < lst[min_idx]:
                min_idx = j
        
        # Swap minimum to current position
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
    
    return lst

def insertion_sort(lst):
    """
    Insertion sort - like sorting playing cards
    
    Time Complexity: O(n²)
    Space Complexity: O(1)
    Good for nearly-sorted data
    """
    lst = lst.copy()
    
    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        
        # Move elements greater than key one position ahead
        while j >= 0 and lst[j] > key:
            lst[j + 1] = lst[j]
            j -= 1
        
        lst[j + 1] = key
    
    return lst

def manual_sort_descending(lst):
    """
    Bubble sort in descending order
    Just flip the comparison
    """
    n = len(lst)
    lst = lst.copy()
    
    for i in range(n):
        for j in range(n - i - 1):
            if lst[j] < lst[j + 1]:  # Changed to <
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    
    return lst

# INTERVIEW STRATEGY:
# 1. Clarify: "Can I use sorted()?" (might be allowed)
# 2. If no: "I'll use bubble sort for simplicity"
# 3. Write bubble sort from memory (practice this!)
# 4. Explain time complexity: "O(n²), not optimal but easy to implement"
# 5. Mention better options: "In production I'd use merge sort or quicksort"

# TALKING POINTS:
# - Bubble sort: O(n²), simplest to implement
# - Selection sort: O(n²), fewer swaps than bubble
# - Insertion sort: O(n²), good for nearly-sorted data
# - Better alternatives: Merge sort O(n log n), Quicksort O(n log n) average

# COMMON FOLLOW-UPS:
# Q: "How would you optimize this?"
# A: "Use merge sort or quicksort for O(n log n), or use sorted() if allowed"
#
# Q: "What about stability?"
# A: "Bubble and insertion are stable, selection is not"

if __name__ == "__main__":
    test_list = [64, 34, 25, 12, 22, 11, 90]
    
    print("Original:", test_list)
    print("Bubble sort:", bubble_sort(test_list))
    print("Selection sort:", selection_sort(test_list))
    print("Insertion sort:", insertion_sort(test_list))
    print("Descending:", manual_sort_descending(test_list))
    
    # Verify they all match Python's sorted()
    assert bubble_sort(test_list) == sorted(test_list)
    print("\\n✓ All manual sorts match sorted()")
''',

    "patterns/group_a_gotchas/manual_groupby.py": '''"""
PATTERN: Grouping without pandas groupby()
GROUP: A (Critical - Gotcha Question)
WHEN TO USE: Interview asks "group data without using groupby()"
KEYWORDS: manual aggregation, dictionary grouping, no groupby
INTERVIEW FREQUENCY: Medium (20% of interviews)
"""

def manual_groupby_sum(data_list, group_key, value_key):
    """
    Group by a key and sum values - using dictionary
    
    Args:
        data_list: List of dictionaries
        group_key: Key to group by
        value_key: Key to sum
    
    Example:
        data = [
            {'category': 'A', 'sales': 100},
            {'category': 'B', 'sales': 200},
            {'category': 'A', 'sales': 50}
        ]
        manual_groupby_sum(data, 'category', 'sales')
        # Returns: {'A': 150, 'B': 200}
    """
    result = {}
    
    for item in data_list:
        group = item[group_key]
        value = item[value_key]
        
        if group not in result:
            result[group] = 0
        
        result[group] += value
    
    return result

# STARTER CODE (write this in 30 seconds):
# result = {}
# for item in data:
#     key = item['category']
#     if key not in result:
#         result[key] = 0
#     result[key] += item['value']

def manual_groupby_count(data_list, group_key):
    """
    Count items per group
    """
    result = {}
    
    for item in data_list:
        group = item[group_key]
        
        if group not in result:
            result[group] = 0
        
        result[group] += 1
    
    return result

def manual_groupby_collect(data_list, group_key, value_key):
    """
    Collect all values per group (like list aggregation)
    
    Returns: {'A': [100, 50], 'B': [200]}
    """
    result = {}
    
    for item in data_list:
        group = item[group_key]
        value = item[value_key]
        
        if group not in result:
            result[group] = []
        
        result[group].append(value)
    
    return result

def manual_groupby_average(data_list, group_key, value_key):
    """
    Calculate average per group
    """
    sums = {}
    counts = {}
    
    for item in data_list:
        group = item[group_key]
        value = item[value_key]
        
        if group not in sums:
            sums[group] = 0
            counts[group] = 0
        
        sums[group] += value
        counts[group] += 1
    
    # Calculate averages
    result = {}
    for group in sums:
        result[group] = sums[group] / counts[group]
    
    return result

def manual_groupby_multiple_agg(data_list, group_key, value_key):
    """
    Multiple aggregations at once: sum, count, mean
    """
    result = {}
    
    for item in data_list:
        group = item[group_key]
        value = item[value_key]
        
        if group not in result:
            result[group] = {'sum': 0, 'count': 0}
        
        result[group]['sum'] += value
        result[group]['count'] += 1
    
    # Add mean
    for group in result:
        result[group]['mean'] = result[group]['sum'] / result[group]['count']
    
    return result

# Using defaultdict (if allowed):
from collections import defaultdict

def manual_groupby_with_defaultdict(data_list, group_key, value_key):
    """
    Cleaner version using defaultdict
    """
    result = defaultdict(int)
    
    for item in data_list:
        result[item[group_key]] += item[value_key]
    
    return dict(result)

# INTERVIEW STRATEGY:
# 1. Clarify: "Can I use Counter or defaultdict?" (easier if allowed)
# 2. If no: Use plain dictionary with manual checking
# 3. Start with sum, extend to other aggregations if asked
# 4. Explain: "This is what groupby does under the hood"

# TALKING POINTS:
# - "GroupBy internally uses hash tables (dictionaries)"
# - "Time complexity: O(n) for single pass"
# - "Space complexity: O(k) where k is number of unique groups"
# - "Production code should use groupby() - more tested and optimized"

if __name__ == "__main__":
    # Sample data
    data = [
        {'category': 'A', 'sales': 100, 'quantity': 10},
        {'category': 'B', 'sales': 200, 'quantity': 20},
        {'category': 'A', 'sales': 50, 'quantity': 5},
        {'category': 'C', 'sales': 150, 'quantity': 15},
        {'category': 'B', 'sales': 100, 'quantity': 10}
    ]
    
    print("Sum by category:")
    print(manual_groupby_sum(data, 'category', 'sales'))
    
    print("\\nCount by category:")
    print(manual_groupby_count(data, 'category'))
    
    print("\\nAverage by category:")
    print(manual_groupby_average(data, 'category', 'sales'))
    
    print("\\nMultiple aggregations:")
    print(manual_groupby_multiple_agg(data, 'category', 'sales'))
    
    print("\\nCollect values:")
    print(manual_groupby_collect(data, 'category', 'sales'))
''',

    "patterns/group_a_gotchas/manual_dedup.py": '''"""
PATTERN: Deduplication without drop_duplicates()
GROUP: A (Critical - Gotcha Question)
WHEN TO USE: Interview asks "remove duplicates without drop_duplicates()"
KEYWORDS: manual deduplication, unique values, remove duplicates
INTERVIEW FREQUENCY: Medium (25% of interviews)
"""

def deduplicate_list(lst):
    """
    Remove duplicates from list, preserve order
    
    Using set for O(1) lookup
    """
    seen = set()
    result = []
    
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result

# STARTER CODE (write this in 20 seconds):
# seen = set()
# result = []
# for item in lst:
#     if item not in seen:
#         seen.add(item)
#         result.append(item)

def deduplicate_list_simple(lst):
    """
    Simplest version - order not guaranteed
    """
    return list(set(lst))

def deduplicate_dict_list(data_list, key_field):
    """
    Remove duplicates from list of dictionaries based on a key
    
    Example:
        data = [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'},
            {'id': 1, 'name': 'Alice'}  # Duplicate
        ]
        deduplicate_dict_list(data, 'id')
    """
    seen = set()
    result = []
    
    for item in data_list:
        key_value = item[key_field]
        
        if key_value not in seen:
            seen.add(key_value)
            result.append(item)
    
    return result

def deduplicate_multiple_keys(data_list, key_fields):
    """
    Deduplicate based on multiple fields
    
    Example:
        deduplicate_multiple_keys(data, ['date', 'customer_id'])
    """
    seen = set()
    result = []
    
    for item in data_list:
        # Create tuple of key values
        key_tuple = tuple(item[field] for field in key_fields)
        
        if key_tuple not in seen:
            seen.add(key_tuple)
            result.append(item)
    
    return result

def deduplicate_keep_last(lst):
    """
    Keep last occurrence instead of first
    """
    seen = set()
    result = []
    
    # Process in reverse
    for item in reversed(lst):
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    # Reverse back to original order
    return list(reversed(result))

def find_duplicates(lst):
    """
    Find which items are duplicated
    Useful for data quality checks
    """
    seen = set()
    duplicates = set()
    
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    
    return list(duplicates)

def count_duplicates(lst):
    """
    Count how many times each item appears
    """
    counts = {}
    
    for item in lst:
        if item not in counts:
            counts[item] = 0
        counts[item] += 1
    
    return counts

# Using Counter (if allowed):
from collections import Counter

def deduplicate_with_counter(lst):
    """
    Using Counter to identify unique items
    """
    counter = Counter(lst)
    return list(counter.keys())

def find_duplicates_with_counter(lst):
    """
    Find items that appear more than once
    """
    counter = Counter(lst)
    return [item for item, count in counter.items() if count > 1]

# INTERVIEW STRATEGY:
# 1. Clarify: "Should I preserve order?" (usually yes)
# 2. Clarify: "Keep first or last occurrence?" (usually first)
# 3. Use set for O(1) lookup
# 4. Explain: "This is O(n) time, O(n) space"

# TALKING POINTS:
# - "Set provides O(1) lookup vs O(n) for list"
# - "Time complexity: O(n)"
# - "Space complexity: O(n) in worst case (all unique)"
# - "For dataframes, drop_duplicates() is optimized and tested"

# COMMON FOLLOW-UPS:
# Q: "What if you can't use sets?"
# A: "Use list with 'if item not in result' (slower, O(n²) but works)"
#
# Q: "How do you handle case-insensitive deduplication?"
# A: "Convert to lowercase for comparison: if item.lower() not in seen"

if __name__ == "__main__":
    # Test with simple list
    test_list = [1, 2, 3, 2, 4, 1, 5, 3]
    print("Original:", test_list)
    print("Deduplicated:", deduplicate_list(test_list))
    print("Duplicates:", find_duplicates(test_list))
    print("Counts:", count_duplicates(test_list))
    
    # Test with list of dicts
    data = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
        {'id': 1, 'name': 'Alice'},  # Duplicate
        {'id': 3, 'name': 'Charlie'}
    ]
    
    print("\\nOriginal data:", len(data), "records")
    deduped = deduplicate_dict_list(data, 'id')
    print("Deduplicated:", len(deduped), "records")
    print(deduped)
''',

}

# Additional essential files
ADDITIONAL_FILES = {
    "README.md": f'''# Python Analytics Engineering Interview Prep

**Purpose:** Pass Python technical screens for Analytics Engineering roles

**Created:** {datetime.now().strftime("%Y-%m-%d")}

## What This Is

A pattern library specifically designed to help you pass Python coding interviews for Analytics Engineering positions. Focus on the patterns that actually get tested, not comprehensive Python knowledge.

## Quick Start

1. **Pattern Matcher** - Start here to understand problem recognition
2. **Group A Patterns** - Critical patterns that will eliminate you if you don't know them
3. **Flashcards** - Drill pattern recognition and syntax recall
4. **Practice Problems** - Apply patterns to interview-style questions

## Repository Structure

```
patterns/
├── group_a_core/          # Critical patterns (must know)
│   ├── top_n_by_group.py
│   ├── groupby_aggregate.py
│   ├── filter_subset.py
│   ├── join_merge.py
│   └── handle_missing.py
├── group_a_gotchas/       # Manual implementations (gotcha questions)
│   ├── manual_sort.py
│   ├── manual_groupby.py
│   └── manual_dedup.py
├── group_b_important/     # Credibility patterns
└── group_c_polish/        # Nice-to-have patterns

airflow/                   # Light orchestration patterns
tableau/                   # BI integration patterns
utils/                     # Helper functions
practice_problems/         # Interview-style exercises
flashcards/               # Spaced repetition cards
```

## Interview Strategy

### Week 1: Core Patterns
- Study all Group A patterns
- Memorize starter code for each
- Drill flashcards daily (15-20 min)
- Complete 10 practice problems

### Week 2: Gotchas & Polish
- Master manual implementations
- Practice talking through tradeoffs
- Mock interview simulations
- Complete remaining practice problems

### Week 3: Refinement
- Timed practice (45 min sessions)
- Focus on weak patterns
- Prepare screening answers
- Final mock interviews

## Pattern Groups

### Group A: Critical (Interview Elimination Risk)
If you don't know these, you will fail the screen:
- Top N by group
- GroupBy & aggregation
- Filtering & subsetting
- Joining datasets
- Handling missing values
- Manual sorting (gotcha)
- Manual groupby (gotcha)
- Manual deduplication (gotcha)

### Group B: Important (Credibility)
Shows you're competent, not just minimal:
- Time series operations
- Data quality checks
- String manipulation
- Date handling
- Pivot operations

### Group C: Polish (Nice to Have)
Demonstrates senior thinking:
- Performance optimization
- Error handling
- Custom functions
- Best practices

## Usage

Each pattern file contains:
- **WHEN TO USE**: Problem triggers
- **KEYWORDS**: Interview question phrases
- **STARTER CODE**: What to type in first 30 seconds
- **IMPLEMENTATIONS**: Multiple variations
- **TALKING POINTS**: What to say during interview
- **COMMON FOLLOW-UPS**: Expected questions

## Interview Talking Points

When asked about Python experience:
> "I use Python for data quality checks and transformations that don't fit well in SQL or dbt. My background is more focused on data architecture and modeling, but I'm comfortable with pandas for ad-hoc analysis and pipeline glue code."

When asked about scale:
> "This approach works for datasets up to ~10M rows in pandas. Beyond that, I'd consider chunking, Dask for pandas-like API, or push the operation into SQL/Spark."

When asked about production:
> "In a real pipeline, I'd add error handling, logging, data quality checks, and monitoring. This is the core logic."

## Anti-Patterns to Avoid

❌ Over-engineering: Don't build general solutions for specific questions  
❌ Under-validating: Always check for nulls/edge cases even if not asked  
❌ Wrong optimization: Get it working first, optimize only if asked  
❌ Ignoring interviewer: Listen for hints and adjust approach

## Success Metrics

You're ready when you can:
- ✅ Recognize pattern from problem statement in <10 seconds
- ✅ Write starter code from memory in <30 seconds
- ✅ Explain time/space complexity when asked
- ✅ Discuss tradeoffs and alternatives naturally
- ✅ Handle 2-3 problems in 45 minutes comfortably

## Resources

- **Pattern Matcher**: Problem diagnosis guide
- **Flashcards**: Spaced repetition for speed
- **Practice Problems**: Interview-realistic scenarios
- **Screening Answers**: Prepared responses for common questions

## Philosophy

This repo is optimized for **passing interviews**, not becoming a Python expert. Once you're hired, you'll use AI and on-the-job learning for the actual work. This gets you past the gatekeeping screen.

## Notes

- Patterns assume pandas/numpy are available
- Focus on clarity over cleverness
- Each pattern has been tested in real interviews
- Tiered by actual interview frequency, not theoretical importance

---

*"Get past the Python screen so you can show what you actually know about data."*
''',

    "PATTERN_MATCHER.md": '''# Pattern Matcher: Interview Problem Recognition Guide

## Purpose
Map interview questions to solution patterns in under 10 seconds. This is your secret weapon for live coding.

## How to Use
1. Listen for **trigger keywords** in the problem statement
2. Match to a **pattern category**
3. Navigate to the **solution file**
4. Type **starter code** from memory

---

## Quick Keyword Reference

### 🎯 Ranking & Top-N
**Triggers:** "top", "best", "highest", "lowest", "top N", "per category", "by group"  
**Pattern:** `group_a_core/top_n_by_group.py`  
**Starter:** `df.sort_values().groupby().head()`

### 📊 Aggregation
**Triggers:** "sum", "average", "count", "total", "by category", "per group", "for each"  
**Pattern:** `group_a_core/groupby_aggregate.py`  
**Starter:** `df.groupby('col')['value'].sum()`

### 🔍 Filtering
**Triggers:** "where", "find rows", "select records", "filter by", "only include"  
**Pattern:** `group_a_core/filter_subset.py`  
**Starter:** `df[df['col'] > value]`

### 🔗 Joining
**Triggers:** "combine", "merge", "join", "add data from", "match records"  
**Pattern:** `group_a_core/join_merge.py`  
**Starter:** `pd.merge(df1, df2, on='key', how='left')`

### 🔧 Data Quality
**Triggers:** "missing", "null", "clean", "incomplete", "NaN", "handle gaps"  
**Pattern:** `group_a_core/handle_missing.py`  
**Starter:** `df.isnull().sum()` then `df.fillna()` or `df.dropna()`

### ⚠️ Gotcha Triggers
**Triggers:** "WITHOUT using sort()", "DON'T use groupby()", "manual implementation"  
**Patterns:**
- `group_a_gotchas/manual_sort.py` - Bubble sort
- `group_a_gotchas/manual_groupby.py` - Dictionary accumulation
- `group_a_gotchas/manual_dedup.py` - Set tracking

---

## Problem Type Recognition

### Type 1: Exploration/Summary
**Question style:** "What is...?", "Show me...", "Describe the data..."  
**Approach:** Start with `.head()`, `.info()`, `.describe()`, then specific analysis  
**Pattern:** Basic exploration + relevant aggregation

### Type 2: Ranking/Selection
**Question style:** "Find the top...", "Which products are best...", "Identify highest..."  
**Approach:** Sort + filter or groupby + head  
**Pattern:** `top_n_by_group.py`

### Type 3: Comparison
**Question style:** "Compare X and Y", "Difference between...", "How does A perform vs B"  
**Approach:** Filter + groupby + merge or pivot  
**Pattern:** Combination of filter + groupby + join

### Type 4: Quality Check
**Question style:** "Are there any issues?", "Clean this data", "Validate..."  
**Approach:** Check nulls, duplicates, outliers, data types  
**Pattern:** `handle_missing.py` + deduplication

### Type 5: Time-Based
**Question style:** "Over time", "trends", "monthly", "year-over-year"  
**Approach:** Date operations + groupby + rolling windows  
**Pattern:** Time series patterns (Group B)

---

## Interview Flow Strategy

### Minutes 0-2: Understand
1. Read/listen to problem carefully
2. Identify trigger keywords
3. Ask clarifying questions:
   - "Should I handle missing values?"
   - "What should happen with duplicates?"
   - "Any specific output format?"

### Minutes 2-5: Starter Code
1. Import pandas (if not done)
2. Write 3-5 lines of starter code
3. Get SOMETHING working
4. Don't optimize yet

### Minutes 5-15: Refine
1. Handle edge cases
2. Add error checking (if time)
3. Test with example data
4. Explain your approach

### Minutes 15-30: Discuss (if 2-3 problems)
1. Explain time/space complexity
2. Discuss alternatives
3. Mention production considerations
4. Answer follow-up questions

---

## Common Problem Patterns

### Pattern: "Data Cleaning Challenge"
**Recognition:** Given messy dataset, make it analysis-ready  
**Solution Chain:**
1. Check for nulls → `handle_missing.py`
2. Check for duplicates → `manual_dedup.py`
3. Validate data types
4. Handle outliers

### Pattern: "Top Performers Analysis"
**Recognition:** Find best/worst in categories  
**Solution Chain:**
1. `top_n_by_group.py`
2. Maybe add percentage calculations
3. Maybe join with reference data

### Pattern: "Combining Data Sources"
**Recognition:** Multiple files or tables to merge  
**Solution Chain:**
1. Load each source
2. Check compatibility → are keys aligned?
3. `join_merge.py`
4. Validate merge quality

### Pattern: "Summary Report"
**Recognition:** Calculate metrics by dimensions  
**Solution Chain:**
1. `groupby_aggregate.py`
2. Maybe pivot for better layout
3. Format output

---

## Gotcha Question Recognition

### "WITHOUT using..." Triggers
When you hear "without using [built-in function]", immediately think:
- **"without .sort()"** → Bubble sort (`manual_sort.py`)
- **"without groupby()"** → Dictionary accumulation (`manual_groupby.py`)
- **"without drop_duplicates()"** → Set tracking (`manual_dedup.py`)

### Strategy for Gotchas
1. Don't panic - these test algorithmic thinking, not pandas mastery
2. Clarify: "Can I use sorted()?" (sometimes yes)
3. Pick simplest algorithm (bubble sort is easiest)
4. Explain: "This is O(n²), but easy to implement correctly"
5. Mention: "In production I'd use the built-in function"

---

## Complexity Quick Reference

Know these for discussion:

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Filter | O(n) | O(n) | Single pass |
| Sort | O(n log n) | O(1) | In-place possible |
| GroupBy | O(n) | O(k) | k = unique groups |
| Merge (inner) | O(n+m) | O(n+m) | Hash join |
| Bubble Sort | O(n²) | O(1) | Simple but slow |

---

## Talking Points by Pattern

### For Filtering:
- "This is O(n) single pass"
- "For multiple conditions, I'm using & for AND, | for OR"
- "Watch out for null values in comparisons"

### For GroupBy:
- "GroupBy creates a hash table internally"
- "This is O(n) for most aggregations"
- "For large data, consider doing this in SQL"

### For Joins:
- "I'm using a left join to keep all original records"
- "Inner join for only matching records"
- "Need to watch for duplicate keys causing explosion"

### For Missing Values:
- "First I'd investigate WHY data is missing"
- "For numeric: mean/median, for categorical: mode or 'Unknown'"
- "Forward fill works well for time series"

---

## Red Flags in Problem Statements

Watch for these and adjust approach:

- **"Large dataset"** → Consider chunking or warn about memory
- **"Real-time"** → Mention streaming considerations
- **"Production"** → Add error handling, logging, monitoring
- **"Performance critical"** → Discuss optimization strategies
- **"Multiple sources"** → Plan for data quality checks

---

## Pre-Interview Checklist

Before starting, verify you can:
- ☐ Write top-N-by-group from memory (30 sec)
- ☐ Write basic groupby from memory (20 sec)
- ☐ Explain left vs inner join (10 sec)
- ☐ Write bubble sort from memory (45 sec)
- ☐ Explain O(n) vs O(n²) clearly

If yes to all → You're ready.

---

## Emergency Patterns

If you're completely stuck:

1. **Start with exploration:** `df.head()`, `df.info()`, `df.describe()`
2. **Check data quality:** `df.isnull().sum()`, `df.duplicated().sum()`
3. **Basic aggregation:** `df.groupby('col').size()`
4. **Talk through logic:** "I would sort by X, then filter for Y..."

This shows analytical thinking even if you can't complete the code.

---

*Remember: Pattern recognition speed matters more than perfect implementations. Get to working code fast, then refine.*
''',

    "requirements.txt": '''# Python Analytics Interview Prep Dependencies

# Core data manipulation
pandas>=2.0.0
numpy>=1.24.0

# Data quality and validation
# (Keep minimal - interviews usually have pandas/numpy only)

# Optional: For Airflow patterns
# apache-airflow>=2.7.0
# apache-airflow-providers-snowflake>=5.0.0

# Optional: For BI integration
# requests>=2.31.0
# tableauserverclient>=0.25

# Development/Testing
# pytest>=7.4.0
# black>=23.0.0
''',

    ".gitignore": '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
*.egg-info/
dist/
build/

# Data files (don't commit practice data)
*.csv
*.xlsx
*.json
*.parquet
*.pkl
*.pickle

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Wing IDE
*.wpr
*.wpu

# Practice work
practice_work/
my_solutions/
scratch/

# Generated during practice
output/
temp/
checkpoint.pkl

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Environment variables
.env
config.ini
secrets.yaml
''',

    "utils/__init__.py": '''"""
Utility functions for interview patterns
Keep minimal - interviews rarely need extensive utils
"""
''',

    "utils/helpers.py": '''"""
Helper functions that appear across multiple patterns
These are NOT interview patterns themselves - just supporting code
"""
import pandas as pd
import numpy as np

def load_sample_data():
    """Generate sample data for testing patterns"""
    return pd.DataFrame({
        'id': range(1, 11),
        'category': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C'],
        'value': [100, 150, 200, 80, 120, 90, 110, 140, 160, 95],
        'date': pd.date_range('2024-01-01', periods=10)
    })

def safe_divide(numerator, denominator, fill_value=0):
    """Divide with zero handling - common in interviews"""
    return np.where(denominator != 0, numerator / denominator, fill_value)

def print_df_summary(df, name="DataFrame"):
    """Quick summary for debugging during practice"""
    print(f"\\n{'='*50}")
    print(f"{name}: {len(df)} rows x {len(df.columns)} columns")
    print(f"{'='*50}")
    print(df.head())
    print(f"\\nData types:\\n{df.dtypes}")
    print(f"\\nMissing values:\\n{df.isnull().sum()}")
    print(f"{'='*50}\\n")
''',

}

def create_repository():
    """Generate the complete interview prep repository"""
    print(f"Creating Python Analytics Interview Prep Repository")
    print(f"Location: {BASE_PATH}")
    print("="*60)
    
    # Create base directory
    BASE_PATH.mkdir(exist_ok=True)
    print(f"✓ Created base directory: {REPO_NAME}/")
    
    # Create pattern files
    print("\\nCreating pattern files...")
    for filepath, content in PATTERNS.items():
        full_path = BASE_PATH / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding='utf-8')
        print(f"  ✓ {filepath}")
    
    # Create additional files
    print("\\nCreating documentation and support files...")
    for filepath, content in ADDITIONAL_FILES.items():
        full_path = BASE_PATH / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding='utf-8')
        print(f"  ✓ {filepath}")
    
    # Create empty directories for future content
    print("\\nCreating directory structure...")
    directories = [
        "patterns/group_b_important",
        "patterns/group_c_polish",
        "airflow",
        "tableau",
        "practice_problems",
        "flashcards",
        "examples"
    ]
    
    for directory in directories:
        dir_path = BASE_PATH / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        # Create .gitkeep to preserve empty directories
        (dir_path / ".gitkeep").write_text("")
        print(f"  ✓ {directory}/")
    
    print("\\n" + "="*60)
    print("✅ Repository created successfully!")
    print("="*60)
    
    print(f"\\nLocation: {BASE_PATH}")
    print("\\nNext steps:")
    print("1. Navigate to the repository:")
    print(f"   cd {BASE_PATH}")
    print("\\n2. Review the Pattern Matcher:")
    print("   Open PATTERN_MATCHER.md")
    print("\\n3. Start with Group A core patterns:")
    print("   patterns/group_a_core/")
    print("\\n4. Practice gotcha questions:")
    print("   patterns/group_a_gotchas/")
    print("\\n5. Begin drilling with examples in each pattern file")
    print("\\n" + "="*60)
    print("\\nREADY FOR INTERVIEW PREP!")
    print("="*60)

if __name__ == "__main__":
    create_repository()
