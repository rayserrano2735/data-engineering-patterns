# Interview Prep: Danaher Staff Data Engineer
**Version: 1.0.5-RC3**

---

## Interview Context

**Company:** Danaher Corporation  
**Role:** Staff Data Engineer  
**Interview Type:** Technical discussion with CTO  
**Interviewer:** Chris Wheeler - Interim Chief Technology Officer  
**Date/Time:** October 9, 2025, 1:00-1:30 PM EDT (30 minutes)

**Key JD Signals:**
- Title says "Data Engineer" but dbt listed as "plus" → Actually Analytics Engineer role
- Snowflake + Fivetran + dbt pattern = warehouse-focused, not lake
- Python/PySpark = gatekeeping test, not 99% of real work
- Real job: dbt transformations in Snowflake
- Interview: Will test Python as filtering mechanism

**CTO Interview Focus:**
- High-level system thinking (not deep syntax)
- When to use which tool
- Design trade-offs
- Strategic approach to data engineering

---

## PySpark Fundamentals

### Why PySpark Exists

**Problem:** pandas DataFrames live in single machine memory. Doesn't scale to TB+ datasets.

**Solution:** PySpark distributes data across cluster, processes in parallel.

**When to use:**
- Data > 100GB (pandas fails)
- Need horizontal scaling
- Working in Databricks/EMR/data lake environments

**When NOT to use (use dbt instead):**
- Data in warehouse (Snowflake, Redshift, BigQuery)
- Standard transformations
- SQL can express the logic
- Team knows SQL better than Python

**Interview answer if asked "Why PySpark?":**
"PySpark for distributed processing when data exceeds single machine capacity or we're in a lakehouse architecture. But for warehouse-based analytics at Danaher with Snowflake, I'd default to dbt for transformations - declarative, testable, and leverages warehouse compute."

---

## PySpark DataFrame API

### Core Concept: Lazy Evaluation

**Critical difference from pandas:**

```python
# pandas - executes immediately
df_pandas = pd.read_csv('data.csv')
result = df_pandas[df_pandas['age'] > 30]  # Happens now

# PySpark - builds execution plan, runs on .show() or .collect()
df_spark = spark.read.csv('data.csv')
result = df_spark.filter(df_spark['age'] > 30)  # Nothing happens yet
result.show()  # NOW it executes
```

**Why this matters:**
- PySpark optimizes entire query before execution
- Can reorder operations for efficiency
- Similar to how SQL query optimizer works

### Creating DataFrames

**From data:**
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Interview").getOrCreate()

# From list of dicts (like you know from Week 1)
data = [
    {'name': 'Alice', 'age': 30, 'dept': 'Engineering'},
    {'name': 'Bob', 'age': 25, 'dept': 'Sales'},
    {'name': 'Charlie', 'age': 35, 'dept': 'Engineering'}
]
df = spark.createDataFrame(data)
```

**From files:**
```python
# CSV
df = spark.read.csv('path/to/file.csv', header=True, inferSchema=True)

# Parquet (common in data lakes)
df = spark.read.parquet('path/to/file.parquet')

# JSON
df = spark.read.json('path/to/file.json')
```

### Selection and Filtering

**Select columns:**
```python
# Select specific columns
df.select('name', 'age').show()

# Alternative syntax
df.select(df.name, df.age).show()
df.select(df['name'], df['age']).show()
```

**Filter rows:**
```python
# Filter with condition
df.filter(df.age > 30).show()

# Multiple conditions
df.filter((df.age > 25) & (df.dept == 'Engineering')).show()

# SQL-style (alternative)
df.where(df.age > 30).show()
```

**Note:** Use `&` for AND, `|` for OR (not `and`/`or` like pandas)

### Aggregation

**GroupBy pattern (like SQL GROUP BY):**

```python
# Count by department
df.groupBy('dept').count().show()

# Multiple aggregations
from pyspark.sql import functions as F

