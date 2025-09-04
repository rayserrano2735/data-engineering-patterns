# Airflow Python for SQL People: The Essential Guide (Astronomer Edition)

## Introduction

This guide teaches you the minimal Python needed to work with Apache Airflow effectively on the Astronomer platform. As a SQL professional, you already handle data transformation logic - you just need Python for orchestration and configuration.

**Time to proficiency: 2-3 weeks of focused learning**

### Using This Guide with Astronomer

This guide includes Astronomer-specific setup and deployment practices. Astronomer simplifies Airflow management while using the same Python code patterns. Look for **[Astronomer Note]** callouts throughout the guide for platform-specific information.

---

## Part A.6: Astronomer Development Workflow

### A.6.1 Local Development Cycle

**[Windows Users]** Run these commands in PowerShell, Command Prompt, or WSL2:

```bash
# 1. Ensure Docker Desktop is running (Windows)
# Check Docker Desktop system tray icon or open Docker Desktop app

# 2. Start your local environment
astro dev start

# 3. Make changes to your DAGs in the dags/ folder
# Changes auto-refresh in the UI
# Use any Windows editor (VS Code, Notepad++, etc.)

# 4. Test your DAG
astro dev pytest  # Run all tests
astro dev parse   # Check for DAG errors

# 5. View logs
astro dev logs    # See all logs
astro dev logs scheduler  # Just scheduler logs

# 6. Stop when done
astro dev stop

# 7. If you encounter issues on Windows:
astro dev kill    # Force stop all containers
astro dev start   # Start fresh
```

**[Windows VS Code Tip]** Install these extensions for better development:
- Python extension
- Docker extension  
- WSL extension (if using WSL2)
- Edit DAG files with Python syntax highlighting

### A.6.2 Adding Dependencies

```python
# requirements.txt - Python packages
apache-airflow-providers-postgres==5.10.0
apache-airflow-providers-snowflake==5.3.0
apache-airflow-providers-amazon==8.16.0
dbt-core==1.7.0
dbt-postgres==1.7.0
pandas==2.0.3  # Only if needed

# packages.txt - System packages (if needed)
git
vim
```

### A.6.3 Testing DAGs

Create tests in the `tests/` folder:

```python
# tests/test_dags.py
import pytest
from airflow.models import DagBag

def test_dag_loaded():
    """Test that DAGs load without errors"""
    dag_bag = DagBag(include_examples=False)
    assert len(dag_bag.import_errors) == 0

def test_warehouse_refresh_dag():
    """Test specific DAG structure"""
    dag_bag = DagBag(include_examples=False)
    dag = dag_bag.get_dag("daily_warehouse_refresh")
    
    assert dag is not None
    assert dag.schedule_interval == "0 2 * * *"
    assert len(dag.tasks) == 5
```

Run tests: `astro dev pytest`

### A.6.4 Deployment to Astronomer Cloud

```bash
# Login to Astronomer
astro login

# List your deployments
astro deployment list

# Deploy to production
astro deploy --deployment-id <your-deployment-id>

# Set production variables
astro deployment variable create --deployment-id <id> \
  --key pipeline_config \
  --value '{"schema": "prod", "tables": ["customers", "orders"]}'

# Set production connections (or use UI)
astro deployment connection create --deployment-id <id> \
  --conn-id warehouse \
  --conn-type postgres \
  --host your-db.amazonaws.com \
  --schema analytics \
  --login your_user \
  --password your_password \
  --port 5432
```

### A.6.5 Astronomer Best Practices

1. **File Organization**:
   ```
   # Windows: Your project might be at C:\Users\YourName\projects\my-airflow-project
   # But in DAG code, always reference Linux container paths:
   
   dags/
   ├── pipelines/           # Main pipeline DAGs
   ├── maintenance/         # Cleanup, backup DAGs
   └── experimental/        # Test DAGs (exclude from prod)
   
   include/
   ├── sql/                 # SQL queries
   ├── dbt/                 # dbt project
   └── scripts/             # Python/Bash scripts
   ```

2. **Environment Management**:
   ```python
   # Use environment variables for different environments
   import os
   
   ENV = os.getenv("ENVIRONMENT", "dev")
   
   if ENV == "prod":
       schedule = "@daily"
       email_on_failure = True
   else:
       schedule = None  # Manual trigger in dev
       email_on_failure = False
   ```

3. **Resource Optimization**:
   ```python
   # Use task pools to limit concurrent tasks
   heavy_task = PostgresOperator(
       task_id="heavy_query",
       pool="database_pool",  # Configure in Astronomer UI
       pool_slots=2,  # Uses 2 slots from pool
       ...
   )
   ```

4. **Windows-Specific Best Practices**:
   - **Line Endings**: Configure Git to use LF endings:
     ```bash
     git config --global core.autocrlf true
     ```
   - **File Paths**: Always use forward slashes in DAG code
   - **Testing**: Test locally with Docker Desktop before deploying
   - **Performance**: Allocate sufficient RAM to Docker Desktop (Settings > Resources)
   - **File Watching**: If DAGs don't refresh, manually restart: `astro dev restart`

