"""
modern_stack_orchestration.py
Complete implementation of Part A: Modern Data Stack Orchestration with Airflow
Author: Ray Serrano
Purpose: All patterns needed for "I'm proficient in Python for Airflow orchestration in the modern data stack"

================================================================================
IMPLEMENTATION DOCUMENTATION FOR MAINTAINERS
================================================================================

SCRIPT STRUCTURE:
-----------------
This file contains 7 independent DAG definitions that demonstrate common 
orchestration patterns. Each DAG is self-contained and can run independently.
DAGs are instantiated at module level so Airflow's DagBag process will find them.

EXECUTION CONTEXT:
------------------
- Runs in Astronomer/Airflow environment (containerized Linux)
- DAGs are parsed every 30 seconds by Airflow scheduler
- Each DAG function is called once during parsing to register the DAG
- Tasks within DAGs execute only when scheduled/triggered
- All paths use forward slashes (Linux container environment)

DEPENDENCIES:
-------------
External Systems Required:
- Fivetran account with configured connectors
- dbt Cloud account with at least one job configured  
- Snowflake/BigQuery/Databricks for data warehouse
- Slack workspace with incoming webhook
- SMTP server or email service for notifications

Airflow Connections (must be configured in UI):
- fivetran_default: HTTP connection with Fivetran API token
- dbt_cloud_default: HTTP connection with dbt Cloud API token
- snowflake_default: Database connection with warehouse credentials
- slack_default: HTTP connection with Slack webhook URL

DAG PATTERNS IMPLEMENTED:
-------------------------
1. simple_sequential_pipeline: Basic A→B→C task flow
2. parallel_sync_pipeline: Multiple tasks converge to single point
3. conditional_pipeline: Branch logic based on day of week
4. data_quality_monitoring: Check data and alert on failures
5. dynamic_connector_sync: Generate tasks from configuration
6. wait_for_dependencies: Sensors to wait for external systems
7. production_data_pipeline: Combines multiple patterns

COMMON MODIFICATIONS:
---------------------
To add a new Fivetran connector:
1. Add connector_id to FIVETRAN_CONNECTORS list (line 35)
2. Ensure connector exists in Fivetran UI
3. Redeploy DAG

To change schedules:
1. Modify schedule parameter in @dag decorator
2. Use cron expression (e.g., "0 6 * * *") or preset (@daily, @hourly)
3. Remember times are in UTC unless configured otherwise

To add notifications:
1. Add SlackWebhookOperator or EmailOperator after any task
2. Use trigger_rule="one_failed" for failure alerts
3. Use trigger_rule="all_success" for success notifications

ERROR HANDLING:
---------------
- Each DAG has default_args with retry logic (2 retries, 5 min delay)
- Failed tasks appear red in Airflow UI
- Email notifications sent on failure if configured
- Slack alerts triggered by failure conditions in monitoring DAGs
- Check Airflow logs: Task Instance → Logs for debugging

PERFORMANCE CONSIDERATIONS:
---------------------------
- DAG parsing happens every 30 seconds - keep top-level code minimal
- Avoid database queries or API calls during parsing (outside tasks)
- Use .expand() for dynamic task mapping (more efficient than loops)
- Set appropriate timeouts on Sensor operators to avoid indefinite waiting
- Use trigger_rule="none_failed_min_one_success" for downstream tasks after branches

TESTING APPROACH:
-----------------
Local testing (with Astronomer CLI):
1. astro dev start
2. Trigger DAG manually in UI (localhost:8080)
3. Check task logs for errors
4. Verify connections are configured correctly

Production deployment:
1. astro dev parse (validates DAG syntax)
2. astro dev pytest (runs any tests in tests/ folder)
3. astro deploy --deployment-id <your-id>
4. Monitor first run carefully

COMMON ISSUES AND SOLUTIONS:
----------------------------
"Connection not found" error:
- Ensure connection ID in code matches exactly in Airflow UI
- Connection IDs are case-sensitive

Tasks not running:
- Check DAG is not paused in UI
- Verify start_date is in the past
- Ensure schedule_interval is set correctly

Import errors:
- Add missing provider packages to requirements.txt
- Run astro dev restart after adding packages

DAG not appearing in UI:
- Check for Python syntax errors
- Ensure DAG is instantiated at module level
- Look for errors in Airflow webserver logs

================================================================================
END OF IMPLEMENTATION DOCUMENTATION
================================================================================
"""

