-- Filename: pivot_examples.sql
-- SQL Pivot Pattern Examples
-- Transform rows into columns for cross-tab analysis

-- =====================================================
-- EXAMPLE DATA: Sales by Quarter
-- =====================================================
WITH sales_data AS (
    SELECT 'Product A' as product, 'Q1' as quarter, 1000 as revenue UNION ALL
    SELECT 'Product A', 'Q2', 1500 UNION ALL
    SELECT 'Product A', 'Q3', 1200 UNION ALL
    SELECT 'Product A', 'Q4', 1800 UNION ALL
    SELECT 'Product B', 'Q1', 2000 UNION ALL
    SELECT 'Product B', 'Q2', 2200 UNION ALL
    SELECT 'Product B', 'Q3', 2100 UNION ALL
    SELECT 'Product B', 'Q4', 2500
)
SELECT * FROM sales_data;

-- =====================================================
-- PATTERN 1: Manual Pivot using CASE statements
-- Works in ALL SQL databases
-- =====================================================

SELECT 
    product,
    SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END) AS Q1,
    SUM(CASE WHEN quarter = 'Q2' THEN revenue ELSE 0 END) AS Q2,
    SUM(CASE WHEN quarter = 'Q3' THEN revenue ELSE 0 END) AS Q3,
    SUM(CASE WHEN quarter = 'Q4' THEN revenue ELSE 0 END) AS Q4,
    SUM(revenue) AS Total
FROM sales_data
GROUP BY product
ORDER BY product;

-- =====================================================
-- PATTERN 2: Using FILTER clause (PostgreSQL, SQLite)
-- Cleaner syntax than CASE statements
-- =====================================================

SELECT 
    product,
    SUM(revenue) FILTER (WHERE quarter = 'Q1') AS Q1,
    SUM(revenue) FILTER (WHERE quarter = 'Q2') AS Q2,
    SUM(revenue) FILTER (WHERE quarter = 'Q3') AS Q3,
    SUM(revenue) FILTER (WHERE quarter = 'Q4') AS Q4,
    SUM(revenue) AS Total
FROM sales_data
GROUP BY product
ORDER BY product;

-- =====================================================
-- PATTERN 3: Multiple Aggregations Pivot
-- Show different metrics per quarter
-- =====================================================

WITH sales_details AS (
    SELECT 
        product,
        quarter,
        revenue,
        revenue * 0.3 as cost,
        revenue * 0.7 as profit
    FROM sales_data
)
SELECT 
    product,
    -- Revenue by quarter
    SUM(CASE WHEN quarter = 'Q1' THEN revenue END) AS Q1_Revenue,
    SUM(CASE WHEN quarter = 'Q2' THEN revenue END) AS Q2_Revenue,
    SUM(CASE WHEN quarter = 'Q3' THEN revenue END) AS Q3_Revenue,
    SUM(CASE WHEN quarter = 'Q4' THEN revenue END) AS Q4_Revenue,
    -- Profit by quarter  
    SUM(CASE WHEN quarter = 'Q1' THEN profit END) AS Q1_Profit,
    SUM(CASE WHEN quarter = 'Q2' THEN profit END) AS Q2_Profit,
    SUM(CASE WHEN quarter = 'Q3' THEN profit END) AS Q3_Profit,
    SUM(CASE WHEN quarter = 'Q4' THEN profit END) AS Q4_Profit,
    -- Totals
    SUM(revenue) AS Total_Revenue,
    SUM(profit) AS Total_Profit
FROM sales_details
GROUP BY product;

-- =====================================================
-- PATTERN 4: Pivot with String Aggregation
-- Useful for creating comma-separated lists
-- =====================================================

WITH employee_skills AS (
    SELECT 'John' as employee, 'SQL' as skill UNION ALL
    SELECT 'John', 'Python' UNION ALL
    SELECT 'John', 'Spark' UNION ALL
    SELECT 'Jane', 'SQL' UNION ALL
    SELECT 'Jane', 'Java' UNION ALL
    SELECT 'Bob', 'Python' UNION ALL
    SELECT 'Bob', 'SQL'
)
SELECT 
    skill,
    STRING_AGG(CASE WHEN employee = 'John' THEN '✓' END, '') AS John,
    STRING_AGG(CASE WHEN employee = 'Jane' THEN '✓' END, '') AS Jane,
    STRING_AGG(CASE WHEN employee = 'Bob' THEN '✓' END, '') AS Bob
FROM employee_skills
GROUP BY skill
ORDER BY skill;

-- =====================================================
-- PATTERN 5: Date-based Pivot (Monthly/Yearly)
-- Common for time series analysis
-- =====================================================

