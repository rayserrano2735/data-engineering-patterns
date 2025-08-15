-- Filename: unpivot_examples.sql
-- SQL Unpivot Pattern Examples
-- Transform columns into rows for normalization and analysis

-- =====================================================
-- UNPIVOT: The reverse of PIVOT operation
-- Converts columns to rows - from wide to long format
-- =====================================================

-- =====================================================
-- EXAMPLE DATA: Quarterly Sales in Pivoted Format
-- =====================================================
WITH pivoted_sales AS (
    SELECT 'Product A' as product, 1000 as Q1, 1500 as Q2, 1200 as Q3, 1800 as Q4 UNION ALL
    SELECT 'Product B', 2000, 2200, 2100, 2500 UNION ALL
    SELECT 'Product C', 1500, 1600, 1700, 1900
)
SELECT * FROM pivoted_sales;

-- =====================================================
-- PATTERN 1: Manual Unpivot using UNION ALL
-- Works in ALL SQL databases
-- =====================================================

WITH pivoted_sales AS (
    SELECT 'Product A' as product, 1000 as Q1, 1500 as Q2, 1200 as Q3, 1800 as Q4 UNION ALL
    SELECT 'Product B', 2000, 2200, 2100, 2500 UNION ALL
    SELECT 'Product C', 1500, 1600, 1700, 1900
)
SELECT product, 'Q1' as quarter, Q1 as revenue FROM pivoted_sales
UNION ALL
SELECT product, 'Q2' as quarter, Q2 as revenue FROM pivoted_sales
UNION ALL
SELECT product, 'Q3' as quarter, Q3 as revenue FROM pivoted_sales
UNION ALL
SELECT product, 'Q4' as quarter, Q4 as revenue FROM pivoted_sales
ORDER BY product, quarter;

-- =====================================================
-- PATTERN 2: Unpivot using CROSS JOIN with CASE
-- More flexible approach
-- =====================================================

WITH pivoted_sales AS (
    SELECT 'Product A' as product, 1000 as Q1, 1500 as Q2, 1200 as Q3, 1800 as Q4 UNION ALL
    SELECT 'Product B', 2000, 2200, 2100, 2500
),
quarters AS (
    SELECT 'Q1' as quarter UNION ALL
    SELECT 'Q2' UNION ALL
    SELECT 'Q3' UNION ALL
    SELECT 'Q4'
)
SELECT 
    p.product,
    q.quarter,
    CASE q.quarter
        WHEN 'Q1' THEN p.Q1
        WHEN 'Q2' THEN p.Q2
        WHEN 'Q3' THEN p.Q3
        WHEN 'Q4' THEN p.Q4
    END as revenue
FROM pivoted_sales p
CROSS JOIN quarters q
ORDER BY product, quarter;

-- =====================================================
-- PATTERN 3: Unpivot Multiple Metric Columns
-- When you have revenue, cost, profit columns for each quarter
-- =====================================================

WITH financial_data AS (
    SELECT 
        'Product A' as product,
        1000 as Q1_Revenue, 300 as Q1_Cost, 700 as Q1_Profit,
        1500 as Q2_Revenue, 400 as Q2_Cost, 1100 as Q2_Profit,
        1200 as Q3_Revenue, 350 as Q3_Cost, 850 as Q3_Profit,
        1800 as Q4_Revenue, 500 as Q4_Cost, 1300 as Q4_Profit
)
SELECT 
    product,
    quarter,
    metric,
    value
FROM (
    -- Q1 Metrics
    SELECT product, 'Q1' as quarter, 'Revenue' as metric, Q1_Revenue as value FROM financial_data
    UNION ALL
    SELECT product, 'Q1', 'Cost', Q1_Cost FROM financial_data
    UNION ALL
    SELECT product, 'Q1', 'Profit', Q1_Profit FROM financial_data
    UNION ALL
    -- Q2 Metrics
    SELECT product, 'Q2', 'Revenue', Q2_Revenue FROM financial_data
    UNION ALL
    SELECT product, 'Q2', 'Cost', Q2_Cost FROM financial_data
    UNION ALL
    SELECT product, 'Q2', 'Profit', Q2_Profit FROM financial_data
    UNION ALL
    -- Q3 Metrics
    SELECT product, 'Q3', 'Revenue', Q3_Revenue FROM financial_data
    UNION ALL
    SELECT product, 'Q3', 'Cost', Q3_Cost FROM financial_data
    UNION ALL
    SELECT product, 'Q3', 'Profit', Q3_Profit FROM financial_data
    UNION ALL
    -- Q4 Metrics
    SELECT product, 'Q4', 'Revenue', Q4_Revenue FROM financial_data
    UNION ALL
    SELECT product, 'Q4', 'Cost', Q4_Cost FROM financial_data
    UNION ALL
    SELECT product, 'Q4', 'Profit', Q4_Profit FROM financial_data
) unpivoted
ORDER BY product, quarter, metric;

-- =====================================================
-- PATTERN 4: Using VALUES for Unpivot (PostgreSQL)
-- Cleaner syntax for PostgreSQL
-- =====================================================

