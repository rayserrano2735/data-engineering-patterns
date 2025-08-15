-- Filename: dynamic_pivot.sql
-- Dynamic Pivot Pattern Examples
-- Generate pivot queries when column values are unknown at design time

-- =====================================================
-- THE CHALLENGE WITH DYNAMIC PIVOTS
-- =====================================================
/*
Standard SQL doesn't support dynamic column generation.
You can't write: PIVOT(SUM(value) FOR category IN (SELECT DISTINCT category FROM table))

Solutions:
1. Two-step process: Query for values, then build pivot
2. Stored procedures with dynamic SQL
3. Application code generation
4. Reporting tool features
*/

-- =====================================================
-- PATTERN 1: PostgreSQL Dynamic Pivot with PL/pgSQL
-- =====================================================

-- Step 1: Create a function that builds and executes dynamic pivot
CREATE OR REPLACE FUNCTION dynamic_pivot(
    table_name text,
    group_column text,
    pivot_column text,
    value_column text,
    aggregate_func text DEFAULT 'SUM'
)
RETURNS TABLE(result json) AS $$
DECLARE
    columns text;
    query text;
BEGIN
    -- Get unique values for pivot columns
    EXECUTE format(
        'SELECT string_agg(DISTINCT 
            format(''%s(CASE WHEN %I = %%L THEN %I END) AS %%I'', 
                   %L, %L, %L, %I), 
            '', '')
         FROM %I',
        aggregate_func, pivot_column, value_column, 
        aggregate_func, pivot_column, value_column,
        pivot_column, table_name
    ) INTO columns;
    
    -- Build the pivot query
    query := format(
        'SELECT %I, %s FROM %I GROUP BY %I ORDER BY %I',
        group_column, columns, table_name, group_column, group_column
    );
    
    -- Execute and return results
    RETURN QUERY EXECUTE query;
END;
$$ LANGUAGE plpgsql;

-- Usage example:
-- SELECT * FROM dynamic_pivot('sales_data', 'product', 'quarter', 'revenue');

-- =====================================================
-- PATTERN 2: SQL Server Dynamic Pivot with sp_executesql
-- =====================================================

-- SQL Server stored procedure for dynamic pivot
CREATE PROCEDURE DynamicPivot
    @TableName NVARCHAR(128),
    @GroupColumn NVARCHAR(128),
    @PivotColumn NVARCHAR(128),
    @ValueColumn NVARCHAR(128),
    @AggregateFunction NVARCHAR(10) = 'SUM'
AS
BEGIN
    DECLARE @columns NVARCHAR(MAX);
    DECLARE @sql NVARCHAR(MAX);
    
    -- Get distinct values for pivot columns
    SELECT @columns = STRING_AGG(QUOTENAME(CAST(ColumnValue AS NVARCHAR(MAX))), ', ')
    FROM (
        SELECT DISTINCT ColumnValue
        FROM (
            SELECT @PivotColumn AS ColumnName, 
                   CAST(@PivotColumn AS NVARCHAR(MAX)) AS ColumnValue
            FROM @TableName
        ) AS DistinctValues
    ) AS ColumnList;
    
    -- Build dynamic pivot query
    SET @sql = N'
    SELECT ' + QUOTENAME(@GroupColumn) + ', ' + @columns + '
    FROM (
        SELECT ' + QUOTENAME(@GroupColumn) + ', 
               ' + QUOTENAME(@PivotColumn) + ', 
               ' + QUOTENAME(@ValueColumn) + '
        FROM ' + QUOTENAME(@TableName) + '
    ) AS SourceTable
    PIVOT (
        ' + @AggregateFunction + '(' + QUOTENAME(@ValueColumn) + ')
        FOR ' + QUOTENAME(@PivotColumn) + ' IN (' + @columns + ')
    ) AS PivotTable
    ORDER BY ' + QUOTENAME(@GroupColumn);
    
    -- Execute dynamic SQL
    EXEC sp_executesql @sql;
END;

-- Usage:
-- EXEC DynamicPivot 'sales_data', 'product', 'quarter', 'revenue', 'SUM';

