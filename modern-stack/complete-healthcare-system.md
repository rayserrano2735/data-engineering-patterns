# Complete Healthcare Analytics System: Snowflake + dbt + MCP + KSQLDB Agents

## 🎯 System Overview

A complete autonomous healthcare analytics system that eliminates traditional BI and manual analysis through SQL-based agents and AI collaboration.

### Architecture Flow
```
┌─────────────────────────────────────────────────────────────┐
│                   Healthcare Data Sources                    │
│         (EHR, Labs, Pharmacy, Claims, Devices)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                        Snowflake                            │
│              (Raw Data → Staging → Marts)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    dbt Transformations                       │
│            (Models, Tests, Documentation)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  dbt Semantic Layer                         │
│          (Metrics, Dimensions, Governance)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ├────────────────────┐
                       ▼                    ▼
┌─────────────────────────────┐  ┌────────────────────────────┐
│      MCP Server             │  │   Direct API Access        │
│  (For Claude Agents Only)   │  │   (For KSQLDB Agents)      │
└──────────┬──────────────────┘  └──────────┬─────────────────┘
           │                                 │
           ▼                                 ▼
┌─────────────────────────────────────────────────────────────┐
│                        KSQLDB                               │
│     (Autonomous SQL Agents - 99% of Operations)             │
│   • Readmission Detection (SQL)                             │
│   • Sepsis Monitoring (SQL)                                 │
│   • Capacity Management (SQL)                               │
│   • Adherence Tracking (SQL)                                │
│   • Drug Interactions (SQL)                                 │
└──────────────┬──────────────────┬───────────────────────────┘
               │                  │
               │                  ▼
               │     ┌────────────────────────────────┐
               │     │   Claude AI Agents (1%)        │
               │     │   (Complex Cases Only)         │
               │     ├────────────────────────────────┤
               │     │ • Clinical Investigation Agent │
               │     │   (Unknown pattern analysis)   │
               │     ├────────────────────────────────┤
               │     │ • Multi-Hospital Coordination │
               │     │   ┌──────────┐  ┌──────────┐ │
               │     │   │Claude A  │←→│Claude B  │ │
               │     │   │(Hosp A)  │  │(Hosp B)  │ │
               │     │   └──────────┘  └──────────┘ │
               │     └────────────┬───────────────────┘
               │                  │
               ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    Action Outputs                           │
│  • Alerts (Critical conditions detected)                    │
│  • Interventions (Automated responses)                      │
│  • Notifications (Staff/provider alerts)                    │
│  • Transfers (Cross-facility coordination)                  │
│  • Reports (Executive summaries)                            │
└─────────────────────────────────────────────────────────────┘
```

### The Division of Labor

```
KSQLDB Agents (Always Running):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Continuous SQL queries that:
• Monitor known patterns 24/7
• Trigger immediate alerts
• Handle 99% of operations
• No AI needed

Claude AI Agents (On-Demand):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Called only when:
• Unknown patterns detected
• Cross-organization negotiation needed
• Complex investigation required
• Human-like reasoning necessary
```

### Data Flow Examples

#### Example 1: Readmission Detection (KSQLDB Only)
```
Snowflake → dbt → Semantic Layer → KSQLDB → Alert
(No AI needed - pure SQL pattern matching)
```

#### Example 2: Complex Clinical Investigation (KSQLDB + Claude)
```
Snowflake → dbt → Semantic Layer → KSQLDB detects anomaly
                                       ↓
                                  MCP Server
                                       ↓
                                  Claude Agent investigates
                                       ↓
                                  New SQL pattern created
                                       ↓
                                  KSQLDB monitors new pattern
```

#### Example 3: Hospital Transfer Negotiation (Multiple Claude Agents)
```
Hospital A                         Hospital B
Snowflake → Semantic Layer       Snowflake → Semantic Layer
     ↓                                 ↓
MCP Server A                      MCP Server B
     ↓                                 ↓
Claude Agent A  ←─[KSQLDB Stream]─→  Claude Agent B
                  (Negotiation)
     ↓                                 ↓
Transfer Approved              Bed Reserved
```

### Key Architecture Principles

1. **KSQLDB First** - SQL agents handle all routine operations
2. **Claude for Complexity** - AI only for cases SQL can't handle
3. **Separation of Concerns** - Each hospital maintains own Claude instance
4. **Message-Based Communication** - Agents communicate through KSQLDB streams
5. **Privacy Preserved** - Patient data never leaves organizational boundary

---

## Phase 1: Snowflake Foundation

### 1.1 Initial Setup

```sql
-- Create healthcare databases
CREATE DATABASE IF NOT EXISTS HEALTHCARE_RAW;
CREATE DATABASE IF NOT EXISTS HEALTHCARE_PROD;

-- Create dedicated warehouse for operations
CREATE WAREHOUSE IF NOT EXISTS HEALTHCARE_WH
    WITH WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 3;

-- Create roles
CREATE ROLE IF NOT EXISTS HEALTHCARE_ANALYST;
CREATE ROLE IF NOT EXISTS DBT_ROLE;
CREATE ROLE IF NOT EXISTS KSQL_ROLE;

-- Grant permissions
GRANT USAGE ON WAREHOUSE HEALTHCARE_WH TO ROLE HEALTHCARE_ANALYST;
GRANT USAGE ON WAREHOUSE HEALTHCARE_WH TO ROLE DBT_ROLE;
GRANT ALL ON DATABASE HEALTHCARE_RAW TO ROLE DBT_ROLE;
GRANT ALL ON DATABASE HEALTHCARE_PROD TO ROLE DBT_ROLE;
```

### 1.2 Healthcare Data Model

```sql
USE DATABASE HEALTHCARE_RAW;
CREATE SCHEMA IF NOT EXISTS EHR;

-- Core patient table
CREATE OR REPLACE TABLE HEALTHCARE_RAW.EHR.patients (
    patient_id VARCHAR(50) PRIMARY KEY,
    mrn VARCHAR(50),
    birth_date DATE,
    gender VARCHAR(10),
    race VARCHAR(50),
    ethnicity VARCHAR(50),
    primary_language VARCHAR(50),
    zip_code VARCHAR(10),
    insurance_type VARCHAR(50),
    payer_category VARCHAR(50),
    primary_care_provider_id VARCHAR(50),
    enrollment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Encounters (admissions, visits)
CREATE OR REPLACE TABLE HEALTHCARE_RAW.EHR.encounters (
    encounter_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50),
    encounter_type VARCHAR(50), -- 'inpatient', 'emergency', 'outpatient', 'telehealth'
    admit_datetime TIMESTAMP,
    discharge_datetime TIMESTAMP,
    facility_id VARCHAR(50),
    department_id VARCHAR(50),
    attending_provider_id VARCHAR(50),
    primary_diagnosis_code VARCHAR(10),
    drg_code VARCHAR(10),
    discharge_disposition VARCHAR(50),
    length_of_stay_days NUMBER,
    readmission_flag BOOLEAN DEFAULT FALSE,
    total_charges DECIMAL(12,2),
    total_payments DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Lab results
CREATE OR REPLACE TABLE HEALTHCARE_RAW.EHR.lab_results (
    lab_result_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50),
    encounter_id VARCHAR(50),
    test_code VARCHAR(20),
    test_name VARCHAR(200),
    result_value VARCHAR(100),
    result_numeric DECIMAL(10,3),
    result_unit VARCHAR(50),
    reference_low DECIMAL(10,3),
    reference_high DECIMAL(10,3),
    abnormal_flag VARCHAR(20), -- 'Normal', 'Low', 'High', 'Critical'
    critical_flag BOOLEAN DEFAULT FALSE,
    collection_datetime TIMESTAMP,
    result_datetime TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Medications
CREATE OR REPLACE TABLE HEALTHCARE_RAW.EHR.medications (
    medication_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50),
    encounter_id VARCHAR(50),
    medication_code VARCHAR(20),
    medication_name VARCHAR(200),
    generic_name VARCHAR(200),
    therapeutic_class VARCHAR(100),
    dosage VARCHAR(100),
    route VARCHAR(50),
    frequency VARCHAR(50),
    start_datetime TIMESTAMP,
    end_datetime TIMESTAMP,
    prescribing_provider_id VARCHAR(50),
    pharmacy_id VARCHAR(50),
    is_high_risk BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Pharmacy dispensing
CREATE OR REPLACE TABLE HEALTHCARE_RAW.EHR.pharmacy_dispenses (
    dispense_id VARCHAR(50) PRIMARY KEY,
    medication_id VARCHAR(50),
    patient_id VARCHAR(50),
    prescription_number VARCHAR(50),
    dispense_datetime TIMESTAMP,
    days_supply NUMBER,
    quantity_dispensed NUMBER,
    refills_remaining NUMBER,
    pharmacy_id VARCHAR(50),
    pharmacist_id VARCHAR(50),
    copay_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Medication adherence
CREATE OR REPLACE TABLE HEALTHCARE_RAW.EHR.medication_adherence (
    adherence_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50),
    medication_id VARCHAR(50),
    measurement_date DATE,
    pdc_score DECIMAL(3,2), -- Proportion of Days Covered
    mpr_score DECIMAL(3,2), -- Medication Possession Ratio
    gaps_in_therapy_days NUMBER,
    days_until_refill NUMBER,
    last_fill_date DATE,
    next_fill_due DATE,
    adherence_status VARCHAR(50), -- 'adherent', 'at_risk', 'non_adherent'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Vital signs
CREATE OR REPLACE TABLE HEALTHCARE_RAW.EHR.vital_signs (
    vital_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50),
    encounter_id VARCHAR(50),
    measurement_datetime TIMESTAMP,
    temperature DECIMAL(4,1),
    heart_rate INTEGER,
    respiratory_rate INTEGER,
    blood_pressure_systolic INTEGER,
    blood_pressure_diastolic INTEGER,
    oxygen_saturation DECIMAL(5,2),
    pain_score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Create streams for CDC to KSQLDB
CREATE OR REPLACE STREAM patients_stream ON TABLE patients;
CREATE OR REPLACE STREAM encounters_stream ON TABLE encounters;
CREATE OR REPLACE STREAM lab_results_stream ON TABLE lab_results;
CREATE OR REPLACE STREAM medications_stream ON TABLE medications;
CREATE OR REPLACE STREAM pharmacy_dispenses_stream ON TABLE pharmacy_dispenses;
CREATE OR REPLACE STREAM adherence_stream ON TABLE medication_adherence;
CREATE OR REPLACE STREAM vitals_stream ON TABLE vital_signs;
```

---

## Phase 2: dbt Models and Semantic Layer

### 2.1 dbt Project Structure

```yaml
# dbt_project.yml
name: 'healthcare_analytics'
version: '1.0.0'
config-version: 2

profile: 'healthcare'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

models:
  healthcare_analytics:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: view
      +schema: intermediate
    marts:
      +materialized: table
      +schema: marts
```

### 2.2 Staging Models

```sql
-- models/staging/stg_patients.sql
{{
    config(
        materialized='view'
    )
}}

WITH source AS (
    SELECT * FROM {{ source('ehr', 'patients') }}
),

transformed AS (
    SELECT
        patient_id,
        mrn,
        birth_date,
        DATEDIFF('year', birth_date, CURRENT_DATE()) AS age,
        CASE 
            WHEN DATEDIFF('year', birth_date, CURRENT_DATE()) < 18 THEN 'Pediatric'
            WHEN DATEDIFF('year', birth_date, CURRENT_DATE()) < 65 THEN 'Adult'
            ELSE 'Geriatric'
        END AS age_group,
        gender,
        race,
        ethnicity,
        primary_language,
        zip_code,
        insurance_type,
        payer_category,
        primary_care_provider_id,
        enrollment_date,
        DATEDIFF('day', enrollment_date, CURRENT_DATE()) AS days_enrolled,
        created_at,
        updated_at
    FROM source
)

SELECT * FROM transformed
```

```sql
-- models/staging/stg_encounters.sql
{{
    config(
        materialized='view'
    )
}}

WITH source AS (
    SELECT * FROM {{ source('ehr', 'encounters') }}
),

transformed AS (
    SELECT
        encounter_id,
        patient_id,
        encounter_type,
        admit_datetime,
        discharge_datetime,
        DATE(admit_datetime) AS admit_date,
        EXTRACT(HOUR FROM admit_datetime) AS admit_hour,
        DAYNAME(admit_datetime) AS admit_day_of_week,
        facility_id,
        department_id,
        attending_provider_id,
        primary_diagnosis_code,
        drg_code,
        discharge_disposition,
        length_of_stay_days,
        CASE 
            WHEN length_of_stay_days = 0 THEN 'Same Day'
            WHEN length_of_stay_days <= 2 THEN 'Short'
            WHEN length_of_stay_days <= 7 THEN 'Medium'
            ELSE 'Long'
        END AS los_category,
        readmission_flag,
        total_charges,
        total_payments,
        total_charges - total_payments AS balance,
        created_at,
        updated_at
    FROM source
)

SELECT * FROM transformed
```

### 2.3 Mart Models