WITH pivoted_sales AS (
    SELECT 'Product A' as product, 1000 as Q1, 1500 as Q2, 1200 as Q3, 1800 as Q4
)
SELECT 
    p.product,
    v.quarter,
    v.revenue
FROM pivoted_sales p
CROSS JOIN LATERAL (
    VALUES 
        ('Q1', p.Q1),
        ('Q2', p.Q2),
        ('Q3', p.Q3),
        ('Q4', p.Q4)
) v(quarter, revenue);

-- =====================================================
-- PATTERN 5: Survey Response Unpivot
-- Converting survey questions from columns to rows
-- =====================================================

WITH survey_responses AS (
    SELECT 
        101 as respondent_id,
        'John' as name,
        5 as question_1,
        4 as question_2,
        5 as question_3,
        3 as question_4,
        4 as question_5
    UNION ALL
    SELECT 102, 'Jane', 4, 4, 3, 5, 5
    UNION ALL
    SELECT 103, 'Bob', 3, 3, 4, 4, 3
)
SELECT 
    respondent_id,
    name,
    question_num,
    response_value
FROM (
    SELECT respondent_id, name, 'Question 1' as question_num, question_1 as response_value FROM survey_responses
    UNION ALL
    SELECT respondent_id, name, 'Question 2', question_2 FROM survey_responses
    UNION ALL
    SELECT respondent_id, name, 'Question 3', question_3 FROM survey_responses
    UNION ALL
    SELECT respondent_id, name, 'Question 4', question_4 FROM survey_responses
    UNION ALL
    SELECT respondent_id, name, 'Question 5', question_5 FROM survey_responses
) unpivoted
ORDER BY respondent_id, question_num;

-- =====================================================
-- PATTERN 6: Date Columns to Rows
-- Converting daily columns to date rows
-- =====================================================

WITH daily_metrics AS (
    SELECT 
        'Store A' as store,
        100 as day_01,
        120 as day_02,
        115 as day_03,
        130 as day_04,
        125 as day_05
)
SELECT 
    store,
    date_num,
    daily_value
FROM (
    SELECT store, 1 as date_num, day_01 as daily_value FROM daily_metrics
    UNION ALL
    SELECT store, 2, day_02 FROM daily_metrics
    UNION ALL
    SELECT store, 3, day_03 FROM daily_metrics
    UNION ALL
    SELECT store, 4, day_04 FROM daily_metrics
    UNION ALL
    SELECT store, 5, day_05 FROM daily_metrics
) unpivoted
ORDER BY store, date_num;

-- =====================================================
-- NATIVE UNPIVOT SYNTAX (SQL Server, Oracle, Snowflake)
-- =====================================================

-- SQL Server / Azure SQL
/*
SELECT product, quarter, revenue
FROM pivoted_sales
UNPIVOT (
    revenue FOR quarter IN (Q1, Q2, Q3, Q4)
) AS unpvt;
*/

-- Snowflake
/*
SELECT *
FROM pivoted_sales
UNPIVOT(revenue FOR quarter IN (Q1, Q2, Q3, Q4))
ORDER BY product, quarter;
*/

-- BigQuery
/*
SELECT product, quarter, revenue
FROM pivoted_sales
UNPIVOT(revenue FOR quarter IN (Q1, Q2, Q3, Q4));
*/

-- =====================================================
-- TIPS AND BEST PRACTICES
-- =====================================================
/*
1. WHEN TO UNPIVOT:
   - Normalizing denormalized data
   - Preparing data for visualization tools
   - Converting wide format to long format for analysis
   - ETL processes requiring normalized structure

2. PERFORMANCE CONSIDERATIONS:
   - UNION ALL is more efficient than UNION (no deduplication)
   - Index the columns being unpivoted if filtering
   - Consider materializing if unpivoting frequently

3. NULL HANDLING:
   - Decide whether to include NULL values in unpivoted results
   - Add WHERE clause to filter: WHERE value IS NOT NULL

4. DATA TYPE CONSISTENCY:
   - Ensure all unpivoted values can be cast to same type
   - Use explicit CAST when mixing data types

5. COMMON USE CASES:
   - Excel/CSV imports with date columns
   - Survey data with question columns
   - Financial data with period columns
   - Sensor data with timestamp columns
   - Converting crosstabs back to normalized form
*/

-- =====================================================
-- EXAMPLE: Filtering NULLs during Unpivot
-- =====================================================

WITH sparse_data AS (
    SELECT 'Product A' as product, 1000 as Q1, NULL as Q2, 1200 as Q3, NULL as Q4
)
SELECT product, quarter, revenue
FROM (
    SELECT product, 'Q1' as quarter, Q1 as revenue FROM sparse_data
    UNION ALL
    SELECT product, 'Q2', Q2 FROM sparse_data
    UNION ALL
    SELECT product, 'Q3', Q3 FROM sparse_data
    UNION ALL
    SELECT product, 'Q4', Q4 FROM sparse_data
) unpivoted
WHERE revenue IS NOT NULL  -- Filter out NULL values
ORDER BY product, quarter;