---

## Part 0: Astronomer Setup

### 0.1 Initial Setup

**[Astronomer Note]** Before writing any Python, set up your Astronomer development environment.

**[Windows Users]** Astronomer requires Docker Desktop and WSL2 (Windows Subsystem for Linux):

1. **Install Prerequisites for Windows:**
   - Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
   - Enable WSL2 backend in Docker Desktop settings
   - Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install)
   - Restart your computer after installations

2. **Install Astronomer CLI:**

   **Windows (PowerShell as Administrator):**
   ```powershell
   # Download the latest Astronomer CLI executable
   Invoke-WebRequest -Uri https://github.com/astronomer/astro-cli/releases/latest/download/astro_1.20.0_windows_amd64.zip -OutFile astro.zip
   
   # Extract and install
   Expand-Archive -Path astro.zip -DestinationPath .
   Move-Item astro.exe "C:\Program Files\"
   
   # Add to PATH (or do this manually via System Properties)
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files", [EnvironmentVariableTarget]::Machine)
   
   # Verify installation (open new PowerShell)
   astro version
   ```
   
   **Alternative: Using WSL2 Terminal (Recommended):**
   ```bash
   # In WSL2 Ubuntu terminal
   curl -sSL install.astronomer.io | sudo bash -s
   ```

3. **Create Project and Start Airflow:**

   **Windows (PowerShell or Command Prompt):**
   ```powershell
   # Create a new Astronomer project
   mkdir my-airflow-project
   cd my-airflow-project
   astro dev init
   
   # Start local Airflow (Docker Desktop must be running)
   astro dev start
   ```

   **Windows (WSL2 Terminal):**
   ```bash
   # Navigate to Windows filesystem if needed
   cd /mnt/c/Users/YourUsername/projects
   mkdir my-airflow-project
   cd my-airflow-project
   astro dev init
   astro dev start
   ```

Your project structure will look like this:
```
my-airflow-project/
├── dags/            # Your DAG Python files go here
├── include/         # SQL files, scripts, config files
├── plugins/         # Custom operators (advanced)
├── tests/           # DAG tests
├── .astro/          # Astronomer config (don't edit)
├── Dockerfile       # For custom dependencies
├── requirements.txt # Python packages
└── packages.txt     # System packages
```

**[Windows Path Note]** When working on Windows:
- Use forward slashes `/` in Python code (works on both Windows and Linux)
- Astronomer runs in Docker containers (Linux), so paths in your DAGs should use Linux-style paths
- Your local Windows paths (like `C:\Users\...`) are only for editing files, not for DAG code

### 0.2 Astronomer Web UI

Access your local Airflow at `http://localhost:8080` with:
- Username: `admin`
- Password: `admin`

**[Windows Tip]** If localhost doesn't work, try `http://127.0.0.1:8080` or check Docker Desktop to ensure containers are running.

### 0.3 Adding Python Dependencies

When you need additional Python packages:

```python
# requirements.txt
dbt-core==1.7.0
dbt-postgres==1.7.0
pandas==2.0.3  # If needed for specific tasks
```

Then restart:
```bash
# Windows PowerShell/Command Prompt or WSL2
astro dev restart
```

### 0.4 Windows Development Tips

**Recommended Windows Setup:**
1. **Code Editor**: Use VS Code with WSL2 Remote extension
2. **Terminal**: Use either:
   - WSL2 Terminal (recommended) for Linux-like experience
   - PowerShell/Windows Terminal for native Windows
3. **File Editing**: Edit DAG files with any Windows editor (VS Code, Notepad++, etc.)
4. **Running Commands**: Use PowerShell, Command Prompt, or WSL2 terminal

**Common Windows Issues and Solutions:**
- **Docker not running**: Ensure Docker Desktop is started before `astro dev start`
- **Permission errors**: Run PowerShell as Administrator for Astro CLI installation
- **Line endings**: Configure Git and your editor to use LF line endings (not CRLF)
- **Path issues**: Use forward slashes in DAG code: `/usr/local/airflow/include/`

---

## Part 1: Python Fundamentals for Airflow

### 1.1 Variables and Basic Data Types

In Airflow, you'll use variables to store configuration values, connection strings, and task parameters.

```python
# Variables (think of these like SQL session variables)
database_name = "analytics_prod"
batch_size = 1000
is_enabled = True
retry_count = 3

# Strings - used for task IDs, SQL queries, file paths
task_name = "extract_customer_data"
file_path = "/data/exports/customers.csv"

# Numbers - for scheduling, retries, timeouts
timeout_seconds = 300
parallel_tasks = 4

# Booleans - for feature flags and conditions
enable_alerts = True
is_production = False
```

### 1.2 Lists and Dictionaries