df.groupBy('dept').agg(
    F.count('name').alias('employee_count'),
    F.avg('age').alias('avg_age'),
    F.max('age').alias('max_age')
).show()
```

**Common aggregate functions:**
- `F.count()`, `F.sum()`, `F.avg()`, `F.min()`, `F.max()`
- `F.countDistinct()` - unique values
- `F.first()`, `F.last()` - within groups

### Joins

**SQL-style joins:**

```python
# Sample data
employees = spark.createDataFrame([
    {'emp_id': 1, 'name': 'Alice', 'dept_id': 10},
    {'emp_id': 2, 'name': 'Bob', 'dept_id': 20}
])

departments = spark.createDataFrame([
    {'dept_id': 10, 'dept_name': 'Engineering'},
    {'dept_id': 20, 'dept_name': 'Sales'}
])

# Inner join (default)
result = employees.join(departments, on='dept_id', how='inner')

# Left join
result = employees.join(departments, on='dept_id', how='left')

# Join types: 'inner', 'left', 'right', 'outer', 'cross'
```

### Transformations with withColumn

**Add or modify columns:**

```python
# Add new column
df = df.withColumn('age_plus_10', df.age + 10)

# Replace column
df = df.withColumn('age', df.age * 2)

# Use functions
from pyspark.sql import functions as F

df = df.withColumn('name_upper', F.upper(df.name))
df = df.withColumn('age_category', 
    F.when(df.age < 30, 'Young')
     .when(df.age < 50, 'Middle')
     .otherwise('Senior')
)
```

### Window Functions

**Ranking and running totals (common interview topic):**

```python
from pyspark.sql.window import Window
from pyspark.sql import functions as F

# Rank employees by salary within department
window_spec = Window.partitionBy('dept').orderBy(F.desc('salary'))

df = df.withColumn('rank', F.rank().over(window_spec))

# Running total
window_spec = Window.partitionBy('dept').orderBy('date').rowsBetween(Window.unboundedPreceding, 0)
df = df.withColumn('running_total', F.sum('amount').over(window_spec))
```

**SQL equivalent:**
```sql
SELECT *, 
       RANK() OVER (PARTITION BY dept ORDER BY salary DESC) as rank
FROM employees
```

### SQL Interface

**You can write SQL if you prefer:**

```python
# Register DataFrame as temp table
df.createOrReplaceTempView('employees')

# Query with SQL
result = spark.sql("""
    SELECT dept, COUNT(*) as count, AVG(age) as avg_age
    FROM employees
    WHERE age > 25
    GROUP BY dept
""")

result.show()
```

**Interview tip:** Mention this - shows you understand tools are interchangeable.

---

## Common PySpark Patterns for Interviews

### Pattern 1: Top N Per Group

**Problem:** Find top 3 highest paid employees in each department

```python
from pyspark.sql.window import Window
from pyspark.sql import functions as F

window_spec = Window.partitionBy('dept').orderBy(F.desc('salary'))

result = df.withColumn('rank', F.rank().over(window_spec)) \
           .filter(F.col('rank') <= 3)
```

### Pattern 2: Deduplicate Records

**Problem:** Remove duplicate records, keep most recent

```python
from pyspark.sql.window import Window
from pyspark.sql import functions as F

# Keep row with latest timestamp per ID
window_spec = Window.partitionBy('customer_id').orderBy(F.desc('timestamp'))

deduplicated = df.withColumn('row_num', F.row_number().over(window_spec)) \
                 .filter(F.col('row_num') == 1) \
                 .drop('row_num')
```

### Pattern 3: Pivot Tables

**Problem:** Transform rows to columns

```python
# From:
# date, product, sales
# 2024-01-01, A, 100
# 2024-01-01, B, 200

# To:
# date, A, B
# 2024-01-01, 100, 200

pivoted = df.groupBy('date').pivot('product').agg(F.sum('sales'))
```

### Pattern 4: Union Datasets

**Problem:** Combine multiple sources

```python
# Same schema
combined = df1.union(df2)

