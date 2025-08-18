# Filename: airflow-patterns/essential_airflow_patterns.py
"""
Essential Airflow Patterns for Data Engineering Interviews
Co-authored by Ray & Aitana (Intelligence²)
Covers 90% of what they actually ask
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup

# ============================================
# PATTERN 1: BASIC DAG STRUCTURE (They always ask this)
# ============================================

# Default arguments (memorize this structure)
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

# Basic DAG definition
dag = DAG(
    'interview_example_dag',
    default_args=default_args,
    description='Data pipeline for ETL',
    schedule_interval='@daily',  # or '0 2 * * *' for cron
    catchup=False,
    tags=['production', 'etl']
)

# ============================================
# PATTERN 2: PYTHON OPERATOR (Most common)
# ============================================

def extract_data(**context):
    """Extract data from source"""
    # Access execution date (they love testing this)
    execution_date = context['execution_date']
    print(f"Running for date: {execution_date}")
    
    # Return data to pass between tasks
    return {'record_count': 1000, 'status': 'success'}

def transform_data(**context):
    """Transform the extracted data"""
    # Pull data from previous task (XCom)
    ti = context['task_instance']
    extracted_data = ti.xcom_pull(task_ids='extract_task')
    
    record_count = extracted_data['record_count']
    transformed_count = record_count * 0.95  # Some filtering
    
    return {'transformed_count': transformed_count}

# Define tasks
extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_data,
    provide_context=True,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform_data,
    provide_context=True,
    dag=dag
)

# ============================================
# PATTERN 3: SNOWFLAKE OPERATOR (For your setup!)
# ============================================

create_staging_table = SnowflakeOperator(
    task_id='create_staging_table',
    sql="""
        CREATE TABLE IF NOT EXISTS staging.daily_data (
            date DATE,
            metric_value NUMBER,
            load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """,
    snowflake_conn_id='snowflake_default',
    dag=dag
)

load_to_staging = SnowflakeOperator(
    task_id='load_to_staging',
    sql="""
        COPY INTO staging.daily_data
        FROM @s3_stage/data/{{ ds }}/
        FILE_FORMAT = (TYPE = PARQUET)
        ON_ERROR = 'CONTINUE'
    """,
    snowflake_conn_id='snowflake_default',
    dag=dag
)

# ============================================
# PATTERN 4: DBT INTEGRATION (Modern stack!)
# ============================================

run_dbt_models = DbtCloudRunJobOperator(
    task_id='run_dbt_models',
    dbt_cloud_conn_id='dbt_cloud_default',
    job_id=12345,
    check_interval=30,
    timeout=300,
    dag=dag
)

# ============================================
# PATTERN 5: TASK GROUPS (Organizational)
# ============================================

with TaskGroup('data_quality_checks', dag=dag) as quality_checks:
    
    check_nulls = SnowflakeOperator(
        task_id='check_nulls',
        sql="""
            SELECT COUNT(*) as null_count
            FROM staging.daily_data
            WHERE metric_value IS NULL
        """,
        snowflake_conn_id='snowflake_default'
    )
    
    check_duplicates = SnowflakeOperator(
        task_id='check_duplicates',
        sql="""
            SELECT COUNT(*) - COUNT(DISTINCT date) as dup_count
            FROM staging.daily_data
        """,
        snowflake_conn_id='snowflake_default'
    )

# ============================================
# PATTERN 6: DYNAMIC TASK GENERATION
# ============================================

# They love asking about dynamic DAGs
tables_to_process = ['users', 'orders', 'products']

for table in tables_to_process:
    task = SnowflakeOperator(
        task_id=f'process_{table}',
        sql=f"""
            INSERT INTO processed.{table}
            SELECT * FROM staging.{table}
            WHERE date = '{{{{ ds }}}}'
        """,
        snowflake_conn_id='snowflake_default',
        dag=dag
    )
    
    # Set dependencies
    load_to_staging >> task >> run_dbt_models

# ============================================
# PATTERN 7: DEPENDENCIES (Critical!)
# ============================================

# Linear dependency
extract_task >> transform_task >> create_staging_table

# Parallel then converge
[check_nulls, check_duplicates] >> run_dbt_models

# Complex dependencies
extract_task >> [transform_task, create_staging_table]
transform_task >> load_to_staging >> quality_checks >> run_dbt_models

# ============================================
# PATTERN 8: SENSORS (Waiting for conditions)
# ============================================

from airflow.sensors.s3_key_sensor import S3KeySensor
from airflow.sensors.sql import SqlSensor

# Wait for file to appear
wait_for_file = S3KeySensor(
    task_id='wait_for_file',
    bucket_key='data/{{ ds }}/complete.flag',
    bucket_name='my-data-bucket',
    aws_conn_id='aws_default',
    poke_interval=300,  # Check every 5 minutes
    timeout=3600,  # Timeout after 1 hour
    dag=dag
)

# Wait for data in database
wait_for_data = SqlSensor(
    task_id='wait_for_data',
    conn_id='snowflake_default',
    sql="""
        SELECT COUNT(*) FROM staging.daily_data
        WHERE date = '{{ ds }}'
    """,
    poke_interval=60,
    dag=dag
)

# ============================================
# PATTERN 9: ERROR HANDLING
# ============================================

def handle_failure(**context):
    """Send alert on failure"""
    task_instance = context['task_instance']
    
    # Log error details
    print(f"Task {task_instance.task_id} failed")
    print(f"Execution date: {context['execution_date']}")
    
    # In production, send to Slack/email
    # slack_webhook(f"DAG {dag_id} failed!")

# Add to any critical task
critical_task = PythonOperator(
    task_id='critical_task',
    python_callable=transform_data,
    on_failure_callback=handle_failure,
    dag=dag
)

# ============================================
# INTERVIEW QUESTIONS & ANSWERS
# ============================================

"""
Q: "How do you handle incremental loads?"
A: "I use high-water mark pattern with XCOM to track last processed timestamp"

Q: "How do you handle late-arriving data?"
A: "Sensors to wait for data, plus reprocessing windows in dbt"

Q: "How do you test DAGs?"
A: "Local Airflow instance, unit tests for Python functions, dry runs"

Q: "How do you handle backfills?"
A: "Set catchup=True carefully, use execution_date in queries"

Q: "How do you monitor DAG performance?"
A: "Airflow metrics, custom logging, Snowflake query history"
"""

# ============================================
# YOUR KILLER MOVE IN INTERVIEWS
# ============================================

"""
When they ask about Airflow, you say:

"I orchestrate dbt models with Airflow. Here's my pattern..."
[Show the dbt integration above]

"The key is keeping transformation logic in dbt where it's testable,
and using Airflow purely for orchestration. This gives us..."
- Version controlled transformations
- Data lineage
- Built-in testing
- Self-documenting pipeline

"Let me show you the actual DAG from my repo..."
[Open THIS file]
"""