Lists and dictionaries are crucial for Airflow configuration.

```python
# Lists - like SQL arrays, ordered collections
tables_to_sync = ["customers", "orders", "products"]
email_recipients = ["data-team@company.com", "ops@company.com"]

# Access list items by index (0-based)
first_table = tables_to_sync[0]  # "customers"

# Dictionaries - key-value pairs, like JSON
default_args = {
    "owner": "data-team",
    "retries": 2,
    "retry_delay": 300,  # seconds
    "email_on_failure": True
}

# Access dictionary values by key
owner = default_args["owner"]  # "data-team"
```

### 1.3 String Formatting

Essential for building dynamic SQL queries and task names.

```python
# F-strings (preferred, Python 3.6+)
schema = "prod"
table = "orders"
query = f"SELECT * FROM {schema}.{table} WHERE date = '2024-01-01'"

# Format method (older but still common)
query = "SELECT * FROM {}.{} WHERE date = '{}'".format(schema, table, "2024-01-01")

# For Airflow templating (Jinja2 style)
templated_query = "SELECT * FROM orders WHERE date = '{{ ds }}'"

# [Windows Note] Always use forward slashes in paths, even on Windows
file_path = "/usr/local/airflow/include/data/file.csv"  # Correct
# NOT: "C:\\Users\\..."  or  "C:/Users/..."  # Wrong for DAG code
```

### 1.4 Functions

Functions organize your DAG logic into reusable pieces.

```python
# Basic function
def get_table_list(schema_name):
    """Return list of tables to process for given schema"""
    if schema_name == "prod":
        return ["customers", "orders", "products"]
    else:
        return ["test_table"]

# Function with multiple parameters
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

### 1.5 Imports

Importing gives you access to Airflow operators and Python libraries.

```python
# Standard library imports
from datetime import datetime, timedelta
import os

# Airflow imports
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator
```

### 1.6 Error Handling

Handle potential failures gracefully.

```python
# Try-except blocks
def check_connection(conn_id):
    try:
        # Attempt to get connection
        connection = Connection.get_connection_from_secrets(conn_id)
        return True
    except Exception as e:
        print(f"Connection {conn_id} not found: {e}")
        return False

# With default values
def get_config_value(key, default_value=None):
    try:
        return Variable.get(key)
    except KeyError:
        return default_value
```

---

## Part 2: Airflow-Specific Python Patterns

### 2.1 The DAG Structure

**[Astronomer Note]** All DAG files must be placed in the `dags/` folder of your Astronomer project.

Every Airflow pipeline follows this basic pattern:

```python
# dags/my_data_pipeline.py  <- File location in Astronomer project

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments for all tasks
default_args = {
    "owner": "data-team",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["alerts@company.com"]
}

# Define the DAG
@dag(
    dag_id="my_data_pipeline",
    default_args=default_args,
    description="Daily customer data processing",
    schedule="0 6 * * *",  # 6 AM daily (cron expression)
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["production", "customers"]
)
def my_data_pipeline():
    
    # Define tasks
    task1 = BashOperator(
        task_id="run_dbt_models",
        bash_command="dbt run --models staging"
    )
    
    task2 = BashOperator(
        task_id="run_tests",
        bash_command="dbt test --models staging"
    )
    
    # Set dependencies
    task1 >> task2  # task2 runs after task1

# Instantiate the DAG
dag_instance = my_data_pipeline()
```

**[Astronomer Note]** After saving this file in `dags/`, run `astro dev pytest` to validate your DAG has no syntax errors.

### 2.2 Working with Dates and Scheduling

Airflow heavily uses datetime objects for scheduling.

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
    "@hourly": "Run once an hour at the beginning of the hour",
    "0 6 * * *": "Run daily at 6 AM",
    "0 */4 * * *": "Run every 4 hours",
    "0 9 * * 1-5": "Run Monday-Friday at 9 AM",
    "0 0 * * 0": "Run weekly on Sunday at midnight"
}
```

### 2.3 Task Dependencies

Define the order of task execution.

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

### 2.4 Dynamic Task Generation

Create tasks programmatically based on configuration.

```python
from airflow.operators.postgres import PostgresOperator

@dag(
    dag_id="dynamic_table_sync",
    start_date=datetime(2024, 1, 1),
    schedule="@daily"
)
def dynamic_sync():
    
    tables = ["customers", "orders", "products", "inventory"]
    
    # Create a task for each table
    for table_name in tables:
        PostgresOperator(
            task_id=f"sync_{table_name}",
            sql=f"CALL sync_procedure('{table_name}', '{{{{ ds }}}}')",
            postgres_conn_id="warehouse"
        )

# Or using list comprehension
def dynamic_sync_v2():
    tables = ["customers", "orders", "products"]
    
    sync_tasks = [
        PostgresOperator(
            task_id=f"sync_{table}",
            sql=f"REFRESH MATERIALIZED VIEW {table}_mv",
            postgres_conn_id="warehouse"
        )
        for table in tables
    ]
    
    # Chain them together
    for i in range(len(sync_tasks) - 1):
        sync_tasks[i] >> sync_tasks[i + 1]
```