```sql
-- models/marts/clinical/fct_patient_encounters.sql
{{
    config(
        materialized='table'
    )
}}

WITH patients AS (
    SELECT * FROM {{ ref('stg_patients') }}
),

encounters AS (
    SELECT * FROM {{ ref('stg_encounters') }}
),

labs AS (
    SELECT * FROM {{ ref('stg_lab_results') }}
),

medications AS (
    SELECT * FROM {{ ref('stg_medications') }}
),

final AS (
    SELECT
        -- Encounter details
        e.encounter_id,
        e.patient_id,
        e.encounter_type,
        e.admit_datetime,
        e.discharge_datetime,
        e.length_of_stay_days,
        e.los_category,
        e.readmission_flag,
        
        -- Patient demographics
        p.age,
        p.age_group,
        p.gender,
        p.race,
        p.ethnicity,
        p.insurance_type,
        p.payer_category,
        
        -- Clinical metrics
        e.primary_diagnosis_code,
        e.drg_code,
        e.discharge_disposition,
        
        -- Financial metrics
        e.total_charges,
        e.total_payments,
        e.balance,
        
        -- Risk scoring
        CASE 
            WHEN p.age >= 65 AND e.length_of_stay_days > 7 THEN 'High'
            WHEN p.age >= 65 OR e.length_of_stay_days > 7 THEN 'Medium'
            ELSE 'Low'
        END AS risk_category,
        
        -- Timestamps
        e.created_at,
        e.updated_at
        
    FROM encounters e
    LEFT JOIN patients p ON e.patient_id = p.patient_id
)

SELECT * FROM final
```

### 2.4 Semantic Layer Configuration

```yaml
# models/marts/semantic_models.yml
semantic_models:
  - name: patient_encounters
    description: Core patient encounter metrics
    model: ref('fct_patient_encounters')
    
    defaults:
      agg_time_dimension: admit_date
    
    entities:
      - name: encounter_id
        type: primary
        expr: encounter_id
      - name: patient_id
        type: foreign
        expr: patient_id
    
    dimensions:
      - name: admit_date
        type: time
        type_params:
          time_granularity: day
      - name: encounter_type
        type: categorical
      - name: age_group
        type: categorical
      - name: payer_category
        type: categorical
      - name: risk_category
        type: categorical
    
    measures:
      - name: encounter_count
        description: Total encounters
        agg: count
        expr: encounter_id
      
      - name: unique_patients
        description: Unique patient count
        agg: count_distinct
        expr: patient_id
      
      - name: total_los_days
        description: Total length of stay
        agg: sum
        expr: length_of_stay_days
      
      - name: avg_los_days
        description: Average length of stay
        agg: average
        expr: length_of_stay_days
      
      - name: readmission_count
        description: Number of readmissions
        agg: sum
        expr: CASE WHEN readmission_flag THEN 1 ELSE 0 END
      
      - name: total_charges
        description: Total charges
        agg: sum
        expr: total_charges
      
      - name: total_payments
        description: Total payments
        agg: sum
        expr: total_payments
```

```yaml
# models/marts/metrics.yml
metrics:
  # Clinical Quality Metrics
  - name: readmission_rate
    description: 30-day readmission rate
    type: ratio
    type_params:
      numerator: readmission_count
      denominator: encounter_count
    filter: |
      encounter_type = 'inpatient'
  
  - name: avg_length_of_stay
    description: Average inpatient LOS
    type: simple
    type_params:
      measure: avg_los_days
    filter: encounter_type = 'inpatient'
  
  # Financial Metrics  
  - name: revenue_per_encounter
    description: Average revenue per encounter
    type: ratio
    type_params:
      numerator: total_payments
      denominator: encounter_count
  
  - name: collection_rate
    description: Payment to charge ratio
    type: ratio
    type_params:
      numerator: total_payments
      denominator: total_charges
```

---

## Phase 3: MCP Server Setup

### 3.1 dbt Cloud Configuration

```bash
# Create service token in dbt Cloud
# Account Settings → Service Tokens → New Token
# Permissions: Metadata Only, Semantic Layer Only, Job Admin

# Note these IDs from dbt Cloud:
DBT_ACCOUNT_ID=12345
DBT_PROJECT_ID=67890
DBT_ENVIRONMENT_ID=11111
DBT_TOKEN=dbtc_xxxxxxxxxxxxx
```

### 3.2 MCP Server Installation

```bash
# Install MCP server
pip install dbt-mcp

# Create configuration file
cat > ~/.dbt-mcp.env << EOF
DBT_HOST=cloud.getdbt.com
DBT_ACCOUNT_ID=${DBT_ACCOUNT_ID}
DBT_PROJECT_ID=${DBT_PROJECT_ID}
DBT_ENVIRONMENT_ID=${DBT_ENVIRONMENT_ID}
DBT_TOKEN=${DBT_TOKEN}
LOG_LEVEL=INFO
EOF

# Test MCP server
uvx --env-file ~/.dbt-mcp.env dbt-mcp
```

---

## Phase 4: KSQLDB Agent System

### 4.1 Kafka Connect Setup

```sql
-- Create Snowflake source connector for CDC
CREATE SOURCE CONNECTOR snowflake_cdc WITH (
    'connector.class' = 'com.snowflake.kafka.connector.SnowflakeSourceConnector',
    'snowflake.url.name' = 'your-account.snowflakecomputing.com',
    'snowflake.user.name' = 'KSQL_USER',
    'snowflake.private.key' = '${file:/secrets/snowflake_key.p8}',
    'snowflake.database.name' = 'HEALTHCARE_RAW',
    'snowflake.schema.name' = 'EHR',
    'tasks.max' = '8',
    'topics' = 'healthcare',
    'topic.prefix' = 'snowflake_',
    'poll.interval' = '10000',
    'offset.storage.topic' = 'connect-offsets',
    'status.storage.topic' = 'connect-status',
    'config.storage.topic' = 'connect-configs'
);
```

### 4.2 Base Healthcare Streams

```sql
-- Patient stream
CREATE STREAM IF NOT EXISTS patients_stream (
    patient_id VARCHAR KEY,
    mrn VARCHAR,
    birth_date BIGINT,
    age INT,
    age_group VARCHAR,
    gender VARCHAR,
    insurance_type VARCHAR,
    payer_category VARCHAR
) WITH (
    KAFKA_TOPIC='snowflake_healthcare_patients',
    VALUE_FORMAT='AVRO'
);

-- Encounters stream
CREATE STREAM IF NOT EXISTS encounters_stream (
    encounter_id VARCHAR KEY,
    patient_id VARCHAR,
    encounter_type VARCHAR,
    admit_datetime BIGINT,
    discharge_datetime BIGINT,
    primary_diagnosis_code VARCHAR,
    drg_code VARCHAR,
    length_of_stay_days INT,
    readmission_flag BOOLEAN,
    total_charges DOUBLE,
    total_payments DOUBLE
) WITH (
    KAFKA_TOPIC='snowflake_healthcare_encounters',
    VALUE_FORMAT='AVRO',
    TIMESTAMP='admit_datetime'
);

-- Lab results stream
CREATE STREAM IF NOT EXISTS lab_results_stream (
    lab_result_id VARCHAR KEY,
    patient_id VARCHAR,
    encounter_id VARCHAR,
    test_name VARCHAR,
    result_numeric DOUBLE,
    abnormal_flag VARCHAR,
    critical_flag BOOLEAN,
    result_datetime BIGINT
) WITH (
    KAFKA_TOPIC='snowflake_healthcare_lab_results',
    VALUE_FORMAT='AVRO',
    TIMESTAMP='result_datetime'
);

-- Medications stream
CREATE STREAM IF NOT EXISTS medications_stream (
    medication_id VARCHAR KEY,
    patient_id VARCHAR,
    medication_name VARCHAR,
    generic_name VARCHAR,
    therapeutic_class VARCHAR,
    start_datetime BIGINT,
    end_datetime BIGINT,
    prescribing_provider_id VARCHAR,
    pharmacy_id VARCHAR,
    is_high_risk BOOLEAN
) WITH (
    KAFKA_TOPIC='snowflake_healthcare_medications',
    VALUE_FORMAT='AVRO'
);

-- Adherence stream
CREATE STREAM IF NOT EXISTS adherence_stream (
    adherence_id VARCHAR KEY,
    patient_id VARCHAR,
    medication_id VARCHAR,
    measurement_date BIGINT,
    pdc_score DOUBLE,
    mpr_score DOUBLE,
    days_until_refill INT,
    adherence_status VARCHAR
) WITH (
    KAFKA_TOPIC='snowflake_healthcare_medication_adherence',
    VALUE_FORMAT='AVRO'
);

-- Vital signs stream
CREATE STREAM IF NOT EXISTS vitals_stream (
    vital_id VARCHAR KEY,
    patient_id VARCHAR,
    encounter_id VARCHAR,
    measurement_datetime BIGINT,
    temperature DOUBLE,
    heart_rate INT,
    respiratory_rate INT,
    bp_systolic INT,
    bp_diastolic INT,
    oxygen_saturation DOUBLE
) WITH (
    KAFKA_TOPIC='snowflake_healthcare_vital_signs',
    VALUE_FORMAT='AVRO',
    TIMESTAMP='measurement_datetime'
);
```

### 4.3 Clinical Operations Agent (Pure SQL)

```sql
-- Real-time census monitoring
CREATE TABLE census_monitoring AS
SELECT
    'FACILITY_001' as facility_id,
    COUNT(*) as current_census,
    COUNT(*) FILTER (WHERE encounter_type = 'inpatient') as inpatient_census,
    COUNT(*) FILTER (WHERE encounter_type = 'emergency') as ed_census,
    250 as total_beds,  -- Configure per facility
    COUNT(*) * 1.0 / 250 as occupancy_rate,
    CASE 
        WHEN COUNT(*) * 1.0 / 250 > 0.95 THEN 'critical'
        WHEN COUNT(*) * 1.0 / 250 > 0.85 THEN 'high'
        ELSE 'normal'
    END as capacity_status
FROM encounters_stream
WHERE discharge_datetime IS NULL
EMIT CHANGES;

-- Capacity alerts
CREATE STREAM capacity_alerts AS
SELECT
    CONCAT('CAP_', CAST(ROWTIME AS VARCHAR)) as alert_id,
    'clinical_ops_agent' as agent_type,
    facility_id,
    'capacity_alert' as alert_type,
    capacity_status as severity,
    CONCAT('Capacity Alert: ', capacity_status, ' - Occupancy: ', 
           CAST(ROUND(occupancy_rate * 100) AS VARCHAR), '%') as message,
    STRUCT(
        current_census := current_census,
        occupancy_rate := occupancy_rate,
        inpatient_census := inpatient_census,
        ed_census := ed_census
    ) as metrics,
    ROWTIME as created_at
FROM census_monitoring
WHERE capacity_status IN ('high', 'critical')
EMIT CHANGES;

-- Readmission monitoring
CREATE TABLE readmission_monitoring AS
SELECT
    patient_id,
    COUNT(*) as admission_count_30d,
    MAX(length_of_stay_days) as max_los_30d,
    COLLECT_LIST(primary_diagnosis_code) as diagnosis_codes,
    CASE
        WHEN COUNT(*) >= 2 THEN 'high'
        WHEN MAX(length_of_stay_days) > 7 THEN 'medium'
        ELSE 'low'
    END as readmission_risk
FROM encounters_stream
WINDOW TUMBLING (SIZE 30 DAYS)
GROUP BY patient_id
HAVING COUNT(*) > 1
EMIT CHANGES;

-- ED throughput monitoring
CREATE TABLE ed_metrics AS
SELECT
    COUNT(*) as ed_census,
    COUNT(*) FILTER (WHERE 
        (ROWTIME - admit_datetime) > 4 * 60 * 60 * 1000  -- 4 hours in ms
    ) as patients_over_4hrs,
    AVG((ROWTIME - admit_datetime) / 1000 / 60) as avg_wait_minutes,
    CASE
        WHEN AVG((ROWTIME - admit_datetime) / 1000 / 60) > 240 THEN 'critical'
        WHEN AVG((ROWTIME - admit_datetime) / 1000 / 60) > 120 THEN 'warning'
        ELSE 'normal'
    END as ed_status
FROM encounters_stream
WHERE encounter_type = 'emergency' 
    AND discharge_datetime IS NULL
WINDOW TUMBLING (SIZE 15 MINUTES)
EMIT CHANGES;
```

### 4.4 Patient Safety Agent (Pure SQL)