# ============================================================================
# IMPORTS - Everything you need for modern stack orchestration
# ============================================================================

from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.email import EmailOperator

# Provider imports (add to requirements.txt as needed)
from airflow.providers.fivetran.operators.fivetran import FivetranOperator
from airflow.providers.fivetran.sensors.fivetran import FivetranSensor
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.providers.slack.operators.slack import SlackWebhookOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.http.sensors.http import HttpSensor

# ============================================================================
# CONFIGURATION - Variables and settings
# ============================================================================

# These would typically come from Airflow Variables or environment
FIVETRAN_CONNECTORS = ["salesforce", "stripe", "zendesk", "hubspot"]
DBT_JOB_ID = 12345
DBT_ACCOUNT_ID = 67890
SLACK_CHANNEL = "#data-alerts"
NOTIFICATION_EMAIL = "data-team@company.com"

# Default arguments for all DAGs
default_args = {
    "owner": "data-team",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": [NOTIFICATION_EMAIL]
}

# ============================================================================
# PATTERN 1: SIMPLE SEQUENTIAL ORCHESTRATION
# ============================================================================

@dag(
    dag_id="simple_sequential_pipeline",
    schedule="@daily",  # Run daily at midnight
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["orchestration", "production"]
)
def simple_sequential_pipeline():
    """
    Pattern 1: Simple sequential orchestration
    Fivetran → dbt Cloud → Notification
    """
    
    # Step 1: Sync data from source
    sync_data = FivetranOperator(
        task_id="sync_salesforce",
        connector_id="salesforce_prod"
    )
    
    # Step 2: Transform in dbt Cloud
    transform_data = DbtCloudRunJobOperator(
        task_id="run_dbt_models",
        job_id=DBT_JOB_ID,
        account_id=DBT_ACCOUNT_ID,
        wait_for_termination=True,
        check_interval=60  # Check every 60 seconds
    )
    
    # Step 3: Send completion notification
    notify_complete = SlackWebhookOperator(
        task_id="notify_completion",
        slack_webhook_conn_id="slack_default",
        message=f"✅ Daily pipeline completed successfully for {{{{ ds }}}}"
    )
    
    # Define dependencies
    sync_data >> transform_data >> notify_complete

# Instantiate the DAG
simple_dag = simple_sequential_pipeline()

# ============================================================================
# PATTERN 2: PARALLEL SYNCS WITH CONVERGENCE
# ============================================================================

@dag(
    dag_id="parallel_sync_pipeline",
    schedule="0 6 * * *",  # Run at 6 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["orchestration", "parallel"]
)
def parallel_sync_pipeline():
    """
    Pattern 2: Sync multiple sources in parallel, then transform
    Multiple Fivetran connectors → dbt Cloud
    """
    
    # Create sync tasks for each connector
    sync_tasks = []
    for connector in FIVETRAN_CONNECTORS:
        sync = FivetranOperator(
            task_id=f"sync_{connector}",
            connector_id=f"{connector}_prod"
        )
        sync_tasks.append(sync)
    
    # Run dbt after ALL syncs complete
    run_transformations = DbtCloudRunJobOperator(
        task_id="run_all_transformations",
        job_id=DBT_JOB_ID,
        account_id=DBT_ACCOUNT_ID,
        wait_for_termination=True
    )
    
    # Send summary email
    send_summary = EmailOperator(
        task_id="send_summary_email",
        to=[NOTIFICATION_EMAIL],
        subject="Pipeline Summary - {{ ds }}",
        html_content="""
        <h3>Daily Pipeline Complete</h3>
        <p>Date: {{ ds }}</p>
        <p>Synced: """ + ", ".join(FIVETRAN_CONNECTORS) + """</p>
        <p>dbt Job: Completed</p>
        """
    )
    
    # Dependencies: All syncs must complete before dbt
    sync_tasks >> run_transformations >> send_summary

