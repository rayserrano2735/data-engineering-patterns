# Airflow Python for SQL People: The Essential Guide (Modern Stack Edition)

## Introduction

This guide teaches SQL professionals the minimal Python needed for Apache Airflow in two parts:

**Part A: Modern Data Stack Orchestration (Start Here)**
- For teams using Fivetran, dbt Cloud, and similar tools
- Airflow as pure orchestrator - no data processing
- 1 week to productivity

**Part B: Legacy/Full Airflow Patterns**
- For teams still using Airflow for ETL/ELT
- Complex data processing in Airflow
- 2-3 weeks to productivity

Most modern teams only need Part A. If your company uses Fivetran + dbt Cloud + Snowflake/BigQuery/Databricks, skip directly to Part A and ignore Part B unless you need it.

---

# PART A: MODERN DATA STACK ORCHESTRATION

*For teams using Fivetran, dbt Cloud, Hightouch, etc. - where Airflow only orchestrates, never processes data*

## A.1: Why Airflow in the Modern Stack?

Honestly? It's debatable. Many teams are moving to:
- **dbt Cloud's native orchestration** (if you only need dbt)
- **Dagster** (better for modern stack)
- **Prefect** (simpler, cloud-native)
- **Temporal** (for complex workflows)

But if you're here, it's likely because:
1. Your company already has Airflow/Astronomer
2. You need to coordinate multiple tools (Fivetran → dbt → Hightouch → Tableau)
3. You have complex dependencies across systems
4. Corporate standards require it

## A.2: Minimum Python for Orchestration Only

### Understanding Decorators (The @ Symbol)

```python
# You'll see this in every modern Airflow DAG:
@dag(schedule="@daily", start_date=datetime(2024, 1, 1))
def my_pipeline():
    ...

# What's that @ thing?
# A decorator is just a wrapper that adds functionality.
# Think of it like gift wrapping - the function stays the same,
# but now it has extra capabilities.

# What @dag actually means:
# "Take my normal Python function and turn it into an Airflow DAG"

# Without decorator (you never write this):
def my_pipeline():
    ...
my_pipeline = dag(schedule="@daily")(my_pipeline)  # Ugly!

# With decorator (what you actually write):
@dag(schedule="@daily")  # Clean!
def my_pipeline():
    ...

# The only decorators you need in Airflow:
@dag         # Makes a function into a DAG
@task        # Makes a function into a task
@task.branch # Makes a function into a branching task

# That's it! Think of @ as "transform this into Airflow component"
```

### Variables and Configuration
```python
# This is 50% of what you need
fivetran_connector_id = "salesforce_prod"
dbt_job_id = 12345
slack_channel = "#data-alerts"

# Configuration dictionary
config = {
    "fivetran_connectors": ["salesforce", "stripe", "zendesk"],
    "dbt_job_id": 12345,
    "notification_email": "data-team@company.com"
}
```

### Imports You Actually Need
```python
from datetime import datetime, timedelta
from airflow.decorators import dag
from airflow.providers.fivetran.operators.fivetran import FivetranOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.providers.slack.operators.slack import SlackWebhookOperator
from airflow.models import Variable
```

### The Only DAG Pattern You Need
```python
@dag(
    schedule="0 6 * * *",  # When to run
    start_date=datetime(2024, 1, 1),
    catchup=False,  # Don't backfill
    tags=["orchestration"]
)
def modern_data_pipeline():
    """Orchestrate Fivetran → dbt Cloud → Reverse ETL"""
    
    # Step 1: Sync data sources
    sync_salesforce = FivetranOperator(
        task_id="sync_salesforce",
        connector_id="salesforce_prod"
    )
    
    sync_stripe = FivetranOperator(
        task_id="sync_stripe", 
        connector_id="stripe_prod"
    )
    
    # Step 2: Transform in dbt Cloud
    run_dbt = DbtCloudRunJobOperator(
        task_id="run_dbt_cloud",
        job_id=12345,
        wait_for_termination=True,
        check_interval=60
    )
    
    # Step 3: Notify completion
    notify = SlackWebhookOperator(
        task_id="notify_completion",
        slack_webhook_conn_id="slack",
        message="Daily pipeline complete ✅"
    )
    
    # Dependencies: Syncs complete → dbt runs → notification
    [sync_salesforce, sync_stripe] >> run_dbt >> notify

my_pipeline = modern_data_pipeline()
```

That's it. This is 90% of modern Airflow usage.