```sql
-- SIRS criteria for sepsis detection
CREATE TABLE sepsis_monitoring AS
SELECT
    v.patient_id,
    v.encounter_id,
    -- SIRS criteria
    MAX(CASE WHEN v.temperature > 38 OR v.temperature < 36 THEN 1 ELSE 0 END) as temp_abnormal,
    MAX(CASE WHEN v.heart_rate > 90 THEN 1 ELSE 0 END) as hr_abnormal,
    MAX(CASE WHEN v.respiratory_rate > 20 THEN 1 ELSE 0 END) as rr_abnormal,
    -- Check for abnormal WBC from recent labs
    MAX(CASE WHEN l.test_name = 'WBC' AND 
        (l.result_numeric > 12000 OR l.result_numeric < 4000) THEN 1 ELSE 0 END) as wbc_abnormal,
    -- Calculate SIRS score
    (MAX(CASE WHEN v.temperature > 38 OR v.temperature < 36 THEN 1 ELSE 0 END) +
     MAX(CASE WHEN v.heart_rate > 90 THEN 1 ELSE 0 END) +
     MAX(CASE WHEN v.respiratory_rate > 20 THEN 1 ELSE 0 END) +
     MAX(CASE WHEN l.test_name = 'WBC' AND 
         (l.result_numeric > 12000 OR l.result_numeric < 4000) THEN 1 ELSE 0 END)) as sirs_score,
    -- Get lactate if available
    MAX(CASE WHEN l.test_name = 'Lactate' THEN l.result_numeric ELSE NULL END) as lactate_level
FROM vitals_stream v
LEFT JOIN lab_results_stream l WITHIN 6 HOURS
    ON v.patient_id = l.patient_id
WINDOW TUMBLING (SIZE 2 HOURS)
GROUP BY v.patient_id, v.encounter_id
EMIT CHANGES;

-- Sepsis alerts
CREATE STREAM sepsis_alerts AS
SELECT
    CONCAT('SEPSIS_', patient_id, '_', CAST(ROWTIME AS VARCHAR)) as alert_id,
    'patient_safety_agent' as agent_type,
    patient_id,
    encounter_id,
    'sepsis_risk' as alert_type,
    'critical' as severity,
    CONCAT('Sepsis Alert: SIRS Score ', CAST(sirs_score AS VARCHAR), 
           ', Lactate: ', CAST(lactate_level AS VARCHAR)) as message,
    STRUCT(
        sirs_score := sirs_score,
        lactate_level := lactate_level,
        temp_abnormal := temp_abnormal,
        hr_abnormal := hr_abnormal,
        rr_abnormal := rr_abnormal,
        wbc_abnormal := wbc_abnormal
    ) as metrics,
    ROWTIME as created_at
FROM sepsis_monitoring
WHERE sirs_score >= 2 
    AND (lactate_level > 2 OR lactate_level IS NULL)
EMIT CHANGES;

-- Critical lab monitoring
CREATE STREAM critical_lab_alerts AS
SELECT
    CONCAT('LAB_', lab_result_id) as alert_id,
    'patient_safety_agent' as agent_type,
    patient_id,
    encounter_id,
    'critical_lab' as alert_type,
    'critical' as severity,
    CONCAT('Critical Lab: ', test_name, ' = ', CAST(result_numeric AS VARCHAR)) as message,
    STRUCT(
        test_name := test_name,
        result_value := result_numeric,
        abnormal_flag := abnormal_flag
    ) as metrics,
    result_datetime as created_at
FROM lab_results_stream
WHERE critical_flag = true
EMIT CHANGES;

-- Fall risk monitoring (simplified)
CREATE TABLE fall_risk_assessment AS
SELECT
    patient_id,
    MAX(age) as patient_age,
    COUNT(DISTINCT medication_id) as medication_count,
    MAX(CASE WHEN therapeutic_class LIKE '%sedative%' 
        OR therapeutic_class LIKE '%hypnotic%' THEN 1 ELSE 0 END) as has_sedatives,
    CASE
        WHEN MAX(age) > 65 AND COUNT(DISTINCT medication_id) > 5 THEN 'high'
        WHEN MAX(age) > 65 OR COUNT(DISTINCT medication_id) > 8 THEN 'medium'
        ELSE 'low'
    END as fall_risk_level
FROM patients_stream p
JOIN medications_stream m ON p.patient_id = m.patient_id
WHERE m.end_datetime IS NULL
WINDOW TUMBLING (SIZE 1 DAY)
GROUP BY patient_id
EMIT CHANGES;
```

### 4.5 Pharmacy Agent (Pure SQL)

```sql
-- Medication adherence monitoring
CREATE TABLE adherence_monitoring AS
SELECT
    patient_id,
    medication_id,
    LATEST_BY_OFFSET(pdc_score) as current_pdc,
    LATEST_BY_OFFSET(days_until_refill) as days_to_refill,
    LATEST_BY_OFFSET(adherence_status) as status,
    CASE
        WHEN LATEST_BY_OFFSET(pdc_score) < 0.4 THEN 'critical'
        WHEN LATEST_BY_OFFSET(pdc_score) < 0.8 THEN 'warning'
        ELSE 'good'
    END as adherence_level
FROM adherence_stream
WINDOW SESSION (30 MINUTES)
GROUP BY patient_id, medication_id
EMIT CHANGES;

-- Non-adherence alerts
CREATE STREAM adherence_alerts AS
SELECT
    CONCAT('ADH_', patient_id, '_', medication_id) as alert_id,
    'pharmacy_agent' as agent_type,
    patient_id,
    medication_id,
    'adherence_issue' as alert_type,
    adherence_level as severity,
    CONCAT('Adherence Alert: PDC = ', CAST(ROUND(current_pdc * 100) AS VARCHAR), 
           '% for medication ', medication_id) as message,
    STRUCT(
        pdc_score := current_pdc,
        days_to_refill := days_to_refill,
        adherence_status := status
    ) as metrics,
    ROWTIME as created_at
FROM adherence_monitoring
WHERE adherence_level IN ('warning', 'critical')
EMIT CHANGES;

-- Drug interaction detection (simplified without external reference)
-- In production, would join with drug interaction reference table
CREATE STREAM potential_interactions AS
SELECT
    m1.patient_id,
    CONCAT('INTERACTION_', m1.patient_id, '_', CAST(ROWTIME AS VARCHAR)) as alert_id,
    'pharmacy_agent' as agent_type,
    'drug_interaction' as alert_type,
    CASE 
        WHEN m1.is_high_risk AND m2.is_high_risk THEN 'high'
        ELSE 'medium'
    END as severity,
    CONCAT('Potential interaction: ', m1.medication_name, ' + ', m2.medication_name) as message,
    STRUCT(
        drug1 := m1.medication_name,
        drug2 := m2.medication_name,
        both_high_risk := (m1.is_high_risk AND m2.is_high_risk)
    ) as metrics,
    ROWTIME as created_at
FROM medications_stream m1
JOIN medications_stream m2 WITHIN 1 HOUR
    ON m1.patient_id = m2.patient_id
WHERE m1.medication_id < m2.medication_id
    AND m1.end_datetime IS NULL
    AND m2.end_datetime IS NULL
    AND (m1.is_high_risk OR m2.is_high_risk)
EMIT CHANGES;

-- Refill reminder generation
CREATE STREAM refill_reminders AS
SELECT
    CONCAT('REFILL_', patient_id, '_', medication_id) as alert_id,
    'pharmacy_agent' as agent_type,
    patient_id,
    medication_id,
    'refill_due' as alert_type,
    CASE
        WHEN days_to_refill <= 3 THEN 'high'
        WHEN days_to_refill <= 7 THEN 'medium'
        ELSE 'low'
    END as severity,
    CONCAT('Refill needed in ', CAST(days_to_refill AS VARCHAR), ' days') as message,
    STRUCT(
        days_to_refill := days_to_refill,
        adherence_score := current_pdc
    ) as metrics,
    ROWTIME as created_at
FROM adherence_monitoring
WHERE days_to_refill <= 7 
    AND days_to_refill > 0
EMIT CHANGES;
```

### 4.6 Agent Coordination Layer

```sql
-- Unified alert stream from all agents
CREATE STREAM all_alerts AS
SELECT * FROM capacity_alerts
UNION ALL
SELECT * FROM sepsis_alerts
UNION ALL
SELECT * FROM critical_lab_alerts
UNION ALL
SELECT * FROM adherence_alerts
UNION ALL
SELECT * FROM potential_interactions
UNION ALL
SELECT * FROM refill_reminders
EMIT CHANGES;

-- Patient alert aggregation
CREATE TABLE patient_alert_summary AS
SELECT
    patient_id,
    COUNT(*) as total_alerts,
    COUNT(DISTINCT agent_type) as agents_alerting,
    COLLECT_LIST(agent_type) as agent_list,
    COLLECT_LIST(alert_type) as alert_types,
    MAX(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) as has_critical,
    MAX(CASE WHEN severity = 'high' THEN 1 ELSE 0 END) as has_high
FROM all_alerts
WINDOW TUMBLING (SIZE 1 HOUR)
GROUP BY patient_id
EMIT CHANGES;

-- Multi-agent coordination triggers
CREATE STREAM coordination_triggers AS
SELECT
    patient_id,
    CONCAT('COORD_', patient_id, '_', CAST(ROWTIME AS VARCHAR)) as coordination_id,
    'multi_agent_response' as action_type,
    CASE
        WHEN has_critical = 1 AND agents_alerting >= 2 THEN 'immediate'
        WHEN has_high = 1 AND agents_alerting >= 3 THEN 'urgent'
        WHEN agents_alerting >= 3 THEN 'review'
        ELSE 'monitor'
    END as response_level,
    CONCAT('Multiple alerts: ', ARRAY_JOIN(agent_list, ', ')) as description,
    total_alerts,
    agents_alerting,
    ROWTIME as created_at
FROM patient_alert_summary
WHERE agents_alerting >= 2 OR has_critical = 1
EMIT CHANGES;

-- Pattern detection for deteriorating patients
CREATE TABLE deterioration_detection AS
SELECT
    patient_id,
    COUNT(*) as alert_count_1hr,
    COUNT(DISTINCT alert_type) as unique_alert_types,
    COUNT(*) FILTER (WHERE severity IN ('critical', 'high')) as severe_alerts,
    CASE
        WHEN COUNT(*) FILTER (WHERE severity = 'critical') >= 2 THEN 'rapid_deterioration'
        WHEN COUNT(*) >= 5 THEN 'deteriorating'
        WHEN COUNT(*) >= 3 AND COUNT(DISTINCT agent_type) >= 2 THEN 'concerning'
        ELSE 'stable'
    END as patient_status
FROM all_alerts
WINDOW TUMBLING (SIZE 1 HOUR)
GROUP BY patient_id
HAVING COUNT(*) >= 3
EMIT CHANGES;
```

### 4.7 Action Generation and Human Oversight

```sql
-- Agent actions table (what agents decide to do)
CREATE STREAM agent_actions (
    action_id VARCHAR KEY,
    agent_type VARCHAR,
    patient_id VARCHAR,
    action_category VARCHAR,
    action_description VARCHAR,
    confidence_score DOUBLE,
    requires_approval BOOLEAN,
    created_at BIGINT
) WITH (
    KAFKA_TOPIC='agent_actions',
    VALUE_FORMAT='JSON'
);

-- Generate actions from alerts
CREATE STREAM generated_actions AS
SELECT
    alert_id as action_id,
    agent_type,
    patient_id,
    CASE alert_type
        WHEN 'sepsis_risk' THEN 'clinical_protocol'
        WHEN 'adherence_issue' THEN 'patient_outreach'
        WHEN 'drug_interaction' THEN 'medication_review'
        WHEN 'capacity_alert' THEN 'resource_management'
        ELSE 'monitoring'
    END as action_category,
    CASE 
        WHEN alert_type = 'sepsis_risk' THEN 'Initiate sepsis bundle'
        WHEN alert_type = 'adherence_issue' THEN 'Contact patient for adherence counseling'
        WHEN alert_type = 'drug_interaction' THEN 'Review medications with prescriber'
        WHEN alert_type = 'capacity_alert' THEN 'Activate surge protocol'
        ELSE message
    END as action_description,
    CASE severity
        WHEN 'critical' THEN 0.95
        WHEN 'high' THEN 0.85
        WHEN 'medium' THEN 0.70
        ELSE 0.50
    END as confidence_score,
    severity = 'critical' as requires_approval,
    created_at
FROM all_alerts
EMIT CHANGES;

-- Actions requiring human approval
CREATE TABLE pending_approvals AS
SELECT
    action_id,
    agent_type,
    patient_id,
    action_category,
    action_description,
    confidence_score,
    created_at as submitted_at
FROM generated_actions
WHERE requires_approval = true
EMIT CHANGES;
```

### 4.8 Output Connectors

```sql
-- Send critical alerts to notification system
CREATE SINK CONNECTOR alert_notifications WITH (
    'connector.class' = 'io.confluent.connect.http.HttpSinkConnector',
    'http.api.url' = 'https://hospital-api.com/notifications',
    'topics.regex' = '.*alerts',
    'tasks.max' = '4',
    'key.converter' = 'org.apache.kafka.connect.storage.StringConverter',
    'value.converter' = 'io.confluent.connect.json.JsonConverter',
    'value.converter.schemas.enable' = 'false',
    'reporter.bootstrap.servers' = 'kafka:9092',
    'reporter.error.topic.name' = 'error-responses',
    'reporter.result.topic.name' = 'success-responses'
);

-- Write all events back to Snowflake for analytics
CREATE SINK CONNECTOR snowflake_sink WITH (
    'connector.class' = 'com.snowflake.kafka.connector.SnowflakeSinkConnector',
    'snowflake.url.name' = 'your-account.snowflakecomputing.com',
    'snowflake.user.name' = 'KSQL_USER',
    'snowflake.private.key' = '${file:/secrets/snowflake_key.p8}',
    'snowflake.database.name' = 'HEALTHCARE_PROD',
    'snowflake.schema.name' = 'AGENT_OUTPUTS',
    'topics' = 'all_alerts,generated_actions,coordination_triggers',
    'tasks.max' = '8',
    'buffer.count.records' = '10000',
    'buffer.flush.time' = '60'
);
```

---

## Phase 5: Deployment and Operations