### 2.5 Using Airflow Variables and Connections

**[Astronomer Note]** In Astronomer, connections and variables can be set via:
1. Local development: Airflow UI at localhost:8080
2. Astronomer Cloud: Environment configuration in Astronomer UI
3. Astronomer CLI: `astro deployment variable create` or `astro deployment connection create`

```python
from airflow.models import Variable
from airflow.hooks.base import BaseHook

# Get Airflow Variables (configured in UI or Astronomer)
environment = Variable.get("environment", default_var="dev")
batch_size = Variable.get("batch_size", default_var=1000, deserialize_json=False)

# Get JSON variable
config = Variable.get("pipeline_config", deserialize_json=True)
# Returns: {"schema": "prod", "tables": ["customers", "orders"]}

# Use in your DAG
@dag(dag_id="configurable_pipeline", start_date=datetime(2024, 1, 1))
def configurable_pipeline():
    
    config = Variable.get("pipeline_config", deserialize_json=True)
    
    for table in config["tables"]:
        PostgresOperator(
            task_id=f"process_{table}",
            sql=f"SELECT * FROM {config['schema']}.{table}",
            postgres_conn_id="warehouse"  # Connection configured in Astronomer
        )
```

**[Astronomer Tip]** For production, set connections via Astronomer Cloud UI or use environment variables:
```bash
# In Astronomer deployment
AIRFLOW_CONN_WAREHOUSE='postgresql://user:pass@host:5432/db'
```

---

## Part 3: Common Airflow Operators

### 3.1 SQL Operators

**[Astronomer Note]** SQL operators require provider packages. Add to `requirements.txt`:
```
apache-airflow-providers-postgres==5.10.0
apache-airflow-providers-snowflake==5.3.0
```

```python
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

# PostgreSQL operator
run_query = PostgresOperator(
    task_id="update_metrics",
    postgres_conn_id="postgres_default",  # Configure in Astronomer UI
    sql="""
        INSERT INTO daily_metrics
        SELECT DATE '{{ ds }}', COUNT(*), SUM(amount)
        FROM orders
        WHERE order_date = '{{ ds }}'
    """
)

# Snowflake operator
snowflake_task = SnowflakeOperator(
    task_id="refresh_views",
    snowflake_conn_id="snowflake_default",  # Configure in Astronomer UI
    sql="CALL refresh_all_views('{{ ds }}')",
    warehouse="COMPUTE_WH",
    database="ANALYTICS",
    schema="PUBLIC"
)
```

**[Astronomer Tip]** You can also store SQL files in the `include/` folder:
```python
# include/sql/update_metrics.sql - Store SQL file here
# Then in your DAG:
PostgresOperator(
    task_id="update_metrics",
    postgres_conn_id="warehouse",
    sql="/usr/local/airflow/include/sql/update_metrics.sql"
)
```

### 3.2 Bash Operators

**[Astronomer Note]** For dbt, you have two options:
1. Install dbt in your Docker image (add to `requirements.txt`)
2. Use the Astronomer Cosmos provider for native dbt integration

**[Windows Note]** Bash commands run inside Linux containers, not Windows. Use Linux commands and paths.

```python
from airflow.operators.bash import BashOperator

# Option 1: Run dbt via Bash (add dbt-core to requirements.txt)
run_dbt = BashOperator(
    task_id="run_dbt_models",
    # Use Linux paths and commands, even on Windows development
    bash_command="cd /usr/local/airflow/include/dbt && dbt run --profiles-dir . --models +customers"
)

# Option 2: Using Astronomer Cosmos (recommended for dbt)
# Add to requirements.txt: astronomer-cosmos
from cosmos import DbtDag, ProfileConfig, ProjectConfig

dbt_dag = DbtDag(
    project_config=ProjectConfig("/usr/local/airflow/include/dbt"),
    profile_config=ProfileConfig(
        profile_name="my_project",
        target_name="prod",
        profiles_yml_filepath="/usr/local/airflow/include/dbt/profiles.yml"
    ),
    dag_id="dbt_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily"
)

# Run Python script
run_script = BashOperator(
    task_id="run_python_script",
    # Linux path, not Windows path
    bash_command="python /usr/local/airflow/include/scripts/process_data.py --date {{ ds }}"
)

# Multiple commands (Linux shell syntax)
complex_bash = BashOperator(
    task_id="complex_task",
    bash_command="""
        echo "Starting process for {{ ds }}"
        export DATE={{ ds }}
        python /usr/local/airflow/include/scripts/extract.py
        python /usr/local/airflow/include/scripts/load.py
        echo "Process complete"
    """
)

# [Windows Warning] These won't work in BashOperator:
# bash_command="dir"  # Windows command - use 'ls' instead
# bash_command="type file.txt"  # Windows - use 'cat file.txt' instead
# bash_command="C:\\scripts\\run.bat"  # Windows path - won't work
```

