# data-engineering-patterns
Personal collection of data engineering patterns and best practices
Built over years of production experience with a modern data stack

## Repository Structure

```
data-engineering-patterns/
├── README.md                    # This file
├── python-essentials/
│   ├── string_manipulation.py   # Name parsing, cleaning
│   ├── data_structures.py       # Lists, dicts, comprehensions
│   ├── file_operations.py       # CSV, JSON, Parquet handling
│   └── common_algorithms.py     # Interview favorites
├── pandas-patterns/
│   ├── data_cleaning.py         # Missing values, duplicates
│   ├── aggregations.py          # GroupBy patterns
│   ├── joins_merges.py          # Different join strategies
│   └── performance_tips.py      # Optimization patterns
├── sql-to-python/
│   ├── window_functions.py      # ROW_NUMBER, RANK in pandas
│   ├── pivoting.py             # PIVOT/UNPIVOT equivalents
│   └── cte_patterns.py         # Breaking complex logic
├── airflow-dags/
│   ├── basic_etl_dag.py        # Simple ETL pattern
│   ├── dbt_orchestration.py    # dbt + Airflow
│   ├── incremental_load.py     # High-water mark pattern
│   ├── data_quality_dag.py     # Quality check patterns
│   └── dynamic_dag_factory.py  # Dynamic DAG generation
├── dbt-patterns/
│   ├── macros/
│   │   ├── generate_alias.sql  # Custom aliasing
│   │   └── incremental_merge.sql
│   ├── models/
│   │   ├── staging/            # Staging patterns
│   │   ├── intermediate/       # Business logic
│   │   └── marts/             # Final models
│   └── tests/
│       └── custom_tests.sql    # Advanced testing
├── snowflake-utilities/
│   ├── stored_procedures/      # Snowflake SPs
│   ├── dynamic_sql.sql        # Dynamic query patterns
│   └── performance_tuning.sql # Optimization queries
├── interview-solutions/
│   ├── fizzbuzz_variations.py  # Classic with twists
│   ├── name_parser_advanced.py # Handles edge cases
│   ├── merge_intervals.py      # Common algorithm
│   └── sql_in_python.py        # SQL logic in Python
└── modern-stack/
    ├── semantic_layer/          # dbt semantic layer
    ├── feature_store/          # Feature engineering
    └── orchestration/          # Modern patterns