WITH monthly_data AS (
    SELECT 
        DATE '2024-01-15' as date, 'Store A' as store, 1000 as sales UNION ALL
    SELECT DATE '2024-02-15', 'Store A', 1200 UNION ALL
    SELECT DATE '2024-03-15', 'Store A', 1100 UNION ALL
    SELECT DATE '2024-01-15', 'Store B', 2000 UNION ALL
    SELECT DATE '2024-02-15', 'Store B', 2100 UNION ALL
    SELECT DATE '2024-03-15', 'Store B', 2200
)
SELECT 
    store,
    SUM(CASE WHEN EXTRACT(MONTH FROM date) = 1 THEN sales END) AS Jan,
    SUM(CASE WHEN EXTRACT(MONTH FROM date) = 2 THEN sales END) AS Feb,
    SUM(CASE WHEN EXTRACT(MONTH FROM date) = 3 THEN sales END) AS Mar,
    SUM(sales) AS Q1_Total,
    AVG(sales) AS Avg_Monthly_Sales
FROM monthly_data
WHERE EXTRACT(YEAR FROM date) = 2024
GROUP BY store;

-- =====================================================
-- PATTERN 6: Conditional Count Pivot
-- Count occurrences instead of summing values
-- =====================================================

WITH support_tickets AS (
    SELECT 'High' as priority, 'Open' as status UNION ALL
    SELECT 'High', 'Open' UNION ALL
    SELECT 'High', 'Closed' UNION ALL
    SELECT 'Medium', 'Open' UNION ALL
    SELECT 'Medium', 'Closed' UNION ALL
    SELECT 'Medium', 'Closed' UNION ALL
    SELECT 'Low', 'Open' UNION ALL
    SELECT 'Low', 'Closed'
)
SELECT 
    priority,
    COUNT(CASE WHEN status = 'Open' THEN 1 END) AS Open_Tickets,
    COUNT(CASE WHEN status = 'Closed' THEN 1 END) AS Closed_Tickets,
    COUNT(*) AS Total_Tickets,
    ROUND(100.0 * COUNT(CASE WHEN status = 'Closed' THEN 1 END) / COUNT(*), 1) AS Closed_Percentage
FROM support_tickets
GROUP BY priority
ORDER BY 
    CASE priority 
        WHEN 'High' THEN 1 
        WHEN 'Medium' THEN 2 
        WHEN 'Low' THEN 3 
    END;

-- =====================================================
-- PATTERN 7: Pivot for Comparison Analysis
-- Compare current vs previous period
-- =====================================================

WITH period_comparison AS (
    SELECT 'Product A' as product, 'Current' as period, 5000 as value UNION ALL
    SELECT 'Product A', 'Previous', 4500 UNION ALL
    SELECT 'Product A', 'Target', 5200 UNION ALL
    SELECT 'Product B', 'Current', 3000 UNION ALL
    SELECT 'Product B', 'Previous', 3200 UNION ALL
    SELECT 'Product B', 'Target', 3500
)
SELECT 
    product,
    MAX(CASE WHEN period = 'Previous' THEN value END) AS Previous,
    MAX(CASE WHEN period = 'Current' THEN value END) AS Current,
    MAX(CASE WHEN period = 'Target' THEN value END) AS Target,
    -- Calculate variations
    MAX(CASE WHEN period = 'Current' THEN value END) - 
    MAX(CASE WHEN period = 'Previous' THEN value END) AS Change,
    ROUND(100.0 * (
        MAX(CASE WHEN period = 'Current' THEN value END) - 
        MAX(CASE WHEN period = 'Previous' THEN value END)
    ) / MAX(CASE WHEN period = 'Previous' THEN value END), 1) AS Change_Percent,
    MAX(CASE WHEN period = 'Target' THEN value END) -
    MAX(CASE WHEN period = 'Current' THEN value END) AS Gap_To_Target
FROM period_comparison
GROUP BY product;

-- =====================================================
-- TIPS AND BEST PRACTICES
-- =====================================================
/*
1. PERFORMANCE:
   - Pivot operations can be expensive on large datasets
   - Consider pre-aggregating data in a staging table
   - Use proper indexes on pivot columns

2. NULL HANDLING:
   - Use COALESCE to replace NULLs with meaningful defaults
   - Example: COALESCE(SUM(CASE WHEN ... THEN value END), 0) AS column

3. DYNAMIC PIVOTS:
   - SQL doesn't support dynamic column generation natively
   - Use procedures or application code for dynamic pivots
   - See dynamic_pivot.sql for examples

4. ALTERNATIVES:
   - Some databases have built-in PIVOT functions (SQL Server, Oracle)
   - Consider using reporting tools for complex pivots
   - Sometimes keeping data normalized is better than pivoting

5. COMMON USE CASES:
   - Financial reports (periods as columns)
   - Survey analysis (questions as columns)
   - Inventory matrices (locations/products)
   - Performance scorecards (KPIs as columns)
*/