### 3.3 Python Operators (using @task decorator)

**[Astronomer Note]** The Astro Python SDK provides additional decorators for data operations, but standard Airflow @task works perfectly for most cases.

```python
from airflow.decorators import task

@task
def extract_data(source_table: str):
    """Python function task"""
    print(f"Extracting from {source_table}")
    # Your Python code here
    return {"rows": 1000, "table": source_table}

@task
def transform_data(extract_result: dict):
    """Transform the extracted data"""
    row_count = extract_result["rows"]
    # Process data
    return {"transformed_rows": row_count * 0.95}

# In your DAG
@dag(dag_id="python_tasks", start_date=datetime(2024, 1, 1))
def python_pipeline():
    extract_result = extract_data("customers")
    transform_result = transform_data(extract_result)

# [Astronomer Optional] Using Astro SDK for dataframe operations
# Add to requirements.txt: astronomer-providers[amazon]
from astro import sql as aql
from astro.files import File
from astro.table import Table

@aql.dataframe  # Astro SDK decorator
def transform_dataframe(df):
    """Work directly with pandas dataframes"""
    return df[df['amount'] > 100]

# Load CSV to database using Astro SDK
load_file = aql.load_file(
    File("/usr/local/airflow/include/data/customers.csv"),
    Table(name="customers", conn_id="warehouse")
)
```

### 3.4 Sensor Operators

**[Astronomer Note]** Sensors are great for waiting on external dependencies. Be mindful of slot usage in Astronomer Cloud.

```python
from airflow.sensors.filesystem import FileSensor
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

# Wait for a file (file would be in include/ folder for local testing)
wait_for_file = FileSensor(
    task_id="wait_for_data_file",
    filepath="/usr/local/airflow/include/data/{{ ds }}/customers.csv",
    fs_conn_id="fs_default",
    poke_interval=300,  # Check every 5 minutes
    timeout=3600,  # Fail after 1 hour
    mode="poke"  # Use "reschedule" mode in production to free up slots
)

# Wait for S3 file
wait_for_s3 = S3KeySensor(
    task_id="wait_for_s3_file",
    bucket_name="data-lake",
    bucket_key="raw/{{ ds }}/orders.parquet",
    aws_conn_id="aws_default",  # Configure in Astronomer UI
    timeout=1800,
    poke_interval=60,
    mode="reschedule"  # Recommended for Astronomer to save resources
)
```

---

## Part 4: Practical DAG Examples

### Example 1: Daily Data Warehouse Refresh

**[Astronomer Note]** Save this as `dags/daily_warehouse_refresh.py` in your Astronomer project.

```python
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta

@dag(
    dag_id="daily_warehouse_refresh",
    schedule="0 2 * * *",  # 2 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        "owner": "data-team",
        "retries": 2,
        "retry_delay": timedelta(minutes=10)
    },
    tags=["production", "warehouse"]
)
def warehouse_refresh():
    
    # Run dbt models (assuming dbt is in include/dbt/)
    run_staging = BashOperator(
        task_id="dbt_run_staging",
        bash_command="cd /usr/local/airflow/include/dbt && dbt run --models staging --profiles-dir ."
    )
    
    run_marts = BashOperator(
        task_id="dbt_run_marts", 
        bash_command="cd /usr/local/airflow/include/dbt && dbt run --models marts --profiles-dir ."
    )
    
    # Run data quality tests
    test_staging = BashOperator(
        task_id="dbt_test_staging",
        bash_command="cd /usr/local/airflow/include/dbt && dbt test --models staging --profiles-dir ."
    )
    
    # Refresh materialized views
    refresh_views = PostgresOperator(
        task_id="refresh_materialized_views",
        postgres_conn_id="warehouse",  # Configure this connection in Astronomer UI
        sql="""
            REFRESH MATERIALIZED VIEW CONCURRENTLY customer_summary_mv;
            REFRESH MATERIALIZED VIEW CONCURRENTLY daily_revenue_mv;
            REFRESH MATERIALIZED VIEW CONCURRENTLY product_metrics_mv;
        """
    )
    
    # Send completion email
    send_notification = EmailOperator(
        task_id="send_completion_email",
        to=["data-team@company.com"],
        subject="Warehouse Refresh Complete - {{ ds }}",
        html_content="""
            <h3>Daily Warehouse Refresh Completed</h3>
            <p>Date: {{ ds }}</p>
            <p>All models and views have been refreshed successfully.</p>
        """
    )
    
    # Define dependencies
    run_staging >> test_staging >> run_marts >> refresh_views >> send_notification

warehouse_dag = warehouse_refresh()
```

### Example 2: Multi-Source Data Integration

