# Cloud-Agnostic TMDB Ingestion into Snowflake Using dbt + Adapter Pattern  
## External Functions + Three Clouds (AWS / Azure / GCP)  
### Python-Free Data Path, dbt-Managed External Functions

This tutorial extends the Snowflake + TMDB adapter pattern by adding **dbt** as the orchestration layer for creating **cloud-agnostic external functions**.

The core idea:

- Snowflake external functions are **cloud-specific** in their DDL (URL + API_INTEGRATION).
- dbt is **environment-aware** (via `profiles.yml`, `target`, and `vars`).
- We let **dbt generate the external function DDL** with Jinja, so your **models and SQL stay identical across clouds**, while only dbt vars change.

The data path remains Python-free:

```text
Snowflake SQL
  → External Function (tmdb_fetch_page)
    → Cloud Adapter (AWS / Azure / GCP)
      → TMDB API
        → JSON → Snowflake VARIANT
```

dbt sits around Snowflake to manage the environment-specific wiring.

---

## 1. Architecture Recap (Adapter Pattern + dbt)

### 1.1 Target Interface (stable function contract)

We define one stable function everywhere:

```sql
tmdb_fetch_page(page NUMBER) → VARIANT
```

Your dbt models, ad-hoc SQL, and notebooks always call:

```sql
SELECT tmdb_fetch_page(1);
```

This function is the **Target** in the adapter pattern.

### 1.2 Adaptee (TMDB API)

TMDB’s real endpoint is:

```http
GET https://api.themoviedb.org/3/movie/popular?api_key=XXX&page=N
```

### 1.3 Adapters (cloud-specific HTTP endpoints)

For each cloud, you implement an HTTP adapter that exposes:

```http
GET /tmdb_popular?page=N
→ returns TMDB /movie/popular JSON
```

on:

- AWS: API Gateway + Lambda  
- Azure: APIM + Azure Function  
- GCP: API Gateway + Cloud Function  

Each has a **base URL** like:

- AWS: `https://aws-gw-1234.execute-api.us-east-1.amazonaws.com/prod`
- Azure: `https://your-apim.azure-api.net`
- GCP: `https://tmdb-gw-xyz.a.run.app`

and the adapter endpoint is: `BASE_URL + '/tmdb_popular'`.

### 1.4 dbt’s role

dbt will:

- hold the **environment-specific base URL** in `vars`  
- hold the **environment-specific integration name** in `vars`  
- generate the `CREATE EXTERNAL FUNCTION` DDL with Jinja  
- keep your **models and function calls identical** across clouds

---

## 2. Snowflake Core Objects (Once, Cloud-Agnostic)

In Snowflake, create the database, schema, and tables that dbt will work with:

```sql
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE DATABASE tmdb_demo;
CREATE OR REPLACE SCHEMA tmdb_demo.raw;

USE DATABASE tmdb_demo;
USE SCHEMA tmdb_demo.raw;

CREATE OR REPLACE TABLE tmdb_movies_raw (
    api_response VARIANT,
    api_endpoint STRING,
    ingest_ts    TIMESTAMP
);

CREATE OR REPLACE TABLE tmdb_movies_bronze (
    movie_id      NUMBER,
    title         STRING,
    overview      STRING,
    release_date  DATE,
    popularity    FLOAT,
    vote_average  FLOAT,
    vote_count    NUMBER,
    raw           VARIANT,
    ingest_ts     TIMESTAMP
);
```

These are the only static objects you need for the core pipeline.

---

## 3. dbt Project Setup

### 3.1 `dbt_project.yml`

Minimal skeleton (merge into your existing project as needed):

```yaml
name: tmdb_adapter
version: 1.0.0
config-version: 2

profile: tmdb_profile

models:
  tmdb_adapter:
    +database: tmdb_demo
    +schema: raw
    +materialized: table

vars:
  tmdb_api_integration_name: "tmdb_api_integration"
  tmdb_adapter_base_url: "https://placeholder"  # overridden per environment
```

### 3.2 `profiles.yml` (conceptual structure)

Each environment (aws / azure / gcp) overrides `vars` with its own base URL and integration name.

```yaml
tmdb_profile:
  target: aws
  outputs:
    aws:
      type: snowflake
      account: "<account>"
      user: "<user>"
      password: "<password>"
      role: "ACCOUNTADMIN"
      warehouse: "COMPUTE_WH"
      database: "TMDB_DEMO"
      schema: "RAW"
      threads: 4
      client_session_keep_alive: false
      vars:
        tmdb_api_integration_name: "tmdb_api_integration"
        tmdb_adapter_base_url: "https://aws-gw-1234.execute-api.us-east-1.amazonaws.com/prod"

    azure:
      type: snowflake
      account: "<account>"
      user: "<user>"
      password: "<password>"
      role: "ACCOUNTADMIN"
      warehouse: "COMPUTE_WH"
      database: "TMDB_DEMO"
      schema: "RAW"
      threads: 4
      client_session_keep_alive: false
      vars:
        tmdb_api_integration_name: "tmdb_api_integration"
        tmdb_adapter_base_url: "https://your-apim.azure-api.net"

    gcp:
      type: snowflake
      account: "<account>"
      user: "<user>"
      password: "<password>"
      role: "ACCOUNTADMIN"
      warehouse: "COMPUTE_WH"
      database: "TMDB_DEMO"
      schema: "RAW"
      threads: 4
      client_session_keep_alive: false
      vars:
        tmdb_api_integration_name: "tmdb_api_integration"
        tmdb_adapter_base_url: "https://tmdb-gw-xyz.a.run.app"
```

Switch target per cloud:

```bash
dbt run --target aws
dbt run --target azure
dbt run --target gcp
```

