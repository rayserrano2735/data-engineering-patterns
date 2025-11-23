# Python‑Free TMDB Ingestion into Snowflake Using External Functions + API Gateway

This tutorial walks you **end‑to‑end** through building a *Python‑less* pipeline that:

- Calls the **TMDB “popular movies” API** from inside Snowflake using an **external function**.
- Proxies the call through **AWS API Gateway + Lambda (Node.js)**.
- Stores the raw API responses in a **Snowflake table** as `VARIANT`.
- Flattens the JSON into a structured **movies table**.

When you’re done, you will:

- Run a single `INSERT … SELECT` in Snowflake.
- See **real TMDB movie records** in a Snowflake table.
- Have a reusable pattern for other APIs.

> Note: This tutorial assumes **Snowflake on AWS**. The pattern is portable to other clouds, but the concrete steps here use AWS API Gateway because Snowflake has first‑class support for it in external functions.

---

## 0. Prerequisites

You will need:

1. **Snowflake**  
   - Account on AWS.
   - Role with privileges: `ACCOUNTADMIN` or a role that can `CREATE INTEGRATION`, `CREATE FUNCTION`, `CREATE TABLE`, etc.

2. **AWS**  
   - An AWS account.
   - Permissions to create:
     - An **IAM role**.
     - An **AWS Lambda** function.
     - An **API Gateway** (REST API).

3. **TMDB**  
   - A TMDB account.
   - An API key (v3 API key is easiest for this example).  
   - Base URL: `https://api.themoviedb.org/3`

We’ll hard‑code `/movie/popular` in the example.

---

## 1. Create the Snowflake Database and Raw Table

First, in Snowflake, create a database, schema, and the raw landing table.

```sql
-- Use your admin role
USE ROLE ACCOUNTADMIN;

-- Create a database + schema for this tutorial
CREATE OR REPLACE DATABASE tmdb_demo;
CREATE OR REPLACE SCHEMA tmdb_demo.raw;

USE DATABASE tmdb_demo;
USE SCHEMA tmdb_demo.raw;

-- Raw landing table for TMDB API responses
CREATE OR REPLACE TABLE tmdb_movies_raw (
    api_response VARIANT,   -- full JSON response for one page
    api_endpoint STRING,    -- e.g. '/movie/popular'
    ingest_ts   TIMESTAMP   -- load timestamp
);
```

We’ll later populate `tmdb_movies_raw` with one row **per page** of TMDB results.

---

## 2. Create the AWS Lambda (Node.js) Proxy for TMDB

We will create a small **Node.js Lambda** that:

- Accepts HTTP GET from API Gateway.
- Reads a `page` query parameter.
- Calls TMDB `/movie/popular` with your API key.
- Returns the **raw JSON body** back to the caller.

### 2.1. Create the Lambda Function

In the AWS Console:

1. Go to **Lambda** → **Create function**.
2. Choose:
   - *Author from scratch*
   - Name: `tmdb_popular_proxy`
   - Runtime: **Node.js 20.x** (or any recent Node.js runtime)
3. Click **Create function**.

Replace the default handler code with:

```js
import fetch from "node-fetch"; // For Node 18+ you can also use global fetch

const TMDB_API_KEY = process.env.TMDB_API_KEY;

export const handler = async (event) => {
  try {
    const page =
      (event.queryStringParameters && event.queryStringParameters.page) || "1";

    const url = new URL("https://api.themoviedb.org/3/movie/popular");
    url.searchParams.set("api_key", TMDB_API_KEY);
    url.searchParams.set("page", page);

    const resp = await fetch(url.toString());
    if (!resp.ok) {
      return {
        statusCode: resp.status,
        body: JSON.stringify({ error: "TMDB error", status: resp.status }),
      };
    }

    const data = await resp.text(); // Return raw JSON as text
    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: data,
    };
  } catch (err) {
    console.error("Lambda error:", err);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Internal error" }),
    };
  }
};
```

**Environment variable:**

- In the Lambda configuration, set:
  - `TMDB_API_KEY = <your_tmdb_api_key>`

**Handler:**  
If using the default `index.mjs` file, set handler to `index.handler`.