parallel_dag = parallel_sync_pipeline()

# ============================================================================
# PATTERN 3: CONDITIONAL ORCHESTRATION
# ============================================================================

@dag(
    dag_id="conditional_pipeline",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["orchestration", "conditional"]
)
def conditional_pipeline():
    """
    Pattern 3: Conditional execution based on business logic
    Only run expensive syncs on weekdays
    """
    
    @task.branch
    def check_if_should_run():
        """Decide whether to run the pipeline"""
        from datetime import date
        
        today = date.today()
        day_of_week = today.weekday()
        
        # Skip weekends (Saturday=5, Sunday=6)
        if day_of_week in [5, 6]:
            return "skip_weekend"
        else:
            return "run_sync"
    
    @task
    def skip_weekend():
        """Log that we're skipping the weekend run"""
        print("Skipping weekend run to save costs")
        return "Weekend - pipeline skipped"
    
    # Check if we should run
    branch_decision = check_if_should_run()
    
    # Main pipeline tasks
    run_sync = FivetranOperator(
        task_id="run_sync",
        connector_id="expensive_api_sync",
        trigger_rule="none_failed"  # Run if not skipped
    )
    
    run_dbt = DbtCloudRunJobOperator(
        task_id="run_dbt",
        job_id=DBT_JOB_ID,
        account_id=DBT_ACCOUNT_ID,
        trigger_rule="none_failed_min_one_success"  # Run if any upstream succeeded
    )
    
    # Set up branching
    branch_decision >> [run_sync, skip_weekend()]
    [run_sync, skip_weekend()] >> run_dbt

conditional_dag = conditional_pipeline()

# ============================================================================
# PATTERN 4: DATA QUALITY MONITORING
# ============================================================================

@dag(
    dag_id="data_quality_monitoring",
    schedule="0 8 * * *",  # Run at 8 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["monitoring", "data-quality"]
)
def data_quality_monitoring():
    """
    Pattern 4: Monitor data freshness and quality
    Check data → Alert if issues
    """
    
    # Check data freshness
    check_freshness = SnowflakeOperator(
        task_id="check_data_freshness",
        snowflake_conn_id="snowflake_default",
        sql="""
            SELECT 
                CASE 
                    WHEN MAX(updated_at) < CURRENT_DATE - INTERVAL '1 day'
                    THEN 'STALE'
                    ELSE 'FRESH'
                END as data_status,
                MAX(updated_at) as last_update,
                CURRENT_TIMESTAMP as check_time
            FROM analytics.fct_orders
        """
    )
    
    # Check row counts
    check_row_counts = SnowflakeOperator(
        task_id="check_row_counts",
        snowflake_conn_id="snowflake_default",
        sql="""
            SELECT 
                'customers' as table_name, COUNT(*) as row_count 
            FROM analytics.dim_customers
            UNION ALL
            SELECT 
                'orders' as table_name, COUNT(*) as row_count 
            FROM analytics.fct_orders
        """
    )
    
    # Alert on any failures
    alert_on_failure = SlackWebhookOperator(
        task_id="alert_data_issues",
        slack_webhook_conn_id="slack_default",
        message="⚠️ Data quality check failed! Check Airflow logs for details.",
        trigger_rule="one_failed"  # Only runs if a check failed
    )
    
    # Success notification
    @task
    def log_success():
        """Log successful quality check"""
        print("✅ All data quality checks passed")
        return "Quality checks passed"
    
    # Set up monitoring flow
    [check_freshness, check_row_counts] >> [alert_on_failure, log_success()]

monitoring_dag = data_quality_monitoring()

# ============================================================================
# PATTERN 5: DYNAMIC TASK GENERATION
# ============================================================================

