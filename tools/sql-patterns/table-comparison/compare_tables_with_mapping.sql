-- Filename: compare_tables_with_mapping.sql
-- =====================================================
-- Table Comparison with Column Mapping Table
-- =====================================================
-- This approach uses a mapping table to handle different column names
-- between two tables, making it reusable and maintainable

-- Step 1: Create a column mapping table
CREATE TABLE IF NOT EXISTS column_mappings (
    mapping_id INT AUTO_INCREMENT PRIMARY KEY,
    comparison_name VARCHAR(100),  -- Name this comparison for reuse
    table1_name VARCHAR(100),
    table1_column VARCHAR(100),
    table2_name VARCHAR(100),
    table2_column VARCHAR(100),
    is_join_key BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes VARCHAR(500)
);

-- Step 2: Insert mapping configuration
-- Example: Comparing customer tables with different column names
INSERT INTO column_mappings (comparison_name, table1_name, table1_column, table2_name, table2_column, is_join_key, notes)
VALUES 
    ('customer_migration', 'customers_old', 'cust_id', 'customers_new', 'customer_id', TRUE, 'Primary key mapping'),
    ('customer_migration', 'customers_old', 'cust_name', 'customers_new', 'customer_name', FALSE, NULL),
    ('customer_migration', 'customers_old', 'cust_email', 'customers_new', 'email_address', FALSE, NULL),
    ('customer_migration', 'customers_old', 'phone', 'customers_new', 'phone_number', FALSE, NULL),
    ('customer_migration', 'customers_old', 'create_dt', 'customers_new', 'created_date', FALSE, NULL),
    ('customer_migration', 'customers_old', 'status_cd', 'customers_new', 'status_code', FALSE, NULL);

-- Step 3: Create a stored procedure that uses the mapping
DELIMITER //