-- =====================================================
-- PATTERN 3: MySQL Dynamic Pivot with Prepared Statements
-- =====================================================

-- MySQL procedure for dynamic pivot
DELIMITER //

CREATE PROCEDURE DynamicPivotMySQL(
    IN table_name VARCHAR(64),
    IN group_column VARCHAR(64),
    IN pivot_column VARCHAR(64),
    IN value_column VARCHAR(64)
)
BEGIN
    SET @sql = NULL;
    
    -- Build the column list dynamically
    SELECT GROUP_CONCAT(DISTINCT
        CONCAT(
            'SUM(CASE WHEN ', pivot_column, ' = ''',
            pivot_value, ''' THEN ', value_column, ' END) AS `',
            pivot_value, '`'
        )
    ) INTO @sql
    FROM (
        SELECT DISTINCT pivot_column AS pivot_value
        FROM table_name
    ) AS distinct_values;
    
    -- Build the complete query
    SET @sql = CONCAT(
        'SELECT ', group_column, ', ', @sql, 
        ' FROM ', table_name,
        ' GROUP BY ', group_column,
        ' ORDER BY ', group_column
    );
    
    -- Execute the dynamic query
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END//

DELIMITER ;

-- =====================================================
-- PATTERN 4: Python Generation for Any Database
-- =====================================================

/*
Python script to generate dynamic pivot SQL:

import pandas as pd
import sqlalchemy

def generate_pivot_sql(table_name, group_col, pivot_col, value_col, agg_func='SUM'):
    # Connect to database
    engine = sqlalchemy.create_engine('your_connection_string')
    
    # Get distinct pivot values
    query = f"SELECT DISTINCT {pivot_col} FROM {table_name} ORDER BY {pivot_col}"
    pivot_values = pd.read_sql(query, engine)[pivot_col].tolist()
    
    # Build CASE statements
    case_statements = []
    for value in pivot_values:
        case = f"{agg_func}(CASE WHEN {pivot_col} = '{value}' THEN {value_col} END) AS {value}"
        case_statements.append(case)
    
    # Build final query
    sql = f"""
    SELECT 
        {group_col},
        {', '.join(case_statements)}
    FROM {table_name}
    GROUP BY {group_col}
    ORDER BY {group_col}
    """
    
    return sql

# Usage
pivot_sql = generate_pivot_sql('sales_data', 'product', 'quarter', 'revenue')
results = pd.read_sql(pivot_sql, engine)
*/

-- =====================================================
-- PATTERN 5: Snowflake Native Dynamic Pivot
-- =====================================================

-- Snowflake supports dynamic pivots natively with ANY keyword!
-- No need for stored procedures or dynamic SQL

-- Dynamic pivot using ANY - automatically includes all values
SELECT *
FROM sales_data
PIVOT(SUM(revenue) FOR quarter IN (ANY))
ORDER BY product;

-- You can also specify the values dynamically from a subquery
SELECT *
FROM sales_data
PIVOT(SUM(revenue) FOR quarter IN (SELECT DISTINCT quarter FROM sales_data))
ORDER BY product;

-- For multiple aggregations
SELECT *
FROM sales_data
PIVOT(SUM(revenue) AS sum_rev, AVG(revenue) AS avg_rev 
      FOR quarter IN (ANY))
ORDER BY product;

-- With filtering on pivot values
SELECT *
FROM sales_data
PIVOT(SUM(revenue) FOR quarter IN (SELECT DISTINCT quarter 
                                   FROM sales_data 
                                   WHERE quarter LIKE 'Q%'))
ORDER BY product;

-- Note: The column names will be automatically generated based on the values
-- For quarter = 'Q1', 'Q2', etc., columns will be named "'Q1'", "'Q2'", etc.

-- =====================================================
-- PATTERN 6: Two-Step Manual Process (Universal)
-- =====================================================

-- Step 1: Get the distinct values
SELECT DISTINCT quarter 
FROM sales_data 
ORDER BY quarter;
-- Returns: Q1, Q2, Q3, Q4

-- Step 2: Manually build the pivot with the values from Step 1
SELECT 
    product,
    SUM(CASE WHEN quarter = 'Q1' THEN revenue END) AS Q1,
    SUM(CASE WHEN quarter = 'Q2' THEN revenue END) AS Q2,
    SUM(CASE WHEN quarter = 'Q3' THEN revenue END) AS Q3,
    SUM(CASE WHEN quarter = 'Q4' THEN revenue END) AS Q4
FROM sales_data
GROUP BY product;

-- =====================================================
-- PATTERN 7: Using Session Variables (MySQL Example)
-- =====================================================

-- Build dynamic SQL using session variables
SET @sql = NULL;

SELECT GROUP_CONCAT(DISTINCT
    CONCAT(
        'SUM(CASE WHEN quarter = ''',
        quarter,
        ''' THEN revenue END) AS `',
        quarter, '`'
    )
) INTO @sql
FROM sales_data;

SET @sql = CONCAT(
    'SELECT product, ', @sql, 
    ' FROM sales_data ',
    'GROUP BY product'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- =====================================================
-- PATTERN 8: BigQuery Dynamic Pivot with EXECUTE IMMEDIATE
-- =====================================================

DECLARE pivot_columns STRING;
DECLARE pivot_query STRING;

-- Get the pivot columns
SET pivot_columns = (
    SELECT STRING_AGG(DISTINCT CONCAT("'", quarter, "'"), ', ')
    FROM `project.dataset.sales_data`
);

-- Build and execute the pivot query
SET pivot_query = FORMAT("""
    SELECT * FROM (
        SELECT product, quarter, revenue
        FROM `project.dataset.sales_data`
    )
    PIVOT (
        SUM(revenue) FOR quarter IN (%s)
    )
    ORDER BY product
""", pivot_columns);

EXECUTE IMMEDIATE pivot_query;

-- =====================================================
-- BEST PRACTICES FOR DYNAMIC PIVOTS
-- =====================================================
/*
1. SECURITY CONSIDERATIONS:
   - Always validate and sanitize column names to prevent SQL injection
   - Use QUOTENAME() or similar functions to escape identifiers
   - Limit who can execute dynamic pivot procedures

2. PERFORMANCE:
   - Dynamic SQL can't be optimized as well as static queries
   - Consider caching results if pivot values don't change often
   - Use materialized views for frequently accessed pivots

3. ALTERNATIVES TO CONSIDER:
   - Use reporting tools (Tableau, Power BI) that handle pivots
   - Pivot in application code (pandas, Excel)
   - Pre-aggregate into a wide table during ETL
   - Use CROSSTAB extension in PostgreSQL

4. ERROR HANDLING:
   - Check for maximum column limits (varies by database)
   - Handle NULL or empty pivot values
   - Validate that columns exist before building query

5. MAINTENANCE:
   - Document which procedures generate dynamic SQL
   - Log generated queries for debugging
   - Consider version control for stored procedures
*/

-- =====================================================
-- EXAMPLE: Safe Dynamic Pivot with Validation
-- =====================================================

-- PostgreSQL function with safety checks
CREATE OR REPLACE FUNCTION safe_dynamic_pivot(
    table_name text,
    group_column text,
    pivot_column text,
    value_column text
)
RETURNS SETOF RECORD AS $$
DECLARE
    columns text;
    query text;
    max_columns integer := 100;  -- Limit columns to prevent issues
    column_count integer;
BEGIN
    -- Validate inputs
    IF table_name IS NULL OR group_column IS NULL OR pivot_column IS NULL OR value_column IS NULL THEN
        RAISE EXCEPTION 'All parameters must be non-null';
    END IF;
    
    -- Check column count
    EXECUTE format('SELECT COUNT(DISTINCT %I) FROM %I', pivot_column, table_name) INTO column_count;
    
    IF column_count > max_columns THEN
        RAISE EXCEPTION 'Too many pivot columns: % (max: %)', column_count, max_columns;
    END IF;
    
    -- Build and execute pivot
    -- ... (rest of pivot logic)
    
    RETURN QUERY EXECUTE query;
END;
$$ LANGUAGE plpgsql;