```python
from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime, timedelta

@dag(
    dag_id="multi_source_integration",
    schedule="0 */6 * * *",  # Every 6 hours
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["integration", "api"]
)
def multi_source_pipeline():
    
    # Check API availability
    check_api = HttpSensor(
        task_id="check_api_availability",
        http_conn_id="api_default",
        endpoint="health",
        poke_interval=60,
        timeout=300
    )
    
    @task
    def fetch_api_data():
        """Fetch data from API"""
        # In practice, you'd use requests or an API operator
        print("Fetching data from API...")
        return {"records": 500}
    
    @task
    def fetch_database_data():
        """Get matching records from database"""
        # Would normally query database
        print("Fetching database records...")
        return {"records": 480}
    
    @task(multiple_outputs=True)
    def compare_sources(api_data, db_data):
        """Compare data from both sources"""
        api_count = api_data["records"]
        db_count = db_data["records"]
        
        return {
            "missing_records": api_count - db_count,
            "sync_needed": api_count != db_count
        }
    
    @task.branch
    def check_sync_needed(comparison_result):
        """Decide whether to sync"""
        if comparison_result["sync_needed"]:
            return "sync_data"
        return "skip_sync"
    
    sync_data = PostgresOperator(
        task_id="sync_data",
        postgres_conn_id="warehouse",
        sql="CALL sync_api_data('{{ ds }}')"
    )
    
    @task
    def skip_sync():
        """Skip sync if not needed"""
        print("Data already in sync")
    
    # Build pipeline
    api_data = fetch_api_data()
    db_data = fetch_database_data()
    comparison = compare_sources(api_data, db_data)
    branch = check_sync_needed(comparison)
    
    # Dependencies
    check_api >> [api_data, db_data]
    [api_data, db_data] >> comparison >> branch
    branch >> [sync_data, skip_sync()]

pipeline = multi_source_pipeline()
```

### Example 3: Dynamic Table Processing

```python
from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
from datetime import datetime, timedelta

@dag(
    dag_id="dynamic_table_processor",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def dynamic_processor():
    
    @task
    def get_tables_to_process():
        """Get list of tables from Airflow Variable"""
        config = Variable.get("table_config", deserialize_json=True)
        # Example config: {"tables": ["customers", "orders"], "schema": "prod"}
        return config
    
    @task
    def create_processing_tasks(config):
        """Dynamically create tasks for each table"""
        tasks = []
        for table in config["tables"]:
            task_id = f"process_{table}"
            tasks.append({
                "task_id": task_id,
                "table": table,
                "schema": config["schema"]
            })
        return tasks
    
    @task
    def process_table(task_config):
        """Process individual table"""
        print(f"Processing {task_config['schema']}.{task_config['table']}")
        # Your processing logic here
        return f"Processed {task_config['table']}"
    
    @task
    def combine_results(results):
        """Combine all processing results"""
        print(f"All tables processed: {len(results)} tables")
        return {"status": "success", "tables_processed": len(results)}
    
    # Build dynamic pipeline
    config = get_tables_to_process()
    task_configs = create_processing_tasks(config)
    
    # Process each table (dynamic task mapping)
    processing_results = process_table.expand(task_config=task_configs)
    
    # Combine results
    final_result = combine_results(processing_results)

dynamic_dag = dynamic_processor()
```

---

## Part 5: Exercises

### Exercise 1: Basic Python Structures
Create variables and data structures for an ETL pipeline configuration:
1. Create a dictionary called `pipeline_config` with keys for "source_db", "target_db", "tables", and "schedule"
2. Add a list of 3 table names to the "tables" key
3. Write a function that takes a table name and returns a SQL query string

### Exercise 2: Date Handling
Write Python code to:
1. Create a start_date for January 15, 2024
2. Calculate a date 7 days before the start_date
3. Create a schedule that runs every Monday at 3 PM

### Exercise 3: Build a Simple DAG
Create a DAG that:
1. Runs daily at 6 AM
2. Has three tasks: extract, transform, load
3. Extract and transform run in parallel, both must complete before load

### Exercise 4: Dynamic Tasks
Write a function that:
1. Takes a list of schemas: ["raw", "staging", "prod"]
2. Creates a PostgresOperator task for each schema that runs `VACUUM ANALYZE` on all tables
3. Sets up the tasks to run sequentially

### Exercise 5: Error Handling and Branching
Create a DAG with:
1. A task that checks row count in a table
2. Branches to either "send_alert" if count is 0 or "continue_processing" if count > 0
3. Includes proper error handling

### Exercise 6: Configuration-Driven Pipeline
Build a DAG that:
1. Reads table names from an Airflow Variable
2. For each table, creates tasks to: validate data, run transformations, update metadata
3. All validation tasks must complete before any transformation starts

---

## Appendix: Exercise Solutions

### Solution 1: Basic Python Structures