## A.3: Common Modern Stack Patterns

### Pattern 1: Sequential Tool Orchestration
```python
@dag(schedule="@daily", start_date=datetime(2024, 1, 1), catchup=False)
def sequential_orchestration():
    """Run tools in sequence"""
    
    fivetran = FivetranOperator(
        task_id="extract",
        connector_id="database_sync"
    )
    
    dbt = DbtCloudRunJobOperator(
        task_id="transform",
        job_id=12345
    )
    
    hightouch = HightouchSyncOperator(
        task_id="reverse_etl",
        sync_id=67890
    )
    
    fivetran >> dbt >> hightouch

dag = sequential_orchestration()
```

### Pattern 2: Parallel Syncs with Convergence
```python
@dag(schedule="@daily", start_date=datetime(2024, 1, 1), catchup=False)
def parallel_syncs():
    """Sync multiple sources, then transform"""
    
    # Define sources to sync
    sources = ["salesforce", "stripe", "zendesk", "hubspot"]
    
    # Create sync task for each
    sync_tasks = []
    for source in sources:
        sync = FivetranOperator(
            task_id=f"sync_{source}",
            connector_id=f"{source}_prod"
        )
        sync_tasks.append(sync)
    
    # Run dbt after ALL syncs complete
    transform = DbtCloudRunJobOperator(
        task_id="dbt_transform",
        job_id=12345
    )
    
    # All syncs must finish before dbt
    sync_tasks >> transform

dag = parallel_syncs()
```

### Pattern 3: Conditional Orchestration
```python
from airflow.decorators import task

@dag(schedule="@daily", start_date=datetime(2024, 1, 1), catchup=False)
def conditional_pipeline():
    """Only run expensive jobs if needed"""
    
    @task.branch
    def check_if_sync_needed():
        """Check if we need to run today"""
        from datetime import date
        
        # Skip weekends
        if date.today().weekday() in [5, 6]:
            return "skip_pipeline"
        else:
            return "run_fivetran"
    
    check = check_if_sync_needed()
    
    run_fivetran = FivetranOperator(
        task_id="run_fivetran",
        connector_id="expensive_api_sync"
    )
    
    @task
    def skip_pipeline():
        print("Skipping weekend run")
    
    run_dbt = DbtCloudRunJobOperator(
        task_id="run_dbt",
        job_id=12345,
        trigger_rule="none_failed_min_one_success"
    )
    
    check >> [run_fivetran, skip_pipeline()] >> run_dbt

dag = conditional_pipeline()
```

### Pattern 4: Monitoring and Alerting
```python
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

@dag(schedule="0 8 * * *", start_date=datetime(2024, 1, 1), catchup=False)
def data_quality_monitoring():
    """Check data freshness after pipeline runs"""
    
    check_freshness = SnowflakeOperator(
        task_id="check_data_freshness",
        snowflake_conn_id="snowflake",
        sql="""
            SELECT CASE 
                WHEN MAX(updated_at) < CURRENT_DATE - 1 
                THEN RAISE_ERROR('Data is stale!')
                ELSE 'Data is fresh'
            END
            FROM analytics.fct_orders
        """
    )
    
    alert_if_stale = SlackWebhookOperator(
        task_id="alert_stale_data",
        slack_webhook_conn_id="slack",
        message="⚠️ Data freshness check failed!",
        trigger_rule="one_failed"  # Only runs if previous task failed
    )
    
    check_freshness >> alert_if_stale

dag = data_quality_monitoring()
```

## A.4: Astronomer Setup for Modern Stack

### Installation (Windows with Docker)

**Prerequisites for Windows:**
1. Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Enable WSL2 backend in Docker Desktop settings
3. Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install)
4. Restart your computer

**Install Astronomer CLI:**

Windows PowerShell (as Administrator):
```powershell
# Download and install
Invoke-WebRequest -Uri https://github.com/astronomer/astro-cli/releases/latest/download/astro_1.20.0_windows_amd64.zip -OutFile astro.zip
Expand-Archive -Path astro.zip -DestinationPath .
Move-Item astro.exe "C:\Program Files\"
# Add to PATH manually via System Properties
```

Or use WSL2 (Recommended):
```bash
curl -sSL install.astronomer.io | sudo bash -s
```

