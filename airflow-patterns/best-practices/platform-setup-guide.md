# Platform Setup Guide - Modern Data Stack Orchestration

*The practical guide to connecting Fivetran, dbt Cloud, Astronomer, and your data warehouse into a working platform*

---

## Overview

This guide covers the actual setup steps needed to build your modern data orchestration platform. Not theory, not code - just the practical "click here, paste there" instructions to get everything connected.

**Time Required**: 2-4 hours for initial setup

**Prerequisites**:
- Credit card for service signups (most have free tiers)
- Admin access to your data warehouse
- Basic understanding of API keys and webhooks

---

## Architecture Decision Tree

Before setup, make these key decisions:

### Environment Strategy

**Option A: Cloud-Only (Recommended for simplicity)**
```
Your Computer → Astronomer Dev → Astronomer Prod
- Edit locally, deploy to cloud
- No Docker needed
- Real connections from start
- 2-3 minute deployment cycles
```

**Option B: Local + Cloud (Recommended for complex development)**
```
Your Computer → Docker Local → Astronomer Dev → Astronomer Prod
- Test instantly locally
- Requires Docker Desktop
- Mock connections locally
- Deploy when ready
```

**Choose Option A if**:
- You're comfortable with dbt Cloud's model
- You have good internet
- You want simplicity
- You're mainly orchestrating, not developing

**Choose Option B if**:
- You need offline development
- You're writing complex DAGs
- You want instant feedback
- You're learning/experimenting

### Deployment Structure

```
Astronomer Organization
├── Development Deployment (your-company-dev)
├── QA Deployment (optional)
└── Production Deployment (your-company-prod)
```

---

## Step 1: Core Account Setup

### 1.1 Astronomer Account