# Different schemas - select common columns first
df1_subset = df1.select('id', 'name', 'date')
df2_subset = df2.select('id', 'name', 'date')
combined = df1_subset.union(df2_subset)
```

### Pattern 5: Incremental Processing

**Problem:** Process only new/changed records

```python
# Read existing data
existing = spark.read.parquet('path/to/existing')

# Read new data
new = spark.read.csv('path/to/new')

# Find truly new records (not in existing)
new_records = new.join(
    existing,
    on='id',
    how='left_anti'  # Returns rows only in new
)

# Append to existing
new_records.write.mode('append').parquet('path/to/existing')
```

---

## PySpark vs Alternatives: Decision Framework

**CTO-level answer:**

| Scenario | Tool | Reason |
|----------|------|--------|
| Data in Snowflake | dbt | Pushdown to warehouse, declarative SQL |
| Data < 10GB | pandas | Simpler API, faster for small data |
| Data 10-100GB | pandas + sampling | Profile with sample, process full in warehouse |
| Data > 100GB | PySpark | Distributed processing required |
| Complex transformations | dbt + macros | Version control, testing, lineage |
| Real-time streaming | PySpark Structured Streaming | Native streaming support |
| Exploratory analysis | pandas | Interactive, mature ecosystem |
| Production ETL | Depends on source/target | Warehouse → dbt, Lake → PySpark |

**Interview talking point:**
"At Danaher with Snowflake as the primary platform, I'd lean heavily on dbt for transformations - it's declarative, testable, and leverages warehouse compute. PySpark would be for edge cases: processing data before warehouse ingestion, integrating with Databricks if that's in the stack, or handling streaming data. The key is using the right tool for the architecture."

---

## ETL/ELT Patterns in PySpark

### ETL (Transform before load)

**When to use:** Data lake sources, need cleansing before warehouse

```python
# Read from source
raw_df = spark.read.csv('s3://raw-data/transactions.csv')

# Transform
cleaned_df = raw_df \
    .filter(F.col('amount') > 0) \
    .withColumn('date', F.to_date('date_string', 'yyyy-MM-dd')) \
    .dropDuplicates(['transaction_id']) \
    .na.drop()  # Remove nulls

# Load to warehouse
cleaned_df.write \
    .mode('append') \
    .option('table', 'transactions') \
    .saveAsTable('warehouse.transactions')
```

### ELT (Load then transform in warehouse)

**When to use:** Warehouse has compute, want transformation history

```python
# Minimal transformation - just load
raw_df.write \
    .mode('append') \
    .saveAsTable('warehouse.raw_transactions')

# Transformations happen in dbt after load
```

**Interview answer:**
"ELT preferred for Snowflake - land raw data in warehouse, transform with dbt. Preserves raw history, leverages warehouse optimization, enables testing. ETL only if source data needs heavy cleansing or we're bridging non-warehouse systems."

---

## Data Quality Patterns

### Schema Validation

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Define expected schema
expected_schema = StructType([
    StructField('id', IntegerType(), False),  # nullable=False
    StructField('name', StringType(), False),
    StructField('age', IntegerType(), True)
])

# Read with schema enforcement
df = spark.read.schema(expected_schema).csv('data.csv')
```

### Data Quality Checks

```python
from pyspark.sql import functions as F

# Check for nulls
null_counts = df.select([
    F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in df.columns
])

# Check for duplicates
duplicate_count = df.groupBy('id').count().filter(F.col('count') > 1).count()

# Check value ranges
invalid_ages = df.filter((F.col('age') < 0) | (F.col('age') > 120)).count()

# Assertion pattern
if invalid_ages > 0:
    raise ValueError(f"Found {invalid_ages} records with invalid ages")
```

### Reconciliation Pattern