**Create Project:**
```bash
# Create project
mkdir airflow-orchestration
cd airflow-orchestration
astro dev init

# Add providers to requirements.txt
echo "astronomer-providers[fivetran]" >> requirements.txt
echo "astronomer-providers[dbt-cloud]" >> requirements.txt
echo "apache-airflow-providers-slack" >> requirements.txt

# Start Airflow
astro dev start  # Docker Desktop must be running
```

**Access Airflow:**
- URL: `http://localhost:8080`
- Username: `admin`
- Password: `admin`

### Skip Local Development If You Want
```bash
# Just deploy straight to Astronomer Cloud
astro deploy --deployment-id your-dev-deployment

# No Docker needed if you're only orchestrating cloud tools
```

## A.5: Environment Variables and Connections

### Configure in Astronomer UI (not code)
```python
# Bad - Don't hardcode
fivetran_api_key = "abc123"  # NO!

# Good - Use Airflow Connections
FivetranOperator(
    conn_id="fivetran_default"  # Configure in Astronomer UI
)
```

### Set up connections in Astronomer Cloud:
1. Go to Astronomer Cloud UI
2. Environment → Connections
3. Add:
   - `fivetran_default` (Fivetran API key)
   - `dbt_cloud_default` (dbt Cloud API token)
   - `snowflake_default` (Database connection)
   - `slack_default` (Webhook URL)

## A.6: Testing Your Orchestration DAGs

```python
# tests/test_orchestration.py
def test_dag_loads():
    """Make sure DAG has no syntax errors"""
    from airflow.models import DagBag
    
    dag_bag = DagBag(include_examples=False)
    dag = dag_bag.get_dag("modern_data_pipeline")
    
    assert dag is not None
    assert len(dag.tasks) == 4

def test_dependencies():
    """Check task dependencies are correct"""
    dag = get_dag("modern_data_pipeline")
    
    sync_task = dag.get_task("sync_salesforce")
    dbt_task = dag.get_task("run_dbt_cloud")
    
    assert dbt_task in sync_task.downstream_list
```

Run tests: `astro dev pytest`

## A.7: When You Actually Need More Python

You might need slightly more Python only if:

1. **Dynamic connector lists from a database**:
```python
@task
def get_active_connectors():
    """Query database for active Fivetran connectors"""
    hook = SnowflakeHook()
    connectors = hook.get_records(
        "SELECT connector_id FROM admin.active_connectors"
    )
    return [c[0] for c in connectors]
```

2. **Complex scheduling logic**:
```python
def should_run_full_refresh():
    """Full refresh on Sundays, incremental otherwise"""
    from datetime import date
    return date.today().weekday() == 6  # Sunday

dbt_mode = "full-refresh" if should_run_full_refresh() else "incremental"
```

3. **Error handling and retries**:
```python
try:
    response = run_api_call()
except Exception as e:
    send_alert(f"Pipeline failed: {e}")
    raise
```

## A.8: Quick Reference - Modern Stack Only

### All the Python you need:
```python
# Variables
connector_id = "salesforce"
job_id = 12345

# Lists  
connectors = ["salesforce", "stripe", "hubspot"]

# Dictionaries
config = {"schedule": "@daily", "retries": 2}

# Simple functions
def is_weekend():
    from datetime import date
    return date.today().weekday() >= 5

# Task dependencies
extract >> transform >> load
[task1, task2] >> task3
```

### All the operators you need:
```python
FivetranOperator()       # Sync data
DbtCloudRunJobOperator() # Transform data
SlackWebhookOperator()   # Send notifications
SnowflakeOperator()      # Run queries
EmailOperator()          # Send emails
```

### Astronomer commands:
```bash
astro dev init      # Create project (once)
astro dev start     # Start local Airflow (Docker required)
astro dev stop      # Stop local Airflow
astro dev restart   # Restart after changes
astro dev pytest    # Run tests
astro deploy        # Deploy to cloud
```

### Windows-specific tips:
- Always ensure Docker Desktop is running first
- Use forward slashes `/` in paths, not backslashes
- If changes don't appear, run `astro dev restart`
- Configure Git for LF line endings: `git config --global core.autocrlf true`

## A.9: Migration Path Away from Airflow

Since the era of Airflow dependency is ending, here's how teams are migrating:

### Option 1: dbt Cloud Native Orchestration
- If you only orchestrate Fivetran → dbt → BI tools
- dbt Cloud can trigger Fivetran syncs now
- No Airflow needed

### Option 2: Fivetran + dbt Cloud Webhooks
- Fivetran completes → webhook triggers dbt Cloud
- dbt Cloud completes → webhook triggers reverse ETL
- Zero orchestration tool needed