```python
# Create the configuration dictionary
pipeline_config = {
    "source_db": "transactional_db",
    "target_db": "analytics_warehouse",
    "tables": ["customers", "orders", "products"],
    "schedule": "@daily"
}

# Function to generate SQL query
def generate_extract_query(table_name, date_filter=None):
    """Generate extraction query for a given table"""
    base_query = f"SELECT * FROM {table_name}"
    
    if date_filter:
        base_query += f" WHERE updated_at >= '{date_filter}'"
    
    return base_query

# Usage examples
query1 = generate_extract_query("customers")
query2 = generate_extract_query("orders", "2024-01-01")
```

### Solution 2: Date Handling

```python
from datetime import datetime, timedelta

# 1. Create start_date
start_date = datetime(2024, 1, 15)

# 2. Calculate 7 days before
week_before = start_date - timedelta(days=7)
print(f"Week before: {week_before}")  # 2024-01-08

# 3. Schedule for Monday 3 PM
schedule = "0 15 * * 1"  # cron expression: minute hour day month dayofweek
# Or if you prefer explicit:
monday_3pm = "0 15 * * MON"
```

### Solution 3: Build a Simple DAG

```python
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from datetime import datetime

@dag(
    dag_id="simple_etl_pipeline",
    schedule="0 6 * * *",  # Daily at 6 AM
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["exercise", "etl"]
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
    
    # Extract and transform run in parallel, both before load
    [extract, transform] >> load

etl_dag = simple_etl()
```

### Solution 4: Dynamic Tasks

```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

def create_vacuum_tasks(schemas):
    """Create VACUUM ANALYZE tasks for each schema"""
    tasks = []
    
    for schema in schemas:
        task = PostgresOperator(
            task_id=f"vacuum_{schema}",
            postgres_conn_id="warehouse",
            sql=f"""
                DO $$
                DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN 
                        SELECT tablename 
                        FROM pg_tables 
                        WHERE schemaname = '{schema}'
                    LOOP
                        EXECUTE 'VACUUM ANALYZE ' || '{schema}.' || r.tablename;
                    END LOOP;
                END $$;
            """
        )
        tasks.append(task)
    
    # Set up sequential execution
    for i in range(len(tasks) - 1):
        tasks[i] >> tasks[i + 1]
    
    return tasks

# Usage in a DAG
@dag(dag_id="vacuum_pipeline", start_date=datetime(2024, 1, 1))
def vacuum_dag():
    schemas = ["raw", "staging", "prod"]
    vacuum_tasks = create_vacuum_tasks(schemas)

dag_instance = vacuum_dag()
```

### Solution 5: Error Handling and Branching

```python
from airflow.decorators import dag, task
from airflow.operators.email import EmailOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

@dag(
    dag_id="branching_pipeline",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def branching_dag():
    
    @task
    def check_row_count():
        """Check row count with error handling"""
        try:
            # Get connection
            pg_hook = PostgresHook(postgres_conn_id="warehouse")
            
            # Execute query
            result = pg_hook.get_first(
                "SELECT COUNT(*) FROM staging.daily_data WHERE date = CURRENT_DATE"
            )
            
            row_count = result[0] if result else 0
            print(f"Row count: {row_count}")
            
            return {"count": row_count, "status": "success"}
            
        except Exception as e:
            print(f"Error checking row count: {e}")
            return {"count": 0, "status": "error", "error_message": str(e)}
    
    @task.branch
    def decide_next_step(count_result):
        """Decide whether to alert or continue"""
        if count_result["status"] == "error" or count_result["count"] == 0:
            return "send_alert"
        else:
            return "continue_processing"
    
    send_alert = EmailOperator(
        task_id="send_alert",
        to=["data-team@company.com"],
        subject="Data Pipeline Alert - No Data Found",
        html_content="""
            <h3>Alert: No data found in staging table</h3>
            <p>Please check the source systems.</p>
        """
    )
    
    @task
    def continue_processing():
        """Continue with normal processing"""
        print("Data found, continuing with processing...")
        # Add processing logic here
        return "Processing completed"
    
    # Build pipeline
    count_result = check_row_count()
    branch_decision = decide_next_step(count_result)
    
    # Set up branching
    branch_decision >> [send_alert, continue_processing()]

branch_dag = branching_dag()
```

### Solution 6: Configuration-Driven Pipeline