```python
# Compare source vs target record counts
source_count = source_df.count()
target_count = target_df.count()

if source_count != target_count:
    print(f"WARNING: Count mismatch - Source: {source_count}, Target: {target_count}")
    
# Compare sums for validation
source_sum = source_df.agg(F.sum('amount')).collect()[0][0]
target_sum = target_df.agg(F.sum('amount')).collect()[0][0]

if abs(source_sum - target_sum) > 0.01:
    raise ValueError("Sum validation failed")
```

---

## Performance Considerations

### Partitioning

**Problem:** Reading entire dataset for filtered queries

```python
# Bad - reads all data then filters
df = spark.read.parquet('data/')
result = df.filter(df.date == '2024-01-01')

# Good - partition by date, only reads relevant partition
df.write.partitionBy('date').parquet('data/')
df = spark.read.parquet('data/')
result = df.filter(df.date == '2024-01-01')  # Only reads 2024-01-01 partition
```

### Caching

**When to cache:** Reusing DataFrame multiple times

```python
# Without cache - reads source data twice
filtered = df.filter(df.age > 30)
count = filtered.count()  # First read
result = filtered.groupBy('dept').count()  # Second read

# With cache - reads once, keeps in memory
filtered = df.filter(df.age > 30).cache()
count = filtered.count()  # Reads and caches
result = filtered.groupBy('dept').count()  # Uses cached data
```

### Broadcast Joins

**Problem:** Joining large table with small table

```python
from pyspark.sql import functions as F

# Small lookup table
small_df = spark.read.csv('departments.csv')  # 100 rows

# Large fact table
large_df = spark.read.parquet('transactions/')  # 1B rows

# Broadcast small table to all nodes
result = large_df.join(F.broadcast(small_df), on='dept_id')
```

---

## Interview Scenarios

### Scenario 1: Data Pipeline Design

**Question:** "How would you design a pipeline to process daily sales data from multiple sources into Snowflake?"

**Approach:**
1. Identify source systems (APIs, databases, files)
2. Choose ingestion tool (Fivetran for SaaS, custom for APIs)
3. Land in S3 or Snowflake stage
4. ELT pattern - load raw to Snowflake
5. Transform with dbt (incremental models)
6. Orchestrate with dbt Cloud or Airflow

**Key points:**
- Minimize Python - use Fivetran + dbt
- PySpark only if source is data lake
- Mention data quality checks at each stage
- Discuss idempotency and reprocessing

### Scenario 2: Performance Problem

**Question:** "Pipeline processing 100M rows takes 4 hours. How do you optimize?"

**Diagnostic approach:**
1. Check if data can stay in warehouse (Snowflake) - avoid Spark entirely
2. If must use Spark:
   - Review partitioning strategy
   - Check for data skew (uneven partition sizes)
   - Identify shuffles (groupBy, join operations)
   - Review caching strategy
3. Profile with Spark UI - find slow stages
4. Consider columnar formats (Parquet vs CSV)

**Answer framework:**
"First question: Can this stay in Snowflake? Warehouse compute is often faster. If we must use Spark, I'd profile with Spark UI to find bottlenecks, optimize partitioning, and eliminate unnecessary shuffles."

### Scenario 3: Data Quality Issue

**Question:** "Production dashboard showing wrong numbers. How do you investigate?"

**Approach:**
1. Compare source vs target row counts
2. Check for duplicates (before/after)
3. Validate aggregations (sum amounts match)
4. Review transformation logic for bugs
5. Check for timezone/date issues
6. Look at data lineage - which upstream system?

**Code to share:**
```python
# Quick validation script
def validate_pipeline(source_df, target_df):
    # Count check
    print(f"Source: {source_df.count()}, Target: {target_df.count()}")
    
    # Sum check
    source_sum = source_df.agg(F.sum('amount')).collect()[0][0]
    target_sum = target_df.agg(F.sum('amount')).collect()[0][0]
    print(f"Source sum: {source_sum}, Target sum: {target_sum}")
    
    # Duplicate check
    source_dups = source_df.groupBy('id').count().filter(F.col('count') > 1).count()
    target_dups = target_df.groupBy('id').count().filter(F.col('count') > 1).count()
    print(f"Source duplicates: {source_dups}, Target duplicates: {target_dups}")
```