### Option 3: Modern Orchestrators
- **Dagster**: Built for modern data stack
- **Prefect**: Simpler, Python-native
- **Temporal**: For complex workflows
- **Mage**: Notebook-based pipelines

### When to Keep Airflow
- Complex cross-system dependencies
- Legacy code that would be expensive to migrate
- Corporate mandate
- Need for on-premise orchestration

## A.11: Appendix - Deep Dive: Understanding Decorators in Airflow

*Optional reading for those who want to truly understand what's happening behind the @ symbol*

```python
# DECORATORS IN AIRFLOW: From Zero to Understanding

# 1. FIRST, UNDERSTAND THAT FUNCTIONS ARE OBJECTS IN PYTHON
def my_etl_process():
    return "Extract, Transform, Load"

# You can assign functions to variables
pipeline = my_etl_process
print(pipeline())  # "Extract, Transform, Load"

# 2. AIRFLOW NEEDS TO TRACK YOUR FUNCTIONS
# Problem: How does Airflow know your function should be a DAG?
def my_pipeline():
    sync_data = "syncing..."
    transform_data = "transforming..."
    
# Airflow: "This is just a function. I don't know what to do with it!"

# 3. THE MANUAL WAY (What decorators do behind the scenes)
from airflow import DAG

def my_pipeline():
    return "pipeline logic"

# Manually convert function to DAG (you never do this!)
my_pipeline_dag = DAG(
    dag_id="my_pipeline",
    schedule="@daily"
)
# This is tedious and separates the logic from configuration

# 4. ENTER THE DECORATOR PATTERN
def make_it_a_dag(func):
    """This decorator converts a function into an Airflow DAG"""
    # Create DAG object with the function's name
    dag = DAG(dag_id=func.__name__)
    # Store the function logic
    dag.function = func
    # Return the DAG object (not the function!)
    return dag

# Manual decoration (showing what @ does)
def my_pipeline():
    return "pipeline logic"

my_pipeline = make_it_a_dag(my_pipeline)  # Transform function → DAG
# Now my_pipeline is a DAG object, not a function!

# 5. THE @ SYNTAX - CLEANER WAY
@make_it_a_dag  # Same as: my_pipeline = make_it_a_dag(my_pipeline)
def my_pipeline():
    return "pipeline logic"

# 6. DECORATORS WITH ARGUMENTS (What Airflow actually uses)
def dag(schedule=None, start_date=None):
    """This is how Airflow's @dag decorator works"""
    def decorator(func):
        # Create DAG with configuration
        dag_object = DAG(
            dag_id=func.__name__,
            schedule=schedule,
            start_date=start_date
        )
        dag_object.function = func
        return dag_object
    return decorator

# Now you can configure your DAG
@dag(schedule="@daily", start_date=datetime(2024, 1, 1))
def my_pipeline():
    return "pipeline logic"

# 7. REAL AIRFLOW EXAMPLE - WHAT'S ACTUALLY HAPPENING
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def my_data_pipeline():
    """
    This function is now:
    1. Registered in Airflow's database
    2. Visible in the UI
    3. Scheduled to run daily
    4. Has retry logic
    5. Can contain tasks
    """
    
    @task  # This decorator transforms function → Airflow Task
    def extract():
        return {"data": "extracted"}
    
    @task
    def transform(data):
        return {"transformed": data}
    
    # These aren't regular functions anymore!
    # They're Airflow Task objects that:
    # - Have dependencies
    # - Can retry on failure
    # - Log to Airflow
    # - Show in the UI
    
    data = extract()
    result = transform(data)

# 8. THE TRANSFORMATION VISUALIZATION
"""
WITHOUT DECORATORS:
my_pipeline() → Regular Python Function
extract() → Regular Python Function  
transform() → Regular Python Function

WITH DECORATORS:
@dag
my_pipeline() → Airflow DAG Object (appears in UI, has schedule)
    @task
    extract() → Airflow Task Object (has retries, logs, dependencies)
    @task  
    transform() → Airflow Task Object (has retries, logs, dependencies)
"""

# 9. DECORATOR STACKING IN AIRFLOW
@task.branch  # Multiple decorators can stack
def decide_path():
    """
    This is actually TWO transformations:
    1. @task makes it an Airflow Task
    2. .branch adds branching logic
    """
    if weekend:
        return "skip_processing"
    else:
        return "run_processing"

# 10. THE MENTAL MODEL FOR AIRFLOW DECORATORS

# Think of decorators as "transformers":
# 
# Regular Function  →  @dag  →  Airflow DAG
# Regular Function  →  @task  →  Airflow Task
# Regular Function  →  @task.branch  →  Airflow Branching Task

# PRACTICAL SUMMARY FOR AIRFLOW USERS:

# When you write:
@dag(schedule="0 6 * * *")
def my_pipeline():
    @task
    def sync_data():
        return "synced"
    
    sync_data()

# Airflow sees:
# - A DAG named "my_pipeline" that runs at 6 AM daily
# - A Task named "sync_data" inside that DAG
# - All the configuration, scheduling, and retry logic is handled

# THE KEY INSIGHT:
# Decorators in Airflow transform your simple Python functions
# into complex orchestration components that Airflow can manage.
# 
# You write simple functions.
# Decorators make them Airflow-aware.
# Airflow handles the rest.
```