Deploy the function.

> If your runtime already has a global `fetch`, you can drop the `node-fetch` import and just use `await fetch(...)`.

---

## 3. Create an API Gateway REST API for the Lambda

Now we expose the Lambda function via **API Gateway**, so Snowflake can call it via HTTPS.

1. In the AWS Console, go to **API Gateway**.
2. Click **Create API** → choose **REST API** → *Build*.
3. Choose:
   - New API
   - Name: `tmdb-popular-api`
   - Endpoint Type: **Regional** (simplest)
4. Click **Create API**.

### 3.1. Create Resource and Method

1. Under your new API, in the left panel, click **Actions** → **Create Resource**.
   - Resource Name: `tmdb_popular`
   - Resource Path: `/tmdb_popular`
2. With `/tmdb_popular` selected, click **Actions** → **Create Method** → choose `GET`.
3. For **GET**:
   - Integration type: **Lambda Function**
   - Use Lambda Proxy integration: **Yes** (recommended)
   - Lambda Region: your region
   - Lambda Function: `tmdb_popular_proxy`
4. Save and grant permissions if prompted.

### 3.2. Deploy the API

1. Click **Actions** → **Deploy API**.
2. Create a new Stage, e.g. `prod`.
3. After deploy, note the **Invoke URL**, which will look like:

   ```text
   https://abcd1234.execute-api.us-east-1.amazonaws.com/prod
   ```

The full endpoint Snowflake will call is:

```text
https://abcd1234.execute-api.us-east-1.amazonaws.com/prod/tmdb_popular
```

We’ll use this URL in Snowflake.

---

## 4. Create the IAM Role for Snowflake and Trust Relationship

Snowflake needs to **assume an IAM role** to call API Gateway.

### 4.1. Create an IAM Policy

1. Go to **IAM** → **Policies** → **Create policy** → JSON.
2. Use a policy like:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:*:<your_aws_account_id>:*"
    }
  ]
}
```

3. Name it: `snowflake_api_gateway_invoke`.

### 4.2. Create an IAM Role for Snowflake

1. Go to **IAM** → **Roles** → **Create role**.
2. Trusted entity type: **Another AWS account**.
   - For now, put any placeholder; we’ll update trust later after we get Snowflake’s user ARN.
3. Attach the `snowflake_api_gateway_invoke` policy.
4. Name the role: `snowflake_tmdb_external_function_role`.

Copy the **Role ARN**, e.g.:

```text
arn:aws:iam::123456789012:role/snowflake_tmdb_external_function_role
```

We’ll use this in Snowflake’s `CREATE API INTEGRATION`.

---

## 5. Create the API Integration in Snowflake

Back in Snowflake:

```sql
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE API INTEGRATION tmdb_api_integration
  API_PROVIDER = aws_api_gateway
  API_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake_tmdb_external_function_role'
  API_ALLOWED_PREFIXES = ('https://abcd1234.execute-api.us-east-1.amazonaws.com/prod/')
  ENABLED = TRUE;
```

Replace:

- `API_AWS_ROLE_ARN` with your IAM role ARN.
- `API_ALLOWED_PREFIXES` with your API Gateway base URL (ending with `/prod/`).

### 5.1. Get Snowflake’s IAM User ARN and External ID

Now run:

```sql
DESCRIBE INTEGRATION tmdb_api_integration;
```

Locate the rows:

- `API_AWS_IAM_USER_ARN`
- `API_AWS_EXTERNAL_ID`

Copy their `property_value` fields. You will use them in the IAM role **trust relationship**.

---

## 6. Update the IAM Role Trust Policy for Snowflake

In AWS IAM:

1. Go to the role `snowflake_tmdb_external_function_role`.
2. Click **Trust relationships** → **Edit trust policy**.
3. Use something like:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "<API_AWS_IAM_USER_ARN_FROM_SNOWFLAKE>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<API_AWS_EXTERNAL_ID_FROM_SNOWFLAKE>"
        }
      }
    }
  ]
}
```

Save the trust policy.

At this point:

- Snowflake knows about the IAM role via `API_INTEGRATION`.
- The IAM role trusts Snowflake via the external ID.