### Scenario 4: Real-time Requirements

**Question:** "Business wants near-real-time dashboards. Current batch runs daily. Options?"

**Options to discuss:**
1. **Increase batch frequency** (every hour) - simplest
2. **Snowflake Streams + Tasks** - warehouse-native CDC
3. **PySpark Structured Streaming** - if data lake architecture
4. **Kafka + Streaming** - true real-time, high complexity

**Answer:**
"Depends on 'near-real-time' definition. If hourly is acceptable, increase batch frequency - lowest complexity. If sub-minute latency required, evaluate Snowflake Streams (if data in warehouse) vs Kafka + Spark Streaming (if data lake). Always start with simplest solution that meets requirements."

---

## Key Talking Points for CTO Interview

### 1. Tool Selection Philosophy
"Right tool for the job. At Danaher with Snowflake, I'd default to dbt for transformations - declarative, testable, leverages warehouse compute. Python/PySpark for edge cases: data lake integration, complex Python libraries, streaming. The goal is maintainable systems, not showcasing technical skills."

### 2. Data Quality Approach
"Shift left - validate early. Schema enforcement at ingestion, not during transformation. Data quality tests in dbt. Reconciliation between source and target. Better to catch issues in dev than explain wrong production numbers."

### 3. Performance Philosophy
"Optimize for developer productivity first, then runtime. Profile before optimizing - find actual bottlenecks, not assumed ones. Often the answer is 'use the warehouse' rather than complex distributed systems."

### 4. Team Scalability
"Code for the team you have. If team knows SQL, dbt beats Python pipelines. Clear lineage and documentation matter more than clever code. Future maintainers will thank you."

### 5. Modern Data Stack Understanding
"ELT over ETL for warehouse environments. Fivetran + Snowflake + dbt is the pattern - minimize custom code. Python for glue between systems or data lake processing. Recognize when Python is solving yesterday's problems."

---

## Quick Reference: Essential PySpark Commands

```python
# Read data
df = spark.read.csv('file.csv', header=True)
df = spark.read.parquet('file.parquet')

# View data
df.show()
df.show(5)  # First 5 rows
df.printSchema()

# Select columns
df.select('col1', 'col2')

# Filter rows
df.filter(df.age > 30)
df.filter((df.age > 30) & (df.city == 'NYC'))

# Aggregate
df.groupBy('dept').count()
df.groupBy('dept').agg(F.avg('salary'))

# Join
df1.join(df2, on='key', how='inner')

# Add column
df.withColumn('new_col', df.col1 + df.col2)

# Remove duplicates
df.dropDuplicates(['id'])

# Sort
df.orderBy('col1')
df.orderBy(F.desc('col1'))

# Write data
df.write.mode('overwrite').parquet('output/')
df.write.mode('append').saveAsTable('table_name')
```

---

## Final Interview Prep Checklist

**Tonight:**
- [ ] Review PySpark patterns above
- [ ] Practice flashcards (see danaher_pyspark_flashcards.txt)
- [ ] Review Interview Mode scenarios
- [ ] Think through Danaher architecture (likely Snowflake + dbt heavy)

**Tomorrow morning:**
- [ ] Quick scan of this document (10 min)
- [ ] Review key talking points
- [ ] Review SQL to PySpark equivalents

**During interview:**
- [ ] Listen for architecture clues (lake vs warehouse)
- [ ] Ask about current stack before suggesting solutions
- [ ] Mention dbt as preferred for warehouse transformations
- [ ] Frame PySpark as tool for specific use cases, not default

**Remember:** 30-minute CTO interview is high-level discussion, not coding test. Focus on judgment, trade-offs, and strategic thinking over syntax.
