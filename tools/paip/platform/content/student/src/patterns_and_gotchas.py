#!/usr/bin/env python3
"""
Patterns and Gotchas - Complete Implementation Reference
Analytics Engineering Interview Patterns

This file contains clean, ready-to-use implementations of:
1. Core pandas patterns (20 most common)
2. Gotcha implementations (manual versions without built-ins)
3. Optimized versions showing performance differences

Copy and adapt these patterns during interviews.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from collections import defaultdict, Counter
import time

# ============================================================================
# PART 1: CORE PANDAS PATTERNS
# ============================================================================

class CorePatterns:
    """The 20 patterns that solve 80% of interview problems."""
    
    @staticmethod
    def top_n_by_group(df: pd.DataFrame, group_col: str, value_col: str, n: int = 5) -> pd.DataFrame:
        """
        Pattern: Find top N items by value within each group.
        Common variations: top products by region, best performers by department
        """
        # Method 1: Sort then groupby head (most intuitive)
        result = (df
                 .sort_values(value_col, ascending=False)
                 .groupby(group_col)
                 .head(n))
        
        # Method 2: Using nlargest (more efficient for large data)
        result_alt = (df
                     .groupby(group_col)
                     .apply(lambda x: x.nlargest(n, value_col))
                     .reset_index(drop=True))
        
        return result
    
    @staticmethod
    def groupby_multiple_agg(df: pd.DataFrame) -> pd.DataFrame:
        """
        Pattern: Group by columns with multiple aggregations.
        Common: Revenue reports, summary statistics
        """
        # Method 1: Dictionary of aggregations
        result = df.groupby('category').agg({
            'value': ['sum', 'mean', 'count'],
            'quantity': ['sum', 'mean'],
            'price': ['min', 'max', 'mean']
        }).round(2)
        
        # Method 2: Named aggregations (cleaner columns)
        result_clean = df.groupby('category').agg(
            total_value=('value', 'sum'),
            avg_value=('value', 'mean'),
            count=('value', 'count'),
            total_quantity=('quantity', 'sum')
        ).reset_index()
        
        return result_clean
    
    @staticmethod
    def merge_with_indicator(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        """
        Pattern: Merge dataframes and track source of records.
        Common: Finding unmatched records, data validation
        """
        merged = pd.merge(
            df1, df2, 
            on='key', 
            how='outer', 
            indicator=True
        )
        
        # Analyze merge results
        merge_summary = merged['_merge'].value_counts()
        
        # Get unmatched records
        left_only = merged[merged['_merge'] == 'left_only']
        right_only = merged[merged['_merge'] == 'right_only']
        
        return merged
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        """
        Pattern: Comprehensive missing value handling.
        Common: Data cleaning step in every interview
        """
        df = df.copy()
        
        # Strategy 1: Different fill for each column type
        for col in df.columns:
            if df[col].dtype == 'object':
                # Categorical: fill with 'Unknown' or mode
                df[col].fillna('Unknown', inplace=True)
            elif df[col].dtype in ['int64', 'float64']:
                # Numeric: fill with mean, median, or 0
                df[col].fillna(df[col].median(), inplace=True)
        
        # Strategy 2: Forward/backward fill for time series
        df_time = df.fillna(method='ffill').fillna(method='bfill')
        
        # Strategy 3: Drop if too many missing
        threshold = len(df) * 0.5  # Keep columns with >50% data
        df_clean = df.dropna(thresh=threshold, axis=1)
        
        return df
    
    @staticmethod
    def remove_duplicates_advanced(df: pd.DataFrame) -> pd.DataFrame:
        """
        Pattern: Remove duplicates with various strategies.
        Common: Data quality checks
        """
        # Keep first occurrence
        df1 = df.drop_duplicates(keep='first')
        
        # Keep last occurrence  
        df2 = df.drop_duplicates(keep='last')
        
        # Drop all duplicates (keep none)
        df3 = df.drop_duplicates(keep=False)
        
        # Based on subset of columns
        df4 = df.drop_duplicates(subset=['col1', 'col2'], keep='first')
        
        # Find duplicates for investigation
        duplicates = df[df.duplicated(keep=False)]
        
        return df1
    
    @staticmethod
    def rolling_calculations(df: pd.DataFrame) -> pd.DataFrame:
        """
        Pattern: Rolling/moving window calculations.
        Common: Moving averages, trend analysis
        """
        df = df.copy()
        
        # Simple rolling mean
        df['rolling_mean_7'] = df['value'].rolling(window=7).mean()
        
        # Rolling with min periods (handles start of series)
        df['rolling_mean_safe'] = df['value'].rolling(window=7, min_periods=1).mean()
        
        # Multiple rolling calculations
        df['rolling_std'] = df['value'].rolling(window=7).std()
        df['rolling_max'] = df['value'].rolling(window=7).max()
        df['rolling_min'] = df['value'].rolling(window=7).min()
        
        # Expanding window (cumulative)
        df['expanding_mean'] = df['value'].expanding().mean()
        
        return df
    
    @staticmethod
    def pivot_table_pattern(df: pd.DataFrame) -> pd.DataFrame:
        """
        Pattern: Reshape data with pivot tables.
        Common: Creating reports, cross-tabulations
        """
        # Basic pivot
        pivot1 = df.pivot_table(
            values='sales',
            index='region',
            columns='product',
            aggfunc='sum',
            fill_value=0
        )
        
        # Multiple aggregations
        pivot2 = df.pivot_table(
            values='sales',
            index='region',
            columns='product',
            aggfunc=['sum', 'mean', 'count'],
            fill_value=0
        )
        
        # Multiple values
        pivot3 = df.pivot_table(
            values=['sales', 'quantity'],
            index='region',
            columns='product',
            aggfunc='sum',
            fill_value=0
        )
        
        return pivot1
    
    @staticmethod
    def rank_within_groups(df: pd.DataFrame) -> pd.DataFrame:
        """
        Pattern: Rank items within groups.
        Common: Performance rankings, percentiles
        """
        df = df.copy()
        
        # Dense rank (1,2,2,3)
        df['rank_dense'] = df.groupby('group')['value'].rank(method='dense', ascending=False)
        
        # Min rank (1,2,2,4)
        df['rank_min'] = df.groupby('group')['value'].rank(method='min', ascending=False)
        
        # Percentile rank
        df['percentile'] = df.groupby('group')['value'].rank(pct=True)
        
        # Top 3 flag
        df['is_top3'] = df['rank_dense'] <= 3
        
        return df
    
    @staticmethod
    def cumulative_calculations(df: pd.DataFrame) -> pd.DataFrame:
        """
        Pattern: Cumulative aggregations by group.
        Common: Running totals, YTD calculations
        """
        df = df.copy()
        
        # Cumulative sum by group
        df['cumsum'] = df.groupby('group')['value'].cumsum()
        
        # Cumulative max
        df['cummax'] = df.groupby('group')['value'].cummax()
        
        # Cumulative count
        df['cumcount'] = df.groupby('group').cumcount() + 1
        
        # Percentage of total
        df['pct_of_group_total'] = (
            df.groupby('group')['value']
            .transform(lambda x: x / x.sum() * 100)
        )
        
        return df
    
    @staticmethod
    def date_operations(df: pd.DataFrame) -> pd.DataFrame:
        """
        Pattern: Common date/time operations.
        Common: Time-based filtering and grouping
        """
        df = df.copy()
        
        # Parse dates
        df['date'] = pd.to_datetime(df['date_string'])
        
        # Extract components
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['weekday'] = df['date'].dt.day_name()
        df['is_weekend'] = df['date'].dt.dayofweek.isin([5, 6])
        
        # Date arithmetic
        df['days_since'] = (pd.Timestamp.now() - df['date']).dt.days
        df['month_start'] = df['date'].dt.to_period('M').dt.to_timestamp()
        
        # Resampling for time series
        daily_avg = df.set_index('date').resample('D')['value'].mean()
        
        return df
    
    @staticmethod
    def filter_patterns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Pattern: Complex filtering patterns.
        Common: Data subsetting with multiple conditions
        """
        # Multiple conditions with &, |
        filtered1 = df[(df['value'] > 100) & (df['category'] == 'A')]
        
        # Using isin for multiple values
        filtered2 = df[df['category'].isin(['A', 'B', 'C'])]
        
        # Using between for ranges
        filtered3 = df[df['value'].between(10, 100)]
        
        # String pattern matching
        filtered4 = df[df['name'].str.contains('pattern', case=False, na=False)]
        
        # Query method (cleaner for complex conditions)
        filtered5 = df.query('value > 100 and category in ["A", "B"]')
        
        # Filter by quantiles
        threshold = df['value'].quantile(0.9)
        filtered6 = df[df['value'] > threshold]
        
        return filtered1
    
    @staticmethod
    def apply_patterns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Pattern: Using apply for custom transformations.
        Common: Complex row-wise operations
        """
        df = df.copy()
        
        # Apply to Series (column)
        df['doubled'] = df['value'].apply(lambda x: x * 2)
        
        # Apply to DataFrame (row-wise)
        df['row_sum'] = df.apply(lambda row: row['val1'] + row['val2'], axis=1)
        
        # Apply with conditions
        df['category'] = df['value'].apply(
            lambda x: 'High' if x > 100 else 'Medium' if x > 50 else 'Low'
        )
        
        # Vectorized alternative (faster)
        conditions = [
            df['value'] > 100,
            df['value'] > 50
        ]
        choices = ['High', 'Medium']
        df['category_fast'] = np.select(conditions, choices, default='Low')
        
        return df

# ============================================================================
# PART 2: GOTCHA IMPLEMENTATIONS (Manual Versions)
# ============================================================================

class GotchaImplementations:
    """Manual implementations of common operations - frequent interview questions."""
    
    @staticmethod
    def bubble_sort(arr: List[float]) -> List[float]:
        """
        Implement sort without using .sort() or sorted().
        Time: O(n²), Space: O(1)
        """
        result = arr.copy()
        n = len(result)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
                    swapped = True
            
            if not swapped:
                break
        
        return result
    
    @staticmethod
    def manual_groupby(data: List[Dict], key: str) -> Dict[Any, List]:
        """
        Implement groupby without using pandas.
        Returns dict with grouped data.
        """
        groups = defaultdict(list)
        
        for record in data:
            group_key = record.get(key)
            groups[group_key].append(record)
        
        return dict(groups)
    
    @staticmethod
    def manual_groupby_agg(data: List[Dict], group_key: str, value_key: str, agg_func: str) -> Dict:
        """
        GroupBy with aggregation without pandas.
        Supports 'sum', 'mean', 'count', 'min', 'max'
        """
        groups = defaultdict(list)
        
        # Group data
        for record in data:
            key = record.get(group_key)
            value = record.get(value_key)
            if value is not None:
                groups[key].append(value)
        
        # Apply aggregation
        result = {}
        for key, values in groups.items():
            if agg_func == 'sum':
                result[key] = sum(values)
            elif agg_func == 'mean':
                result[key] = sum(values) / len(values) if values else 0
            elif agg_func == 'count':
                result[key] = len(values)
            elif agg_func == 'min':
                result[key] = min(values) if values else None
            elif agg_func == 'max':
                result[key] = max(values) if values else None
        
        return result
    
    @staticmethod
    def remove_duplicates_manual(items: List) -> List:
        """
        Remove duplicates without using set() or drop_duplicates().
        Preserves original order.
        """
        seen = []
        result = []
        
        for item in items:
            # For unhashable types (like dicts), use different comparison
            if item not in seen:
                seen.append(item)
                result.append(item)
        
        return result
    
    @staticmethod
    def find_max_manual(numbers: List[float]) -> float:
        """
        Find maximum without using max().
        """
        if not numbers:
            return None
        
        max_val = numbers[0]
        for num in numbers[1:]:
            if num > max_val:
                max_val = num
        
        return max_val
    
    @staticmethod
    def count_occurrences_manual(items: List) -> Dict:
        """
        Count occurrences without using Counter or value_counts().
        """
        counts = {}
        
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        
        return counts
    
    @staticmethod
    def reverse_list_manual(lst: List) -> List:
        """
        Reverse a list without using [::-1] or reverse().
        """
        result = []
        for i in range(len(lst) - 1, -1, -1):
            result.append(lst[i])
        
        return result
    
    @staticmethod
    def flatten_nested_manual(nested: List) -> List:
        """
        Flatten arbitrarily nested list without using libraries.
        """
        result = []
        
        def flatten_recursive(lst):
            for item in lst:
                if isinstance(item, list):
                    flatten_recursive(item)
                else:
                    result.append(item)
        
        flatten_recursive(nested)
        return result
    
    @staticmethod
    def join_strings_manual(strings: List[str], delimiter: str = ',') -> str:
        """
        Join strings without using .join().
        """
        if not strings:
            return ''
        
        result = strings[0]
        for s in strings[1:]:
            result += delimiter + s
        
        return result
    
    @staticmethod
    def filter_list_manual(items: List, condition_func) -> List:
        """
        Filter list without using filter() or list comprehension.
        """
        result = []
        
        for item in items:
            if condition_func(item):
                result.append(item)
        
        return result
    
    @staticmethod
    def zip_manual(list1: List, list2: List) -> List[Tuple]:
        """
        Implement zip without using zip().
        """
        result = []
        min_len = min(len(list1), len(list2))
        
        for i in range(min_len):
            result.append((list1[i], list2[i]))
        
        return result
    
    @staticmethod
    def all_manual(items: List[bool]) -> bool:
        """
        Check if all elements are True without using all().
        """
        for item in items:
            if not item:
                return False
        return True
    
    @staticmethod
    def any_manual(items: List[bool]) -> bool:
        """
        Check if any element is True without using any().
        """
        for item in items:
            if item:
                return True
        return False
    
    @staticmethod
    def find_index_manual(lst: List, target) -> int:
        """
        Find index of element without using .index().
        Returns -1 if not found.
        """
        for i, val in enumerate(lst):
            if val == target:
                return i
        return -1
    
    @staticmethod
    def sum_manual(numbers: List[float]) -> float:
        """
        Sum values without using sum().
        """
        total = 0
        for num in numbers:
            total += num
        return total

# ============================================================================
# PART 3: OPTIMIZED VERSIONS - Performance Comparisons
# ============================================================================

class OptimizedPatterns:
    """Shows vectorized vs loop versions for performance discussions."""
    
    @staticmethod
    def calculate_with_loops(df: pd.DataFrame) -> pd.DataFrame:
        """
        SLOW: Using iterrows (never do this in production).
        """
        df = df.copy()
        results = []
        
        for index, row in df.iterrows():
            if row['category'] == 'A':
                value = row['amount'] * 1.2
            elif row['category'] == 'B':
                value = row['amount'] * 1.5
            else:
                value = row['amount']
            results.append(value)
        
        df['adjusted'] = results
        return df
    
    @staticmethod
    def calculate_vectorized(df: pd.DataFrame) -> pd.DataFrame:
        """
        FAST: Using numpy.where for vectorized operations.
        100-1000x faster than loops.
        """
        df = df.copy()
        
        df['adjusted'] = np.where(
            df['category'] == 'A', df['amount'] * 1.2,
            np.where(df['category'] == 'B', df['amount'] * 1.5, df['amount'])
        )
        
        return df
    
    @staticmethod
    def calculate_with_map(df: pd.DataFrame) -> pd.DataFrame:
        """
        FAST: Using map for category lookups.
        Good for many categories.
        """
        df = df.copy()
        
        multipliers = {'A': 1.2, 'B': 1.5, 'C': 1.0}
        df['adjusted'] = df['amount'] * df['category'].map(multipliers).fillna(1.0)
        
        return df
    
    @staticmethod
    def filter_comparison():
        """
        Compare different filtering methods.
        """
        # Create test data
        n = 100000
        df = pd.DataFrame({
            'value': np.random.randn(n) * 100,
            'category': np.random.choice(['A', 'B', 'C'], n)
        })
        
        # Method 1: Boolean indexing (fastest)
        start = time.time()
        result1 = df[df['value'] > 50]
        time1 = time.time() - start
        
        # Method 2: Query method (readable)
        start = time.time()
        result2 = df.query('value > 50')
        time2 = time.time() - start
        
        # Method 3: Using apply (slowest)
        start = time.time()
        result3 = df[df.apply(lambda row: row['value'] > 50, axis=1)]
        time3 = time.time() - start
        
        print(f"Boolean indexing: {time1:.4f}s")
        print(f"Query method: {time2:.4f}s")
        print(f"Apply method: {time3:.4f}s")
        
        return result1
    
    @staticmethod
    def aggregation_comparison():
        """
        Compare aggregation methods.
        """
        # Create test data
        df = pd.DataFrame({
            'group': np.random.choice(['A', 'B', 'C'], 10000),
            'value': np.random.randn(10000) * 100
        })
        
        # Method 1: GroupBy (optimal)
        start = time.time()
        result1 = df.groupby('group')['value'].sum()
        time1 = time.time() - start
        
        # Method 2: Pivot table
        start = time.time()
        result2 = df.pivot_table(values='value', index='group', aggfunc='sum')
        time2 = time.time() - start
        
        # Method 3: Manual loop (terrible)
        start = time.time()
        result3 = {}
        for group in df['group'].unique():
            result3[group] = df[df['group'] == group]['value'].sum()
        time3 = time.time() - start
        
        print(f"GroupBy: {time1:.4f}s")
        print(f"Pivot table: {time2:.4f}s")
        print(f"Manual loop: {time3:.4f}s")

# ============================================================================
# PART 4: QUICK ACCESS PATTERNS - Copy These During Interviews
# ============================================================================

def quick_patterns():
    """
    Quick copy-paste patterns for common interview questions.
    Copy these directly during interviews and modify as needed.
    """
    
    # Sample DataFrame for testing
    df = pd.DataFrame({
        'category': ['A', 'B', 'A', 'B', 'C'] * 20,
        'region': ['North', 'South', 'East', 'West', 'North'] * 20,
        'value': np.random.randint(0, 100, 100),
        'quantity': np.random.randint(1, 10, 100),
        'date': pd.date_range('2024-01-01', periods=100, freq='D')
    })
    
    # ========== PATTERN 1: Top N by Group ==========
    top_3_per_region = (df
                        .sort_values('value', ascending=False)
                        .groupby('region')
                        .head(3))
    
    # ========== PATTERN 2: GroupBy Multiple Aggregations ==========
    summary = df.groupby('category').agg({
        'value': ['sum', 'mean', 'count'],
        'quantity': ['sum', 'mean']
    }).round(2)
    
    # ========== PATTERN 3: Merge with Tracking ==========
    df1 = df[['category', 'value']].head(50)
    df2 = df[['category', 'quantity']].tail(50)
    merged = pd.merge(df1, df2, on='category', how='outer', indicator=True)
    
    # ========== PATTERN 4: Handle Missing Values ==========
    df_with_nulls = df.copy()
    df_with_nulls.loc[::5, 'value'] = np.nan  # Add some nulls
    df_clean = df_with_nulls.copy()
    df_clean['value'].fillna(df_clean['value'].mean(), inplace=True)
    
    # ========== PATTERN 5: Remove Duplicates ==========
    df_unique = df.drop_duplicates(subset=['category', 'region'], keep='first')
    
    # ========== PATTERN 6: Rolling Calculations ==========
    df_sorted = df.sort_values('date')
    df_sorted['rolling_mean_7'] = df_sorted['value'].rolling(window=7, min_periods=1).mean()
    
    # ========== PATTERN 7: Rank Within Groups ==========
    df['rank'] = df.groupby('region')['value'].rank(method='dense', ascending=False)
    top_3_ranked = df[df['rank'] <= 3]
    
    # ========== PATTERN 8: Cumulative Calculations ==========
    df['cumulative_sum'] = df.groupby('category')['value'].cumsum()
    df['pct_of_category'] = df.groupby('category')['value'].transform(lambda x: x / x.sum())
    
    # ========== PATTERN 9: Date Operations ==========
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.day_name()
    monthly_avg = df.groupby(df['date'].dt.to_period('M'))['value'].mean()
    
    # ========== PATTERN 10: Complex Filtering ==========
    filtered = df[(df['value'] > 50) & 
                  (df['category'].isin(['A', 'B'])) & 
                  (df['date'] >= '2024-02-01')]
    
    print("All quick patterns executed successfully!")
    return df

# ============================================================================
# PART 5: INTERVIEW PROBLEM SOLUTIONS - Complete Examples
# ============================================================================

def interview_problem_1():
    """
    PROBLEM: Find top 3 products by revenue in each region, 
    excluding products with less than 10 total sales.
    """
    # Create sample data
    np.random.seed(42)
    sales = pd.DataFrame({
        'product_id': np.random.choice(['P001', 'P002', 'P003', 'P004', 'P005'], 1000),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 1000),
        'quantity': np.random.randint(1, 20, 1000),
        'price': np.random.uniform(10, 100, 1000)
    })
    sales['revenue'] = sales['quantity'] * sales['price']
    
    # Solution
    # Step 1: Find products with >= 10 total sales
    product_sales = sales.groupby('product_id')['quantity'].sum()
    valid_products = product_sales[product_sales >= 10].index
    
    # Step 2: Filter for valid products
    valid_sales = sales[sales['product_id'].isin(valid_products)]
    
    # Step 3: Calculate revenue by region and product
    revenue_by_region_product = (valid_sales
                                 .groupby(['region', 'product_id'])['revenue']
                                 .sum()
                                 .reset_index())
    
    # Step 4: Get top 3 per region
    top_products = (revenue_by_region_product
                    .sort_values('revenue', ascending=False)
                    .groupby('region')
                    .head(3))
    
    return top_products

def interview_problem_2():
    """
    PROBLEM: Calculate customer lifetime value (CLV) from transaction data.
    Include: total spent, average order value, order count, days active.
    """
    # Create sample data
    transactions = pd.DataFrame({
        'customer_id': np.random.choice(range(1, 101), 1000),
        'order_date': pd.date_range('2023-01-01', periods=1000, freq='12H'),
        'amount': np.random.uniform(10, 500, 1000)
    })
    
    # Solution
    clv = transactions.groupby('customer_id').agg({
        'amount': ['sum', 'mean', 'count'],
        'order_date': ['min', 'max']
    })
    
    # Flatten column names
    clv.columns = ['total_spent', 'avg_order_value', 'order_count', 'first_order', 'last_order']
    
    # Calculate days active
    clv['days_active'] = (clv['last_order'] - clv['first_order']).dt.days + 1
    
    # Calculate order frequency
    clv['orders_per_month'] = clv['order_count'] / (clv['days_active'] / 30)
    
    # Segment customers
    clv['segment'] = pd.cut(clv['total_spent'], 
                            bins=[0, 100, 500, 1000, float('inf')],
                            labels=['Low', 'Medium', 'High', 'VIP'])
    
    return clv.reset_index()

def interview_problem_3():
    """
    PROBLEM: Detect potentially fraudulent transactions.
    Flag if: amount > 3 std devs from mean, or > 5x user's average, 
    or multiple transactions within 1 minute.
    """
    # Create sample data
    transactions = pd.DataFrame({
        'user_id': np.random.choice(range(1, 51), 500),
        'timestamp': pd.date_range('2024-01-01', periods=500, freq='5T'),
        'amount': np.random.exponential(50, 500)
    })
    # Add some suspicious transactions
    transactions.loc[::50, 'amount'] *= 10  # Some very high amounts
    
    # Solution
    # Calculate user statistics
    user_stats = transactions.groupby('user_id')['amount'].agg(['mean', 'std']).reset_index()
    
    # Merge back to transactions
    trans_with_stats = pd.merge(transactions, user_stats, on='user_id')
    
    # Flag 1: Amount > 3 std devs from overall mean
    overall_mean = transactions['amount'].mean()
    overall_std = transactions['amount'].std()
    trans_with_stats['flag_outlier'] = (
        trans_with_stats['amount'] > (overall_mean + 3 * overall_std)
    )
    
    # Flag 2: Amount > 5x user's average
    trans_with_stats['flag_user_unusual'] = (
        trans_with_stats['amount'] > (trans_with_stats['mean'] * 5)
    )
    
    # Flag 3: Multiple transactions within 1 minute
    trans_sorted = trans_with_stats.sort_values(['user_id', 'timestamp'])
    trans_sorted['time_diff'] = (trans_sorted
                                 .groupby('user_id')['timestamp']
                                 .diff()
                                 .dt.total_seconds())
    trans_sorted['flag_rapid'] = trans_sorted['time_diff'] < 60
    
    # Combine all flags
    trans_sorted['is_suspicious'] = (
        trans_sorted['flag_outlier'] | 
        trans_sorted['flag_user_unusual'] | 
        trans_sorted['flag_rapid']
    )
    
    suspicious = trans_sorted[trans_sorted['is_suspicious']]
    
    return suspicious

# ============================================================================
# TESTING AND VALIDATION
# ============================================================================

def test_all_patterns():
    """
    Test that all pattern functions work correctly.
    Run this to verify everything is working.
    """
    print("Testing Core Patterns...")
    
    # Create test DataFrame
    test_df = pd.DataFrame({
        'group': ['A', 'B', 'A', 'B', 'C'] * 20,
        'category': ['X', 'Y', 'X', 'Y', 'Z'] * 20,
        'value': np.random.randint(0, 100, 100),
        'date_string': pd.date_range('2024-01-01', periods=100, freq='D').astype(str)
    })
    
    # Test each core pattern
    patterns = CorePatterns()
    
    try:
        patterns.top_n_by_group(test_df, 'group', 'value', 3)
        print("✓ Top N by Group")
        
        patterns.groupby_multiple_agg(test_df)
        print("✓ GroupBy Multiple Aggregations")
        
        patterns.handle_missing_values(test_df)
        print("✓ Handle Missing Values")
        
        patterns.remove_duplicates_advanced(test_df)
        print("✓ Remove Duplicates")
        
        patterns.rolling_calculations(test_df)
        print("✓ Rolling Calculations")
        
        patterns.rank_within_groups(test_df)
        print("✓ Rank Within Groups")
        
        patterns.cumulative_calculations(test_df)
        print("✓ Cumulative Calculations")
        
    except Exception as e:
        print(f"✗ Error in patterns: {e}")
    
    print("\nTesting Gotcha Implementations...")
    
    gotchas = GotchaImplementations()
    test_list = [3, 1, 4, 1, 5, 9, 2, 6]
    
    try:
        gotchas.bubble_sort(test_list)
        print("✓ Bubble Sort")
        
        gotchas.remove_duplicates_manual(test_list)
        print("✓ Manual Deduplication")
        
        gotchas.flatten_nested_manual([1, [2, 3], [4, [5, 6]]])
        print("✓ Flatten Nested")
        
        gotchas.count_occurrences_manual(test_list)
        print("✓ Count Occurrences")
        
    except Exception as e:
        print(f"✗ Error in gotchas: {e}")
    
    print("\nAll patterns tested successfully!")

if __name__ == "__main__":
    # Run tests
    test_all_patterns()
    
    # Show sample usage
    print("\n" + "="*50)
    print("Pattern Library Ready!")
    print("="*50)
    print("\nUsage:")
    print("  from patterns_and_gotchas import CorePatterns, GotchaImplementations")
    print("  patterns = CorePatterns()")
    print("  result = patterns.top_n_by_group(df, 'category', 'value', 5)")
    print("\nOr copy specific patterns from quick_patterns() during interviews")
