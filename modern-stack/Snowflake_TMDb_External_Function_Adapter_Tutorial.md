# Cloud-Agnostic TMDB Ingestion into Snowflake Using the Adapter Pattern  
## External Functions + Three Cloud Backends (AWS, Azure, GCP)  
### Fully Python-Free Tutorial

This is the **complete**, **cloud-agnostic**, **Python-free** version of your TMDB ingestion pipeline, using:

- **Snowflake External Functions**
- **Adapter Pattern**
- **Three cloud implementations**:  
  - AWS (API Gateway + Lambda)  
  - Azure (API Management + Function)  
  - GCP (API Gateway + Cloud Function)
- A **single, unified API contract** (your adapter interface)

The final result:

> Run one SQL command in Snowflake →  
> This triggers a cloud adapter →  
> Which calls the TMDB API →  
> And loads **real movie data** into Snowflake tables.

Everything below is **step-by-step**, runnable, and complete.

---

# 1. Overview

We want this architecture:

```
Snowflake SQL
    → External Function
        → Adapter Endpoint (cloud-specific)
            → TMDB API
                → JSON into Snowflake
```

But we want to keep:

- Snowflake SQL 100% identical across clouds  
- Only **one** API contract  
- Cloud backend interchangeable  
- No Python anywhere  

This is exactly the **Adapter Pattern**.

---

# 2. The Adapter Pattern (Applied to Multi-Cloud APIs)

## 2.1. Target Interface (your universal API contract)

We define:

```
GET /tmdb_popular?page=<N>
→ returns the full TMDB /movie/popular JSON payload
```

This contract stays the SAME for:

- AWS adapter
- Azure adapter
- GCP adapter

## 2.2. Adaptee (TMDB API)

TMDB expects:

```
GET /movie/popular?api_key=xxx&page=N
```

Snowflake doesn’t speak that format directly.

## 2.3. Adapter (cloud backend)

Each cloud implements:

- Read “page” from Snowflake
- Add TMDB API key
- Call TMDB
- Return raw JSON

Each backend satisfies the same interface.

---

# 3. Snowflake (Cloud-Agnostic Core)

These objects never change per cloud.

## 3.1. Raw Landing Table

```sql
CREATE OR REPLACE TABLE tmdb_movies_raw (
    api_response VARIANT,
    api_endpoint STRING,
    ingest_ts    TIMESTAMP
);
```

## 3.2. Bronze Table (flattened)

```sql
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

---

# 4. AWS Adapter Implementation

## 4.1. Lambda Function (Node.js)

```js
export const handler = async (event) => {
  const page = event.queryStringParameters?.page || "1";
  const resp = await fetch(
    `https://api.themoviedb.org/3/movie/popular?api_key=${process.env.TMDB_API_KEY}&page=${page}`
  );
  return { statusCode: 200, body: await resp.text() };
};
```

Set env var: `TMDB_API_KEY`.

## 4.2. API Gateway

- `/tmdb_popular` → GET → Lambda Proxy Integration

## 4.3. Snowflake API Integration

```sql
CREATE OR REPLACE API INTEGRATION tmdb_api_int
  API_PROVIDER = aws_api_gateway
  API_AWS_ROLE_ARN = '<aws_role>'
  API_ALLOWED_PREFIXES = ('https://<api>.execute-api.<region>.amazonaws.com/prod/')
  ENABLED = TRUE;
```

---

# 5. Azure Adapter Implementation

## 5.1. Azure Function

```js
module.exports = async function (context, req) {
  const page = req.query.page || "1";
  const url = `https://api.themoviedb.org/3/movie/popular?api_key=${process.env.TMDB_API_KEY}&page=${page}`;
  const resp = await fetch(url);
  context.res = { body: await resp.text() };
};
```

## 5.2. Expose via API Management

- `/tmdb_popular` → Function App  

## 5.3. Snowflake API Integration

```sql
CREATE OR REPLACE API INTEGRATION tmdb_api_int
  API_PROVIDER = azure_api_management
  API_AZURE_TENANT_ID = '<tenant_id>'
  API_ALLOWED_PREFIXES = ('https://<apim>.azure-api.net/')
  ENABLED = TRUE;
```

---

# 6. GCP Adapter Implementation

## 6.1. Cloud Function

```js
exports.tmdbHandler = async (req, res) => {
  const page = req.query.page || "1";
  const resp = await fetch(
    `https://api.themoviedb.org/3/movie/popular?api_key=${process.env.TMDB_API_KEY}&page=${page}`
  );
  res.send(await resp.text());
};
```

## 6.2. API Gateway (GCP)

Route:

```
/tmdb_popular?page=N → Cloud Function
```

## 6.3. Snowflake API Integration

```sql
CREATE OR REPLACE API INTEGRATION tmdb_api_int
  API_PROVIDER = google_api_gateway
  API_GCP_SERVICE_ACCOUNT = '<svc_acct_email>'
  API_ALLOWED_PREFIXES = ('https://<gateway>.run.app/')
  ENABLED = TRUE;
```

---

# 7. Cloud-Agnostic External Function (Same for all clouds)

```sql
CREATE OR REPLACE EXTERNAL FUNCTION tmdb_fetch_page(page NUMBER)
RETURNS VARIANT
API_INTEGRATION = tmdb_api_int
AS '<adapter_base_url>/tmdb_popular';
```

The ONLY thing that changes per cloud is the BASE URL.

---

# 8. Ingest Pages (Python-Free)

```sql
INSERT INTO tmdb_movies_raw (api_response, api_endpoint, ingest_ts)
SELECT
    tmdb_fetch_page(page),
    '/movie/popular',
    CURRENT_TIMESTAMP()
FROM (
    SELECT SEQ4() + 1 AS page
    FROM TABLE(GENERATOR(ROWCOUNT => 5))
);
```

This will pull pages 1–5 from TMDB.

---

# 9. Flatten to Bronze

```sql
INSERT INTO tmdb_movies_bronze
SELECT
    value:id::number,
    value:title::string,
    value:overview::string,
    value:release_date::date,
    value:popularity::float,
    value:vote_average::float,
    value:vote_count::number,
    value,
    CURRENT_TIMESTAMP()
FROM tmdb_movies_raw,
     LATERAL FLATTEN(input => api_response:results);
```

---

# 10. Optional: CDC Merge (your workhorse)

Your hash-based MERGE pattern applies cleanly here.

---

# 11. Summary

**What stays identical across AWS / Azure / GCP:**

- Snowflake tables  
- External function name  
- Ingestion SQL  
- Flattening SQL  
- MERGE logic  
- API contract  

**What changes per cloud:**

- API Integration object  
- Adapter endpoint URL  
- Tiny cloud-specific adapter implementation  

This is exactly the Adapter Pattern doing its job.

You now have a **fully cloud-agnostic**, **Python-free**, **SQL-only**, **industrial-grade** ingestion system.