@dag(
    dag_id="dynamic_connector_sync",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["orchestration", "dynamic"]
)
def dynamic_connector_sync():
    """
    Pattern 5: Dynamically create tasks based on configuration
    Read config → Create sync tasks → Transform
    """
    
    @task
    def get_active_connectors():
        """Get list of active connectors from configuration"""
        # In production, this might query a database or API
        # For now, use Airflow Variable
        try:
            connectors = Variable.get("active_connectors", deserialize_json=True)
        except:
            # Fallback to default list
            connectors = ["salesforce", "stripe"]
        
        return connectors
    
    @task
    def sync_connector(connector_id: str):
        """Sync a single connector (task version of FivetranOperator)"""
        print(f"Syncing connector: {connector_id}")
        # In production, you'd use FivetranOperator
        # This is just to show the pattern
        return f"Synced {connector_id}"
    
    @task
    def run_dbt_for_sources(sync_results):
        """Run dbt models after all syncs complete"""
        print(f"Running dbt for {len(sync_results)} sources")
        return "dbt completed"
    
    # Build dynamic pipeline
    connectors = get_active_connectors()
    sync_results = sync_connector.expand(connector_id=connectors)
    dbt_result = run_dbt_for_sources(sync_results)

dynamic_dag = dynamic_connector_sync()

# ============================================================================
# PATTERN 6: WAIT FOR EXTERNAL DEPENDENCIES
# ============================================================================

@dag(
    dag_id="wait_for_dependencies",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["orchestration", "sensors"]
)
def wait_for_dependencies():
    """
    Pattern 6: Wait for external systems before proceeding
    Wait for API → Wait for Fivetran → Run dbt
    """
    
    # Wait for external API to be available
    wait_for_api = HttpSensor(
        task_id="wait_for_api",
        http_conn_id="api_default",
        endpoint="health",
        poke_interval=300,  # Check every 5 minutes
        timeout=3600,  # Timeout after 1 hour
        mode="poke"  # Use "reschedule" in production to free up slots
    )
    
    # Sync after API is available
    sync_from_api = FivetranOperator(
        task_id="sync_api_data",
        connector_id="api_connector"
    )
    
    # Wait for Fivetran sync to complete
    wait_for_sync = FivetranSensor(
        task_id="wait_for_sync_completion",
        connector_id="api_connector",
        poke_interval=60,
        timeout=1800
    )
    
    # Transform after sync completes
    transform = DbtCloudRunJobOperator(
        task_id="transform_api_data",
        job_id=DBT_JOB_ID,
        account_id=DBT_ACCOUNT_ID
    )
    
    # Chain dependencies
    wait_for_api >> sync_from_api >> wait_for_sync >> transform

sensor_dag = wait_for_dependencies()

# ============================================================================
# PATTERN 7: FULL PRODUCTION PIPELINE
# ============================================================================