### 5.1 Infrastructure as Code

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Kafka ecosystem
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    volumes:
      - zookeeper-data:/var/lib/zookeeper/data
      - zookeeper-logs:/var/lib/zookeeper/log

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
    volumes:
      - kafka-data:/var/lib/kafka/data

  schema-registry:
    image: confluentinc/cp-schema-registry:7.5.0
    depends_on:
      - kafka
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: kafka:9092

  ksqldb-server:
    image: confluentinc/cp-ksqldb-server:7.5.0
    depends_on:
      - kafka
      - schema-registry
    ports:
      - "8088:8088"
    environment:
      KSQL_BOOTSTRAP_SERVERS: kafka:9092
      KSQL_LISTENERS: http://0.0.0.0:8088
      KSQL_KSQL_SCHEMA_REGISTRY_URL: http://schema-registry:8081
      KSQL_KSQL_SERVICE_ID: healthcare_ksql
      KSQL_KSQL_QUERIES_FILE: /queries/agents.sql
    volumes:
      - ./ksql-queries:/queries

  ksqldb-cli:
    image: confluentinc/cp-ksqldb-cli:7.5.0
    depends_on:
      - ksqldb-server
    entrypoint: /bin/sh
    tty: true

  kafka-connect:
    image: confluentinc/cp-kafka-connect:7.5.0
    depends_on:
      - kafka
      - schema-registry
    ports:
      - "8083:8083"
    environment:
      CONNECT_BOOTSTRAP_SERVERS: kafka:9092
      CONNECT_REST_PORT: 8083
      CONNECT_GROUP_ID: healthcare-connect
      CONNECT_CONFIG_STORAGE_TOPIC: connect-configs
      CONNECT_OFFSET_STORAGE_TOPIC: connect-offsets
      CONNECT_STATUS_STORAGE_TOPIC: connect-status
      CONNECT_KEY_CONVERTER: io.confluent.connect.avro.AvroConverter
      CONNECT_VALUE_CONVERTER: io.confluent.connect.avro.AvroConverter
      CONNECT_KEY_CONVERTER_SCHEMA_REGISTRY_URL: http://schema-registry:8081
      CONNECT_VALUE_CONVERTER_SCHEMA_REGISTRY_URL: http://schema-registry:8081
      CONNECT_PLUGIN_PATH: /usr/share/java,/usr/share/confluent-hub-components
    volumes:
      - ./connectors:/usr/share/confluent-hub-components
    command:
      - bash
      - -c
      - |
        confluent-hub install --no-prompt snowflakeinc/snowflake-kafka-connector:latest
        confluent-hub install --no-prompt confluentinc/kafka-connect-http:latest
        /etc/confluent/docker/run

  # MCP Server
  mcp-server:
    build: ./mcp
    ports:
      - "3000:3000"
    environment:
      DBT_HOST: cloud.getdbt.com
      DBT_ACCOUNT_ID: ${DBT_ACCOUNT_ID}
      DBT_PROJECT_ID: ${DBT_PROJECT_ID}
      DBT_ENVIRONMENT_ID: ${DBT_ENVIRONMENT_ID}
      DBT_TOKEN: ${DBT_TOKEN}
    restart: unless-stopped

  # Monitoring
  control-center:
    image: confluentinc/cp-enterprise-control-center:7.5.0
    depends_on:
      - kafka
      - schema-registry
      - ksqldb-server
    ports:
      - "9021:9021"
    environment:
      CONTROL_CENTER_BOOTSTRAP_SERVERS: kafka:9092
      CONTROL_CENTER_KSQL_KSQLDB1_URL: http://ksqldb-server:8088
      CONTROL_CENTER_KSQL_KSQLDB1_ADVERTISED_URL: http://localhost:8088
      CONTROL_CENTER_SCHEMA_REGISTRY_URL: http://schema-registry:8081
      CONTROL_CENTER_REPLICATION_FACTOR: 1

volumes:
  zookeeper-data:
  zookeeper-logs:
  kafka-data:
```

### 5.2 Monitoring Dashboard

```sql
-- Agent performance monitoring in KSQLDB
CREATE TABLE agent_performance AS
SELECT
    agent_type,
    COUNT(*) as alerts_generated,
    COUNT(DISTINCT patient_id) as patients_monitored,
    COUNT(*) FILTER (WHERE severity = 'critical') as critical_alerts,
    COUNT(*) FILTER (WHERE severity = 'high') as high_alerts,
    AVG(CASE WHEN severity = 'critical' THEN 1.0
             WHEN severity = 'high' THEN 0.75
             WHEN severity = 'medium' THEN 0.5
             ELSE 0.25 END) as avg_severity_score
FROM all_alerts
WINDOW TUMBLING (SIZE 1 HOUR)
GROUP BY agent_type
EMIT CHANGES;

-- System health metrics
CREATE TABLE system_health AS
SELECT
    COUNT(*) as total_alerts_per_hour,
    COUNT(DISTINCT patient_id) as active_patients,
    COUNT(DISTINCT agent_type) as active_agents,
    COUNT(*) FILTER (WHERE severity = 'critical') as critical_count,
    AVG(CASE 
        WHEN alert_type = 'capacity_alert' THEN 1.0 
        ELSE 0.0 
    END) as capacity_pressure
FROM all_alerts
WINDOW TUMBLING (SIZE 1 HOUR)
EMIT CHANGES;
```

---

## Phase 6: Testing and Validation

### 6.1 Data Quality Tests in dbt

```sql
-- tests/assert_patient_age_valid.sql
SELECT *
FROM {{ ref('stg_patients') }}
WHERE age < 0 OR age > 120

-- tests/assert_los_positive.sql
SELECT *
FROM {{ ref('stg_encounters') }}
WHERE length_of_stay_days < 0

-- tests/assert_adherence_range.sql
SELECT *
FROM {{ source('ehr', 'medication_adherence') }}
WHERE pdc_score < 0 OR pdc_score > 1
```

### 6.2 Agent Testing in KSQLDB

```sql
-- Test sepsis detection logic
CREATE STREAM test_sepsis_scenario AS
SELECT
    'TEST_001' as patient_id,
    'ENC_001' as encounter_id,
    39.5 as temperature,  -- Fever
    95 as heart_rate,     -- Elevated
    22 as respiratory_rate, -- Elevated
    120 as bp_systolic,
    80 as bp_diastolic,
    95.0 as oxygen_saturation,
    ROWTIME as measurement_datetime
FROM vitals_stream
WHERE false;  -- Empty stream for testing

-- Insert test data
INSERT INTO test_sepsis_scenario VALUES (
    'TEST_001', 'ENC_001', 39.5, 95, 22, 120, 80, 95.0, ROWTIME
);

-- Verify alert generation
SELECT * FROM sepsis_alerts WHERE patient_id = 'TEST_001';
```

---

## Learning Roadmap: From Zero to Autonomous Healthcare Analytics

### 🚀 Choose Your Path: Serverless vs Local

#### Option A: Serverless (Recommended - Zero Installation)
**Everything runs in the cloud - you only need a browser!**

**Services to Sign Up For:**
1. **Snowflake** - https://signup.snowflake.com (30-day trial)
2. **dbt Cloud** - https://www.getdbt.com/signup (Free developer plan)
3. **Confluent Cloud** - https://confluent.cloud ($400 credits trial)

**Advantages:**
- Zero local installation
- Works on any computer (Windows/Mac/Linux/Chromebook)
- No Docker, Python, or WSL2 needed
- IT-friendly (no software to approve)
- Always up-to-date

**When to Use:**
- Corporate environments with installation restrictions
- Quick POCs and demos
- Learning the concepts
- Production deployments

#### Option B: Local Development (For Deep Learning)
**Run everything locally for complete control**

**Requirements:**
- Docker Desktop
- Python/Anaconda
- WSL2 (Windows only)
- 16GB+ RAM recommended

**When to Use:**
- Learning the underlying infrastructure
- Debugging complex issues
- Offline development
- Cost-sensitive development

---

### Serverless Path: Week-by-Week Guide

#### Week 1: Cloud Setup (All in Browser)

**Day 1: Account Creation**
```
1. Snowflake Trial
   - Go to: https://signup.snowflake.com
   - Choose: Enterprise Edition, 30-day trial
   - Save: Account URL, Username, Password

2. dbt Cloud
   - Go to: https://www.getdbt.com/signup  
   - Choose: Developer plan (free)
   - Save: Account ID (from URL after login)

3. Confluent Cloud
   - Go to: https://confluent.cloud
   - Start: Free trial ($400 credits)
   - Save: Cluster endpoint, API keys
```

**Day 2-3: Snowflake Setup with Sample Healthcare Data**
```sql
-- In Snowflake Web UI (Worksheets)
-- Run this complete script to set up everything with test data

USE ROLE ACCOUNTADMIN;

-- Create database
CREATE DATABASE IF NOT EXISTS HEALTHCARE_PROD;
USE DATABASE HEALTHCARE_PROD;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS RAW;
CREATE SCHEMA IF NOT EXISTS STAGING;
CREATE SCHEMA IF NOT EXISTS MARTS;

-- Use RAW schema for source data
USE SCHEMA RAW;