---

## 7. Create the External Function in Snowflake

Now define the external function that wraps calls to your API Gateway + Lambda proxy.

Still in `tmdb_demo.raw`:

```sql
USE DATABASE tmdb_demo;
USE SCHEMA tmdb_demo.raw;

CREATE OR REPLACE EXTERNAL FUNCTION tmdb_fetch_page(page NUMBER)
RETURNS VARIANT
API_INTEGRATION = tmdb_api_integration
AS 'https://abcd1234.execute-api.us-east-1.amazonaws.com/prod/tmdb_popular';
```

- `page` is passed to API Gateway as a query parameter, which Lambda uses.
- The function returns the **entire TMDB response JSON** for that page as `VARIANT`.

### 7.1. Quick Test

Test the function:

```sql
SELECT tmdb_fetch_page(1) AS page1;
```

You should see a single `VARIANT` value containing fields like:

- `page`
- `results`
- `total_pages`
- `total_results`

If it errors, check:

- API Gateway logs.
- Lambda logs (CloudWatch).
- IAM role trust + policy.
- `API_ALLOWED_PREFIXES`.

---

## 8. Load Multiple Pages into the Raw Table

This is the **Python‑free equivalent** of your `fetch_all_pages` + `load_to_snowflake` pipeline.

```sql
-- Insert N pages (e.g. first 5 pages) into the raw table
INSERT INTO tmdb_movies_raw (api_response, api_endpoint, ingest_ts)
SELECT
    tmdb_fetch_page(page) AS api_response,
    '/movie/popular'      AS api_endpoint,
    CURRENT_TIMESTAMP()   AS ingest_ts
FROM (
    SELECT SEQ4() + 1 AS page
    FROM TABLE(GENERATOR(ROWCOUNT => 5))
);
```

This will:

- Call TMDB pages 1–5.
- Insert **5 rows** into `tmdb_movies_raw`.
- Each row has one entire TMDB page JSON in `api_response`.

Verify:

```sql
SELECT COUNT(*) FROM tmdb_movies_raw;

SELECT api_response:page::int      AS page,
       ARRAY_SIZE(api_response:results) AS movies_in_page
FROM tmdb_movies_raw
ORDER BY page;
```

You should see at most 20 movies per page (TMDB default).

---

## 9. Flatten into a Structured Movies Table

Now we flatten the JSON into a per‑movie table.

### 9.1. Create the Movies Table

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

### 9.2. Populate `tmdb_movies_bronze`

```sql
INSERT INTO tmdb_movies_bronze (
    movie_id,
    title,
    overview,
    release_date,
    popularity,
    vote_average,
    vote_count,
    raw,
    ingest_ts
)
SELECT
    value:id::number               AS movie_id,
    value:title::string            AS title,
    value:overview::string         AS overview,
    value:release_date::date       AS release_date,
    value:popularity::float        AS popularity,
    value:vote_average::float      AS vote_average,
    value:vote_count::number       AS vote_count,
    value                          AS raw,
    r.ingest_ts                    AS ingest_ts
FROM tmdb_movies_raw AS r,
     LATERAL FLATTEN(input => r.api_response:results);
```

Verify:

```sql
SELECT COUNT(*) FROM tmdb_movies_bronze;

SELECT movie_id, title, release_date, popularity
FROM tmdb_movies_bronze
ORDER BY popularity DESC
LIMIT 10;
```

At this point you have **real TMDB movie records** in an actual Snowflake table, loaded via:

- External function  
- API Gateway  
- Node.js Lambda  

…and **no Python anywhere in the ingest path.**

---

## 10. Where to Go Next

Once the movies are in `tmdb_movies_bronze`, you can:

- Build a **dimension table** with your hash‑based `MERGE` CDC pattern.
- Add **genre lookup**, **cast/crew**, etc., by calling other TMDB endpoints via additional external functions.
- Schedule the pipeline with **Snowflake Tasks** to refresh data daily.

But the core tutorial requirement is complete:

> A **step‑by‑step, Python‑free process** that ends with running SQL in Snowflake to populate an actual table from an actual external API.