# Table Comparison Pattern: Column-Level Difference Detection

## Tutorial Overview

This tutorial teaches you how to build a reusable procedure that compares any two tables at the column level, identifying:
- Value differences in matching columns
- NULL values (actual data, not missing columns)
- Schema differences (columns present in only one table)
- Rows that exist in only one table

**Output format:** `(key, column_name, value_a, value_b, diff_type)`

**What you'll build:**
1. Understanding the query logic step-by-step
2. A reusable Snowflake stored procedure
3. A reusable Databricks Python function

---

## Part 1: Understanding the Query Logic

Let's build the comparison query piece by piece, explaining each step.

### Step 1: Identify All Columns in Both Tables

```sql
WITH all_columns AS (
  SELECT 
    column_name,
    MAX(CASE WHEN source = 'A' THEN 1 ELSE 0 END) AS in_a,
    MAX(CASE WHEN source = 'B' THEN 1 ELSE 0 END) AS in_b
  FROM (
    -- Get all columns from table A (excluding key)
    SELECT column_name, 'A' AS source 
    FROM information_schema.columns 
    WHERE table_schema = 'PUBLIC' 
      AND table_name = 'TABLE_A' 
      AND column_name != 'KEY_COL'
    UNION ALL
    -- Get all columns from table B (excluding key)
    SELECT column_name, 'B' AS source 
    FROM information_schema.columns 
    WHERE table_schema = 'PUBLIC' 
      AND table_name = 'TABLE_B' 
      AND column_name != 'KEY_COL'
  )
  GROUP BY column_name
)
SELECT * FROM all_columns;
```

**What this does:**
- Queries `information_schema.columns` to get metadata about both tables
- Tags each column with its source table ('A' or 'B')
- Uses `MAX(CASE WHEN...)` aggregation to create flags:
  - `in_a = 1` means column exists in table A
  - `in_b = 1` means column exists in table B
  - A column with `in_a = 1, in_b = 1` exists in both tables
  - A column with `in_a = 1, in_b = 0` exists only in A
  - A column with `in_a = 0, in_b = 1` exists only in B

**Example output:**
| column_name | in_a | in_b |
|-------------|------|------|
| name        | 1    | 1    |
| address     | 1    | 1    |
| phone       | 1    | 0    |
| acctbal     | 0    | 1    |

This tells us `phone` is only in table A and `acctbal` is only in table B.

### Step 2: Transform Columns to Rows (UNPIVOT)

```sql
unpivoted_a AS (
  SELECT 
    key_column,
    column_name,
    column_value
  FROM table_a
  UNPIVOT (
    column_value FOR column_name IN (name, address, phone)
  )
)
```

**What this does:**
- Converts each column into a row with `(key, column_name, column_value)` format
- Must specify columns explicitly (or build dynamically)

**Example transformation:**

**Before UNPIVOT (wide format):**
| key_column | name | address | phone |
|------------|------|---------|-------|
| 1          | John | 123 St  | 555-1234 |

**After UNPIVOT (long format):**
| key_column | column_name | column_value |
|------------|-------------|--------------|
| 1          | name        | John         |
| 1          | address     | 123 St       |
| 1          | phone       | 555-1234     |

**Why do this?** It allows us to compare all columns in a single query instead of writing separate comparisons for each column.

### Step 3: Join the Unpivoted Tables

```sql
FROM unpivoted_a a
FULL OUTER JOIN unpivoted_b b
  ON a.key_column = b.key_column 
  AND a.column_name = b.column_name
```

**What this does:**
- Joins on BOTH key column AND column name
- Uses FULL OUTER JOIN to catch all scenarios:
  1. **Both sides match:** key=1, column=name exists in both tables
  2. **Left only:** key=1, column=phone exists in table A but phone column doesn't exist in table B
  3. **Right only:** key=1, column=acctbal exists in table B but acctbal column doesn't exist in table A
  4. **Key mismatch:** key=99 exists in A but not in B (or vice versa)

**Example join results:**
| a.key | a.column_name | a.column_value | b.key | b.column_name | b.column_value |
|-------|---------------|----------------|-------|---------------|----------------|
| 1     | name          | John           | 1     | name          | John           |
| 1     | address       | 123 St         | 1     | address       | 456 Ave        |
| 1     | phone         | 555-1234       | NULL  | NULL          | NULL           |
| NULL  | NULL          | NULL           | 1     | acctbal       | 1000.00        |

Row 1: Both have same value (no difference)
Row 2: Different values (value_difference)
Row 3: phone exists in A but not in B's schema (column_only_in_a)
Row 4: acctbal exists in B but not in A's schema (column_only_in_b)

### Step 4: Add Schema Metadata

```sql
JOIN all_columns c 
  ON c.column_name = COALESCE(a.column_name, b.column_name)
```

**What this does:**
- Joins our column metadata from Step 1
- Uses `COALESCE(a.column_name, b.column_name)` because one side might be NULL
- This gives us the `in_a` and `in_b` flags for each row

**Why?** We need to distinguish:
- `value_a = NULL` because the data is NULL (in_a = 1, value is NULL)
- `value_a = NULL` because the column doesn't exist (in_a = 0)

### Step 5: Handle Missing Columns vs NULL Values

```sql
SELECT 
  COALESCE(a.key_column, b.key_column) AS key,
  COALESCE(a.column_name, b.column_name) AS column_name,
  CASE 
    WHEN c.in_a = 0 THEN '<COLUMN_MISSING>'
    ELSE a.column_value 
  END AS value_a,
  CASE 
    WHEN c.in_b = 0 THEN '<COLUMN_MISSING>'
    ELSE b.column_value 
  END AS value_b,
  CASE
    WHEN c.in_a = 0 THEN 'column_only_in_b'
    WHEN c.in_b = 0 THEN 'column_only_in_a'
    ELSE 'value_difference'
  END AS diff_type
```

