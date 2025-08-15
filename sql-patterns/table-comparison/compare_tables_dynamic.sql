-- Filename: compare_tables_dynamic.sql
-- Dynamic Table Comparison Pattern
-- Compares two tables column by column and returns only rows with differences
-- Works with any two tables without hardcoding column names

-- =====================================================
-- SNOWFLAKE / SQL SERVER / PostgreSQL Version (using INFORMATION_SCHEMA)
-- =====================================================

-- Step 1: Create a stored procedure for dynamic comparison
CREATE OR REPLACE PROCEDURE compare_tables(
    table1_name VARCHAR,
    table2_name VARCHAR,
    join_key VARCHAR,
    schema_name VARCHAR DEFAULT 'public'
)
RETURNS TABLE()
LANGUAGE SQL
AS
$$
DECLARE
    column_list VARCHAR;
    compare_sql VARCHAR;
    unpivot_sql VARCHAR;
BEGIN
    -- Get all common columns except the join key
    SELECT LISTAGG(
        CASE 
            WHEN column_name != :join_key 
            THEN column_name 
        END, ', '
    ) INTO :column_list
    FROM (
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = :schema_name 
          AND table_name = :table1_name
        INTERSECT
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = :schema_name 
          AND table_name = :table2_name
    );

    -- Build the dynamic SQL
    SET compare_sql = '
    WITH compared AS (
        SELECT 
            t1.' || :join_key || ' as key_value,
            ''table1'' as source,
            t1.*
        FROM ' || :schema_name || '.' || :table1_name || ' t1
        UNION ALL
        SELECT 
            t2.' || :join_key || ' as key_value,
            ''table2'' as source,
            t2.*
        FROM ' || :schema_name || '.' || :table2_name || ' t2
    ),
    unpivoted AS (
        SELECT 
            key_value,
            source,
            column_name,
            column_value
        FROM compared
        UNPIVOT (
            column_value FOR column_name IN (' || :column_list || ')
        )
    ),
    differences AS (
        SELECT 
            key_value,
            column_name,
            MAX(CASE WHEN source = ''table1'' THEN column_value END) as table1_value,
            MAX(CASE WHEN source = ''table2'' THEN column_value END) as table2_value
        FROM unpivoted
        GROUP BY key_value, column_name
        HAVING table1_value != table2_value 
           OR (table1_value IS NULL AND table2_value IS NOT NULL)
           OR (table1_value IS NOT NULL AND table2_value IS NULL)
    )
    SELECT * FROM differences
    ORDER BY key_value, column_name';

    RETURN TABLE(EXECUTE IMMEDIATE :compare_sql);
END;
$$;

-- Usage Example:
CALL compare_tables('customers_old', 'customers_new', 'customer_id', 'public');


-- =====================================================
-- Generic SQL Version (for databases without stored procedures)
-- Can be adapted to specific SQL dialects
-- =====================================================

-- Step 1: First, identify common columns between tables
WITH common_columns AS (
    -- This part varies by database
    -- For PostgreSQL:
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'table1'
    INTERSECT
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'table2'
)
SELECT * FROM common_columns;

-- Step 2: Manually build comparison for each column (example with 3 columns)
WITH comparison_data AS (
    SELECT 
        t1.id as key_value,
        'column1' as column_name,
        t1.column1::text as table1_value,
        t2.column1::text as table2_value
    FROM table1 t1
    FULL OUTER JOIN table2 t2 ON t1.id = t2.id
    WHERE t1.column1 != t2.column1 
       OR (t1.column1 IS NULL AND t2.column1 IS NOT NULL)
       OR (t1.column1 IS NOT NULL AND t2.column1 IS NULL)
    
    UNION ALL
    
    SELECT 
        t1.id as key_value,
        'column2' as column_name,
        t1.column2::text as table1_value,
        t2.column2::text as table2_value
    FROM table1 t1
    FULL OUTER JOIN table2 t2 ON t1.id = t2.id
    WHERE t1.column2 != t2.column2
       OR (t1.column2 IS NULL AND t2.column2 IS NOT NULL)
       OR (t1.column2 IS NOT NULL AND t2.column2 IS NULL)
    
    UNION ALL
    
    SELECT 
        t1.id as key_value,
        'column3' as column_name,
        t1.column3::text as table1_value,
        t2.column3::text as table2_value
    FROM table1 t1
    FULL OUTER JOIN table2 t2 ON t1.id = t2.id
    WHERE t1.column3 != t2.column3
       OR (t1.column3 IS NULL AND t2.column3 IS NOT NULL)
       OR (t1.column3 IS NOT NULL AND t2.column3 IS NULL)
)
SELECT * FROM comparison_data
ORDER BY key_value, column_name;


