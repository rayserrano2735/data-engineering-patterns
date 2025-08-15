# SQL Pivot Pattern Guide

## Overview
Transform rows into columns for cross-tabulation analysis and reporting. This pattern is essential for creating summary reports, comparison matrices, and data visualizations.

## Problem Statement
You have data in a normalized format (rows) but need to present it in a cross-tab format (columns) for:
- Executive dashboards
- Comparison reports  
- Time-series analysis
- Survey results
- Financial statements

## Core Pattern

### Basic Pivot Syntax
```sql
-- Universal pattern using CASE statements
SELECT 
    group_column,
    SUM(CASE WHEN pivot_column = 'Value1' THEN metric END) AS Value1,
    SUM(CASE WHEN pivot_column = 'Value2' THEN metric END) AS Value2,
    SUM(CASE WHEN pivot_column = 'Value3' THEN metric END) AS Value3
FROM source_table
GROUP BY group_column;
```

## Common Use Cases

### 1. Sales by Quarter
Transform quarterly sales data from rows to columns:
```sql
-- From: product, quarter, revenue (rows)
-- To: product, Q1, Q2, Q3, Q4 (columns)
```

### 2. Survey Responses
Convert survey answers into a matrix format:
```sql
-- From: respondent, question, answer (rows)  
-- To: respondent, Question1, Question2, Question3 (columns)
```

### 3. Status Counts
Summarize counts by status:
```sql
-- From: category, status (rows)
-- To: category, open_count, closed_count, pending_count (columns)
```

## Implementation Examples

### Example 1: Simple Pivot
```sql
SELECT 
    product,
    SUM(CASE WHEN quarter = 'Q1' THEN revenue END) AS Q1,
    SUM(CASE WHEN quarter = 'Q2' THEN revenue END) AS Q2,
    SUM(CASE WHEN quarter = 'Q3' THEN revenue END) AS Q3,
    SUM(CASE WHEN quarter = 'Q4' THEN revenue END) AS Q4
FROM sales_data
GROUP BY product;
```

### Example 2: Multiple Aggregations
```sql
SELECT 
    store,
    -- Revenue
    SUM(CASE WHEN month = 'Jan' THEN revenue END) AS Jan_Revenue,
    SUM(CASE WHEN month = 'Feb' THEN revenue END) AS Feb_Revenue,
    -- Profit
    SUM(CASE WHEN month = 'Jan' THEN profit END) AS Jan_Profit,
    SUM(CASE WHEN month = 'Feb' THEN profit END) AS Feb_Profit
FROM monthly_data
GROUP BY store;
```

## Database-Specific Syntax

### Snowflake/BigQuery
```sql
-- Native PIVOT syntax
SELECT * FROM sales_data
PIVOT(SUM(revenue) FOR quarter IN ('Q1', 'Q2', 'Q3', 'Q4'))
ORDER BY product;
```

### PostgreSQL
```sql
-- Using crosstab function
SELECT * FROM crosstab(
    'SELECT product, quarter, revenue FROM sales_data ORDER BY 1,2'
) AS ct(product text, Q1 numeric, Q2 numeric, Q3 numeric, Q4 numeric);
```

### SQL Server
```sql
-- PIVOT operator
SELECT product, [Q1], [Q2], [Q3], [Q4]
FROM sales_data
PIVOT (
    SUM(revenue)
    FOR quarter IN ([Q1], [Q2], [Q3], [Q4])
) AS pvt;
```

## Best Practices

### 1. Performance Optimization
- Pre-aggregate data when possible
- Index pivot columns
- Consider materialized views for frequently used pivots

### 2. NULL Handling
```sql
-- Replace NULLs with zeros
COALESCE(SUM(CASE WHEN quarter = 'Q1' THEN revenue END), 0) AS Q1
```

### 3. Dynamic Pivots
For unknown column values, use:
- Stored procedures
- Application code
- Two-step process (query for values, then build pivot)

### 4. Readability
```sql
-- Use clear column aliases
SUM(CASE WHEN status = 'active' THEN 1 END) AS Active_Count  -- Good
SUM(CASE WHEN status = 'active' THEN 1 END) AS cnt_act       -- Bad
```

## When to Use Pivots

### ✅ Good Use Cases
- Fixed, known set of columns
- Reporting and dashboards
- Data export for Excel/visualization tools
- Comparison analysis

### ❌ When to Avoid
- Unknown or highly variable column values
- Very large result sets (100+ columns)
- When normalized data is needed downstream
- Real-time transactional queries

## Common Pitfalls

1. **Too Many Columns**: Pivoting unique IDs creates one column per ID
2. **Type Mismatches**: Ensure all pivoted values are the same data type
3. **Performance Issues**: Pivoting large datasets without indexes
4. **Maintenance**: Hard-coded column names need updates when data changes

## Testing Your Pivots

```sql
-- Always verify:
-- 1. Row counts match expected
SELECT COUNT(DISTINCT product) FROM source;  -- Should match pivot rows

-- 2. Totals are preserved
SELECT SUM(revenue) FROM source;  -- Should match sum of pivot columns

-- 3. No data is lost
-- Compare pivoted back to original
```

## Related Patterns
- **Unpivot**: Reverse operation (columns to rows)
- **Dynamic SQL**: For unknown pivot columns
- **Window Functions**: For running totals alongside pivots
- **CTEs**: For complex multi-step pivots

## Interview Talking Points
- "I use pivots for executive dashboards where columns represent time periods"
- "I always consider performance - pivoting millions of rows requires strategy"
- "I handle NULLs explicitly to avoid confusion in reports"
- "For dynamic columns, I use a two-step process or stored procedures"

## Example Files
- `pivot_examples.sql` - Complete working examples
- `unpivot_examples.sql` - Reverse operation examples
- `dynamic_pivot.sql` - Dynamic column generation
- `database-specific/` - Vendor-specific implementations

---

*Remember: Pivoting is about presentation. Keep your source data normalized and pivot at the reporting layer when possible.*