@dag(
    dag_id="production_data_pipeline",
    schedule="0 2 * * *",  # Run at 2 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["production", "complete"]
)
def production_data_pipeline():
    """
    Complete production pipeline combining multiple patterns:
    - Parallel syncs
    - Data quality checks
    - Conditional logic
    - Notifications
    """
    
    @task
    def start_pipeline():
        """Log pipeline start"""
        from datetime import datetime
        print(f"Pipeline started at {datetime.now()}")
        return {"status": "started", "timestamp": datetime.now().isoformat()}
    
    # Start the pipeline
    pipeline_start = start_pipeline()
    
    # Sync all data sources in parallel
    sync_tasks = []
    for connector in FIVETRAN_CONNECTORS:
        sync = FivetranOperator(
            task_id=f"sync_{connector}",
            connector_id=f"{connector}_prod"
        )
        sync_tasks.append(sync)
    
    # Wait for all syncs to complete
    @task
    def validate_syncs():
        """Ensure all syncs completed successfully"""
        print(f"All {len(FIVETRAN_CONNECTORS)} syncs completed")
        return "syncs_validated"
    
    syncs_complete = validate_syncs()
    
    # Run dbt Cloud job
    run_dbt = DbtCloudRunJobOperator(
        task_id="run_dbt_cloud",
        job_id=DBT_JOB_ID,
        account_id=DBT_ACCOUNT_ID,
        wait_for_termination=True,
        check_interval=60
    )
    
    # Run data quality checks
    quality_check = SnowflakeOperator(
        task_id="run_quality_checks",
        snowflake_conn_id="snowflake_default",
        sql="""
            -- Check for data freshness and completeness
            WITH checks AS (
                SELECT 
                    COUNT(*) as total_checks,
                    SUM(CASE WHEN check_passed THEN 1 ELSE 0 END) as passed_checks
                FROM analytics.data_quality_results
                WHERE check_date = CURRENT_DATE
            )
            SELECT 
                CASE 
                    WHEN passed_checks = total_checks THEN 'PASSED'
                    ELSE 'FAILED'
                END as quality_status
            FROM checks
        """
    )
    
    # Send success notification
    success_notification = SlackWebhookOperator(
        task_id="notify_success",
        slack_webhook_conn_id="slack_default",
        message="""
        ✅ Production Pipeline Complete
        Date: {{ ds }}
        Status: All systems operational
        Next run: {{ next_ds }}
        """,
        trigger_rule="all_success"
    )
    
    # Send failure alert
    failure_alert = SlackWebhookOperator(
        task_id="alert_failure",
        slack_webhook_conn_id="slack_default",
        message="""
        🚨 Production Pipeline Failed
        Date: {{ ds }}
        Check Airflow logs for details
        """,
        trigger_rule="one_failed"
    )
    
    # Define the complete pipeline flow
    pipeline_start >> sync_tasks >> syncs_complete >> run_dbt >> quality_check
    quality_check >> [success_notification, failure_alert]

production_dag = production_data_pipeline()

# ============================================================================
# HELPER FUNCTIONS (Reusable across DAGs)
# ============================================================================

def get_config_value(key: str, default_value=None):
    """Safely get configuration from Airflow Variables"""
    try:
        return Variable.get(key)
    except:
        return default_value

def is_business_day():
    """Check if today is a business day"""
    from datetime import date
    return date.today().weekday() < 5  # Monday = 0, Friday = 4

def should_run_full_refresh():
    """Determine if we should run a full refresh (Sundays only)"""
    from datetime import date
    return date.today().weekday() == 6  # Sunday = 6

# ============================================================================
# CONFIGURATION REFERENCE
# ============================================================================

"""
Required Airflow Connections (configure in Astronomer UI):
- fivetran_default: Fivetran API connection
- dbt_cloud_default: dbt Cloud API connection  
- snowflake_default: Snowflake database connection
- slack_default: Slack webhook connection
- api_default: External API connection

Required Airflow Variables (configure in Astronomer UI):
- active_connectors: JSON list of Fivetran connector IDs
- dbt_job_id: dbt Cloud job ID
- notification_email: Email for alerts
- pipeline_config: JSON configuration for pipeline

Python packages to add to requirements.txt:
- astronomer-providers[fivetran]
- astronomer-providers[dbt-cloud]
- apache-airflow-providers-slack
- apache-airflow-providers-snowflake
"""

# ============================================================================
# END OF SCRIPT
# ============================================================================

"""
This script contains all the patterns you need for:
"I'm proficient in Python for Airflow orchestration in the modern data stack"

Patterns included:
1. Simple sequential orchestration
2. Parallel syncs with convergence
3. Conditional execution
4. Data quality monitoring
5. Dynamic task generation
6. Waiting for dependencies
7. Complete production pipeline

Next steps:
1. Copy this script to your dags/ folder
2. Update connection IDs and variables for your environment
3. Choose the patterns you need
4. Delete the patterns you don't need
5. Deploy to Astronomer

Remember: This is orchestration only. No data processing in Airflow!
Transformations belong in dbt, ingestion belongs in Fivetran.
"""