## The Bottom Line for Airflow Orchestration:

You only need to remember:
- `@dag` = Transform function into an Airflow DAG
- `@task` = Transform function into an Airflow Task
- `@task.branch` = Transform function into a branching Task

That's sufficient for "I'm proficient in Python for Airflow orchestration in the modern data stack."

But now you understand WHY it works!

---

# PART B: LEGACY/FULL AIRFLOW PATTERNS

*For teams still using Airflow for data processing, not just orchestration*

## Part B.0: Astronomer Setup (Detailed)

### B.0.1 Initial Setup

This section covers detailed setup for teams doing complex Airflow work beyond simple orchestration.

**Project Structure:**
```
my-airflow-project/
├── dags/            # Your DAG Python files
├── include/         # SQL files, scripts, config files
├── plugins/         # Custom operators (advanced)
├── tests/           # DAG tests
├── .astro/          # Astronomer config (don't edit)
├── Dockerfile       # For custom dependencies
├── requirements.txt # Python packages
└── packages.txt     # System packages
```

### B.0.2 Adding Python Dependencies

For complex data processing, you might need:
```python
# requirements.txt
pandas==2.0.3
numpy==1.24.3
requests==2.31.0
sqlalchemy==2.0.0
great-expectations==0.17.0
```

## Part B.1: Python Fundamentals for Complex Airflow

### B.1.1 Variables and Basic Data Types

```python
# Variables for configuration
database_name = "analytics_prod"
batch_size = 1000
is_enabled = True
retry_count = 3

# Strings
task_name = "extract_customer_data"
file_path = "/usr/local/airflow/include/data/customers.csv"

# Numbers
timeout_seconds = 300
parallel_tasks = 4

# Booleans
enable_alerts = True
is_production = False
```

### B.1.2 Lists and Dictionaries

```python
# Lists - ordered collections
tables_to_sync = ["customers", "orders", "products"]
email_recipients = ["data-team@company.com", "ops@company.com"]

# Access list items by index (0-based)
first_table = tables_to_sync[0]  # "customers"

# Dictionaries - key-value pairs
default_args = {
    "owner": "data-team",
    "retries": 2,
    "retry_delay": 300,
    "email_on_failure": True
}

# Access dictionary values by key
owner = default_args["owner"]  # "data-team"
```

### B.1.3 String Formatting

```python
# F-strings (preferred)
schema = "prod"
table = "orders"
query = f"SELECT * FROM {schema}.{table} WHERE date = '2024-01-01'"

# Format method
query = "SELECT * FROM {}.{} WHERE date = '{}'".format(schema, table, "2024-01-01")

# Airflow templating
templated_query = "SELECT * FROM orders WHERE date = '{{ ds }}'"
```

### B.1.4 Functions

```python
def get_table_list(schema_name):
    """Return list of tables to process for given schema"""
    if schema_name == "prod":
        return ["customers", "orders", "products"]
    else:
        return ["test_table"]

def build_query(table_name, date_column="created_at", lookback_days=7):
    """Build a SQL query with parameters"""
    query = f"""
    SELECT * 
    FROM {table_name}
    WHERE {date_column} >= CURRENT_DATE - {lookback_days}
    """
    return query

# Using the functions
tables = get_table_list("prod")
my_query = build_query("orders", lookback_days=30)
```

### B.1.5 Imports

```python
# Standard library imports
from datetime import datetime, timedelta
import os

# Airflow imports
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
```

### B.1.6 Error Handling