1. **Sign up** at [astronomer.io](https://astronomer.io)
2. **Create Organization**: "YourCompany Data"
3. **Create Deployments**:
   - Name: `yourcompany-dev`
   - Cluster: Choose closest region
   - Resource Size: Small (for dev)
   - Repeat for `yourcompany-prod` with Medium resources

4. **Install CLI**:
   ```bash
   # Windows PowerShell (Admin)
   winget install astronomer.astro
   
   # Or download from GitHub releases
   ```

5. **Authenticate**:
   ```bash
   astro login
   ```

### 1.2 Fivetran Account

1. **Sign up** at [fivetran.com](https://fivetran.com)
2. **Note your API Key**:
   - Account Settings → API Config
   - Generate API Key
   - Copy immediately (shown once)
   - Format: `Basic <base64_encoded_key:secret>`

3. **Create connectors** (at least one):
   - Sources → Add Connector
   - Choose source (e.g., PostgreSQL, Salesforce)
   - Note the Connector ID (in URL after creation)
   - Example: `speaking_increasingly`

### 1.3 dbt Cloud Account

1. **Sign up** at [getdbt.com](https://getdbt.com)
2. **Create Project**:
   - Connect to your git repository
   - Connect to your data warehouse
   
3. **Create Job**:
   - Jobs → New Job
   - Name: "Daily Transform"
   - Commands: `dbt run`
   - Schedule: Off (Airflow will trigger)
   - **Note Job ID** from URL: `12345`

4. **Get API Token**:
   - Account Settings → API Access
   - Generate Service Account Token
   - Copy token (shown once)

5. **Find Account ID**:
   - Check URL: `cloud.getdbt.com/deploy/XXXXX/`
   - Account ID is the `XXXXX` number

### 1.4 Data Warehouse Access

**Snowflake**:
```sql
-- Create Airflow user
CREATE USER airflow_user PASSWORD = 'strong_password';
CREATE ROLE airflow_role;
GRANT ROLE airflow_role TO USER airflow_user;
GRANT USAGE ON WAREHOUSE compute_wh TO ROLE airflow_role;
GRANT USAGE ON DATABASE analytics TO ROLE airflow_role;
GRANT USAGE ON ALL SCHEMAS IN DATABASE analytics TO ROLE airflow_role;
GRANT SELECT ON ALL TABLES IN DATABASE analytics TO ROLE airflow_role;
```

Connection string format:
```
snowflake://airflow_user:password@account.region/analytics/public?warehouse=compute_wh&role=airflow_role
```

**BigQuery**:
1. Create Service Account in GCP Console
2. Download JSON key file
3. Grant BigQuery Data Viewer and Job User roles

### 1.5 Slack Webhook

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create New App → From Scratch
3. Choose workspace
4. Incoming Webhooks → Activate
5. Add New Webhook → Choose channel
6. Copy Webhook URL
   - Format: `https://hooks.slack.com/services/T00/B00/xxxxx`

---

## Step 2: Astronomer Configuration

### 2.1 Project Structure

Create local project:
```bash
mkdir airflow-orchestration
cd airflow-orchestration
astro dev init
```

Structure created:
```
airflow-orchestration/
├── dags/
│   └── modern_stack_orchestration.py  # Your DAGs here
├── include/                            # SQL files, configs
├── requirements.txt                    # Python packages
├── Dockerfile                          # Don't modify unless necessary
└── .astro/                            # Astronomer config
```

### 2.2 Add Required Packages

Edit `requirements.txt`:
```
astronomer-providers[fivetran]==1.0.0
astronomer-providers[dbt-cloud]==1.0.0
apache-airflow-providers-slack==7.3.0
apache-airflow-providers-snowflake==5.1.0
```

### 2.3 Configure Connections

**Method A: Via Astronomer UI (Recommended)**

1. Open Astronomer Cloud UI
2. Select your deployment
3. Environment → Connections
4. Add each connection:

**Fivetran Connection**:
- Connection ID: `fivetran_default`
- Connection Type: HTTP
- Host: `https://api.fivetran.com`
- Extra: 
  ```json
  {
    "Authorization": "Basic <your_base64_key>"
  }
  ```

**dbt Cloud Connection**:
- Connection ID: `dbt_cloud_default`
- Connection Type: HTTP
- Host: `https://cloud.getdbt.com`
- Extra:
  ```json
  {
    "Authorization": "Token <your_token>",
    "Account-Id": "<your_account_id>"
  }
  ```

**Snowflake Connection**:
- Connection ID: `snowflake_default`
- Connection Type: Snowflake
- Host: `<account>.<region>.snowflakecomputing.com`
- Schema: `public`
- Login: `airflow_user`
- Password: `<password>`
- Database: `analytics`
- Warehouse: `compute_wh`
- Role: `airflow_role`

**Slack Connection**:
- Connection ID: `slack_default`
- Connection Type: HTTP
- Host: `https://hooks.slack.com/services`
- Password: `T00/B00/xxxxx` (the part after /services/)

**Method B: Via Environment Variables**

In Astronomer UI → Environment → Environment Variables:

```bash
AIRFLOW_CONN_FIVETRAN_DEFAULT='http://:Basic%20<base64_key>@api.fivetran.com'
AIRFLOW_CONN_DBT_CLOUD_DEFAULT='http://:Token%20<token>@cloud.getdbt.com?Account-Id=<account_id>'
AIRFLOW_CONN_SNOWFLAKE_DEFAULT='snowflake://user:pass@account.region/db/schema?warehouse=wh&role=role'
AIRFLOW_CONN_SLACK_DEFAULT='https://:@hooks.slack.com/services/T00/B00/xxxxx'
```

### 2.4 Configure Variables

Astronomer UI → Environment → Variables:

- Key: `fivetran_connectors`
  Value: `["salesforce_prod", "stripe_prod", "hubspot_prod"]`

- Key: `dbt_job_id`
  Value: `12345`

- Key: `dbt_account_id`
  Value: `67890`

- Key: `notification_email`
  Value: `data-team@company.com`

---

## Step 3: Deployment Workflow

### 3.1 Initial Deployment

1. **Add your DAG**:
   ```bash
   # Copy modern_stack_orchestration.py to dags/
   cp modern_stack_orchestration.py dags/
   ```

2. **Validate locally** (optional):
   ```bash
   astro dev parse  # Check for syntax errors
   ```

3. **Deploy to Dev**:
   ```bash
   astro deploy --deployment-id <dev-deployment-id>
   ```

4. **Monitor deployment**:
   - Check Astronomer UI for deployment status
   - Takes 2-3 minutes
   - Green checkmark when complete

### 3.2 Testing Your Platform

1. **Access Airflow UI**:
   - Astronomer Cloud → Open Airflow
   - Or direct URL: `https://<deployment-id>.astronomer.run`

2. **Verify DAGs loaded**:
   - Should see your DAGs in the list
   - Check for import errors (red banner)

3. **Test connections**:
   - Admin → Connections
   - Click test for each connection
   - ✓ Green = connected

4. **Trigger test run**:
   - Find `simple_sequential_pipeline`
   - Toggle ON (unpause)
   - Click "Trigger DAG" (play button)
   - Watch tasks turn green

### 3.3 Production Deployment

After testing in dev:

```bash
# Deploy to production
astro deploy --deployment-id <prod-deployment-id>

# Or use CI/CD (GitHub Actions example):
name: Deploy to Production
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: astronomer/deploy-action@v1
        with:
          deployment-id: ${{ secrets.PROD_DEPLOYMENT_ID }}
          astronomer-key: ${{ secrets.ASTRONOMER_KEY }}
```

---

## Step 4: Validation Checklist

### Pre-Launch Checklist

**Accounts Created:**
- [ ] Astronomer account with dev/prod deployments
- [ ] Fivetran with at least one connector
- [ ] dbt Cloud with one job
- [ ] Slack webhook configured
- [ ] Data warehouse user created

**Connections Configured:**
- [ ] fivetran_default tested successfully
- [ ] dbt_cloud_default tested successfully
- [ ] snowflake_default tested successfully
- [ ] slack_default tested successfully

**Variables Set:**
- [ ] fivetran_connectors list
- [ ] dbt_job_id
- [ ] notification_email

**DAGs Visible:**
- [ ] DAGs appear in Airflow UI
- [ ] No import errors
- [ ] Can manually trigger

### First Run Validation

1. **Trigger `simple_sequential_pipeline`**
2. **Check each task**:
   - Fivetran sync → Check Fivetran dashboard
   - dbt run → Check dbt Cloud run history
   - Slack notification → Check Slack channel

3. **Verify data flow**:
   ```sql
   -- In your data warehouse
   SELECT MAX(updated_at) 
   FROM analytics.fct_orders;
   -- Should show recent timestamp
   ```

---

## Step 5: Ongoing Operations

### Daily Checks (2 minutes)

1. **Airflow UI Dashboard**:
   - All DAGs should be green
   - Check for failed tasks (red)
   - Review task duration trends

2. **Quick health check**:
   ```sql
   -- Run in data warehouse
   SELECT 
     MAX(updated_at) as last_update,
     COUNT(*) as row_count
   FROM analytics.fct_daily_metrics
   WHERE date >= CURRENT_DATE - 7;
   ```

### Weekly Maintenance (10 minutes)

1. **Review logs** for warnings
2. **Check resource usage** in Astronomer
3. **Update connections** if tokens expired
4. **Clear old logs**:
   ```bash
   astro deploy --deployment-id <id> --force
   ```

### Common Issues and Fixes

**DAG not appearing**:
- Check for Python syntax errors
- Ensure file is in `dags/` folder
- Look for errors in Astronomer logs

**Connection failed**:
- Verify API keys haven't expired
- Check IP whitelist settings
- Test connection in Airflow UI

**Task timing out**:
- Increase timeout in operator
- Check external service status
- Review task logs for details

**Slack not notifying**:
- Verify webhook URL is correct
- Check channel permissions
- Test webhook with curl

---

## Step 6: Cost Management

### Estimated Monthly Costs

**Free/Minimal Tier**:
- Astronomer: $0 (trial) - $150 (starter)
- Fivetran: $0 (trial) - $120 (1 connector)
- dbt Cloud: $0 (developer) - $100 (team)
- Total: $0-370/month

**Small Production**:
- Astronomer: $300 (small cluster)
- Fivetran: $500 (5 connectors)
- dbt Cloud: $100 (team)
- Total: ~$900/month

**Optimization Tips**:
1. Use Fivetran incremental syncs
2. Schedule dbt runs efficiently
3. Right-size Astronomer resources
4. Use sensor `reschedule` mode to save slots

---

## Appendix: Quick Commands Reference

### Astronomer CLI
```bash
astro login                          # Authenticate
astro deployment list               # List all deployments
astro deploy --deployment-id <id>  # Deploy to specific environment
astro deployment logs <id>         # View logs
astro dev parse                     # Validate DAGs locally
```

### Connection Test URLs
```bash
# Test Fivetran
curl -H "Authorization: Basic <key>" https://api.fivetran.com/v1/users

# Test dbt Cloud  
curl -H "Authorization: Token <token>" https://cloud.getdbt.com/api/v2/accounts/<id>/

# Test Slack
curl -X POST -H 'Content-type: application/json' --data '{"text":"Test"}' https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### SQL Validation Queries
```sql
-- Check latest sync
SELECT table_name, MAX(updated_at) as last_sync
FROM information_schema.tables
JOIN <table> ON 1=1
GROUP BY table_name;

-- Monitor pipeline health
SELECT 
  DATE(updated_at) as date,
  COUNT(*) as records_processed
FROM analytics.pipeline_log
WHERE updated_at >= CURRENT_DATE - 7
GROUP BY 1
ORDER BY 1 DESC;
```

---

## Next Steps

1. **Complete setup** using this guide (2-4 hours)
2. **Run test pipeline** with simple_sequential_pipeline
3. **Add your specific** Fivetran connectors and dbt jobs
4. **Monitor for a week** to ensure stability
5. **Add complexity** gradually (more sources, transformations)

Remember: Start simple, validate each step, then expand. The platform is modular - you can add/remove components without breaking others.

---

*End of Platform Setup Guide*