-- 1. PATIENTS TABLE WITH TEST DATA
CREATE OR REPLACE TABLE patients (
    patient_id VARCHAR(50),
    mrn VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    gender VARCHAR(10),
    race VARCHAR(50),
    ethnicity VARCHAR(50),
    primary_language VARCHAR(50),
    zip_code VARCHAR(10),
    insurance_type VARCHAR(50),
    insurance_plan VARCHAR(100),
    primary_care_provider_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Insert 50 test patients with realistic distribution
INSERT INTO patients 
SELECT * FROM VALUES
    -- Elderly Medicare patients (high utilization)
    ('P001', 'MRN001', 'John', 'Smith', '1945-03-15', 'Male', 'White', 'Non-Hispanic', 'English', '02139', 'Medicare', 'Medicare Advantage', 'DR001', CURRENT_TIMESTAMP()),
    ('P002', 'MRN002', 'Mary', 'Johnson', '1948-07-22', 'Female', 'White', 'Non-Hispanic', 'English', '02142', 'Medicare', 'Traditional Medicare', 'DR001', CURRENT_TIMESTAMP()),
    ('P003', 'MRN003', 'James', 'Williams', '1950-11-08', 'Male', 'Black', 'Non-Hispanic', 'English', '02144', 'Medicare', 'Medicare Advantage', 'DR002', CURRENT_TIMESTAMP()),
    ('P004', 'MRN004', 'Patricia', 'Brown', '1942-05-30', 'Female', 'White', 'Hispanic', 'Spanish', '02145', 'Medicare', 'Traditional Medicare', 'DR002', CURRENT_TIMESTAMP()),
    ('P005', 'MRN005', 'Robert', 'Jones', '1946-09-12', 'Male', 'White', 'Non-Hispanic', 'English', '02140', 'Medicare', 'Medicare Advantage', 'DR003', CURRENT_TIMESTAMP()),
    
    -- Working age commercial insurance
    ('P006', 'MRN006', 'Jennifer', 'Garcia', '1975-04-18', 'Female', 'White', 'Hispanic', 'English', '02139', 'Commercial', 'BCBS PPO', 'DR001', CURRENT_TIMESTAMP()),
    ('P007', 'MRN007', 'Michael', 'Miller', '1980-08-25', 'Male', 'Asian', 'Non-Hispanic', 'English', '02142', 'Commercial', 'Aetna HMO', 'DR002', CURRENT_TIMESTAMP()),
    ('P008', 'MRN008', 'Linda', 'Davis', '1978-12-03', 'Female', 'Black', 'Non-Hispanic', 'English', '02144', 'Commercial', 'United PPO', 'DR003', CURRENT_TIMESTAMP()),
    ('P009', 'MRN009', 'David', 'Rodriguez', '1982-06-14', 'Male', 'White', 'Hispanic', 'Spanish', '02145', 'Commercial', 'Cigna PPO', 'DR001', CURRENT_TIMESTAMP()),
    ('P010', 'MRN010', 'Sarah', 'Martinez', '1985-10-27', 'Female', 'White', 'Hispanic', 'English', '02140', 'Commercial', 'BCBS HMO', 'DR002', CURRENT_TIMESTAMP()),
    
    -- Medicaid patients
    ('P011', 'MRN011', 'Christopher', 'Anderson', '1990-02-11', 'Male', 'White', 'Non-Hispanic', 'English', '02139', 'Medicaid', 'MassHealth', 'DR003', CURRENT_TIMESTAMP()),
    ('P012', 'MRN012', 'Jessica', 'Taylor', '1988-07-08', 'Female', 'Black', 'Non-Hispanic', 'English', '02142', 'Medicaid', 'MassHealth', 'DR001', CURRENT_TIMESTAMP()),
    ('P013', 'MRN013', 'Daniel', 'Thomas', '1992-11-19', 'Male', 'White', 'Non-Hispanic', 'English', '02144', 'Medicaid', 'MassHealth', 'DR002', CURRENT_TIMESTAMP()),
    ('P014', 'MRN014', 'Ashley', 'Jackson', '1995-03-25', 'Female', 'Black', 'Non-Hispanic', 'English', '02145', 'Medicaid', 'MassHealth', 'DR003', CURRENT_TIMESTAMP()),
    ('P015', 'MRN015', 'Matthew', 'White', '1993-09-05', 'Male', 'White', 'Non-Hispanic', 'English', '02140', 'Medicaid', 'MassHealth', 'DR001', CURRENT_TIMESTAMP()),
    
    -- Add more for realistic volume
    ('P016', 'MRN016', 'Emily', 'Harris', '1955-01-12', 'Female', 'White', 'Non-Hispanic', 'English', '02139', 'Medicare', 'Medicare Advantage', 'DR002', CURRENT_TIMESTAMP()),
    ('P017', 'MRN017', 'Joshua', 'Martin', '1979-05-28', 'Male', 'Asian', 'Non-Hispanic', 'Mandarin', '02142', 'Commercial', 'Aetna PPO', 'DR003', CURRENT_TIMESTAMP()),
    ('P018', 'MRN018', 'Amanda', 'Thompson', '1987-08-15', 'Female', 'White', 'Non-Hispanic', 'English', '02144', 'Commercial', 'United HMO', 'DR001', CURRENT_TIMESTAMP()),
    ('P019', 'MRN019', 'Andrew', 'Lee', '1991-12-22', 'Male', 'Asian', 'Non-Hispanic', 'English', '02145', 'Medicaid', 'MassHealth', 'DR002', CURRENT_TIMESTAMP()),
    ('P020', 'MRN020', 'Brittany', 'Clark', '1994-04-07', 'Female', 'Black', 'Non-Hispanic', 'English', '02140', 'Medicaid', 'MassHealth', 'DR003', CURRENT_TIMESTAMP());

-- 2. ENCOUNTERS TABLE WITH REALISTIC PATTERNS
CREATE OR REPLACE TABLE encounters (
    encounter_id VARCHAR(50),
    patient_id VARCHAR(50),
    encounter_type VARCHAR(50),
    admit_datetime TIMESTAMP,
    discharge_datetime TIMESTAMP,
    facility VARCHAR(50),
    department VARCHAR(50),
    attending_provider_id VARCHAR(50),
    primary_diagnosis_code VARCHAR(10),
    primary_diagnosis_desc VARCHAR(200),
    drg_code VARCHAR(10),
    length_of_stay_days INTEGER,
    total_charges DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Insert encounters with readmission patterns
INSERT INTO encounters
SELECT * FROM VALUES
    -- Patient P001 - Frequent readmissions (high risk)
    ('E001', 'P001', 'Inpatient', '2024-01-05 08:30:00', '2024-01-10 14:00:00', 'Main Hospital', 'Cardiology', 'DR001', 'I50.9', 'Heart failure, unspecified', '291', 5, 45000.00, CURRENT_TIMESTAMP()),
    ('E002', 'P001', 'Emergency', '2024-01-25 22:15:00', '2024-01-26 06:00:00', 'Main Hospital', 'Emergency', 'DR004', 'R07.9', 'Chest pain, unspecified', NULL, 0, 5500.00, CURRENT_TIMESTAMP()),
    ('E003', 'P001', 'Inpatient', '2024-01-26 06:00:00', '2024-01-30 16:00:00', 'Main Hospital', 'Cardiology', 'DR001', 'I50.9', 'Heart failure, unspecified', '291', 4, 38000.00, CURRENT_TIMESTAMP()),
    ('E004', 'P001', 'Outpatient', '2024-02-15 10:00:00', '2024-02-15 11:30:00', 'Main Hospital', 'Cardiology', 'DR001', 'Z09', 'Follow-up examination', NULL, 0, 350.00, CURRENT_TIMESTAMP()),
    ('E005', 'P001', 'Inpatient', '2024-02-28 14:20:00', '2024-03-05 10:00:00', 'Main Hospital', 'Cardiology', 'DR001', 'I50.9', 'Heart failure, unspecified', '291', 5, 52000.00, CURRENT_TIMESTAMP()),
    
    -- Patient P002 - Regular care, well-controlled
    ('E006', 'P002', 'Outpatient', '2024-01-10 09:00:00', '2024-01-10 10:00:00', 'Main Hospital', 'Primary Care', 'DR001', 'E11.9', 'Type 2 diabetes', NULL, 0, 250.00, CURRENT_TIMESTAMP()),
    ('E007', 'P002', 'Outpatient', '2024-02-10 09:00:00', '2024-02-10 10:00:00', 'Main Hospital', 'Primary Care', 'DR001', 'E11.9', 'Type 2 diabetes', NULL, 0, 250.00, CURRENT_TIMESTAMP()),
    ('E008', 'P002', 'Outpatient', '2024-03-10 09:00:00', '2024-03-10 10:00:00', 'Main Hospital', 'Primary Care', 'DR001', 'E11.9', 'Type 2 diabetes', NULL, 0, 250.00, CURRENT_TIMESTAMP()),
    
    -- Patient P003 - Emergency visit with admission
    ('E009', 'P003', 'Emergency', '2024-02-01 03:45:00', '2024-02-01 08:00:00', 'Main Hospital', 'Emergency', 'DR004', 'J44.0', 'COPD with acute exacerbation', NULL, 0, 8500.00, CURRENT_TIMESTAMP()),
    ('E010', 'P003', 'Inpatient', '2024-02-01 08:00:00', '2024-02-06 14:00:00', 'Main Hospital', 'Pulmonology', 'DR002', 'J44.0', 'COPD with acute exacerbation', '190', 5, 42000.00, CURRENT_TIMESTAMP()),
    
    -- Patient P006 - Maternity care
    ('E011', 'P006', 'Outpatient', '2024-01-15 14:00:00', '2024-01-15 15:00:00', 'Main Hospital', 'Obstetrics', 'DR003', 'Z34.00', 'Prenatal care', NULL, 0, 400.00, CURRENT_TIMESTAMP()),
    ('E012', 'P006', 'Outpatient', '2024-02-15 14:00:00', '2024-02-15 15:00:00', 'Main Hospital', 'Obstetrics', 'DR003', 'Z34.00', 'Prenatal care', NULL, 0, 400.00, CURRENT_TIMESTAMP()),
    ('E013', 'P006', 'Inpatient', '2024-03-20 06:00:00', '2024-03-22 18:00:00', 'Main Hospital', 'Obstetrics', 'DR003', 'O80', 'Normal delivery', '767', 2, 18000.00, CURRENT_TIMESTAMP()),
    
    -- Add more varied encounters
    ('E014', 'P007', 'Outpatient', '2024-01-20 11:00:00', '2024-01-20 12:00:00', 'Main Hospital', 'Orthopedics', 'DR002', 'M79.3', 'Myalgia', NULL, 0, 450.00, CURRENT_TIMESTAMP()),
    ('E015', 'P008', 'Emergency', '2024-02-05 19:30:00', '2024-02-06 02:00:00', 'Main Hospital', 'Emergency', 'DR004', 'S52.5', 'Fracture of radius', NULL, 0, 12000.00, CURRENT_TIMESTAMP()),
    ('E016', 'P011', 'Emergency', '2024-01-18 23:00:00', '2024-01-19 04:00:00', 'Main Hospital', 'Emergency', 'DR004', 'K92.2', 'Gastrointestinal hemorrhage', NULL, 0, 9500.00, CURRENT_TIMESTAMP()),
    ('E017', 'P011', 'Inpatient', '2024-01-19 04:00:00', '2024-01-22 16:00:00', 'Main Hospital', 'Gastroenterology', 'DR001', 'K92.2', 'Gastrointestinal hemorrhage', '378', 3, 28000.00, CURRENT_TIMESTAMP()),
    ('E018', 'P012', 'Outpatient', '2024-02-22 13:00:00', '2024-02-22 14:00:00', 'Main Hospital', 'Psychiatry', 'DR003', 'F32.9', 'Major depressive disorder', NULL, 0, 350.00, CURRENT_TIMESTAMP()),
    ('E019', 'P013', 'Telehealth', '2024-03-01 10:00:00', '2024-03-01 10:30:00', 'Virtual', 'Primary Care', 'DR001', 'Z00.00', 'General examination', NULL, 0, 150.00, CURRENT_TIMESTAMP()),
    ('E020', 'P014', 'Outpatient', '2024-02-28 15:00:00', '2024-02-28 16:00:00', 'Main Hospital', 'Endocrinology', 'DR002', 'E10.9', 'Type 1 diabetes', NULL, 0, 475.00, CURRENT_TIMESTAMP());

-- 3. LAB RESULTS TABLE
CREATE OR REPLACE TABLE lab_results (
    lab_id VARCHAR(50),
    patient_id VARCHAR(50),
    encounter_id VARCHAR(50),
    test_code VARCHAR(20),
    test_name VARCHAR(200),
    result_value VARCHAR(100),
    result_numeric DECIMAL(10,2),
    result_unit VARCHAR(50),
    reference_low DECIMAL(10,2),
    reference_high DECIMAL(10,2),
    abnormal_flag VARCHAR(20),
    critical_flag BOOLEAN,
    result_datetime TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Insert lab results including critical values
INSERT INTO lab_results
SELECT * FROM VALUES
    -- P001 labs showing deterioration
    ('L001', 'P001', 'E001', 'BNP', 'B-type Natriuretic Peptide', '850', 850, 'pg/mL', 0, 100, 'High', FALSE, '2024-01-05 10:00:00', CURRENT_TIMESTAMP()),
    ('L002', 'P001', 'E001', 'CR', 'Creatinine', '2.1', 2.1, 'mg/dL', 0.6, 1.2, 'High', FALSE, '2024-01-05 10:00:00', CURRENT_TIMESTAMP()),
    ('L003', 'P001', 'E003', 'BNP', 'B-type Natriuretic Peptide', '1250', 1250, 'pg/mL', 0, 100, 'Critical', TRUE, '2024-01-26 08:00:00', CURRENT_TIMESTAMP()),
    ('L004', 'P001', 'E003', 'K', 'Potassium', '6.2', 6.2, 'mEq/L', 3.5, 5.0, 'Critical', TRUE, '2024-01-26 08:00:00', CURRENT_TIMESTAMP()),
    
    -- P002 routine diabetes monitoring
    ('L005', 'P002', 'E006', 'A1C', 'Hemoglobin A1C', '6.8', 6.8, '%', 4.0, 5.6, 'High', FALSE, '2024-01-10 09:30:00', CURRENT_TIMESTAMP()),
    ('L006', 'P002', 'E006', 'GLU', 'Glucose', '142', 142, 'mg/dL', 70, 100, 'High', FALSE, '2024-01-10 09:30:00', CURRENT_TIMESTAMP()),
    ('L007', 'P002', 'E007', 'GLU', 'Glucose', '128', 128, 'mg/dL', 70, 100, 'High', FALSE, '2024-02-10 09:30:00', CURRENT_TIMESTAMP()),
    ('L008', 'P002', 'E008', 'A1C', 'Hemoglobin A1C', '6.5', 6.5, '%', 4.0, 5.6, 'High', FALSE, '2024-03-10 09:30:00', CURRENT_TIMESTAMP()),
    
    -- P003 COPD exacerbation labs
    ('L009', 'P003', 'E009', 'WBC', 'White Blood Cell Count', '18.5', 18.5, 'K/uL', 4.5, 11.0, 'High', FALSE, '2024-02-01 04:00:00', CURRENT_TIMESTAMP()),
    ('L010', 'P003', 'E009', 'CRP', 'C-Reactive Protein', '125', 125, 'mg/L', 0, 10, 'High', FALSE, '2024-02-01 04:00:00', CURRENT_TIMESTAMP()),
    ('L011', 'P003', 'E010', 'ABG_PO2', 'Arterial PO2', '58', 58, 'mmHg', 80, 100, 'Critical', TRUE, '2024-02-01 08:30:00', CURRENT_TIMESTAMP()),
    
    -- More routine labs
    ('L012', 'P006', 'E011', 'HCG', 'Human Chorionic Gonadotropin', '25000', 25000, 'mIU/mL', NULL, NULL, 'Normal', FALSE, '2024-01-15 14:30:00', CURRENT_TIMESTAMP()),
    ('L013', 'P007', 'E014', 'ESR', 'Erythrocyte Sedimentation Rate', '45', 45, 'mm/hr', 0, 20, 'High', FALSE, '2024-01-20 11:30:00', CURRENT_TIMESTAMP()),
    ('L014', 'P011', 'E016', 'HGB', 'Hemoglobin', '7.2', 7.2, 'g/dL', 12.0, 16.0, 'Critical', TRUE, '2024-01-18 23:30:00', CURRENT_TIMESTAMP()),
    ('L015', 'P011', 'E017', 'HGB', 'Hemoglobin', '9.8', 9.8, 'g/dL', 12.0, 16.0, 'Low', FALSE, '2024-01-20 08:00:00', CURRENT_TIMESTAMP());

-- 4. MEDICATIONS TABLE
CREATE OR REPLACE TABLE medications (
    medication_id VARCHAR(50),
    patient_id VARCHAR(50),
    encounter_id VARCHAR(50),
    medication_name VARCHAR(200),
    generic_name VARCHAR(200),
    dosage VARCHAR(100),
    route VARCHAR(50),
    frequency VARCHAR(50),
    start_datetime TIMESTAMP,
    end_datetime TIMESTAMP,
    prescribing_provider_id VARCHAR(50),
    is_high_risk BOOLEAN,
    therapeutic_class VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Insert medications with interaction potential
INSERT INTO medications
SELECT * FROM VALUES
    -- P001 complex cardiac regimen
    ('M001', 'P001', 'E001', 'Lasix', 'Furosemide', '40mg', 'Oral', 'BID', '2024-01-05 14:00:00', NULL, 'DR001', FALSE, 'Diuretic', CURRENT_TIMESTAMP()),
    ('M002', 'P001', 'E001', 'Coreg', 'Carvedilol', '25mg', 'Oral', 'BID', '2024-01-05 14:00:00', NULL, 'DR001', FALSE, 'Beta Blocker', CURRENT_TIMESTAMP()),
    ('M003', 'P001', 'E001', 'Lisinopril', 'Lisinopril', '10mg', 'Oral', 'Daily', '2024-01-05 14:00:00', NULL, 'DR001', FALSE, 'ACE Inhibitor', CURRENT_TIMESTAMP()),
    ('M004', 'P001', 'E001', 'Warfarin', 'Warfarin', '5mg', 'Oral', 'Daily', '2024-01-05 14:00:00', NULL, 'DR001', TRUE, 'Anticoagulant', CURRENT_TIMESTAMP()),
    ('M005', 'P001', 'E003', 'Digoxin', 'Digoxin', '0.25mg', 'Oral', 'Daily', '2024-01-26 10:00:00', NULL, 'DR001', TRUE, 'Cardiac Glycoside', CURRENT_TIMESTAMP()),
    
    -- P002 diabetes medications
    ('M006', 'P002', 'E006', 'Metformin', 'Metformin', '1000mg', 'Oral', 'BID', '2024-01-10 10:00:00', NULL, 'DR001', FALSE, 'Antidiabetic', CURRENT_TIMESTAMP()),
    ('M007', 'P002', 'E006', 'Januvia', 'Sitagliptin', '100mg', 'Oral', 'Daily', '2024-01-10 10:00:00', NULL, 'DR001', FALSE, 'Antidiabetic', CURRENT_TIMESTAMP()),
    
    -- P003 COPD medications
    ('M008', 'P003', 'E010', 'Symbicort', 'Budesonide/Formoterol', '160/4.5mcg', 'Inhaled', 'BID', '2024-02-01 10:00:00', NULL, 'DR002', FALSE, 'Bronchodilator', CURRENT_TIMESTAMP()),
    ('M009', 'P003', 'E010', 'Prednisone', 'Prednisone', '40mg', 'Oral', 'Daily', '2024-02-01 10:00:00', '2024-02-08 10:00:00', 'DR002', FALSE, 'Corticosteroid', CURRENT_TIMESTAMP()),
    ('M010', 'P003', 'E010', 'Azithromycin', 'Azithromycin', '500mg', 'Oral', 'Daily', '2024-02-01 10:00:00', '2024-02-05 10:00:00', 'DR002', FALSE, 'Antibiotic', CURRENT_TIMESTAMP()),
    
    -- More medications
    ('M011', 'P006', 'E011', 'Prenatal Vitamins', 'Prenatal Vitamins', '1 tab', 'Oral', 'Daily', '2024-01-15 15:00:00', NULL, 'DR003', FALSE, 'Vitamin', CURRENT_TIMESTAMP()),
    ('M012', 'P007', 'E014', 'Ibuprofen', 'Ibuprofen', '800mg', 'Oral', 'TID', '2024-01-20 12:00:00', '2024-01-27 12:00:00', 'DR002', FALSE, 'NSAID', CURRENT_TIMESTAMP()),
    ('M013', 'P011', 'E017', 'Pantoprazole', 'Pantoprazole', '40mg', 'IV', 'BID', '2024-01-19 06:00:00', '2024-01-22 14:00:00', 'DR001', FALSE, 'Proton Pump Inhibitor', CURRENT_TIMESTAMP()),
    ('M014', 'P012', 'E018', 'Sertraline', 'Sertraline', '50mg', 'Oral', 'Daily', '2024-02-22 14:00:00', NULL, 'DR003', FALSE, 'Antidepressant', CURRENT_TIMESTAMP()),
    ('M015', 'P014', 'E020', 'Insulin Glargine', 'Lantus', '20 units', 'Subcutaneous', 'Daily', '2024-02-28 16:00:00', NULL, 'DR002', TRUE, 'Insulin', CURRENT_TIMESTAMP());

-- 5. MEDICATION ADHERENCE TABLE
CREATE OR REPLACE TABLE medication_adherence (
    adherence_id VARCHAR(50),
    patient_id VARCHAR(50),
    medication_id VARCHAR(50),
    measurement_date DATE,
    pdc_score DECIMAL(3,2),  -- Proportion of Days Covered
    days_until_refill INTEGER,
    adherence_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Insert adherence data showing patterns
INSERT INTO medication_adherence
SELECT * FROM VALUES
    -- P001 poor adherence (contributing to readmissions)
    ('A001', 'P001', 'M001', '2024-02-01', 0.65, 5, 'at_risk', CURRENT_TIMESTAMP()),
    ('A002', 'P001', 'M002', '2024-02-01', 0.58, 3, 'non_adherent', CURRENT_TIMESTAMP()),
    ('A003', 'P001', 'M003', '2024-02-01', 0.70, 7, 'at_risk', CURRENT_TIMESTAMP()),
    ('A004', 'P001', 'M004', '2024-02-01', 0.45, 1, 'non_adherent', CURRENT_TIMESTAMP()),
    ('A005', 'P001', 'M001', '2024-03-01', 0.55, 2, 'non_adherent', CURRENT_TIMESTAMP()),
    
    -- P002 good adherence
    ('A006', 'P002', 'M006', '2024-02-01', 0.95, 25, 'adherent', CURRENT_TIMESTAMP()),
    ('A007', 'P002', 'M007', '2024-02-01', 0.92, 23, 'adherent', CURRENT_TIMESTAMP()),
    ('A008', 'P002', 'M006', '2024-03-01', 0.93, 24, 'adherent', CURRENT_TIMESTAMP()),
    ('A009', 'P002', 'M007', '2024-03-01', 0.90, 22, 'adherent', CURRENT_TIMESTAMP()),
    
    -- P003 moderate adherence
    ('A010', 'P003', 'M008', '2024-02-15', 0.78, 10, 'at_risk', CURRENT_TIMESTAMP()),
    ('A011', 'P003', 'M008', '2024-03-01', 0.75, 8, 'at_risk', CURRENT_TIMESTAMP()),
    
    -- More adherence patterns
    ('A012', 'P011', 'M013', '2024-02-01', 0.88, 20, 'adherent', CURRENT_TIMESTAMP()),
    ('A013', 'P012', 'M014', '2024-03-01', 0.82, 15, 'adherent', CURRENT_TIMESTAMP()),
    ('A014', 'P014', 'M015', '2024-03-01', 0.35, 0, 'non_adherent', CURRENT_TIMESTAMP());

-- 6. VITAL SIGNS TABLE (for sepsis detection)
CREATE OR REPLACE TABLE vital_signs (
    vital_id VARCHAR(50),
    patient_id VARCHAR(50),
    encounter_id VARCHAR(50),
    measurement_datetime TIMESTAMP,
    temperature DECIMAL(4,1),
    heart_rate INTEGER,
    respiratory_rate INTEGER,
    systolic_bp INTEGER,
    diastolic_bp INTEGER,
    oxygen_saturation DECIMAL(5,2),
    pain_score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Insert vital signs including concerning patterns
INSERT INTO vital_signs
SELECT * FROM VALUES
    -- P001 showing signs of decompensation
    ('V001', 'P001', 'E001', '2024-01-05 08:30:00', 98.2, 92, 20, 145, 92, 94.0, 3, CURRENT_TIMESTAMP()),
    ('V002', 'P001', 'E001', '2024-01-05 14:30:00', 98.5, 98, 22, 150, 95, 93.0, 4, CURRENT_TIMESTAMP()),
    ('V003', 'P001', 'E001', '2024-01-06 06:30:00', 98.8, 105, 24, 155, 98, 92.0, 5, CURRENT_TIMESTAMP()),
    ('V004', 'P001', 'E003', '2024-01-26 06:30:00', 99.2, 110, 26, 160, 100, 91.0, 6, CURRENT_TIMESTAMP()),
    ('V005', 'P001', 'E003', '2024-01-26 14:30:00', 99.8, 115, 28, 165, 102, 90.0, 7, CURRENT_TIMESTAMP()),
    
    -- P003 with potential sepsis indicators (SIRS criteria)
    ('V006', 'P003', 'E009', '2024-02-01 04:00:00', 101.5, 112, 24, 135, 85, 92.0, 4, CURRENT_TIMESTAMP()),
    ('V007', 'P003', 'E010', '2024-02-01 08:30:00', 102.1, 118, 26, 130, 82, 91.0, 5, CURRENT_TIMESTAMP()),
    ('V008', 'P003', 'E010', '2024-02-01 14:30:00', 101.8, 115, 25, 132, 84, 92.0, 4, CURRENT_TIMESTAMP()),
    
    -- Normal vitals for comparison
    ('V009', 'P002', 'E006', '2024-01-10 09:00:00', 98.6, 72, 16, 128, 82, 98.0, 0, CURRENT_TIMESTAMP()),
    ('V010', 'P002', 'E007', '2024-02-10 09:00:00', 98.4, 70, 14, 125, 80, 99.0, 0, CURRENT_TIMESTAMP()),
    ('V011', 'P002', 'E008', '2024-03-10 09:00:00', 98.5, 68, 15, 122, 78, 98.5, 0, CURRENT_TIMESTAMP()),
    
    -- More vital signs
    ('V012', 'P006', 'E011', '2024-01-15 14:00:00', 98.3, 78, 16, 118, 76, 99.0, 0, CURRENT_TIMESTAMP()),
    ('V013', 'P007', 'E014', '2024-01-20 11:00:00', 98.7, 82, 18, 132, 86, 98.0, 6, CURRENT_TIMESTAMP()),
    ('V014', 'P011', 'E016', '2024-01-18 23:00:00', 97.8, 108, 20, 95, 60, 96.0, 8, CURRENT_TIMESTAMP()),
    ('V015', 'P011', 'E017', '2024-01-19 08:00:00', 98.0, 95, 18, 105, 65, 97.0, 5, CURRENT_TIMESTAMP());

-- Verify data loaded
SELECT 'Patients' as table_name, COUNT(*) as row_count FROM patients
UNION ALL
SELECT 'Encounters', COUNT(*) FROM encounters
UNION ALL
SELECT 'Lab Results', COUNT(*) FROM lab_results
UNION ALL
SELECT 'Medications', COUNT(*) FROM medications
UNION ALL
SELECT 'Adherence', COUNT(*) FROM medication_adherence
UNION ALL
SELECT 'Vital Signs', COUNT(*) FROM vital_signs
ORDER BY table_name;

-- Sample queries to test the data
-- 1. Find patients with multiple admissions (readmission risk)
SELECT 
    patient_id,
    COUNT(*) as admission_count,
    MIN(admit_datetime) as first_admission,
    MAX(admit_datetime) as last_admission
FROM encounters
WHERE encounter_type = 'Inpatient'
GROUP BY patient_id
HAVING COUNT(*) > 1
ORDER BY admission_count DESC;

-- 2. Check medication adherence issues
SELECT 
    p.patient_id,
    p.first_name,
    p.last_name,
    AVG(ma.pdc_score) as avg_adherence,
    COUNT(DISTINCT ma.medication_id) as medication_count
FROM patients p
JOIN medication_adherence ma ON p.patient_id = ma.patient_id
WHERE ma.adherence_status IN ('at_risk', 'non_adherent')
GROUP BY p.patient_id, p.first_name, p.last_name
ORDER BY avg_adherence;

-- 3. Identify critical lab values
SELECT 
    p.patient_id,
    p.first_name,
    p.last_name,
    lr.test_name,
    lr.result_numeric,
    lr.critical_flag,
    lr.result_datetime
FROM patients p
JOIN lab_results lr ON p.patient_id = lr.patient_id
WHERE lr.critical_flag = TRUE
ORDER BY lr.result_datetime DESC;
```

**Day 4-5: dbt Cloud Setup (Web IDE)**
```yaml
# In dbt Cloud Web IDE
# No local files needed!

# 1. Connect to Snowflake
# Settings → Credentials → Enter Snowflake details

# 2. Initialize repository  
# dbt Cloud creates git repo for you

# 3. Create first model
# models/staging/stg_patients.sql
SELECT 
    patient_id,
    birth_date,
    DATEDIFF('year', birth_date, CURRENT_DATE()) AS age,
    gender,
    insurance_type
FROM {{ source('raw', 'patients') }}

# 4. Run in cloud
# Click "Run" button - no CLI needed!
```

#### Week 2: Semantic Layer (All in dbt Cloud)

**Day 6-7: Define Metrics (Web IDE)**
```yaml
# In dbt Cloud IDE
# models/marts/metrics.yml

metrics:
  - name: patient_count
    type: count_distinct
    type_params:
      entity: patient_id
      
  - name: avg_length_of_stay
    type: average
    type_params:
      measure: length_of_stay_days
      
  - name: readmission_rate
    type: ratio
    type_params:
      numerator: readmission_count
      denominator: encounter_count
```

**Day 8-10: Test Semantic Layer**
```python
# Can test via dbt Cloud API
# Or use their GraphQL interface
# No local MCP server needed initially

import requests

# Get metrics via API
headers = {"Authorization": f"Token {DBT_CLOUD_TOKEN}"}
response = requests.get(
    "https://cloud.getdbt.com/api/v2/metrics",
    headers=headers
)
```

#### Week 3: Confluent Cloud KSQLDB (All in Browser)

**Day 11-12: Create Kafka Cluster**
```
1. In Confluent Cloud Console
2. Create Cluster → Basic → Choose region
3. Create ksqlDB cluster → Click "Create"
4. All managed - no Docker needed!
```

**Day 13-15: First KSQLDB Queries (Web Editor)**
```sql
-- In Confluent Cloud ksqlDB Editor
-- No CLI needed!

-- Create stream from Snowflake CDC
CREATE SOURCE CONNECTOR snowflake_cdc WITH (
    'connector.class' = 'SnowflakeCdcSource',
    'snowflake.url' = '<your-account>.snowflakecomputing.com',
    'snowflake.user' = '<username>',
    'snowflake.password' = '<password>',
    'snowflake.database.name' = 'HEALTHCARE_PROD',
    'tasks.max' = '1'
);

-- Create encounters stream
CREATE STREAM encounters_stream (
    encounter_id VARCHAR KEY,
    patient_id VARCHAR,
    encounter_type VARCHAR,
    admit_date VARCHAR,
    discharge_date VARCHAR
) WITH (
    KAFKA_TOPIC='HEALTHCARE_PROD.RAW.ENCOUNTERS',
    VALUE_FORMAT='AVRO'
);

-- Create readmission detection
CREATE TABLE readmissions AS
SELECT
    patient_id,
    COUNT(*) as admission_count
FROM encounters_stream
WINDOW TUMBLING (SIZE 30 DAYS)
WHERE encounter_type = 'Inpatient'
GROUP BY patient_id
HAVING COUNT(*) > 1;

-- View results in UI
SELECT * FROM readmissions;
```

#### Week 4: Connect Everything (Cloud to Cloud)

**Day 16-18: Snowflake → Confluent**
```sql
-- In Snowflake, create change streams
CREATE STREAM encounters_changes ON TABLE encounters;

-- Confluent automatically syncs via CDC connector
-- No local Kafka Connect needed!
```

**Day 19-20: Test End-to-End**
```sql
-- 1. Insert in Snowflake (Web UI)
INSERT INTO encounters VALUES 
    ('E003', 'P001', 'Inpatient', '2024-03-01', '2024-03-03', 2);

-- 2. Check in Confluent ksqlDB (Web UI)
SELECT * FROM readmissions WHERE patient_id = 'P001';
-- Should show admission_count = 3

-- 3. View in Confluent metrics
-- All visible in web dashboards!
```

#### Week 5: Production Deployment

**Day 21-25: Monitoring & Alerts**
```sql
-- In Confluent ksqlDB
CREATE STREAM alerts AS
SELECT 
    patient_id,
    'High readmission risk' as alert_message,
    admission_count
FROM readmissions
WHERE admission_count >= 2;

-- Configure webhook for alerts
CREATE SINK CONNECTOR alert_webhook WITH (
    'connector.class' = 'HttpSink',
    'http.api.url' = 'https://your-api.com/alerts',
    'topics' = 'ALERTS'
);
```

---

### 🪟 Windows Considerations (For Local Path Only)

If you choose the local development path on Windows:

#### Prerequisites for Windows

1. **Install WSL2 (Windows Subsystem for Linux)**
```powershell
# Run as Administrator in PowerShell
wsl --install
# Restart computer after installation
# This installs Ubuntu by default

# Verify installation
wsl --list --verbose
```

2. **Install Docker Desktop for Windows**
   - Download from: https://www.docker.com/products/docker-desktop
   - During installation, ensure "Use WSL 2 based engine" is checked
   - After installation, go to Settings → Resources → WSL Integration
   - Enable integration with your WSL2 distro

3. **Install Python via Anaconda (Recommended for Windows)**
   - Download from: https://www.anaconda.com/download
   - Adds Python, pip, and conda without PATH issues
   - Creates isolated environments easily

4. **Install Git for Windows**
   - Download from: https://git-scm.com/download/win
   - During installation, choose "Git from the command line and also from 3rd-party software"

5. **Choose Your Terminal**
   - **Windows Terminal** (Recommended): Install from Microsoft Store
   - Configure to use both PowerShell and WSL2 Ubuntu
   - Alternative: Use VSCode's integrated terminal

#### Windows-Specific Environment Variables
```powershell
# In PowerShell (Run as Administrator)
# Set environment variables permanently
[System.Environment]::SetEnvironmentVariable('DBT_PROFILES_DIR', "$env:USERPROFILE\.dbt", 'User')
[System.Environment]::SetEnvironmentVariable('DBT_PROJECT_DIR', "$env:USERPROFILE\healthcare_analytics", 'User')

# Verify they're set
$env:DBT_PROFILES_DIR
$env:DBT_PROJECT_DIR
```

### Phase 1: Foundation (Weeks 1-2) - Windows Adjusted
**Goal**: Get the backend data infrastructure running

#### Week 1: Snowflake Setup

**Day 1-2: Account and Environment**
```sql
-- Same Snowflake setup (runs in browser, no Windows issues)
-- Sign up at: https://signup.snowflake.com
```

**Day 5: dbt Installation and Setup (Windows)**

**Option 1: Using Anaconda (Recommended)**
```powershell
# Open Anaconda Prompt
conda create -n dbt_env python=3.9
conda activate dbt_env
pip install dbt-core dbt-snowflake

# Verify installation
dbt --version
```

**Option 2: Using WSL2**
```bash
# Open Windows Terminal → Ubuntu tab
python3 -m venv dbt_env
source dbt_env/bin/activate
pip install dbt-core dbt-snowflake
```

**Configure profiles.yml (Windows paths)**
```yaml
# Location: C:\Users\<YourUsername>\.dbt\profiles.yml
# Note: Use forward slashes even on Windows

healthcare_analytics:
  outputs:
    dev:
      type: snowflake
      account: <your_account>
      user: <your_username>
      password: <your_password>
      role: ANALYTICS_ENGINEER
      database: HEALTHCARE_DEV
      warehouse: HEALTHCARE_WH
      schema: ANALYTICS
      threads: 4
  target: dev
```

**Create dbt project (Windows PowerShell)**
```powershell
# Navigate to your workspace
cd $env:USERPROFILE\Documents
dbt init healthcare_analytics
cd healthcare_analytics

# Open in VSCode (if installed)
code .
```

#### Week 2: First dbt Models

**Day 6-10: Same as original but with Windows paths**
```powershell
# Run dbt commands in PowerShell or Anaconda Prompt
dbt run
dbt test

# Generate docs
dbt docs generate
dbt docs serve
# This opens browser automatically
```

### Phase 2: Semantic Layer (Week 3) - Windows Adjusted
**Goal**: Create queryable business metrics

**Day 13-14: MCP Server Setup (Windows)**

```powershell
# Option 1: Install in Anaconda environment
conda activate dbt_env
pip install dbt-mcp

# Create environment file (Windows)
# Location: C:\Users\<YourUsername>\.dbt-mcp.env
```

**Windows .env file format:**
```ini
# Note: No quotes needed in Windows .env files
DBT_HOST=cloud.getdbt.com
DBT_ACCOUNT_ID=12345
DBT_PROJECT_ID=67890
DBT_ENVIRONMENT_ID=11111
DBT_TOKEN=dbtc_xxxxxxxxxxxxx
```

**Set environment variables (PowerShell)**
```powershell
# Temporary (current session only)
$env:DBT_ACCOUNT_ID="12345"
$env:DBT_PROJECT_ID="67890"
$env:DBT_ENVIRONMENT_ID="11111"
$env:DBT_TOKEN="dbtc_xxxxxxxxxxxxx"

# Permanent (all future sessions)
[System.Environment]::SetEnvironmentVariable('DBT_ACCOUNT_ID', '12345', 'User')
[System.Environment]::SetEnvironmentVariable('DBT_PROJECT_ID', '67890', 'User')
[System.Environment]::SetEnvironmentVariable('DBT_ENVIRONMENT_ID', '11111', 'User')
[System.Environment]::SetEnvironmentVariable('DBT_TOKEN', 'dbtc_xxxxxxxxxxxxx', 'User')

# Restart PowerShell after setting permanent variables
```

**Test MCP on Windows:**
```powershell
# If uvx doesn't work on Windows, use Python directly
python -m dbt_mcp

# Or create a batch file for easy running
echo "python -m dbt_mcp" > run_mcp.bat
.\run_mcp.bat
```

### Phase 3: Streaming Foundation (Week 4) - Windows Adjusted
**Goal**: Get KSQLDB running with sample data

**Day 16-17: Docker Setup (Windows)**

**CRITICAL: Use WSL2 for Docker operations**
```bash
# Open Windows Terminal → Ubuntu tab (WSL2)
# Navigate to your project
cd /mnt/c/Users/<YourUsername>/Documents/healthcare_analytics

# Create docker-compose file here
nano docker-compose-minimal.yml
# Paste the yaml content

# Start Docker stack
docker-compose -f docker-compose-minimal.yml up -d

# Verify containers running
docker ps
```

**Common Windows Docker Issues:**
1. **"Docker daemon not running"**
   - Ensure Docker Desktop is running
   - Check system tray for Docker icon
   - Restart Docker Desktop

2. **Port conflicts**
   - Windows may use ports 8088, 9092
   - Check with: `netstat -an | findstr :8088`
   - Modify docker-compose.yml ports if needed

3. **File path issues**
   - Always use WSL2 paths: `/mnt/c/Users/...`
   - Not Windows paths: `C:\Users\...`

**Day 18-19: KSQLDB CLI Access (Windows)**
```bash
# Must use WSL2 terminal
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088

# Alternative: Use KSQLDB UI
# Open browser: http://localhost:8088
```

### Phase 4: First Agent (Week 5) - Windows Adjusted

**Day 21-25: Same KSQLDB commands work**
```bash
# Connect to KSQLDB from WSL2
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088

# Run the same SQL commands
# No Windows-specific changes needed here
```

### Phase 5: Integration (Week 6) - Windows Adjusted

**Day 26-27: Kafka Connect (Windows)**
```bash
# Install connector in WSL2
docker exec -it kafka-connect bash
confluent-hub install snowflakeinc/snowflake-kafka-connector:latest

# Create config file in WSL2
cd /mnt/c/Users/<YourUsername>/Documents/healthcare_analytics
nano snowflake-source.json

# Submit connector (from WSL2)
curl -X POST -H "Content-Type: application/json" \
  --data @snowflake-source.json \
  http://localhost:8083/connectors
```

### Windows-Specific Troubleshooting

**Issue: "command not found" in PowerShell**
```powershell
# Check if command exists
where dbt
where python

# If not found, check PATH
$env:PATH -split ';'

# Add to PATH if needed
$env:PATH += ";C:\Users\<YourUsername>\Anaconda3\Scripts"
```

**Issue: SSL/Certificate errors**
```powershell
# Common with corporate Windows machines
pip config set global.trusted-host "pypi.org files.pythonhosted.org"
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org dbt-core
```

**Issue: Line ending problems (CRLF vs LF)**
```powershell
# Configure Git to handle line endings
git config --global core.autocrlf true

# In VSCode, set default line ending
# File → Preferences → Settings → Search "eol"
# Set to \n (LF)
```

**Issue: Docker not starting**
```powershell
# Check WSL2 status
wsl --status

# Restart WSL2
wsl --shutdown
wsl

# Check Docker service
Get-Service com.docker.service
Restart-Service com.docker.service
```

**Issue: Firewall blocking ports**
```powershell
# Run as Administrator
# Open ports for Kafka/KSQLDB
New-NetFirewallRule -DisplayName "Kafka" -Direction Inbound -LocalPort 9092 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "KSQLDB" -Direction Inbound -LocalPort 8088 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "Kafka Connect" -Direction Inbound -LocalPort 8083 -Protocol TCP -Action Allow
```

### Windows Best Practices

1. **Use WSL2 for Docker/Kafka/KSQLDB**
   - Better performance
   - Fewer compatibility issues
   - Native Linux tools work

2. **Use Anaconda for Python/dbt**
   - Cleaner environment management
   - No PATH conflicts
   - Easy package installation

3. **VSCode as IDE**
   - Great WSL2 integration
   - Terminal switching (PowerShell/WSL)
   - dbt extensions available

4. **File Management**
   - Keep code in Windows filesystem
   - Access from WSL via `/mnt/c/`
   - Use Git for version control

5. **Terminal Strategy**
   - PowerShell/Anaconda Prompt: dbt, Python
   - WSL2/Ubuntu: Docker, Kafka, KSQLDB
   - Windows Terminal: Switch between both

### Windows Quick Reference

| Task | Use | Command Location |
|------|-----|------------------|
| dbt commands | PowerShell/Anaconda | `dbt run` |
| Docker operations | WSL2 | `docker-compose up` |
| KSQLDB CLI | WSL2 | `docker exec -it ksqldb-cli` |
| Python scripts | PowerShell/Anaconda | `python script.py` |
| File editing | Windows/VSCode | Normal Windows paths |
| Kafka operations | WSL2 | Inside Docker containers |

### Success Milestones Checklist (Windows Verified)
```sql
-- 1. Sign up for Snowflake trial
-- Go to: https://signup.snowflake.com
-- Choose: Enterprise Edition (30-day trial with $400 credits)
-- Select: AWS/Azure/GCP based on your preference

-- 2. Log into Snowflake and run initial setup
USE ROLE ACCOUNTADMIN;

-- Create your development environment
CREATE DATABASE IF NOT EXISTS HEALTHCARE_DEV;
CREATE WAREHOUSE IF NOT EXISTS HEALTHCARE_WH 
    WITH WAREHOUSE_SIZE = 'XSMALL' 
    AUTO_SUSPEND = 60;

-- Create your user role
CREATE ROLE IF NOT EXISTS ANALYTICS_ENGINEER;
GRANT USAGE ON WAREHOUSE HEALTHCARE_WH TO ROLE ANALYTICS_ENGINEER;
GRANT ALL ON DATABASE HEALTHCARE_DEV TO ROLE ANALYTICS_ENGINEER;
GRANT ROLE ANALYTICS_ENGINEER TO USER <your_username>;

USE ROLE ANALYTICS_ENGINEER;
USE WAREHOUSE HEALTHCARE_WH;
USE DATABASE HEALTHCARE_DEV;
```

**Day 3-4: Create Sample Healthcare Data**
```sql
-- Create a simple schema to start
CREATE SCHEMA IF NOT EXISTS RAW;

-- Start with just 3 core tables
CREATE OR REPLACE TABLE HEALTHCARE_DEV.RAW.patients (
    patient_id VARCHAR(50),
    birth_date DATE,
    gender VARCHAR(10),
    insurance_type VARCHAR(50)
);

CREATE OR REPLACE TABLE HEALTHCARE_DEV.RAW.encounters (
    encounter_id VARCHAR(50),
    patient_id VARCHAR(50),
    encounter_type VARCHAR(50),
    admit_date DATE,
    discharge_date DATE,
    length_of_stay_days INTEGER
);

CREATE OR REPLACE TABLE HEALTHCARE_DEV.RAW.lab_results (
    lab_id VARCHAR(50),
    patient_id VARCHAR(50),
    test_name VARCHAR(100),
    result_value DECIMAL(10,2),
    result_date DATE
);

-- Insert sample data to work with
INSERT INTO patients VALUES
    ('P001', '1950-01-15', 'Female', 'Medicare'),
    ('P002', '1975-06-22', 'Male', 'Commercial'),
    ('P003', '1988-11-30', 'Female', 'Medicaid');

INSERT INTO encounters VALUES
    ('E001', 'P001', 'Inpatient', '2024-01-15', '2024-01-20', 5),
    ('E002', 'P001', 'Emergency', '2024-02-01', '2024-02-01', 0),
    ('E003', 'P002', 'Outpatient', '2024-01-10', '2024-01-10', 0);

-- Verify data loaded
SELECT COUNT(*) as patient_count FROM patients;
SELECT COUNT(*) as encounter_count FROM encounters;
```

**Day 5: dbt Installation and Setup**
```bash
# Install dbt locally
pip install dbt-core dbt-snowflake

# Create a new dbt project
dbt init healthcare_analytics
cd healthcare_analytics

# Configure profiles.yml (~/.dbt/profiles.yml)
```

```yaml
healthcare_analytics:
  outputs:
    dev:
      type: snowflake
      account: <your_account>
      user: <your_username>
      password: <your_password>
      role: ANALYTICS_ENGINEER
      database: HEALTHCARE_DEV
      warehouse: HEALTHCARE_WH
      schema: ANALYTICS
      threads: 4
  target: dev
```

#### Week 2: First dbt Models

**Day 6-7: Create Staging Models**
```sql
-- models/staging/_sources.yml
version: 2

sources:
  - name: raw
    database: HEALTHCARE_DEV
    schema: RAW
    tables:
      - name: patients
      - name: encounters
      - name: lab_results

-- models/staging/stg_patients.sql
SELECT
    patient_id,
    birth_date,
    DATEDIFF('year', birth_date, CURRENT_DATE()) AS age,
    gender,
    insurance_type
FROM {{ source('raw', 'patients') }}

-- models/staging/stg_encounters.sql
SELECT
    encounter_id,
    patient_id,
    encounter_type,
    admit_date,
    discharge_date,
    length_of_stay_days
FROM {{ source('raw', 'encounters') }}
```

**Day 8-9: Create Your First Mart**
```sql
-- models/marts/patient_summary.sql
WITH patients AS (
    SELECT * FROM {{ ref('stg_patients') }}
),
encounters AS (
    SELECT * FROM {{ ref('stg_encounters') }}
)
SELECT
    p.patient_id,
    p.age,
    p.gender,
    p.insurance_type,
    COUNT(DISTINCT e.encounter_id) as total_encounters,
    SUM(e.length_of_stay_days) as total_los_days
FROM patients p
LEFT JOIN encounters e ON p.patient_id = e.patient_id
GROUP BY 1,2,3,4
```

**Day 10: Run and Test**
```bash
# Run your models
dbt run

# Test your models
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

**First Success Checkpoint:**
```sql
-- Query your mart in Snowflake
SELECT 
    insurance_type,
    COUNT(*) as patient_count,
    AVG(total_encounters) as avg_encounters
FROM HEALTHCARE_DEV.ANALYTICS.patient_summary
GROUP BY 1;
-- You should see summarized data!
```

### Phase 2: Semantic Layer (Week 3)
**Goal**: Create queryable business metrics

**Day 11-12: dbt Semantic Layer Setup**

```yaml
# models/marts/metrics.yml
version: 2

semantic_models:
  - name: patient_summary_semantic
    model: ref('patient_summary')
    
    entities:
      - name: patient_id
        type: primary
        expr: patient_id
    
    dimensions:
      - name: age
        type: number
      - name: gender
        type: categorical
      - name: insurance_type
        type: categorical
    
    measures:
      - name: patient_count
        agg: count_distinct
        expr: patient_id
      - name: encounter_count
        agg: sum
        expr: total_encounters
      - name: total_los
        agg: sum
        expr: total_los_days

metrics:
  - name: avg_encounters_per_patient
    type: ratio
    type_params:
      numerator: encounter_count
      denominator: patient_count
  
  - name: avg_los
    type: simple
    type_params:
      measure: total_los
```

**Day 13-14: MCP Server Setup**

```bash
# 1. Get dbt Cloud trial (required for semantic layer)
# Sign up at: https://www.getdbt.com/signup/

# 2. Create service token
# Account Settings → Service Tokens → New Token

# 3. Install MCP server
pip install dbt-mcp

# 4. Configure environment
export DBT_ACCOUNT_ID=<your_account_id>
export DBT_PROJECT_ID=<your_project_id>
export DBT_ENVIRONMENT_ID=<your_environment_id>
export DBT_TOKEN=<your_service_token>

# 5. Test MCP connection
uvx dbt-mcp
```

**Day 15: Query Metrics via MCP**
```python
# test_mcp.py
import requests

headers = {
    "Authorization": f"Token {DBT_TOKEN}",
    "Content-Type": "application/json"
}

query = {
    "metrics": ["avg_encounters_per_patient"],
    "group_by": ["insurance_type"]
}

response = requests.post(
    f"https://cloud.getdbt.com/api/v2/accounts/{DBT_ACCOUNT_ID}/metrics/query",
    headers=headers,
    json=query
)

print(response.json())
# You should see metrics by insurance type!
```

### Phase 3: Streaming Foundation (Week 4)
**Goal**: Get KSQLDB running with sample data

**Day 16-17: Docker Setup**

```yaml
# docker-compose-minimal.yml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  ksqldb-server:
    image: confluentinc/cp-ksqldb-server:7.5.0
    depends_on:
      - kafka
    ports:
      - "8088:8088"
    environment:
      KSQL_BOOTSTRAP_SERVERS: kafka:9092
      KSQL_LISTENERS: http://0.0.0.0:8088

  ksqldb-cli:
    image: confluentinc/cp-ksqldb-cli:7.5.0
    depends_on:
      - ksqldb-server
    entrypoint: /bin/sh
    tty: true
```

```bash
# Start the stack
docker-compose -f docker-compose-minimal.yml up -d

# Connect to KSQLDB CLI
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
```

**Day 18-19: First KSQLDB Queries**
```sql
-- In KSQLDB CLI
-- Create your first stream
CREATE STREAM test_patients (
    patient_id VARCHAR KEY,
    age INT,
    gender VARCHAR
) WITH (
    KAFKA_TOPIC='test_patients',
    VALUE_FORMAT='JSON',
    PARTITIONS=1
);

-- Insert test data
INSERT INTO test_patients VALUES ('P001', 74, 'Female');
INSERT INTO test_patients VALUES ('P002', 49, 'Male');

-- Query the stream
SELECT * FROM test_patients EMIT CHANGES;
-- Press Ctrl+C to stop

-- Create a simple aggregation
CREATE TABLE patient_counts AS
SELECT 
    gender,
    COUNT(*) as count
FROM test_patients
GROUP BY gender
EMIT CHANGES;

-- Query the table
SELECT * FROM patient_counts;
```

**Day 20: Connect to Snowflake (Simplified)**
```sql
-- In Snowflake, create a stream on your table
CREATE OR REPLACE STREAM patient_changes ON TABLE patients;

-- Insert new data to see changes
INSERT INTO patients VALUES ('P004', '2000-05-15', 'Male', 'Commercial');

-- View changes
SELECT * FROM patient_changes;

-- These changes can be sent to Kafka via Snowflake connector
-- (Full setup in Phase 4)
```

### Phase 4: First Agent (Week 5)
**Goal**: Create your first autonomous agent

**Day 21-22: Simple Monitoring Agent**
```sql
-- In KSQLDB: Create a simple readmission detection agent

-- First, create encounter stream
CREATE STREAM encounters (
    encounter_id VARCHAR KEY,
    patient_id VARCHAR,
    encounter_type VARCHAR,
    admit_date VARCHAR
) WITH (
    KAFKA_TOPIC='encounters',
    VALUE_FORMAT='JSON'
);

-- Insert test data (simulating readmission)
INSERT INTO encounters VALUES ('E001', 'P001', 'Inpatient', '2024-01-01');
INSERT INTO encounters VALUES ('E002', 'P001', 'Inpatient', '2024-01-20');

-- Create readmission detection
CREATE TABLE readmissions AS
SELECT
    patient_id,
    COUNT(*) as admission_count,
    COLLECT_LIST(admit_date) as admission_dates
FROM encounters
WINDOW TUMBLING (SIZE 30 DAYS)
WHERE encounter_type = 'Inpatient'
GROUP BY patient_id
HAVING COUNT(*) > 1
EMIT CHANGES;

-- Check for readmissions
SELECT * FROM readmissions;
-- You should see P001 flagged!
```

**Day 23-25: Create Alert Stream**
```sql
-- Generate alerts from patterns
CREATE STREAM readmission_alerts AS
SELECT
    CONCAT('ALERT_', patient_id) as alert_id,
    patient_id,
    'High readmission risk' as message,
    admission_count,
    ROWTIME as alert_time
FROM readmissions
WHERE admission_count >= 2
EMIT CHANGES;

-- Monitor alerts
SELECT * FROM readmission_alerts EMIT CHANGES;
```

### Phase 5: Integration (Week 6)
**Goal**: Connect all pieces together

**Day 26-27: Snowflake → Kafka Pipeline**
```bash
# Install Snowflake Kafka Connector
confluent-hub install snowflakeinc/snowflake-kafka-connector:latest

# Configure connector (create snowflake-source.json)
{
  "name": "snowflake-source",
  "config": {
    "connector.class": "com.snowflake.kafka.connector.SnowflakeSourceConnector",
    "snowflake.url.name": "<your-account>.snowflakecomputing.com",
    "snowflake.user.name": "<username>",
    "snowflake.password": "<password>",
    "snowflake.database.name": "HEALTHCARE_DEV",
    "snowflake.schema.name": "RAW",
    "tasks.max": "1",
    "snowflake.table.name": "PATIENTS,ENCOUNTERS",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false"
  }
}

# Submit connector
curl -X POST -H "Content-Type: application/json" \
  --data @snowflake-source.json \
  http://localhost:8083/connectors
```

**Day 28-30: Complete Loop Test**
```sql
-- 1. Insert data in Snowflake
INSERT INTO HEALTHCARE_DEV.RAW.encounters VALUES
    ('E999', 'P001', 'Inpatient', '2024-03-01', '2024-03-05', 4);

-- 2. Verify in KSQLDB (should flow automatically)
SELECT * FROM encounters EMIT CHANGES;

-- 3. Check if alert generated
SELECT * FROM readmission_alerts WHERE patient_id = 'P001';

-- 4. View in monitoring table
SELECT * FROM patient_counts;
```

### Success Milestones Checklist

#### Foundation Success
- [ ] Snowflake account created
- [ ] Sample healthcare data loaded
- [ ] First dbt model runs successfully
- [ ] Can query mart tables

#### Semantic Layer Success
- [ ] Metrics defined in dbt
- [ ] MCP server connects
- [ ] Can query metrics via API
- [ ] Returns correct aggregations

#### Streaming Success
- [ ] Docker stack running
- [ ] Can create KSQLDB streams
- [ ] Can insert and query data
- [ ] Aggregations update in real-time

#### Agent Success
- [ ] First agent detects patterns
- [ ] Alerts generate automatically
- [ ] Can see real-time updates
- [ ] Data flows end-to-end

#### Integration Success
- [ ] Snowflake changes flow to Kafka
- [ ] KSQLDB processes changes
- [ ] Agents react to new data
- [ ] Complete pipeline works

### Troubleshooting Guide

**Common Issue 1: dbt connection fails**
```bash
# Test connection
dbt debug

# Check credentials in profiles.yml
# Verify Snowflake role has correct permissions
```

**Common Issue 2: KSQLDB queries hang**
```sql
-- Check topic exists
SHOW TOPICS;

-- Check stream has data
PRINT 'topic_name' FROM BEGINNING;

-- Verify stream schema
DESCRIBE EXTENDED stream_name;
```

**Common Issue 3: No data flowing**
```bash
# Check Kafka connector status
curl http://localhost:8083/connectors/snowflake-source/status

# View connector logs
docker logs kafka-connect

# Verify Snowflake stream has changes
SELECT * FROM stream_name;
```

### Next Steps After Basics Work

Once you have the foundation running:

1. **Add Complexity Gradually**
   - Add more tables (medications, vitals)
   - Create more sophisticated agents
   - Add agent coordination

2. **Optimize for Production**
   - Set up proper error handling
   - Add monitoring dashboards
   - Configure alerting

3. **Expand Agent Intelligence**
   - Add pattern detection
   - Implement sliding windows
   - Create agent communication

Remember: Get each phase working before moving to the next. Each successful query builds confidence and understanding!