Same code, different vars.

---

## 4. dbt Macro for External Function Creation

Create `macros/tmdb_external_function.sql`:

```jinja
{% macro create_tmdb_external_function() %}

  {%- set api_integration_name = var("tmdb_api_integration_name") -%}
  {%- set base_url             = var("tmdb_adapter_base_url") -%}

  {%- if api_integration_name is none or api_integration_name == "" -%}
    {{ exceptions.raise("tmdb_api_integration_name var is not set") }}
  {%- endif -%}

  {%- if base_url is none or base_url == "" -%}
    {{ exceptions.raise("tmdb_adapter_base_url var is not set") }}
  {%- endif -%}

  {{ log("Creating external function tmdb_fetch_page using " ~ api_integration_name ~ " and base URL " ~ base_url, info=True) }}

  {% set ddl %}
    CREATE OR REPLACE EXTERNAL FUNCTION tmdb_fetch_page(page NUMBER)
    RETURNS VARIANT
    API_INTEGRATION = {{ api_integration_name }}
    AS '{{ base_url }}/tmdb_popular';
  {% endset %}

  {% do run_query(ddl) %}

{% endmacro %}
```

This macro:

- pulls environment-specific values from `vars`  
- issues the `CREATE OR REPLACE EXTERNAL FUNCTION` DDL  
- ensures the function signature and name are identical across clouds

You can keep `API INTEGRATION` creation in IaC, or add a second macro if you want dbt to manage it too.

---

## 5. Bootstrapping the External Function with dbt

### 5.1 Manual `run-operation`

Per environment, run:

```bash
dbt run-operation create_tmdb_external_function --target aws
dbt run-operation create_tmdb_external_function --target azure
dbt run-operation create_tmdb_external_function --target gcp
```

Each call:

- uses the target’s `vars`  
- creates `tmdb_fetch_page` wired to that cloud’s adapter

### 5.2 Optional: `on-run-start` hook

If you want the function to always exist before models execute, in `dbt_project.yml`:

```yaml
on-run-start:
  - "{{ create_tmdb_external_function() }}"
```

Then `dbt run --target aws` will automatically ensure `tmdb_fetch_page` exists, with the correct base URL for AWS; likewise for Azure/GCP.

---

## 6. dbt Model: Ingest TMDB Pages into Raw Table

Create `models/ingest_tmdb_raw.sql`:

```jinja
{{ config(
    materialized='table'
) }}

WITH pages AS (
    SELECT
        seq4() + 1 AS page_number
    FROM TABLE(GENERATOR(ROWCOUNT => 5))
)

SELECT
    tmdb_fetch_page(page_number)      AS api_response,
    '/movie/popular'                  AS api_endpoint,
    CURRENT_TIMESTAMP()               AS ingest_ts,
    page_number
FROM pages
```

Notes:

- For a first pass, `materialized='table'` is fine.
- You can change to incremental and use `page_number` as a key if you want.

Run per environment:

```bash
dbt run --models ingest_tmdb_raw --target aws
dbt run --models ingest_tmdb_raw --target azure
dbt run --models ingest_tmdb_raw --target gcp
```

The model is identical in each case; only the function wiring differs.

---

## 7. dbt Model: Flatten to Bronze

Create `models/tmdb_movies_bronze.sql`:

```jinja
{{ config(
    materialized='table'
) }}

WITH flattened AS (
    SELECT
        r.page_number,
        f.value                         AS movie_json,
        f.value:id::number              AS movie_id,
        f.value:title::string           AS title,
        f.value:overview::string        AS overview,
        f.value:release_date::date      AS release_date,
        f.value:popularity::float       AS popularity,
        f.value:vote_average::float     AS vote_average,
        f.value:vote_count::number      AS vote_count,
        r.ingest_ts
    FROM {{ ref('ingest_tmdb_raw') }} AS r,
         LATERAL FLATTEN(input => r.api_response:results) f
)

SELECT
    movie_id,
    title,
    overview,
    release_date,
    popularity,
    vote_average,
    vote_count,
    movie_json          AS raw,
    ingest_ts
FROM flattened
```

Run per environment:

```bash
dbt run --models tmdb_movies_bronze --target aws
dbt run --models tmdb_movies_bronze --target azure
dbt run --models tmdb_movies_bronze --target gcp
```

Again, the model is identical.

---

## 8. Verification Queries in Snowflake

After running dbt in an environment:

```sql
USE DATABASE tmdb_demo;
USE SCHEMA tmdb_demo.raw;

SELECT COUNT(*) AS raw_page_rows
FROM tmdb_movies_raw;

SELECT COUNT(*) AS movie_count
FROM tmdb_movies_bronze;

SELECT movie_id, title, release_date, popularity
FROM tmdb_movies_bronze
ORDER BY popularity DESC
LIMIT 10;
```

The behavior is consistent across AWS, Azure, and GCP.

---

## 9. What This dbt Pattern Achieves

Given Snowflake’s limitations (no env var in the `AS 'https://...'` URL, no single shared base URL across clouds), we:

- Move the **cloud-specific wiring** into dbt `vars`.
- Keep the **function name and signature** (`tmdb_fetch_page(page NUMBER)`) stable.
- Keep all **models, MERGE logic, and downstream SQL** identical across clouds.
- Use the **Adapter Pattern** at two levels:
  - HTTP adapter in each cloud (TMDB ↔ gateway)  
  - dbt macro as the adapter between environment-specific settings and Snowflake DDL  

Net result:

- **Python-free** data path  
- **Cloud-agnostic** dbt models and SQL  
- **dbt-managed external functions** per environment  
- Clean separation between **infra details** and **analytic logic**