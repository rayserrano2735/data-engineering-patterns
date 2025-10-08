# Interview Prep: SimplePractice Senior Data Engineer
**Version: 1.0.5-RC3**

---

## Interview Context

**Company:** SimplePractice  
**Role:** Senior Data Engineer  
**Date:** October 10, 2025 (Friday)

**Key JD Signals:**
- dbt + Snowflake + Fivetran = Analytics Engineer role (despite "Data Engineer" title)
- Python for: Airflow orchestration, data quality frameworks, API integration
- Customer-facing dashboards (external use case - different constraints than internal BI)

**Python Focus:** You can handle dbt/SQL/Snowflake. This prep covers only the Python aspects:
1. Airflow DAGs and orchestration
2. Data quality frameworks in Python
3. API integration patterns
4. When to use Python vs when dbt handles it

---

## Airflow Fundamentals

### Why Airflow at SimplePractice

Orchestrates the data pipeline: trigger dbt runs, run Python quality checks, coordinate ingestion jobs.

**Not for:** Transformations (that's dbt). Just scheduling and dependencies.

### DAG Basics

**DAG = Directed Acyclic Graph:** Set of tasks with dependencies, no cycles.

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email': ['data-alerts@simplepractice.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'daily_appointments_pipeline',
    default_args=default_args,
    description='Process daily appointment data',
    schedule_interval='0 2 * * *',  # 2 AM daily
    catchup=False
)
```

**Key concepts:**
- `schedule_interval`: Cron expression or timedelta
- `catchup=False`: Don't backfill missed runs
- `default_args`: Apply to all tasks in DAG

### Task Dependencies

```python
# Define tasks
extract_appointments = BashOperator(
    task_id='extract_appointments',
    bash_command='python /scripts/extract_appointments.py',
    dag=dag
)

run_dbt = BashOperator(
    task_id='run_dbt_models',
    bash_command='cd /dbt && dbt run --models marts.fct_appointments',
    dag=dag
)

validate_data = PythonOperator(
    task_id='validate_appointment_data',
    python_callable=validate_appointments,
    dag=dag
)

send_alert = PythonOperator(
    task_id='send_completion_alert',
    python_callable=send_slack_notification,
    dag=dag
)

# Set dependencies - two ways to express same thing:

# Method 1: Bitshift operators
extract_appointments >> run_dbt >> validate_data >> send_alert

# Method 2: set_downstream/set_upstream
extract_appointments.set_downstream(run_dbt)
run_dbt.set_downstream(validate_data)
validate_data.set_downstream(send_alert)
```

**Visual DAG:**
```
extract_appointments → run_dbt → validate_data → send_alert
```

### PythonOperator with Functions

```python
def validate_appointments(**context):
    """
    Custom validation logic in Python.
    context provides access to execution date, task instance, etc.
    """
    import snowflake.connector
    
    # Get execution date from Airflow context
    execution_date = context['ds']  # YYYY-MM-DD string
    
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user='airflow_user',
        password='{{ var.value.snowflake_password }}',  # From Airflow variables
        account='simplepractice',
        warehouse='ANALYTICS_WH',
        database='ANALYTICS',
        schema='MARTS'
    )
    
    cursor = conn.cursor()
    
    # Check row count
    cursor.execute(f"""
        SELECT COUNT(*) FROM fct_appointments
        WHERE appointment_date = '{execution_date}'
    """)
    row_count = cursor.fetchone()[0]
    
    if row_count == 0:
        raise ValueError(f"No appointments found for {execution_date}")
    
    # Check for nulls in required fields
    cursor.execute(f"""
        SELECT COUNT(*) FROM fct_appointments
        WHERE appointment_date = '{execution_date}'
        AND (client_id IS NULL OR clinician_id IS NULL)
    """)
    null_count = cursor.fetchone()[0]
    
    if null_count > 0:
        raise ValueError(f"Found {null_count} records with null IDs")
    
    cursor.close()
    conn.close()
    
    print(f"✓ Validation passed: {row_count} appointments processed")

# Use in DAG
validate_data = PythonOperator(
    task_id='validate_appointment_data',
    python_callable=validate_appointments,
    provide_context=True,  # Passes context to function
    dag=dag
)
```

### XCom for Passing Data Between Tasks

```python
def extract_appointment_count(**context):
    """Task 1: Calculate count"""
    import snowflake.connector
    
    conn = snowflake.connector.connect(...)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM staging.appointments")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    
    # Push to XCom
    context['task_instance'].xcom_push(key='appointment_count', value=count)
    return count