```python
def check_connection(conn_id):
    try:
        connection = Connection.get_connection_from_secrets(conn_id)
        return True
    except Exception as e:
        print(f"Connection {conn_id} not found: {e}")
        return False

def get_config_value(key, default_value=None):
    try:
        return Variable.get(key)
    except KeyError:
        return default_value
```

## Part B.2: Airflow-Specific Python Patterns

### B.2.1 The DAG Structure

```python
# dags/my_data_pipeline.py
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "data-team",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["alerts@company.com"]
}

@dag(
    dag_id="my_data_pipeline",
    default_args=default_args,
    description="Daily customer data processing",
    schedule="0 6 * * *",  # 6 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["production", "customers"]
)
def my_data_pipeline():
    
    task1 = BashOperator(
        task_id="run_dbt_models",
        bash_command="dbt run --models staging"
    )
    
    task2 = BashOperator(
        task_id="run_tests",
        bash_command="dbt test --models staging"
    )
    
    task1 >> task2

dag_instance = my_data_pipeline()
```

### B.2.2 Working with Dates and Scheduling

```python
from datetime import datetime, timedelta

# Define specific start date
start_date = datetime(2024, 1, 1)

# Calculate dates relative to now
yesterday = datetime.now() - timedelta(days=1)
last_week = datetime.now() - timedelta(weeks=1)
three_hours_ago = datetime.now() - timedelta(hours=3)

# Common schedule intervals (cron expressions)
schedules = {
    "@daily": "Run once a day at midnight",
    "@hourly": "Run once an hour",
    "0 6 * * *": "Run daily at 6 AM",
    "0 */4 * * *": "Run every 4 hours",
    "0 9 * * 1-5": "Run Monday-Friday at 9 AM",
    "0 0 * * 0": "Run weekly on Sunday"
}
```

### B.2.3 Task Dependencies

```python
# Linear dependencies
extract >> transform >> load

# Fan-out pattern
extract >> [transform_customers, transform_orders, transform_products]

# Fan-in pattern
[validate_customers, validate_orders] >> generate_report

# Complex dependencies
extract >> transform
transform >> [load_warehouse, load_lake]
[load_warehouse, load_lake] >> validate
validate >> [send_email, update_dashboard]
```

## Part B.3: Exercises

### Exercise 1: Basic Python Structures
Create variables and data structures for an ETL pipeline configuration.

### Exercise 2: Date Handling
Write Python code to create date ranges and schedules.

### Exercise 3: Build a Simple DAG
Create a DAG with three tasks that run in sequence.

### Exercise 4: Dynamic Tasks
Write a function that creates tasks dynamically based on a list.

### Exercise 5: Error Handling and Branching
Create a DAG with conditional logic and error handling.

## Part B.4: Exercise Solutions

### Solution 1: Basic Python Structures
```python
pipeline_config = {
    "source_db": "transactional_db",
    "target_db": "analytics_warehouse",
    "tables": ["customers", "orders", "products"],
    "schedule": "@daily"
}

def generate_extract_query(table_name, date_filter=None):
    base_query = f"SELECT * FROM {table_name}"
    if date_filter:
        base_query += f" WHERE updated_at >= '{date_filter}'"
    return base_query
```

### Solution 2: Date Handling
```python
from datetime import datetime, timedelta

start_date = datetime(2024, 1, 15)
week_before = start_date - timedelta(days=7)
schedule = "0 15 * * 1"  # Monday 3 PM
```

### Solution 3: Build a Simple DAG
```python
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from datetime import datetime

@dag(
    dag_id="simple_etl_pipeline",
    schedule="0 6 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def simple_etl():
    extract = BashOperator(
        task_id="extract_data",
        bash_command="echo 'Extracting data...'"
    )
    
    transform = BashOperator(
        task_id="transform_data",
        bash_command="echo 'Transforming data...'"
    )
    
    load = BashOperator(
        task_id="load_data",
        bash_command="echo 'Loading data...'"
    )
    
    [extract, transform] >> load

etl_dag = simple_etl()
```

---

## Conclusion

**For Modern Data Stack Users (Part A):**
- 1 week to learn
- Focus on orchestration only
- "I'm proficient in Airflow orchestration for the modern data stack"

**For Legacy Systems (Part B):**
- 2-3 weeks to learn
- Complex Python and data processing
- Consider migrating to modern tools instead

Most readers only need Part A. The future is orchestrating specialized tools, not writing Python ETL.