```python
from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

@dag(
    dag_id="config_driven_pipeline",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def config_pipeline():
    
    @task
    def get_table_config():
        """Read table configuration from Airflow Variable"""
        # Expects JSON like: {"tables": ["customers", "orders", "products"]}
        config = Variable.get("table_processing_config", deserialize_json=True)
        return config["tables"]
    
    @task
    def validate_table(table_name: str):
        """Validate data quality for a table"""
        print(f"Validating {table_name}")
        # Add actual validation logic here
        return {"table": table_name, "validation": "passed"}
    
    @task 
    def transform_table(table_name: str, validation_result: dict):
        """Run transformations after validation passes"""
        if validation_result["validation"] == "passed":
            print(f"Transforming {table_name}")
            # Add transformation logic
            return {"table": table_name, "transformed": True}
        else:
            print(f"Skipping transformation for {table_name} - validation failed")
            return {"table": table_name, "transformed": False}
    
    @task
    def update_metadata(table_name: str, transform_result: dict):
        """Update metadata after transformation"""
        if transform_result["transformed"]:
            print(f"Updating metadata for {table_name}")
            # Add metadata update logic
            return f"Metadata updated for {table_name}"
        return f"Metadata not updated for {table_name}"
    
    @task
    def wait_for_validations(validation_results):
        """Gate task to ensure all validations complete"""
        failed = [r for r in validation_results if r["validation"] != "passed"]
        if failed:
            print(f"Warning: {len(failed)} tables failed validation")
        return "All validations completed"
    
    # Get configuration
    tables = get_table_config()
    
    # Create validation tasks for all tables
    validation_results = validate_table.expand(table_name=tables)
    
    # Wait for all validations
    validation_gate = wait_for_validations(validation_results)
    
    # After validation gate, run transformations
    # Note: We need to pair tables with validation results
    @task
    def create_transform_pairs(tables, validation_results):
        """Pair tables with their validation results"""
        pairs = []
        for table, validation in zip(tables, validation_results):
            pairs.append({"table": table, "validation": validation})
        return pairs
    
    transform_pairs = create_transform_pairs(tables, validation_results)
    
    # Run transformations
    @task
    def run_transform_pipeline(pair):
        """Run transform and metadata update for a table"""
        transform_result = transform_table(pair["table"], pair["validation"])
        metadata_result = update_metadata(pair["table"], transform_result)
        return metadata_result
    
    # Set up dependencies
    validation_results >> validation_gate
    validation_gate >> transform_pairs
    
    # Run transformation pipeline for each table
    final_results = run_transform_pipeline.expand(pair=transform_pairs)

config_dag = config_pipeline()
```

---

## Quick Reference Card

### Essential Imports
```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
```

### Common Patterns
```python
# Get current date in Airflow template
"{{ ds }}"  # Format: YYYY-MM-DD

# Get Airflow Variable
var = Variable.get("key", default_var="default")

# Task dependencies
task1 >> task2  # task2 after task1
[task1, task2] >> task3  # task3 after both

# Cron expressions
"@daily"  # Midnight daily
"0 6 * * *"  # 6 AM daily
"0 */4 * * *"  # Every 4 hours
```

### Astronomer CLI Commands
```bash
# Windows: Run in PowerShell, Command Prompt, or WSL2
astro dev init      # Initialize project
astro dev start     # Start local Airflow (Docker Desktop must be running)
astro dev stop      # Stop local Airflow  
astro dev restart   # Restart after changes
astro dev pytest    # Run tests
astro dev parse     # Validate DAGs
astro deploy        # Deploy to cloud
astro dev kill      # Force stop (useful on Windows if containers hang)
```

### Windows Development Quick Tips
```python
# In your DAG files:
# ✅ CORRECT - Linux container paths
file_path = "/usr/local/airflow/include/data/file.csv"
bash_command = "python /usr/local/airflow/include/script.py"

# ❌ WRONG - Windows paths won't work in DAGs
file_path = "C:\\Users\\YourName\\data\\file.csv"
bash_command = "python C:/projects/script.py"

# Remember: You edit files in Windows, but Airflow runs in Linux containers
```

### Debugging Tips
1. Use `print()` statements liberally - they appear in Airflow logs
2. Test Python functions separately before adding to DAG
3. Use Airflow's "Test" button to run individual tasks
4. Check connection IDs match exactly (case-sensitive)
5. Verify Variable names are correct in the Airflow UI
6. **[Astronomer]** Check logs with `astro dev logs`
7. **[Astronomer]** Validate DAGs with `astro dev parse` before deploying
8. **[Windows]** Ensure Docker Desktop is running before any `astro dev` commands
9. **[Windows]** If file changes don't appear, run `astro dev restart`
10. **[Windows]** Use forward slashes `/` in all DAG paths, not backslashes `\`

---

## Next Steps

1. **Week 1**: Master Part 1 (Python Fundamentals) - practice daily
2. **Week 2**: Work through Part 2 (Airflow Patterns) and Part 3 (Operators)
3. **Week 3**: Build the example DAGs and complete all exercises
4. **Ongoing**: Modify existing DAGs at work, gradually building complexity

**Astronomer-Specific Next Steps:**
1. Set up your local Astronomer environment (`astro dev init`)
2. Try the example DAGs in your local environment
3. Practice the deployment workflow with a test deployment
4. Explore the Astronomer Registry for example DAGs

Remember: You don't need to be a Python expert. Focus on these patterns, and you'll handle 95% of Airflow work. The rest you can learn as needed.