def check_appointment_threshold(**context):
    """Task 2: Use count from Task 1"""
    # Pull from XCom
    count = context['task_instance'].xcom_pull(
        task_ids='extract_appointment_count',
        key='appointment_count'
    )
    
    threshold = 1000
    if count < threshold:
        raise ValueError(f"Only {count} appointments, expected > {threshold}")
    
    print(f"✓ Count {count} exceeds threshold {threshold}")

# Tasks
task1 = PythonOperator(
    task_id='extract_appointment_count',
    python_callable=extract_appointment_count,
    provide_context=True,
    dag=dag
)

task2 = PythonOperator(
    task_id='check_appointment_threshold',
    python_callable=check_appointment_threshold,
    provide_context=True,
    dag=dag
)

task1 >> task2
```

### Branching Logic

```python
from airflow.operators.python import BranchPythonOperator

def check_data_volume(**context):
    """Decide which path to take based on data volume"""
    import snowflake.connector
    
    conn = snowflake.connector.connect(...)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM staging.raw_appointments")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    
    # Branch based on volume
    if count > 100000:
        return 'run_full_refresh'  # Task ID to execute
    else:
        return 'run_incremental'   # Task ID to execute

branch_task = BranchPythonOperator(
    task_id='check_volume',
    python_callable=check_data_volume,
    provide_context=True,
    dag=dag
)

full_refresh = BashOperator(
    task_id='run_full_refresh',
    bash_command='dbt run --full-refresh --models fct_appointments',
    dag=dag
)

incremental = BashOperator(
    task_id='run_incremental',
    bash_command='dbt run --models fct_appointments',
    dag=dag
)

# DAG structure:
# check_volume → run_full_refresh (if count > 100K)
#             → run_incremental (if count <= 100K)
branch_task >> [full_refresh, incremental]
```

### Sensors for External Dependencies

```python
from airflow.sensors.s3_key_sensor import S3KeySensor

# Wait for file to appear in S3 before proceeding
wait_for_file = S3KeySensor(
    task_id='wait_for_appointments_file',
    bucket_name='simplepractice-raw-data',
    bucket_key='appointments/{{ ds }}/data.csv',  # Uses execution date
    aws_conn_id='aws_default',
    timeout=3600,  # 1 hour timeout
    poke_interval=300,  # Check every 5 minutes
    dag=dag
)

process_file = BashOperator(
    task_id='process_appointments',
    bash_command='python /scripts/process_appointments.py',
    dag=dag
)

wait_for_file >> process_file
```

---

## Data Quality Framework in Python

### Why Python for Data Quality

dbt tests handle SQL-based validation. Python for:
- Complex business logic
- External API checks (e.g., verify appointment IDs exist in source system)
- Statistical anomaly detection
- Cross-system reconciliation

### Pattern: Data Quality Checker Class

```python
import snowflake.connector
from datetime import datetime