-- =====================================================
-- Python/Jinja2 Template Version (for dynamic SQL generation)
-- Use this with dbt, Python, or any templating engine
-- =====================================================

{% set columns_to_compare = get_column_names(table1) | intersect(get_column_names(table2)) | reject('==', join_key) %}

WITH comparison_data AS (
    {% for column in columns_to_compare %}
    SELECT 
        t1.{{ join_key }} as key_value,
        '{{ column }}' as column_name,
        CAST(t1.{{ column }} AS VARCHAR) as table1_value,
        CAST(t2.{{ column }} AS VARCHAR) as table2_value
    FROM {{ table1 }} t1
    FULL OUTER JOIN {{ table2 }} t2 
        ON t1.{{ join_key }} = t2.{{ join_key }}
    WHERE t1.{{ column }} != t2.{{ column }}
       OR (t1.{{ column }} IS NULL AND t2.{{ column }} IS NOT NULL)
       OR (t1.{{ column }} IS NOT NULL AND t2.{{ column }} IS NULL)
    {% if not loop.last %}
    UNION ALL
    {% endif %}
    {% endfor %}
)
SELECT 
    key_value,
    column_name,
    table1_value,
    table2_value
FROM comparison_data
ORDER BY key_value, column_name;


-- =====================================================
-- BigQuery Version (using INFORMATION_SCHEMA and EXECUTE IMMEDIATE)
-- =====================================================

DECLARE column_list STRING;
DECLARE compare_sql STRING;

-- Get column list
SET column_list = (
    SELECT STRING_AGG(column_name, ', ')
    FROM (
        SELECT column_name
        FROM `project.dataset.INFORMATION_SCHEMA.COLUMNS`
        WHERE table_name = 'table1'
        INTERSECT DISTINCT
        SELECT column_name
        FROM `project.dataset.INFORMATION_SCHEMA.COLUMNS`
        WHERE table_name = 'table2'
    )
    WHERE column_name != 'id'  -- exclude join key
);

-- Build and execute dynamic SQL
SET compare_sql = FORMAT("""
    WITH base_data AS (
        SELECT 
            t1.id as key_value,
            TO_JSON_STRING(t1) as t1_json,
            TO_JSON_STRING(t2) as t2_json
        FROM `project.dataset.table1` t1
        FULL OUTER JOIN `project.dataset.table2` t2
            ON t1.id = t2.id
    ),
    differences AS (
        SELECT 
            key_value,
            SPLIT(diff, ':')[OFFSET(0)] as column_name,
            JSON_EXTRACT_SCALAR(t1_json, '$.' || SPLIT(diff, ':')[OFFSET(0)]) as table1_value,
            JSON_EXTRACT_SCALAR(t2_json, '$.' || SPLIT(diff, ':')[OFFSET(0)]) as table2_value
        FROM base_data,
        UNNEST(SPLIT('%s', ', ')) as diff
        WHERE JSON_EXTRACT_SCALAR(t1_json, '$.' || diff) != JSON_EXTRACT_SCALAR(t2_json, '$.' || diff)
           OR (JSON_EXTRACT_SCALAR(t1_json, '$.' || diff) IS NULL 
               AND JSON_EXTRACT_SCALAR(t2_json, '$.' || diff) IS NOT NULL)
           OR (JSON_EXTRACT_SCALAR(t1_json, '$.' || diff) IS NOT NULL 
               AND JSON_EXTRACT_SCALAR(t2_json, '$.' || diff) IS NULL)
    )
    SELECT * FROM differences
    ORDER BY key_value, column_name
""", column_list);

EXECUTE IMMEDIATE compare_sql;


-- =====================================================
-- Expected Output Format:
-- =====================================================
-- key_value | column_name | table1_value | table2_value
-- ----------|-------------|--------------|-------------
-- 100       | column1     | ab           | cde
-- 100       | column3     | xyz          | NULL
-- 101       | column2     | 123          | 456
-- 102       | column4     | NULL         | new_value