**What this does:**
- Uses `COALESCE` to handle when one side is NULL from the FULL OUTER JOIN
- Checks `c.in_a = 0` to detect when column doesn't exist in table A
  - If column missing: Show `<COLUMN_MISSING>` instead of NULL
  - If column exists: Show the actual value (even if it's NULL)
- Creates `diff_type` to categorize the difference

**Example output interpretation:**

| key | column_name | value_a | value_b | diff_type |
|-----|-------------|---------|---------|-----------|
| 1   | name        | John    | Jane    | value_difference |
| 1   | address     | NULL    | 456 Ave | value_difference |
| 1   | phone       | 555-1234 | <COLUMN_MISSING> | column_only_in_a |
| 1   | acctbal     | <COLUMN_MISSING> | 1000.00 | column_only_in_b |

- Row 1: Both tables have `name` column, but values differ
- Row 2: Both tables have `address` column, A has NULL, B has a value
- Row 3: Only A has `phone` column
- Row 4: Only B has `acctbal` column

### Step 6: Filter to Only Differences

```sql
WHERE a.column_value IS DISTINCT FROM b.column_value
   OR c.in_a = 0 
   OR c.in_b = 0
```

**What this does:**
- `IS DISTINCT FROM` catches value differences INCLUDING NULL comparisons:
  - `'John' IS DISTINCT FROM 'Jane'` → TRUE
  - `NULL IS DISTINCT FROM 'value'` → TRUE
  - `NULL IS DISTINCT FROM NULL` → FALSE (same!)
- `c.in_a = 0` catches columns that exist only in B
- `c.in_b = 0` catches columns that exist only in A

**Why IS DISTINCT FROM?**
Regular `!=` doesn't work with NULLs:
- `NULL != 'value'` → NULL (not TRUE!)
- `NULL != NULL` → NULL (not FALSE!)

---

## Part 2: Core Concepts Summary

### UNPIVOT Transformation
Converts columnar data into row format, enabling single-query comparison of all columns.

### FULL OUTER JOIN
Catches three scenarios:
- Rows in both tables (compare values)
- Rows only in table A
- Rows only in table B

### IS DISTINCT FROM
Properly handles NULL comparisons unlike `!=` or `<>`.

### Dynamic Column Detection
Uses information schema to differentiate between NULL values and missing columns.

---

## Part 3: Snowflake Reusable Procedure

Let's create a stored procedure that can compare any two tables.

### Step 1: Create Test Data

```sql
-- Use the TPCH sample database
USE SCHEMA SNOWFLAKE_SAMPLE_DATA.TPCH_SF1;

-- Create a working schema for our test
CREATE SCHEMA IF NOT EXISTS comparison_demo;
USE SCHEMA comparison_demo;

-- Create two versions of CUSTOMER table with differences
CREATE OR REPLACE TABLE customer_v1 AS
SELECT 
  C_CUSTKEY,
  C_NAME,
  C_ADDRESS,
  C_NATIONKEY,
  C_PHONE
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER
WHERE C_CUSTKEY <= 10;

CREATE OR REPLACE TABLE customer_v2 AS
SELECT 
  C_CUSTKEY,
  C_NAME,
  C_ADDRESS,
  C_NATIONKEY,
  -- C_PHONE removed (schema difference)
  C_ACCTBAL  -- new column added (schema difference)
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER
WHERE C_CUSTKEY <= 10;

-- Introduce data differences
UPDATE customer_v2 SET C_NAME = 'MODIFIED NAME' WHERE C_CUSTKEY = 1;
UPDATE customer_v2 SET C_ADDRESS = NULL WHERE C_CUSTKEY = 2;
UPDATE customer_v1 SET C_ADDRESS = NULL WHERE C_CUSTKEY = 3;
UPDATE customer_v2 SET C_NATIONKEY = 99 WHERE C_CUSTKEY = 4;

-- View the test data
SELECT * FROM customer_v1 ORDER BY C_CUSTKEY;
SELECT * FROM customer_v2 ORDER BY C_CUSTKEY;
```

### Step 2: Create the Reusable Stored Procedure

```sql
CREATE OR REPLACE PROCEDURE compare_tables(
  schema_a VARCHAR,
  table_a VARCHAR,
  schema_b VARCHAR,
  table_b VARCHAR,
  key_columns ARRAY,
  exclude_columns ARRAY DEFAULT []
)
RETURNS TABLE(
  key VARCHAR,
  column_name VARCHAR,
  value_a VARCHAR,
  value_b VARCHAR,
  diff_type VARCHAR
)
LANGUAGE SQL
AS
$$
DECLARE
  column_list_a VARCHAR;
  column_list_b VARCHAR;
  key_cols_str VARCHAR;
  exclude_cols_str VARCHAR;
  sql_query VARCHAR;
BEGIN
  -- Build key column join condition
  key_cols_str := (
    SELECT LISTAGG('a.key_' || seq || ' = b.key_' || seq, ' AND ')
    FROM (SELECT seq4() as seq FROM TABLE(FLATTEN(input => :key_columns)))
  );
  
  -- Build exclude condition for information schema query
  IF (ARRAY_SIZE(:exclude_columns) > 0) THEN
    exclude_cols_str := ' AND column_name NOT IN (' || 
      (SELECT LISTAGG('''' || value || '''', ',') FROM TABLE(FLATTEN(input => :exclude_columns))) || ')';
  ELSE
    exclude_cols_str := '';
  END IF;
  
  -- Get column list for table A (excluding key and excluded columns)
  column_list_a := (
    SELECT LISTAGG(column_name, ', ') WITHIN GROUP (ORDER BY column_name)
    FROM information_schema.columns
    WHERE table_schema = :schema_a
      AND table_name = :table_a
      AND column_name NOT IN (SELECT value FROM TABLE(FLATTEN(input => :key_columns)))
    HAVING COUNT(*) > 0
  ) || exclude_cols_str;
  
  -- Get column list for table B
  column_list_b := (
    SELECT LISTAGG(column_name, ', ') WITHIN GROUP (ORDER BY column_name)
    FROM information_schema.columns
    WHERE table_schema = :schema_b
      AND table_name = :table_b
      AND column_name NOT IN (SELECT value FROM TABLE(FLATTEN(input => :key_columns)))
    HAVING COUNT(*) > 0
  ) || exclude_cols_str;
  
  -- Build the dynamic comparison query
  sql_query := '
  WITH all_columns AS (
    SELECT 
      column_name,
      MAX(CASE WHEN source = ''A'' THEN 1 ELSE 0 END) AS in_a,
      MAX(CASE WHEN source = ''B'' THEN 1 ELSE 0 END) AS in_b
    FROM (
      SELECT column_name, ''A'' AS source 
      FROM information_schema.columns 
      WHERE table_schema = ''' || :schema_a || ''' 
        AND table_name = ''' || :table_a || ''' 
        AND column_name NOT IN (' || 
          (SELECT LISTAGG('''' || value || '''', ',') FROM TABLE(FLATTEN(input => :key_columns))) || ')
        ' || exclude_cols_str || '
      UNION ALL
      SELECT column_name, ''B'' AS source 
      FROM information_schema.columns 
      WHERE table_schema = ''' || :schema_b || ''' 
        AND table_name = ''' || :table_b || ''' 
        AND column_name NOT IN (' || 
          (SELECT LISTAGG('''' || value || '''', ',') FROM TABLE(FLATTEN(input => :key_columns))) || ')
        ' || exclude_cols_str || '
    )
    GROUP BY column_name
  ),
  keys_a AS (
    SELECT ' || 
      (SELECT LISTAGG(value || ' AS key_' || seq4(), ', ') 
       FROM TABLE(FLATTEN(input => :key_columns))) || '
    FROM ' || :schema_a || '.' || :table_a || '
  ),
  keys_b AS (
    SELECT ' || 
      (SELECT LISTAGG(value || ' AS key_' || seq4(), ', ') 
       FROM TABLE(FLATTEN(input => :key_columns))) || '
    FROM ' || :schema_b || '.' || :table_b || '
  ),
  all_keys AS (
    SELECT * FROM keys_a
    UNION
    SELECT * FROM keys_b
  ),
  unpivoted_a AS (
    SELECT 
      ' || (SELECT LISTAGG('a.key_' || seq4(), ', ') 
            FROM TABLE(FLATTEN(input => :key_columns))) || ',
      column_name,
      column_value
    FROM ' || :schema_a || '.' || :table_a || ' a
    UNPIVOT (
      column_value FOR column_name IN (' || column_list_a || ')
    )
  ),
  unpivoted_b AS (
    SELECT 
      ' || (SELECT LISTAGG('b.key_' || seq4(), ', ') 
            FROM TABLE(FLATTEN(input => :key_columns))) || ',
      column_name,
      column_value
    FROM ' || :schema_b || '.' || :table_b || ' b
    UNPIVOT (
      column_value FOR column_name IN (' || column_list_b || ')
    )
  )
  SELECT 
    ' || (SELECT LISTAGG('COALESCE(a.key_' || seq4() || ', b.key_' || seq4() || ')', ' || ''|'' || ') 
          FROM TABLE(FLATTEN(input => :key_columns))) || ' AS key,
    COALESCE(a.column_name, b.column_name) AS column_name,
    CASE 
      WHEN c.in_a = 0 THEN ''<COLUMN_MISSING>''
      ELSE a.column_value 
    END AS value_a,
    CASE 
      WHEN c.in_b = 0 THEN ''<COLUMN_MISSING>''
      ELSE b.column_value 
    END AS value_b,
    CASE
      WHEN c.in_a = 0 THEN ''column_only_in_b''
      WHEN c.in_b = 0 THEN ''column_only_in_a''
      ELSE ''value_difference''
    END AS diff_type
  FROM unpivoted_a a
  FULL OUTER JOIN unpivoted_b b
    ON ' || key_cols_str || '
    AND a.column_name = b.column_name
  JOIN all_columns c 
    ON c.column_name = COALESCE(a.column_name, b.column_name)
  WHERE a.column_value IS DISTINCT FROM b.column_value
     OR c.in_a = 0 
     OR c.in_b = 0
  ORDER BY key, column_name';
  
  -- Create temporary result table
  LET res RESULTSET := (EXECUTE IMMEDIATE :sql_query);
  RETURN TABLE(res);
END;
$$;
```

### Step 3: Use the Procedure

```sql
-- Single key column comparison
CALL compare_tables(
  'COMPARISON_DEMO',           -- schema A
  'CUSTOMER_V1',               -- table A
  'COMPARISON_DEMO',           -- schema B
  'CUSTOMER_V2',               -- table B
  ARRAY_CONSTRUCT('C_CUSTKEY') -- key columns
);
```

**Expected Output:**
```
KEY | COLUMN_NAME  | VALUE_A              | VALUE_B         | DIFF_TYPE
----|--------------|----------------------|-----------------|------------------
1   | C_ACCTBAL    | <COLUMN_MISSING>     | 711.56          | column_only_in_b
1   | C_NAME       | Customer#000000001   | MODIFIED NAME   | value_difference
1   | C_PHONE      | 25-989-741-2988      | <COLUMN_MISSING>| column_only_in_a
2   | C_ACCTBAL    | <COLUMN_MISSING>     | 121.65          | column_only_in_b
2   | C_ADDRESS    | XSTf4,NCwDVaWNe...   | NULL            | value_difference
2   | C_PHONE      | 28-190-982-9759      | <COLUMN_MISSING>| column_only_in_a
3   | C_ACCTBAL    | <COLUMN_MISSING>     | 7498.12         | column_only_in_b
3   | C_ADDRESS    | NULL                 | MG9kdTD2WBHm    | value_difference
3   | C_PHONE      | 11-719-748-3364      | <COLUMN_MISSING>| column_only_in_a
4   | C_ACCTBAL    | <COLUMN_MISSING>     | 2866.83         | column_only_in_b
4   | C_NATIONKEY  | 4                    | 99              | value_difference
4   | C_PHONE      | 14-128-190-5944      | <COLUMN_MISSING>| column_only_in_a
```

### Step 4: Advanced Usage - Composite Keys

```sql
-- Create tables with composite keys
CREATE OR REPLACE TABLE orders_v1 AS
SELECT 
  O_ORDERKEY,
  O_CUSTKEY,
  O_ORDERSTATUS,
  O_TOTALPRICE,
  O_ORDERDATE
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
WHERE O_ORDERKEY <= 10;

CREATE OR REPLACE TABLE orders_v2 AS
SELECT 
  O_ORDERKEY,
  O_CUSTKEY,
  O_ORDERSTATUS,
  O_TOTALPRICE,
  O_CLERK  -- Different column
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
WHERE O_ORDERKEY <= 10;

-- Modify some data
UPDATE orders_v2 SET O_TOTALPRICE = O_TOTALPRICE * 1.1 WHERE O_ORDERKEY = 1;

-- Compare with composite key
CALL compare_tables(
  'COMPARISON_DEMO',
  'ORDERS_V1',
  'COMPARISON_DEMO',
  'ORDERS_V2',
  ARRAY_CONSTRUCT('O_ORDERKEY', 'O_CUSTKEY'),  -- Composite key
  ARRAY_CONSTRUCT()                             -- No exclusions
);
```

### Step 5: Excluding Columns

```sql
-- Compare but exclude certain columns
CALL compare_tables(
  'COMPARISON_DEMO',
  'CUSTOMER_V1',
  'COMPARISON_DEMO',
  'CUSTOMER_V2',
  ARRAY_CONSTRUCT('C_CUSTKEY'),
  ARRAY_CONSTRUCT('C_ADDRESS')  -- Exclude address from comparison
);
```

### Procedure Parameters Explained

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `schema_a` | VARCHAR | Schema containing first table | `'PUBLIC'` |
| `table_a` | VARCHAR | First table name | `'CUSTOMER_V1'` |
| `schema_b` | VARCHAR | Schema containing second table | `'PUBLIC'` |
| `table_b` | VARCHAR | Second table name | `'CUSTOMER_V2'` |
| `key_columns` | ARRAY | Columns that uniquely identify rows | `ARRAY_CONSTRUCT('ID')` or `ARRAY_CONSTRUCT('ID', 'DATE')` |
| `exclude_columns` | ARRAY (optional) | Columns to skip in comparison | `ARRAY_CONSTRUCT('UPDATED_AT')` |

### How the Procedure Works

1. **Validates key columns**: Checks that specified keys exist in both tables
2. **Builds column lists**: Dynamically generates lists of columns to compare (excluding keys and any excluded columns)
3. **Constructs join condition**: Creates the appropriate join logic for single or composite keys
4. **Generates SQL**: Builds the full comparison query with proper column lists
5. **Executes and returns**: Runs the dynamic SQL and returns results as a table

---

## Part 4: Databricks Reusable Solutions

Databricks offers multiple approaches depending on your runtime version and preferences.

### Option A: SQL Stored Procedure (DBR 12.2+)

Pure SQL solution using EXECUTE IMMEDIATE, similar to Snowflake.

#### Step 1: Create Test Data

```sql
-- Use your catalog
USE CATALOG main;  -- or your catalog name
CREATE SCHEMA IF NOT EXISTS comparison_demo;
USE SCHEMA comparison_demo;

-- Create simple test tables
CREATE OR REPLACE TABLE customer_v1 (
  c_custkey INT,
  c_name STRING,
  c_address STRING,
  c_nationkey INT,
  c_phone STRING
);

INSERT INTO customer_v1 VALUES
  (1, 'Customer#000000001', 'IVhzIApeRb ot,c,E', 15, '25-989-741-2988'),
  (2, 'Customer#000000002', 'XSTf4,NCwDVaWNe6tEgvwfmRchLXak', 13, '23-768-687-3665'),
  (3, 'Customer#000000003', 'MG9kdTD2WBHm', 1, '11-719-748-3364'),
  (4, 'Customer#000000004', 'XxVSJsLAGtn', 4, '14-128-190-5944');

CREATE OR REPLACE TABLE customer_v2 (
  c_custkey INT,
  c_name STRING,
  c_address STRING,
  c_nationkey INT,
  c_acctbal DECIMAL(15,2)
);

INSERT INTO customer_v2 VALUES
  (1, 'MODIFIED NAME', 'IVhzIApeRb ot,c,E', 15, 711.56),
  (2, 'Customer#000000002', NULL, 13, 121.65),
  (3, 'Customer#000000003', 'MG9kdTD2WBHm', 1, 7498.12),
  (4, 'Customer#000000004', 'XxVSJsLAGtn', 99, 2866.83);

SELECT * FROM customer_v1 ORDER BY c_custkey;
SELECT * FROM customer_v2 ORDER BY c_custkey;
```

#### Step 2: Create SQL Stored Procedure

```sql
CREATE OR REPLACE PROCEDURE compare_tables(
  catalog_a STRING,
  schema_a STRING,
  table_a STRING,
  catalog_b STRING,
  schema_b STRING,
  table_b STRING,
  key_columns STRING,  -- Comma-separated: 'col1,col2'
  exclude_columns STRING DEFAULT ''  -- Comma-separated or empty
)
RETURNS TABLE(
  key STRING,
  column_name STRING,
  value_a STRING,
  value_b STRING,
  diff_type STRING
)
LANGUAGE SQL
BEGIN
  DECLARE full_table_a STRING;
  DECLARE full_table_b STRING;
  DECLARE key_array ARRAY<STRING>;
  DECLARE exclude_array ARRAY<STRING>;
  DECLARE columns_a_list STRING;
  DECLARE columns_b_list STRING;
  DECLARE union_a STRING;
  DECLARE union_b STRING;
  DECLARE key_concat STRING;
  DECLARE key_join_cond STRING;
  DECLARE exclude_clause STRING;
  DECLARE sql_query STRING;
  
  -- Build fully qualified table names
  SET full_table_a = catalog_a || '.' || schema_a || '.' || table_a;
  SET full_table_b = catalog_b || '.' || schema_b || '.' || table_b;
  
  -- Convert comma-separated strings to arrays
  SET key_array = split(key_columns, ',');
  SET exclude_array = CASE 
    WHEN exclude_columns = '' THEN array()
    ELSE split(exclude_columns, ',')
  END;
  
  -- Build exclude clause for information schema queries
  SET exclude_clause = CASE 
    WHEN size(exclude_array) > 0 THEN 
      ' AND column_name NOT IN (' || 
      array_join(transform(exclude_array, x -> concat("'", x, "'")), ',') || 
      ')'
    ELSE ''
  END;
  
  -- Build key concatenation expression for composite keys
  SET key_concat = array_join(
    transform(key_array, x -> concat('CAST(', x, ' AS STRING)')),
    " || '|' || "
  );
  
  -- Build key join condition
  SET key_join_cond = array_join(
    transform(key_array, x -> concat('a.', x, ' = b.', x)),
    ' AND '
  );
  
  -- Get columns from table A
  SET columns_a_list = (
    EXECUTE IMMEDIATE 
      'SELECT array_join(collect_list(column_name), ",") ' ||
      'FROM ' || catalog_a || '.information_schema.columns ' ||
      'WHERE table_catalog = "' || catalog_a || '" ' ||
      '  AND table_schema = "' || schema_a || '" ' ||
      '  AND table_name = "' || table_a || '" ' ||
      '  AND column_name NOT IN (' || 
          array_join(transform(key_array, x -> concat("'", x, "'")), ',') || 
      ')' || exclude_clause ||
      ' ORDER BY ordinal_position'
  );
  
  -- Get columns from table B
  SET columns_b_list = (
    EXECUTE IMMEDIATE
      'SELECT array_join(collect_list(column_name), ",") ' ||
      'FROM ' || catalog_b || '.information_schema.columns ' ||
      'WHERE table_catalog = "' || catalog_b || '" ' ||
      '  AND table_schema = "' || schema_b || '" ' ||
      '  AND table_name = "' || table_b || '" ' ||
      '  AND column_name NOT IN (' || 
          array_join(transform(key_array, x -> concat("'", x, "'")), ',') || 
      ')' || exclude_clause ||
      ' ORDER BY ordinal_position'
  );
  
  -- Build UNION ALL for table A unpivot
  SET union_a = (
    SELECT array_join(
      transform(
        split(columns_a_list, ','),
        col -> concat(
          'SELECT ', key_concat, ' AS key_column, ',
          '''', col, ''' AS column_name, ',
          'CAST(', col, ' AS STRING) AS column_value ',
          'FROM ', full_table_a
        )
      ),
      ' UNION ALL '
    )
  );
  
  -- Build UNION ALL for table B unpivot
  SET union_b = (
    SELECT array_join(
      transform(
        split(columns_b_list, ','),
        col -> concat(
          'SELECT ', key_concat, ' AS key_column, ',
          '''', col, ''' AS column_name, ',
          'CAST(', col, ' AS STRING) AS column_value ',
          'FROM ', full_table_b
        )
      ),
      ' UNION ALL '
    )
  );
  
  -- Build the full comparison query
  SET sql_query = 
    'WITH all_columns AS ( ' ||
    '  SELECT  ' ||
    '    column_name, ' ||
    '    MAX(CASE WHEN source = ''A'' THEN 1 ELSE 0 END) AS in_a, ' ||
    '    MAX(CASE WHEN source = ''B'' THEN 1 ELSE 0 END) AS in_b ' ||
    '  FROM ( ' ||
    '    SELECT column_name, ''A'' AS source  ' ||
    '    FROM ' || catalog_a || '.information_schema.columns  ' ||
    '    WHERE table_catalog = ''' || catalog_a || '''  ' ||
    '      AND table_schema = ''' || schema_a || '''  ' ||
    '      AND table_name = ''' || table_a || '''  ' ||
    '      AND column_name NOT IN (' || 
          array_join(transform(key_array, x -> concat("'", x, "'")), ',') || 
    ')' || exclude_clause ||
    '    UNION ALL ' ||
    '    SELECT column_name, ''B'' AS source  ' ||
    '    FROM ' || catalog_b || '.information_schema.columns  ' ||
    '    WHERE table_catalog = ''' || catalog_b || '''  ' ||
    '      AND table_schema = ''' || schema_b || '''  ' ||
    '      AND table_name = ''' || table_b || '''  ' ||
    '      AND column_name NOT IN (' || 
          array_join(transform(key_array, x -> concat("'", x, "'")), ',') || 
    ')' || exclude_clause ||
    '  ) ' ||
    '  GROUP BY column_name ' ||
    '), ' ||
    'unpivoted_a AS ( ' ||
    union_a ||
    '), ' ||
    'unpivoted_b AS ( ' ||
    union_b ||
    ') ' ||
    'SELECT  ' ||
    '  COALESCE(a.key_column, b.key_column) AS key, ' ||
    '  COALESCE(a.column_name, b.column_name) AS column_name, ' ||
    '  CASE  ' ||
    '    WHEN c.in_a = 0 THEN ''<COLUMN_MISSING>'' ' ||
    '    ELSE a.column_value  ' ||
    '  END AS value_a, ' ||
    '  CASE  ' ||
    '    WHEN c.in_b = 0 THEN ''<COLUMN_MISSING>'' ' ||
    '    ELSE b.column_value  ' ||
    '  END AS value_b, ' ||
    '  CASE ' ||
    '    WHEN c.in_a = 0 THEN ''column_only_in_b'' ' ||
    '    WHEN c.in_b = 0 THEN ''column_only_in_a'' ' ||
    '    ELSE ''value_difference'' ' ||
    '  END AS diff_type ' ||
    'FROM unpivoted_a a ' ||
    'FULL OUTER JOIN unpivoted_b b ' ||
    '  ON a.key_column = b.key_column  ' ||
    '  AND a.column_name = b.column_name ' ||
    'JOIN all_columns c  ' ||
    '  ON c.column_name = COALESCE(a.column_name, b.column_name) ' ||
    'WHERE (a.column_value IS NULL AND b.column_value IS NOT NULL) ' ||
    '   OR (a.column_value IS NOT NULL AND b.column_value IS NULL) ' ||
    '   OR (a.column_value != b.column_value) ' ||
    '   OR c.in_a = 0  ' ||
    '   OR c.in_b = 0 ' ||
    'ORDER BY key, column_name';
  
  -- Execute and return results
  RETURN EXECUTE IMMEDIATE sql_query;
END;
```

#### Step 3: Use the Procedure

```sql
-- Single key column comparison
CALL compare_tables(
  'main',              -- catalog A
  'comparison_demo',   -- schema A
  'customer_v1',       -- table A
  'main',              -- catalog B
  'comparison_demo',   -- schema B
  'customer_v2',       -- table B
  'c_custkey',         -- key columns (comma-separated)
  ''                   -- exclude columns (empty)
);
```

**Expected Output:**
```
key | column_name  | value_a              | value_b         | diff_type
----|--------------|----------------------|-----------------|------------------
1   | c_acctbal    | <COLUMN_MISSING>     | 711.56          | column_only_in_b
1   | c_name       | Customer#000000001   | MODIFIED NAME   | value_difference
1   | c_phone      | 25-989-741-2988      | <COLUMN_MISSING>| column_only_in_a
2   | c_acctbal    | <COLUMN_MISSING>     | 121.65          | column_only_in_b
2   | c_address    | XSTf4,NCwDVaWNe...   | NULL            | value_difference
2   | c_phone      | 23-768-687-3665      | <COLUMN_MISSING>| column_only_in_a
```

#### Step 4: Advanced Usage Examples

```sql
-- Composite key (multiple columns)
CALL compare_tables(
  'main',
  'comparison_demo',
  'orders_v1',
  'main',
  'comparison_demo',
  'orders_v2',
  'o_orderkey,o_custkey',  -- Composite key: comma-separated
  ''
);

-- Excluding columns
CALL compare_tables(
  'main',
  'comparison_demo',
  'customer_v1',
  'main',
  'comparison_demo',
  'customer_v2',
  'c_custkey',
  'c_address,c_phone'  -- Exclude these columns
);

-- Cross-catalog comparison
CALL compare_tables(
  'prod',
  'sales',
  'customers',
  'dev',
  'sales',
  'customers',
  'customer_id',
  'updated_at'
);
```

#### Key Differences from Snowflake

| Feature | Snowflake | Databricks SQL |
|---------|-----------|----------------|
| **Array construction** | `ARRAY_CONSTRUCT('a','b')` | `array('a','b')` or `split('a,b', ',')` |
| **String aggregation** | `LISTAGG(col, ',')` | `array_join(collect_list(col), ',')` |
| **Array transformation** | Loop or JSON functions | `transform(array, lambda)` |
| **Execute immediate** | Returns RESULTSET directly | Returns table/scalar based on query |
| **Variable syntax** | `$variable` or `:variable` | Just `variable` |

### Option B: Python Function

Pure Python solution with PySpark, no SQL stored procedures needed.

#### Step 1: Create Test Data

```sql
-- Use TPCH catalog (adjust catalog/schema names as needed)
-- For Databricks Community Edition or workspace without samples:
USE CATALOG main;  -- or your catalog name
CREATE SCHEMA IF NOT EXISTS comparison_demo;
USE SCHEMA comparison_demo;

-- If you don't have access to TPCH, create simple test tables:
CREATE OR REPLACE TABLE customer_v1 (
  c_custkey INT,
  c_name STRING,
  c_address STRING,
  c_nationkey INT,
  c_phone STRING
);

INSERT INTO customer_v1 VALUES
  (1, 'Customer#000000001', 'IVhzIApeRb ot,c,E', 15, '25-989-741-2988'),
  (2, 'Customer#000000002', 'XSTf4,NCwDVaWNe6tEgvwfmRchLXak', 13, '23-768-687-3665'),
  (3, 'Customer#000000003', 'MG9kdTD2WBHm', 1, '11-719-748-3364'),
  (4, 'Customer#000000004', 'XxVSJsLAGtn', 4, '14-128-190-5944');

CREATE OR REPLACE TABLE customer_v2 (
  c_custkey INT,
  c_name STRING,
  c_address STRING,
  c_nationkey INT,
  c_acctbal DECIMAL(15,2)
);

INSERT INTO customer_v2 VALUES
  (1, 'MODIFIED NAME', 'IVhzIApeRb ot,c,E', 15, 711.56),
  (2, 'Customer#000000002', NULL, 13, 121.65),
  (3, 'Customer#000000003', 'MG9kdTD2WBHm', 1, 7498.12),
  (4, 'Customer#000000004', 'XxVSJsLAGtn', 99, 2866.83);

-- View test data
SELECT * FROM customer_v1 ORDER BY c_custkey;
SELECT * FROM customer_v2 ORDER BY c_custkey;
```

### Option B: Python Function

Pure Python solution with PySpark, no SQL stored procedures needed.

#### Create the Python Function

```python
# Create this as a notebook or save as a Python module

from pyspark.sql import SparkSession
from typing import List, Optional

def compare_tables(
    catalog_a: str,
    schema_a: str, 
    table_a: str,
    catalog_b: str,
    schema_b: str,
    table_b: str,
    key_columns: List[str],
    exclude_columns: Optional[List[str]] = None
):
    """
    Compare two tables at the column level.
    
    Parameters:
    -----------
    catalog_a : str
        Catalog containing first table
    schema_a : str
        Schema containing first table
    table_a : str
        First table name
    catalog_b : str
        Catalog containing second table
    schema_b : str
        Schema containing second table  
    table_b : str
        Second table name
    key_columns : List[str]
        List of columns that uniquely identify rows
    exclude_columns : List[str], optional
        Columns to exclude from comparison
        
    Returns:
    --------
    DataFrame with columns: key, column_name, value_a, value_b, diff_type
    """
    
    spark = SparkSession.builder.getOrCreate()
    exclude_columns = exclude_columns or []
    
    # Build full table names
    full_table_a = f"{catalog_a}.{schema_a}.{table_a}"
    full_table_b = f"{catalog_b}.{schema_b}.{table_b}"
    
    # Get columns from each table
    exclude_clause_a = ""
    exclude_clause_b = ""
    if exclude_columns:
        exclude_list = "'" + "','".join(exclude_columns) + "'"
        exclude_clause_a = f"AND column_name NOT IN ({exclude_list})"
        exclude_clause_b = f"AND column_name NOT IN ({exclude_list})"
    
    key_list = "'" + "','".join(key_columns) + "'"
    
    columns_a_df = spark.sql(f"""
        SELECT column_name
        FROM {catalog_a}.information_schema.columns
        WHERE table_catalog = '{catalog_a}'
          AND table_schema = '{schema_a}'
          AND table_name = '{table_a}'
          AND column_name NOT IN ({key_list})
          {exclude_clause_a}
        ORDER BY ordinal_position
    """)
    columns_a = [row.column_name for row in columns_a_df.collect()]
    
    columns_b_df = spark.sql(f"""
        SELECT column_name
        FROM {catalog_b}.information_schema.columns
        WHERE table_catalog = '{catalog_b}'
          AND table_schema = '{schema_b}'
          AND table_name = '{table_b}'
          AND column_name NOT IN ({key_list})
          {exclude_clause_b}
        ORDER BY ordinal_position
    """)
    columns_b = [row.column_name for row in columns_b_df.collect()]
    
    # Build UNION ALL for unpivoting
    key_cols_str = ", ".join(key_columns)
    key_concat = " || '|' || ".join([f"CAST({k} AS STRING)" for k in key_columns])
    
    union_a_parts = [
        f"SELECT {key_concat} AS key_column, '{col}' AS column_name, CAST({col} AS STRING) AS column_value FROM {full_table_a}"
        for col in columns_a
    ]
    union_a = " UNION ALL ".join(union_a_parts)
    
    union_b_parts = [
        f"SELECT {key_concat} AS key_column, '{col}' AS column_name, CAST({col} AS STRING) AS column_value FROM {full_table_b}"
        for col in columns_b
    ]
    union_b = " UNION ALL ".join(union_b_parts)
    
    # Build the full comparison query
    query = f"""
    WITH all_columns AS (
      SELECT 
        column_name,
        MAX(CASE WHEN source = 'A' THEN 1 ELSE 0 END) AS in_a,
        MAX(CASE WHEN source = 'B' THEN 1 ELSE 0 END) AS in_b
      FROM (
        SELECT column_name, 'A' AS source 
        FROM {catalog_a}.information_schema.columns
        WHERE table_catalog = '{catalog_a}'
          AND table_schema = '{schema_a}'
          AND table_name = '{table_a}'
          AND column_name NOT IN ({key_list})
          {exclude_clause_a}
        UNION ALL
        SELECT column_name, 'B' AS source 
        FROM {catalog_b}.information_schema.columns
        WHERE table_catalog = '{catalog_b}'
          AND table_schema = '{schema_b}'
          AND table_name = '{table_b}'
          AND column_name NOT IN ({key_list})
          {exclude_clause_b}
      )
      GROUP BY column_name
    ),
    unpivoted_a AS (
      {union_a}
    ),
    unpivoted_b AS (
      {union_b}
    )
    SELECT 
      COALESCE(a.key_column, b.key_column) AS key,
      COALESCE(a.column_name, b.column_name) AS column_name,
      CASE 
        WHEN c.in_a = 0 THEN '<COLUMN_MISSING>'
        ELSE a.column_value 
      END AS value_a,
      CASE 
        WHEN c.in_b = 0 THEN '<COLUMN_MISSING>'
        ELSE b.column_value 
      END AS value_b,
      CASE
        WHEN c.in_a = 0 THEN 'column_only_in_b'
        WHEN c.in_b = 0 THEN 'column_only_in_a'
        ELSE 'value_difference'
      END AS diff_type
    FROM unpivoted_a a
    FULL OUTER JOIN unpivoted_b b
      ON a.key_column = b.key_column 
      AND a.column_name = b.column_name
    JOIN all_columns c 
      ON c.column_name = COALESCE(a.column_name, b.column_name)
    WHERE (a.column_value IS NULL AND b.column_value IS NOT NULL)
       OR (a.column_value IS NOT NULL AND b.column_value IS NULL)
       OR (a.column_value != b.column_value)
       OR c.in_a = 0 
       OR c.in_b = 0
    ORDER BY key, column_name
    """
    
    return spark.sql(query)
```

#### Use the Python Function

```python
# Single key column comparison
result = compare_tables(
    catalog_a='main',
    schema_a='comparison_demo',
    table_a='customer_v1',
    catalog_b='main',
    schema_b='comparison_demo',
    table_b='customer_v2',
    key_columns=['c_custkey']
)

display(result)
```

#### Advanced Usage

```python
# Composite key
result = compare_tables(
    catalog_a='main',
    schema_a='comparison_demo',
    table_a='orders_v1',
    catalog_b='main',
    schema_b='comparison_demo',
    table_b='orders_v2',
    key_columns=['o_orderkey', 'o_custkey']
)
display(result)

# Excluding columns
result = compare_tables(
    catalog_a='main',
    schema_a='comparison_demo',
    table_a='customer_v1',
    catalog_b='main',
    schema_b='comparison_demo',
    table_b='customer_v2',
    key_columns=['c_custkey'],
    exclude_columns=['c_address', 'c_phone']
)
display(result)
```

#### Save as Reusable Module

```python
# Save to /Workspace/Shared/utils/table_comparison.py
# Then import and use in any notebook:

from utils.table_comparison import compare_tables

result = compare_tables(
    catalog_a='main',
    schema_a='comparison_demo',
    table_a='customer_v1',
    catalog_b='main',
    schema_b='comparison_demo',
    table_b='customer_v2',
    key_columns=['c_custkey']
)
```

### Which Option to Choose?

| Criteria | SQL Procedure (Option A) | Python Function (Option B) |
|----------|-------------------------|---------------------------|
| **DBR Version** | Requires 12.2+ | Works on all versions |
| **Skill Set** | SQL-focused teams | Python-comfortable teams |
| **Debugging** | Harder (string concatenation) | Easier (IDE support) |
| **Performance** | Similar | Similar |
| **Portability** | SQL Warehouse native | Requires notebook/cluster |
| **Syntax** | Verbose string building | Cleaner with f-strings |
| **Best For** | Pure SQL environments | Mixed SQL/Python workflows |

**Recommendation:** Use **Option A (SQL Procedure)** if your team prefers SQL and you're on DBR 12.2+. Use **Option B (Python)** if you work in notebooks or need easier debugging.

---

## Part 5: Platform Comparison

| Feature | Snowflake | Databricks SQL Procedure | Databricks Python |
|---------|-----------|-------------------------|-------------------|
| **UNPIVOT** | Native support | Use UNION ALL | Use UNION ALL |
| **Dynamic SQL** | `EXECUTE IMMEDIATE` with variables | `EXECUTE IMMEDIATE` with string building | Python f-strings |
| **IS DISTINCT FROM** | Supported | Must use explicit NULL checks | Must use explicit NULL checks |
| **Stored Procedures** | Native SQL procedures | SQL procedures (DBR 12.2+) | Python UDFs or notebooks |
| **Information Schema** | Standard SQL access | Unity Catalog information_schema | Unity Catalog information_schema |
| **Array Parameters** | `ARRAY_CONSTRUCT()` | `split()` or `array()` | Python lists |
| **String Aggregation** | `LISTAGG()` | `array_join(collect_list())` | Python `join()` |
| **Debugging** | Good | Harder (string concatenation) | Easiest (IDE support) |
| **Best For** | Snowflake users | SQL-first Databricks teams | Mixed SQL/Python workflows |

### Syntax Differences Cheat Sheet

**Building arrays:**
```sql
-- Snowflake
ARRAY_CONSTRUCT('col1', 'col2', 'col3')

-- Databricks SQL
array('col1', 'col2', 'col3')
split('col1,col2,col3', ',')

-- Databricks Python
['col1', 'col2', 'col3']
```

**Aggregating to string:**
```sql
-- Snowflake
LISTAGG(column_name, ',') WITHIN GROUP (ORDER BY column_name)

-- Databricks SQL
array_join(collect_list(column_name), ',')

-- Databricks Python
','.join(column_list)
```

**Transforming arrays:**
```sql
-- Snowflake
-- Use JSON functions or loops

-- Databricks SQL
transform(array_col, x -> concat("'", x, "'"))

-- Databricks Python
[f"'{x}'" for x in array_col]
```

---

## Part 6: Interview Guide

### How to Present This Pattern

**1. Start with the problem:**
> "I need to compare two tables at the column level to identify all differences, including schema mismatches where columns exist in only one table."

**2. Explain the high-level approach:**
> "I'll transform the columnar data into rows using UNPIVOT, then use a FULL OUTER JOIN to catch all scenarios - matching rows, rows in only one table, and columns that exist in only one table."

**3. Walk through the logic step-by-step:**
- Show the UNPIVOT transformation with a simple example
- Explain the FULL OUTER JOIN and what each join result means
- Demonstrate IS DISTINCT FROM for NULL handling
- Show how you differentiate between NULL values and missing columns

**4. Discuss edge cases:**
- Composite keys
- Data type mismatches (need to CAST to common type)
- Very wide tables (performance considerations)
- Rows that exist in only one table

**5. Show the reusable implementation:**
> "Rather than write this query manually each time, I'd create a stored procedure that accepts table names, key columns, and optional exclusion lists as parameters."

**6. Discuss platform-specific implementations:**
- **Snowflake:** Native UNPIVOT with EXECUTE IMMEDIATE
- **Databricks:** Choice between SQL stored procedure (DBR 12.2+) or Python function
- **Other platforms:** May need STACK (Spark) or manual UNION ALL approach

### Common Follow-up Questions

**Q: How would you handle millions of rows?**
A: 
- Partition by key ranges and parallelize
- Use incremental comparison with change data capture
- Sample for initial validation (e.g., compare 10% of data first)
- Add WHERE clauses to limit comparison scope
- Consider comparing aggregates/checksums first, then drill into differences

**Q: What about data type mismatches?**
A: Cast everything to STRING in the UNPIVOT for comparison. For numeric columns, you might want type-specific comparisons (e.g., threshold for floating point):
```sql
WHERE ABS(CAST(a.column_value AS FLOAT) - CAST(b.column_value AS FLOAT)) > 0.01
```

**Q: How do you handle composite keys?**
A: Concatenate with a delimiter or use multiple join conditions:
```sql
-- Option 1: Concatenate
SELECT CONCAT(col1, '|', col2, '|', col3) AS key_column, ...

-- Option 2: Multiple conditions
ON a.key1 = b.key1 AND a.key2 = b.key2 AND a.key3 = b.key3
```

**Q: Performance optimization?**
A:
- Add indexes on key columns
- Use columnar storage formats (Parquet)
- Partition both tables on key columns
- For very wide tables, compare columns in batches
- Use parallel execution hints if available

**Q: What if tables have different column orders?**
A: Not a problem - UNPIVOT matches by name, not position. Column order doesn't matter.

**Q: How would you test this procedure?**
A:
1. Test with identical tables (should return 0 rows)
2. Test with value differences only
3. Test with schema differences only
4. Test with both value and schema differences
5. Test with NULL values in both tables
6. Test with composite keys
7. Test with one-sided rows (keys in A but not B)

### Pro Tips for Interviews

1. **Start simple, build up complexity**: Show the basic pattern first, then add dynamic SQL
2. **Think out loud**: Explain your reasoning as you write
3. **Ask clarifying questions**: "Should we handle case-sensitive column names?" "Are there any columns we should always exclude like timestamps?"
4. **Consider practical concerns**: "In production, I'd add logging to track comparison metrics" or "I'd add a parameter for max_differences to prevent massive result sets"
5. **Know your platform**: Understand the differences between Snowflake, Databricks, BigQuery, etc.

---

## Part 7: Production Enhancements

### Add Filtering

```sql
-- Filter to specific keys
WHERE COALESCE(a.key_column, b.key_column) IN (1, 2, 3)

-- Filter to specific columns
AND COALESCE(a.column_name, b.column_name) IN ('col1', 'col2')

-- Numeric threshold comparison
AND TRY_CAST(a.column_value AS FLOAT) IS NOT NULL  -- Only numeric columns
AND ABS(CAST(a.column_value AS FLOAT) - CAST(b.column_value AS FLOAT)) > 0.01
```

### Add Metadata

```sql
SELECT 
  CURRENT_TIMESTAMP() AS comparison_timestamp,
  :schema_a || '.' || :table_a AS source_table_a,
  :schema_b || '.' || :table_b AS source_table_b,
  HASH(a.column_value) AS hash_a,
  HASH(b.column_value) AS hash_b,
  -- ... rest of columns
```

### Add Summary Statistics

```sql
-- After the main comparison query
WITH comparison_results AS (
  -- Your comparison query here
)
SELECT 
  diff_type,
  COUNT(*) AS difference_count,
  COUNT(DISTINCT key) AS affected_keys,
  COUNT(DISTINCT column_name) AS affected_columns
FROM comparison_results
GROUP BY diff_type;
```

### Create Materialized View

```sql
-- Snowflake
CREATE OR REPLACE TABLE comparison_results AS
CALL compare_tables(...);

-- Schedule refresh
CREATE OR REPLACE TASK refresh_comparison
  WAREHOUSE = compute_wh
  SCHEDULE = 'USING CRON 0 2 * * * UTC'
AS
  CREATE OR REPLACE TABLE comparison_results AS
  CALL compare_tables(...);
```

---

## Summary

This pattern provides a flexible, reusable solution for comparing tables at the column level. Key takeaways:

1. **UNPIVOT transforms columns to rows** for unified comparison
2. **FULL OUTER JOIN catches all scenarios** including one-sided rows
3. **IS DISTINCT FROM handles NULLs properly** unlike standard comparison operators
4. **Dynamic column detection** differentiates between NULL data and missing columns
5. **Reusable procedures** make this pattern applicable to any table pair

The approach scales from simple single-key comparisons to complex composite-key scenarios with column exclusions, making it a powerful tool for data quality, migration validation, and regression testing.

## Snowflake Implementation

### Step 1: Create Test Tables

```sql
-- Use the TPCH sample database
USE SCHEMA SNOWFLAKE_SAMPLE_DATA.TPCH_SF1;

-- Create two versions of CUSTOMER table with differences
CREATE OR REPLACE TABLE customer_v1 AS
SELECT 
  C_CUSTKEY,
  C_NAME,
  C_ADDRESS,
  C_NATIONKEY,
  C_PHONE
FROM CUSTOMER
WHERE C_CUSTKEY <= 10;

CREATE OR REPLACE TABLE customer_v2 AS
SELECT 
  C_CUSTKEY,
  C_NAME,
  C_ADDRESS,
  C_NATIONKEY,
  -- C_PHONE removed (schema difference)
  C_ACCTBAL  -- new column added (schema difference)
FROM CUSTOMER
WHERE C_CUSTKEY <= 10;

-- Introduce data differences
UPDATE customer_v2 SET C_NAME = 'MODIFIED NAME' WHERE C_CUSTKEY = 1;
UPDATE customer_v2 SET C_ADDRESS = NULL WHERE C_CUSTKEY = 2;
UPDATE customer_v1 SET C_ADDRESS = NULL WHERE C_CUSTKEY = 3;
```

### Step 2: Dynamic Column List Generation

```sql
-- Build column lists for each table
SET column_list_a = (
  SELECT LISTAGG(column_name, ', ') WITHIN GROUP (ORDER BY column_name)
  FROM information_schema.columns
  WHERE table_schema = 'PUBLIC'
    AND table_name = 'CUSTOMER_V1'
    AND column_name != 'C_CUSTKEY'  -- Exclude key column
);

SET column_list_b = (
  SELECT LISTAGG(column_name, ', ') WITHIN GROUP (ORDER BY column_name)
  FROM information_schema.columns
  WHERE table_schema = 'PUBLIC'
    AND table_name = 'CUSTOMER_V2'
    AND column_name != 'C_CUSTKEY'  -- Exclude key column
);

-- View what columns will be compared
SELECT $column_list_a AS columns_in_v1;
SELECT $column_list_b AS columns_in_v2;
```

### Step 3: Full Comparison Query

```sql
SET sql_query = '
WITH all_columns AS (
  SELECT 
    column_name,
    MAX(CASE WHEN source = ''A'' THEN 1 ELSE 0 END) AS in_a,
    MAX(CASE WHEN source = ''B'' THEN 1 ELSE 0 END) AS in_b
  FROM (
    SELECT column_name, ''A'' AS source 
    FROM information_schema.columns 
    WHERE table_schema = ''PUBLIC'' 
      AND table_name = ''CUSTOMER_V1'' 
      AND column_name != ''C_CUSTKEY''
    UNION ALL
    SELECT column_name, ''B'' AS source 
    FROM information_schema.columns 
    WHERE table_schema = ''PUBLIC'' 
      AND table_name = ''CUSTOMER_V2'' 
      AND column_name != ''C_CUSTKEY''
  )
  GROUP BY column_name
),
unpivoted_a AS (
  SELECT 
    C_CUSTKEY AS key_column,
    column_name,
    column_value
  FROM customer_v1
  UNPIVOT (
    column_value FOR column_name IN (' || $column_list_a || ')
  )
),
unpivoted_b AS (
  SELECT 
    C_CUSTKEY AS key_column,
    column_name,
    column_value
  FROM customer_v2
  UNPIVOT (
    column_value FOR column_name IN (' || $column_list_b || ')
  )
)
SELECT 
  COALESCE(a.key_column, b.key_column) AS key,
  COALESCE(a.column_name, b.column_name) AS column_name,
  CASE 
    WHEN c.in_a = 0 THEN ''<COLUMN_MISSING>''
    ELSE a.column_value 
  END AS value_a,
  CASE 
    WHEN c.in_b = 0 THEN ''<COLUMN_MISSING>''
    ELSE b.column_value 
  END AS value_b,
  CASE
    WHEN c.in_a = 0 THEN ''column_only_in_b''
    WHEN c.in_b = 0 THEN ''column_only_in_a''
    ELSE ''value_difference''
  END AS diff_type
FROM unpivoted_a a
FULL OUTER JOIN unpivoted_b b
  ON a.key_column = b.key_column 
  AND a.column_name = b.column_name
JOIN all_columns c 
  ON c.column_name = COALESCE(a.column_name, b.column_name)
WHERE a.column_value IS DISTINCT FROM b.column_value
   OR c.in_a = 0 
   OR c.in_b = 0
ORDER BY key, column_name';

EXECUTE IMMEDIATE $sql_query;
```

### Expected Output

| key | column_name | value_a | value_b | diff_type |
|-----|-------------|---------|---------|-----------|
| 1   | C_NAME      | Customer#000000001 | MODIFIED NAME | value_difference |
| 1   | C_PHONE     | 25-989-741-2988 | <COLUMN_MISSING> | column_only_in_a |
| 1   | C_ACCTBAL   | <COLUMN_MISSING> | 711.56 | column_only_in_b |
| 2   | C_ADDRESS   | XSTf4,NCwDVaWNe6tEgvwfmRchLXak | NULL | value_difference |
| 3   | C_ADDRESS   | NULL | MG9kdTD2WBHm | value_difference |

## Databricks Implementation

Databricks doesn't have native UNPIVOT until DBR 14+, so we use `STACK` or manual UNION ALL approach.

### Step 1: Create Test Tables

```sql
-- Use TPCH catalog (adjust catalog/schema names as needed)
USE CATALOG samples;
USE SCHEMA tpch;

-- Create two versions with differences
CREATE OR REPLACE TABLE customer_v1 AS
SELECT 
  c_custkey,
  c_name,
  c_address,
  c_nationkey,
  c_phone
FROM customer
WHERE c_custkey <= 10;

CREATE OR REPLACE TABLE customer_v2 AS
SELECT 
  c_custkey,
  c_name,
  c_address,
  c_nationkey,
  c_acctbal  -- new column, c_phone removed
FROM customer
WHERE c_custkey <= 10;

-- Introduce differences
UPDATE customer_v2 SET c_name = 'MODIFIED NAME' WHERE c_custkey = 1;
UPDATE customer_v2 SET c_address = NULL WHERE c_custkey = 2;
UPDATE customer_v1 SET c_address = NULL WHERE c_custkey = 3;
```

### Step 2: Manual UNION ALL Approach (Most Compatible)

```sql
WITH all_columns AS (
  SELECT 
    column_name,
    MAX(CASE WHEN source = 'A' THEN 1 ELSE 0 END) AS in_a,
    MAX(CASE WHEN source = 'B' THEN 1 ELSE 0 END) AS in_b
  FROM (
    SELECT column_name, 'A' AS source 
    FROM information_schema.columns 
    WHERE table_schema = 'tpch' 
      AND table_name = 'customer_v1' 
      AND column_name != 'c_custkey'
    UNION ALL
    SELECT column_name, 'B' AS source 
    FROM information_schema.columns 
    WHERE table_schema = 'tpch' 
      AND table_name = 'customer_v2' 
      AND column_name != 'c_custkey'
  )
  GROUP BY column_name
),
unpivoted_a AS (
  SELECT c_custkey AS key_column, 'c_name' AS column_name, CAST(c_name AS STRING) AS column_value FROM customer_v1
  UNION ALL
  SELECT c_custkey, 'c_address', CAST(c_address AS STRING) FROM customer_v1
  UNION ALL
  SELECT c_custkey, 'c_nationkey', CAST(c_nationkey AS STRING) FROM customer_v1
  UNION ALL
  SELECT c_custkey, 'c_phone', CAST(c_phone AS STRING) FROM customer_v1
),
unpivoted_b AS (
  SELECT c_custkey AS key_column, 'c_name' AS column_name, CAST(c_name AS STRING) AS column_value FROM customer_v2
  UNION ALL
  SELECT c_custkey, 'c_address', CAST(c_address AS STRING) FROM customer_v2
  UNION ALL
  SELECT c_custkey, 'c_nationkey', CAST(c_nationkey AS STRING) FROM customer_v2
  UNION ALL
  SELECT c_custkey, 'c_acctbal', CAST(c_acctbal AS STRING) FROM customer_v2
)
SELECT 
  COALESCE(a.key_column, b.key_column) AS key,
  COALESCE(a.column_name, b.column_name) AS column_name,
  CASE 
    WHEN c.in_a = 0 THEN '<COLUMN_MISSING>'
    ELSE a.column_value 
  END AS value_a,
  CASE 
    WHEN c.in_b = 0 THEN '<COLUMN_MISSING>'
    ELSE b.column_value 
  END AS value_b,
  CASE
    WHEN c.in_a = 0 THEN 'column_only_in_b'
    WHEN c.in_b = 0 THEN 'column_only_in_a'
    ELSE 'value_difference'
  END AS diff_type
FROM unpivoted_a a
FULL OUTER JOIN unpivoted_b b
  ON a.key_column = b.key_column 
  AND a.column_name = b.column_name
JOIN all_columns c 
  ON c.column_name = COALESCE(a.column_name, b.column_name)
WHERE (a.column_value IS NULL AND b.column_value IS NOT NULL)
   OR (a.column_value IS NOT NULL AND b.column_value IS NULL)
   OR (a.column_value != b.column_value)
   OR c.in_a = 0 
   OR c.in_b = 0
ORDER BY key, column_name;
```

### Step 3: Using STACK (Databricks DBR 14+)

```sql
WITH all_columns AS (
  -- Same as above
),
unpivoted_a AS (
  SELECT 
    c_custkey AS key_column,
    col_name AS column_name,
    col_value AS column_value
  FROM customer_v1
  LATERAL VIEW STACK(
    4,
    'c_name', CAST(c_name AS STRING),
    'c_address', CAST(c_address AS STRING),
    'c_nationkey', CAST(c_nationkey AS STRING),
    'c_phone', CAST(c_phone AS STRING)
  ) AS col_name, col_value
),
unpivoted_b AS (
  SELECT 
    c_custkey AS key_column,
    col_name AS column_name,
    col_value AS column_value
  FROM customer_v2
  LATERAL VIEW STACK(
    4,
    'c_name', CAST(c_name AS STRING),
    'c_address', CAST(c_address AS STRING),
    'c_nationkey', CAST(c_nationkey AS STRING),
    'c_acctbal', CAST(c_acctbal AS STRING)
  ) AS col_name, col_value
)
-- Rest same as above
```

### Step 4: Dynamic SQL in Databricks (Python)

```python
# Get column lists
columns_a = spark.sql("""
  SELECT collect_list(column_name) as cols
  FROM information_schema.columns 
  WHERE table_schema = 'tpch' 
    AND table_name = 'customer_v1' 
    AND column_name != 'c_custkey'
""").collect()[0]['cols']

columns_b = spark.sql("""
  SELECT collect_list(column_name) as cols
  FROM information_schema.columns 
  WHERE table_schema = 'tpch' 
    AND table_name = 'customer_v2' 
    AND column_name != 'c_custkey'
""").collect()[0]['cols']

# Build UNION ALL statements
union_a = " UNION ALL ".join([
    f"SELECT c_custkey AS key_column, '{col}' AS column_name, CAST({col} AS STRING) AS column_value FROM customer_v1"
    for col in columns_a
])

union_b = " UNION ALL ".join([
    f"SELECT c_custkey AS key_column, '{col}' AS column_name, CAST({col} AS STRING) AS column_value FROM customer_v2"
    for col in columns_b
])

# Execute full query
query = f"""
WITH all_columns AS (
  SELECT 
    column_name,
    MAX(CASE WHEN source = 'A' THEN 1 ELSE 0 END) AS in_a,
    MAX(CASE WHEN source = 'B' THEN 1 ELSE 0 END) AS in_b
  FROM (
    SELECT column_name, 'A' AS source 
    FROM information_schema.columns 
    WHERE table_schema = 'tpch' AND table_name = 'customer_v1' AND column_name != 'c_custkey'
    UNION ALL
    SELECT column_name, 'B' AS source 
    FROM information_schema.columns 
    WHERE table_schema = 'tpch' AND table_name = 'customer_v2' AND column_name != 'c_custkey'
  )
  GROUP BY column_name
),
unpivoted_a AS ({union_a}),
unpivoted_b AS ({union_b})
SELECT 
  COALESCE(a.key_column, b.key_column) AS key,
  COALESCE(a.column_name, b.column_name) AS column_name,
  CASE WHEN c.in_a = 0 THEN '<COLUMN_MISSING>' ELSE a.column_value END AS value_a,
  CASE WHEN c.in_b = 0 THEN '<COLUMN_MISSING>' ELSE b.column_value END AS value_b,
  CASE
    WHEN c.in_a = 0 THEN 'column_only_in_b'
    WHEN c.in_b = 0 THEN 'column_only_in_a'
    ELSE 'value_difference'
  END AS diff_type
FROM unpivoted_a a
FULL OUTER JOIN unpivoted_b b
  ON a.key_column = b.key_column AND a.column_name = b.column_name
JOIN all_columns c ON c.column_name = COALESCE(a.column_name, b.column_name)
WHERE (a.column_value IS NULL AND b.column_value IS NOT NULL)
   OR (a.column_value IS NOT NULL AND b.column_value IS NULL)
   OR (a.column_value != b.column_value)
   OR c.in_a = 0 OR c.in_b = 0
ORDER BY key, column_name
"""

result = spark.sql(query)
display(result)
```

## Key Platform Differences

| Feature | Snowflake | Databricks |
|---------|-----------|------------|
| **UNPIVOT** | Native support | DBR 14+ or use STACK/UNION ALL |
| **Dynamic SQL** | `EXECUTE IMMEDIATE` with variables | Python string interpolation |
| **IS DISTINCT FROM** | Supported | Use explicit NULL checks |
| **Variable syntax** | `$variable` or `:variable` | Python f-strings |
| **LISTAGG** | Native function | Use `collect_list()` + `array_join()` |

## Interview Tips

When presenting this pattern in an interview:

1. **Start with the problem**: "We need to compare two tables at the column level and identify all differences, including schema mismatches"

2. **Explain the approach**: "I'll use UNPIVOT to transform columns into rows, then FULL OUTER JOIN to catch all differences"

3. **Show awareness of edge cases**:
   - NULL values in matching columns vs missing columns
   - Rows that exist in only one table
   - Data type mismatches requiring CAST

4. **Discuss trade-offs**:
   - Performance: UNPIVOT can be expensive on wide tables
   - Alternative: Column-by-column comparison for specific columns
   - Dynamic SQL adds complexity but provides flexibility

5. **Mention variations**: "In production, I'd parameterize the schema, table names, and key columns, and add filtering for specific keys or columns"

## Production Enhancements

```sql
-- Add filters for specific keys
WHERE a.column_value IS DISTINCT FROM b.column_value
  AND COALESCE(a.key_column, b.key_column) IN (1, 2, 3)

-- Add column filtering
AND COALESCE(a.column_name, b.column_name) IN ('col1', 'col2')

-- Add difference threshold for numeric columns
AND ABS(CAST(a.column_value AS FLOAT) - CAST(b.column_value AS FLOAT)) > 0.01

-- Add metadata
SELECT 
  CURRENT_TIMESTAMP() AS comparison_timestamp,
  'customer_v1' AS source_table_a,
  'customer_v2' AS source_table_b,
  -- ... rest of query
```

## Common Interview Follow-ups

**Q: How would you handle millions of rows?**
A: Partition by key ranges, parallelize comparison, use incremental approach with change data capture, or sample for initial validation.

**Q: What about data type mismatches?**
A: Cast everything to STRING in the UNPIVOT, or handle type-specific comparisons separately.

**Q: How do you handle composite keys?**
A: Concatenate key columns with a delimiter: `CONCAT(col1, '|', col2)` or use multiple join conditions.

**Q: Performance optimization?**
A: Create indexes on key columns, use columnar storage, partition tables, or compare only changed rows using timestamps/versions.