class DataQualityChecker:
    """Framework for running data quality checks"""
    
    def __init__(self, connection_params):
        self.conn = snowflake.connector.connect(**connection_params)
        self.cursor = self.conn.cursor()
        self.failures = []
    
    def check_row_count(self, table, min_rows, max_rows=None):
        """Validate row count within expected range"""
        self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = self.cursor.fetchone()[0]
        
        if count < min_rows:
            self.failures.append(
                f"{table}: Only {count} rows, expected >= {min_rows}"
            )
        
        if max_rows and count > max_rows:
            self.failures.append(
                f"{table}: {count} rows exceeds max {max_rows}"
            )
        
        return count
    
    def check_null_percentage(self, table, column, max_null_pct):
        """Ensure null rate below threshold"""
        query = f"""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN {column} IS NULL THEN 1 ELSE 0 END) as null_count
        FROM {table}
        """
        self.cursor.execute(query)
        total, null_count = self.cursor.fetchone()
        
        if total == 0:
            return
        
        null_pct = (null_count / total) * 100
        
        if null_pct > max_null_pct:
            self.failures.append(
                f"{table}.{column}: {null_pct:.1f}% nulls, max allowed {max_null_pct}%"
            )
        
        return null_pct
    
    def check_referential_integrity(self, child_table, child_key, parent_table, parent_key):
        """Validate foreign key relationships"""
        query = f"""
        SELECT COUNT(*) FROM {child_table} c
        LEFT JOIN {parent_table} p ON c.{child_key} = p.{parent_key}
        WHERE p.{parent_key} IS NULL AND c.{child_key} IS NOT NULL
        """
        self.cursor.execute(query)
        orphaned_count = self.cursor.fetchone()[0]
        
        if orphaned_count > 0:
            self.failures.append(
                f"{child_table}.{child_key}: {orphaned_count} orphaned records"
            )
        
        return orphaned_count
    
    def check_date_range(self, table, date_column, min_date, max_date):
        """Validate dates within expected range"""
        query = f"""
        SELECT COUNT(*) FROM {table}
        WHERE {date_column} < '{min_date}' OR {date_column} > '{max_date}'
        """
        self.cursor.execute(query)
        out_of_range = self.cursor.fetchone()[0]
        
        if out_of_range > 0:
            self.failures.append(
                f"{table}.{date_column}: {out_of_range} dates outside {min_date} to {max_date}"
            )
        
        return out_of_range
    
    def check_duplicate_keys(self, table, key_columns):
        """Check for duplicate values in what should be unique"""
        keys = ', '.join(key_columns)
        query = f"""
        SELECT COUNT(*) FROM (
            SELECT {keys}, COUNT(*) as cnt
            FROM {table}
            GROUP BY {keys}
            HAVING COUNT(*) > 1
        )
        """
        self.cursor.execute(query)
        duplicate_count = self.cursor.fetchone()[0]
        
        if duplicate_count > 0:
            self.failures.append(
                f"{table}: {duplicate_count} duplicate key combinations ({keys})"
            )
        
        return duplicate_count
    
    def get_report(self):
        """Return all failures"""
        self.cursor.close()
        self.conn.close()
        
        if self.failures:
            return {
                'status': 'FAILED',
                'failure_count': len(self.failures),
                'failures': self.failures
            }
        else:
            return {
                'status': 'PASSED',
                'failure_count': 0
            }

# Usage in Airflow
def run_quality_checks(**context):
    """Airflow task that runs all quality checks"""
    
    checker = DataQualityChecker({
        'user': 'airflow',
        'password': '{{ var.value.snowflake_password }}',
        'account': 'simplepractice',
        'warehouse': 'ANALYTICS_WH',
        'database': 'ANALYTICS',
        'schema': 'MARTS'
    })
    
    # Run checks
    checker.check_row_count('fct_appointments', min_rows=1000)
    checker.check_null_percentage('fct_appointments', 'client_id', max_null_pct=0.1)
    checker.check_referential_integrity(
        'fct_appointments', 'client_id',
        'dim_clients', 'client_id'
    )
    checker.check_date_range(
        'fct_appointments', 'appointment_date',
        '2020-01-01', datetime.now().strftime('%Y-%m-%d')
    )
    checker.check_duplicate_keys('fct_appointments', ['appointment_id'])
    
    # Get results
    report = checker.get_report()
    
    if report['status'] == 'FAILED':
        # Send to Slack, email, or monitoring system
        error_message = '\n'.join(report['failures'])
        raise ValueError(f"Data quality checks failed:\n{error_message}")
    
    print(f"✓ All quality checks passed")
```

---

## API Integration Patterns

### Why Python for APIs

SimplePractice likely integrates with: payment processors, scheduling systems, marketing platforms. Python handles API calls, then lands data in Snowflake for dbt transformation.

### Pattern: API Extractor Class

```python
import requests
import json
from datetime import datetime, timedelta