CREATE PROCEDURE compare_mapped_tables(IN comparison_name_param VARCHAR(100))
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_table1_col VARCHAR(100);
    DECLARE v_table2_col VARCHAR(100);
    DECLARE v_join_key1 VARCHAR(100);
    DECLARE v_join_key2 VARCHAR(100);
    DECLARE v_table1_name VARCHAR(100);
    DECLARE v_table2_name VARCHAR(100);
    DECLARE v_sql TEXT DEFAULT '';
    DECLARE v_union_sql TEXT DEFAULT '';
    
    -- Cursor for column mappings
    DECLARE col_cursor CURSOR FOR
        SELECT table1_column, table2_column
        FROM column_mappings
        WHERE comparison_name = comparison_name_param
          AND is_join_key = FALSE
          AND is_active = TRUE;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Get table names and join keys
    SELECT DISTINCT table1_name, table2_name 
    INTO v_table1_name, v_table2_name
    FROM column_mappings
    WHERE comparison_name = comparison_name_param
    LIMIT 1;
    
    SELECT table1_column, table2_column
    INTO v_join_key1, v_join_key2
    FROM column_mappings
    WHERE comparison_name = comparison_name_param
      AND is_join_key = TRUE
    LIMIT 1;
    
    -- Build the comparison query dynamically
    OPEN col_cursor;
    
    read_loop: LOOP
        FETCH col_cursor INTO v_table1_col, v_table2_col;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        IF v_union_sql != '' THEN
            SET v_union_sql = CONCAT(v_union_sql, ' UNION ALL ');
        END IF;
        
        SET v_union_sql = CONCAT(v_union_sql, '
            SELECT 
                COALESCE(t1.', v_join_key1, ', t2.', v_join_key2, ') as key_value,
                ''', v_table1_col, ''' as column_name,
                CAST(t1.', v_table1_col, ' AS CHAR) as table1_value,
                CAST(t2.', v_table2_col, ' AS CHAR) as table2_value
            FROM ', v_table1_name, ' t1
            FULL OUTER JOIN ', v_table2_name, ' t2 
                ON t1.', v_join_key1, ' = t2.', v_join_key2, '
            WHERE t1.', v_table1_col, ' != t2.', v_table2_col, '
               OR (t1.', v_table1_col, ' IS NULL AND t2.', v_table2_col, ' IS NOT NULL)
               OR (t1.', v_table1_col, ' IS NOT NULL AND t2.', v_table2_col, ' IS NULL)
        ');
    END LOOP;
    
    CLOSE col_cursor;
    
    -- Final query with all comparisons
    SET @final_sql = CONCAT('
        WITH comparison_data AS (
            ', v_union_sql, '
        )
        SELECT 
            key_value,
            column_name,
            table1_value,
            table2_value
        FROM comparison_data
        ORDER BY key_value, column_name
    ');
    
    -- Execute the dynamic SQL
    PREPARE stmt FROM @final_sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END//

DELIMITER ;

-- Step 4: Use the stored procedure
CALL compare_mapped_tables('customer_migration');


-- =====================================================
-- Helper Views and Queries
-- =====================================================

-- View to see all active mappings
CREATE VIEW v_active_mappings AS
SELECT 
    comparison_name,
    table1_name,
    table1_column,
    table2_name,
    table2_column,
    CASE WHEN is_join_key THEN 'JOIN KEY' ELSE 'DATA' END as column_type,
    notes
FROM column_mappings
WHERE is_active = TRUE
ORDER BY comparison_name, is_join_key DESC, table1_column;

-- Query to validate mapping completeness
-- Shows columns in table1 that aren't mapped
SELECT 
    c.column_name as unmapped_column
FROM information_schema.columns c
WHERE c.table_name = 'customers_old'
  AND c.table_schema = DATABASE()
  AND c.column_name NOT IN (
    SELECT table1_column 
    FROM column_mappings 
    WHERE comparison_name = 'customer_migration'
      AND table1_name = 'customers_old'
  );

-- Query to generate initial mapping suggestions based on similar names
WITH t1_cols AS (
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'customers_old' 
      AND table_schema = DATABASE()
),
t2_cols AS (
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = 'customers_new' 
      AND table_schema = DATABASE()
)
SELECT 
    t1.column_name as table1_column,
    t2.column_name as suggested_table2_column,
    'Auto-suggested based on similarity' as notes
FROM t1_cols t1
CROSS JOIN t2_cols t2
WHERE 
    -- Simple similarity matching
    LOWER(REPLACE(t1.column_name, '_', '')) = LOWER(REPLACE(t2.column_name, '_', ''))
    OR SOUNDEX(t1.column_name) = SOUNDEX(t2.column_name)
    OR (
        -- Common patterns
        t1.column_name LIKE '%id' AND t2.column_name LIKE '%id'
        OR t1.column_name LIKE '%name%' AND t2.column_name LIKE '%name%'
        OR t1.column_name LIKE '%date%' AND t2.column_name LIKE '%date%'
        OR t1.column_name LIKE '%email%' AND t2.column_name LIKE '%email%'
    )
ORDER BY t1.column_name;


-- =====================================================
-- Alternative: JSON-based mapping for modern databases
-- =====================================================

-- For PostgreSQL, MySQL 8+, or other databases with JSON support
CREATE TABLE IF NOT EXISTS comparison_configs (
    config_id INT AUTO_INCREMENT PRIMARY KEY,
    config_name VARCHAR(100) UNIQUE,
    mapping_json JSON,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert mapping as JSON
INSERT INTO comparison_configs (config_name, mapping_json)
VALUES ('customer_migration', '{
    "table1": "customers_old",
    "table2": "customers_new",
    "join_keys": {
        "table1_key": "cust_id",
        "table2_key": "customer_id"
    },
    "column_mappings": [
        {"table1_col": "cust_name", "table2_col": "customer_name"},
        {"table1_col": "cust_email", "table2_col": "email_address"},
        {"table1_col": "phone", "table2_col": "phone_number"},
        {"table1_col": "create_dt", "table2_col": "created_date"},
        {"table1_col": "status_cd", "table2_col": "status_code"}
    ]
}');

-- Query using JSON mapping (PostgreSQL example)
WITH mapping AS (
    SELECT 
        mapping_json->>'table1' as table1,
        mapping_json->>'table2' as table2,
        mapping_json->'join_keys'->>'table1_key' as join_key1,
        mapping_json->'join_keys'->>'table2_key' as join_key2,
        jsonb_array_elements(mapping_json->'column_mappings') as col_map
    FROM comparison_configs
    WHERE config_name = 'customer_migration'
)
SELECT 
    table1,
    col_map->>'table1_col' as table1_column,
    table2,
    col_map->>'table2_col' as table2_column
FROM mapping;