class SimplePracticeAPIExtractor:
    """Extract data from external APIs and load to Snowflake"""
    
    def __init__(self, api_key, snowflake_conn):
        self.api_key = api_key
        self.conn = snowflake_conn
        self.base_url = "https://api.partner.com/v1"
    
    def extract_appointments(self, start_date, end_date):
        """
        Extract appointments from external scheduling API.
        Handles pagination, rate limiting, retries.
        """
        appointments = []
        page = 1
        has_more = True
        
        while has_more:
            # API call with parameters
            response = requests.get(
                f"{self.base_url}/appointments",
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                params={
                    'start_date': start_date,
                    'end_date': end_date,
                    'page': page,
                    'per_page': 100
                },
                timeout=30
            )
            
            # Handle errors
            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code} - {response.text}")
            
            data = response.json()
            appointments.extend(data['appointments'])
            
            # Check pagination
            has_more = data.get('has_more', False)
            page += 1
            
            # Rate limiting - wait between requests
            if has_more:
                import time
                time.sleep(0.5)  # 500ms delay
        
        return appointments
    
    def load_to_snowflake(self, data, table_name):
        """Load extracted data to Snowflake staging table"""
        cursor = self.conn.cursor()
        
        # Create staging table if not exists
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS staging.{table_name} (
            raw_data VARIANT,
            extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
        """)
        
        # Insert data as JSON
        for record in data:
            cursor.execute(
                f"INSERT INTO staging.{table_name} (raw_data) SELECT PARSE_JSON(%s)",
                (json.dumps(record),)
            )
        
        self.conn.commit()
        cursor.close()
        
        print(f"✓ Loaded {len(data)} records to staging.{table_name}")
    
    def extract_and_load(self, start_date, end_date):
        """Complete ETL: extract from API, load to Snowflake"""
        appointments = self.extract_appointments(start_date, end_date)
        self.load_to_snowflake(appointments, 'api_appointments')
        return len(appointments)

# Usage in Airflow
def extract_partner_appointments(**context):
    """Airflow task for API extraction"""
    import snowflake.connector
    
    # Get execution date
    execution_date = context['ds']
    
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user='airflow',
        password='{{ var.value.snowflake_password }}',
        account='simplepractice',
        warehouse='LOADING_WH',
        database='RAW',
        schema='STAGING'
    )
    
    # Extract and load
    extractor = SimplePracticeAPIExtractor(
        api_key='{{ var.value.partner_api_key }}',
        snowflake_conn=conn
    )
    
    count = extractor.extract_and_load(
        start_date=execution_date,
        end_date=execution_date
    )
    
    conn.close()
    
    print(f"✓ Extracted {count} appointments from partner API")
```

### Handling API Rate Limits

```python
import time
from functools import wraps

def rate_limit(max_per_second):
    """Decorator to enforce rate limiting"""
    min_interval = 1.0 / max_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = min_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_per_second=2)  # Max 2 requests per second
def call_api(endpoint):
    """Rate-limited API call"""
    response = requests.get(endpoint)
    return response.json()

# Usage
for i in range(10):
    data = call_api(f"https://api.partner.com/appointments?page={i}")
    # Automatically enforces 500ms between calls
```

---

## Python vs dbt: Decision Framework

**Use dbt (SQL) for:**
- Transformations on data already in Snowflake
- Joins, aggregations, window functions
- Data modeling (star schema, dimensional models)
- Business logic that's set-based
- Anything analysts need to understand/modify

**Use Python for:**
- Orchestration (Airflow DAGs)
- API calls to external systems
- Complex business logic that's hard in SQL
- Statistical analysis, ML models
- Data quality checks with complex logic
- File manipulation before warehouse load

**SimplePractice example:**
- Python: Extract appointments from scheduling API, load JSON to Snowflake staging
- dbt: Parse JSON, join with client/clinician tables, calculate no-show rates, build fct_appointments
- Python: Run quality checks on fct_appointments, alert if issues
- Airflow: Orchestrate the sequence

**Interview talking point:**
"I prefer dbt for transformations—it's declarative, testable, and accessible to analysts. Python for glue code: orchestration, API integration, and checks that need procedural logic. The rule is: if it can be SQL, make it SQL."

---

## Common Interview Scenarios

### Scenario 1: Design Daily Pipeline

**Question:** "Design the daily pipeline for processing clinic appointments."

**Approach:**
1. **Extraction:** Fivetran pulls from backend database to Snowflake raw schema (no Python needed)
2. **Orchestration:** Airflow DAG triggers at 2 AM
3. **Transformation:** dbt models process raw → staging → marts
4. **Quality checks:** Python validates row counts, nulls, referential integrity
5. **Customer dashboards:** Refresh BI tool caches

**Python pieces:**
```python
# Airflow DAG structure
extract → dbt_run → quality_checks → cache_refresh → alert

# quality_checks task uses DataQualityChecker class
# alert task sends Slack notification on failure
```

### Scenario 2: Customer-Facing Analytics

**Question:** "Clinicians want a dashboard showing their no-show rate. What's different about customer-facing vs internal analytics?"

**Considerations:**
- **Security:** Row-level security (clinician only sees their data)
- **Performance:** Pre-aggregate, can't let customer queries slow warehouse
- **Reliability:** More critical than internal - affects customer perception
- **Cost:** Customers generate unpredictable query load

**Python role:**
- Pre-compute aggregations in Python, write to dedicated customer tables
- Cache warming: Python script pre-runs common queries
- Monitoring: Python checks query performance, alerts if slow

```python
def precompute_clinician_metrics():
    """Pre-compute metrics for customer dashboards"""
    cursor.execute("""
    CREATE OR REPLACE TABLE customer_metrics.clinician_no_show_rate AS
    SELECT 
        clinician_id,
        date_trunc('month', appointment_date) as month,
        count(*) as total_appointments,
        sum(is_no_show) as no_shows,
        (sum(is_no_show) / count(*)) * 100 as no_show_rate
    FROM marts.fct_appointments
    WHERE appointment_date >= dateadd('month', -12, current_date())
    GROUP BY 1, 2
    """)
    
    # Small table, fast queries, no complex joins in customer dashboards
```

### Scenario 3: Data Quality Issue

**Question:** "Finance reports revenue numbers don't match backend system. How do you investigate?"

**Python investigation script:**
```python
def reconcile_revenue():
    """Compare Snowflake analytics to source system"""
    
    # Get Snowflake total
    cursor.execute("""
    SELECT SUM(payment_amount)
    FROM marts.fct_payments
    WHERE payment_date = CURRENT_DATE - 1
    """)
    snowflake_total = cursor.fetchone()[0]
    
    # Get source system total via API
    response = requests.get(
        "https://api.backend.com/revenue",
        params={'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')}
    )
    source_total = response.json()['total_revenue']
    
    # Compare
    difference = abs(snowflake_total - source_total)
    tolerance = 0.01  # 1 cent tolerance for rounding
    
    if difference > tolerance:
        # Investigate: missing records, duplicates, wrong amounts
        cursor.execute("""
        SELECT 
            COUNT(*) as record_count,
            COUNT(DISTINCT payment_id) as unique_count
        FROM marts.fct_payments
        WHERE payment_date = CURRENT_DATE - 1
        """)
        record_count, unique_count = cursor.fetchone()
        
        report = {
            'snowflake_total': snowflake_total,
            'source_total': source_total,
            'difference': difference,
            'record_count': record_count,
            'duplicate_count': record_count - unique_count
        }
        
        # Alert with details
        send_alert(f"Revenue reconciliation failed: {json.dumps(report, indent=2)}")
    else:
        print("✓ Revenue reconciliation passed")
```

---

## Quick Reference: Essential Python for Data Engineering

```python
# Airflow DAG structure
dag = DAG('pipeline_name', default_args=..., schedule_interval='0 2 * * *')
task1 >> task2 >> task3  # Dependencies

# PythonOperator
task = PythonOperator(
    task_id='task_name',
    python_callable=my_function,
    provide_context=True,
    dag=dag
)

# XCom (pass data between tasks)
context['task_instance'].xcom_push(key='my_key', value=data)
data = context['task_instance'].xcom_pull(task_ids='other_task', key='my_key')

# Snowflake connection
import snowflake.connector
conn = snowflake.connector.connect(user=..., password=..., account=...)
cursor = conn.cursor()
cursor.execute("SELECT * FROM table")
results = cursor.fetchall()

# API calls
response = requests.get(url, headers={...}, params={...}, timeout=30)
data = response.json()

# Data quality pattern
class DataQualityChecker:
    def check_row_count(self, table, min_rows): ...
    def check_null_percentage(self, table, column, max_pct): ...
    def check_referential_integrity(self, child, parent): ...
```

---

## Final Interview Prep Checklist

**Thursday night:**
- [ ] Review Airflow patterns (DAGs, dependencies, XCom)
- [ ] Review flashcards (see simplepractice_python_flashcards.txt)
- [ ] Think through: When Python vs when dbt?

**Friday morning:**
- [ ] Quick scan of this document (10 min)
- [ ] Review data quality framework pattern
- [ ] Review API integration pattern

**During interview:**
- [ ] Ask about their current stack before suggesting solutions
- [ ] Emphasize dbt for transformations, Python for orchestration/APIs
- [ ] Mention customer-facing analytics constraints (security, performance, reliability)
- [ ] Frame Python as "glue code" not primary transformation tool

**Remember:** SimplePractice uses dbt heavily. Python is secondary - for orchestration, API integration, and complex checks. Default to "dbt handles that" unless it's clearly a Python use case.
