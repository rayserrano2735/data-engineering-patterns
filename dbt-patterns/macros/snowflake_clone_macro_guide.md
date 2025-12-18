# Snowflake Database Clone Macro User Guide

A dbt macro for generating DDL to clone Snowflake databases with flexible options for schema filtering, time travel, and multi-role permissions.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Parameters Reference](#parameters-reference)
4. [Usage Examples](#usage-examples)
5. [Permission Levels](#permission-levels)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Overview

The `clone_database` macro generates Snowflake DDL statements for cloning databases. It outputs SQL that you can review and execute directly in Snowflake, giving you full control over the cloning process.

### Key Features

- **Full or partial cloning**: Clone an entire database or select specific schemas
- **Time travel support**: Clone from a specific point in time
- **Multi-role permissions**: Configure read-only, read-write, and owner access levels
- **Future grants**: Automatically set up grants for objects created after the clone
- **Safe defaults**: Optional drop-if-exists prevents accidental overwrites

---

## Installation

Save the macro to your dbt project's `macros/` directory:

```
your_dbt_project/
├── macros/
│   └── clone_database.sql    <-- Place the macro here
├── models/
├── dbt_project.yml
└── ...
```

---

## Parameters Reference

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `source_db` | string | Yes | — | Name of the source database to clone |
| `target_db` | string | Yes | — | Name of the target (cloned) database |
| `role` | string | Yes | — | Role that will own the cloned database |
| `drop_if_exists` | boolean | No | `true` | Drop target database if it already exists |
| `warehouse` | string | No | `none` | Warehouse to use for the clone operation |
| `clone_timestamp` | string | No | `none` | ISO timestamp for time-travel clone |
| `schemas` | list | No | `none` | List of specific schemas to clone (default: all) |
| `read_only_roles` | list | No | `none` | Roles to grant read-only access |
| `read_write_roles` | list | No | `none` | Roles to grant read-write access |

---

## Usage Examples

### Basic Clone

Clone an entire database with default settings:

```bash
dbt run-operation clone_database --args '{
  "source_db": "ANALYTICS",
  "target_db": "DEV_ANALYTICS_RSERRANO",
  "role": "DEV_ROLE"
}'
```

**Generated DDL:**
```sql
USE ROLE DEV_ROLE;
DROP DATABASE IF EXISTS DEV_ANALYTICS_RSERRANO;
CREATE DATABASE DEV_ANALYTICS_RSERRANO CLONE ANALYTICS;
GRANT OWNERSHIP ON DATABASE DEV_ANALYTICS_RSERRANO TO ROLE DEV_ROLE COPY CURRENT GRANTS;
-- ... additional permission grants
```

---

### With Warehouse Specification

Specify which warehouse to use for the operation:

```bash
dbt run-operation clone_database --args '{
  "source_db": "ANALYTICS",
  "target_db": "DEV_ANALYTICS_RSERRANO",
  "role": "DEV_ROLE",
  "warehouse": "DEV_WH"
}'
```

**When to use:** When your role has access to multiple warehouses, or when you want to ensure a specific warehouse size is used for large clone operations.

---

### Time Travel Clone

Clone the database as it existed at a specific point in time:

```bash
dbt run-operation clone_database --args '{
  "source_db": "ANALYTICS",
  "target_db": "DEV_ANALYTICS_RSERRANO",
  "role": "DEV_ROLE",
  "clone_timestamp": "2024-01-15 10:30:00"
}'
```

**Generated DDL:**
```sql
CREATE DATABASE DEV_ANALYTICS_RSERRANO CLONE ANALYTICS
    AT (TIMESTAMP => '2024-01-15 10:30:00'::TIMESTAMP_LTZ);
```

**When to use:**
- Recovering from accidental data changes
- Creating a snapshot for testing against a known state
- Debugging issues that occurred at a specific time

**Note:** Time travel availability depends on your Snowflake edition and the `DATA_RETENTION_TIME_IN_DAYS` setting (default: 1 day for Standard, up to 90 days for Enterprise+).

---

### Schema-Specific Clone

Clone only specific schemas instead of the entire database:

```bash
dbt run-operation clone_database --args '{
  "source_db": "ANALYTICS",
  "target_db": "DEV_ANALYTICS_RSERRANO",
  "role": "DEV_ROLE",
  "schemas": ["STAGING", "MARTS", "CORE"]
}'
```

**Generated DDL:**
```sql
CREATE DATABASE DEV_ANALYTICS_RSERRANO;
CREATE SCHEMA DEV_ANALYTICS_RSERRANO.STAGING CLONE ANALYTICS.STAGING;
CREATE SCHEMA DEV_ANALYTICS_RSERRANO.MARTS CLONE ANALYTICS.MARTS;
CREATE SCHEMA DEV_ANALYTICS_RSERRANO.CORE CLONE ANALYTICS.CORE;
```

**When to use:**
- You only need a subset of the database
- Reducing clone time and storage for large databases
- Isolating specific areas for development or testing

---

### Multiple Roles with Different Access Levels

Grant different permission levels to multiple roles:

```bash
dbt run-operation clone_database --args '{
  "source_db": "ANALYTICS",
  "target_db": "DEV_ANALYTICS_RSERRANO",
  "role": "DEV_ROLE",
  "read_only_roles": ["ANALYST_ROLE", "REPORTING_ROLE"],
  "read_write_roles": ["DATA_ENGINEER_ROLE"]
}'
```

**When to use:**
- Development environments shared across teams
- QA environments where testers need read access
- Training environments with mixed access needs

---

### Full Featured Example

Combine all options for maximum control:

```bash
dbt run-operation clone_database --args '{
  "source_db": "ANALYTICS",
  "target_db": "DEV_ANALYTICS_RSERRANO",
  "role": "DEV_ROLE",
  "drop_if_exists": true,
  "warehouse": "DEV_WH",
  "clone_timestamp": "2024-01-15 10:30:00",
  "schemas": ["STAGING", "MARTS"],
  "read_only_roles": ["ANALYST_ROLE", "REPORTING_ROLE"],
  "read_write_roles": ["DATA_ENGINEER_ROLE"]
}'
```

---

### Preserve Existing Database

Set `drop_if_exists` to false to prevent accidental overwrites:

```bash
dbt run-operation clone_database --args '{
  "source_db": "ANALYTICS",
  "target_db": "DEV_ANALYTICS_RSERRANO",
  "role": "DEV_ROLE",
  "drop_if_exists": false
}'
```

**Note:** The clone will fail if the target database already exists.

---

## Permission Levels

The macro supports three permission levels:

### Owner (the `role` parameter)

Full control over the cloned database:
- `OWNERSHIP` on database, schemas, tables, and views
- `CREATE SCHEMA` on database
- `CREATE TABLE`, `CREATE VIEW` on schemas
- `SELECT`, `INSERT`, `UPDATE`, `DELETE` on all tables
- `USAGE` on functions and procedures

### Read-Write (`read_write_roles` parameter)

Modify data but not structure:
- `USAGE` on database and schemas
- `SELECT` on all tables and views
- `INSERT`, `UPDATE`, `DELETE` on all tables

### Read-Only (`read_only_roles` parameter)

View data only:
- `USAGE` on database and schemas
- `SELECT` on all tables and views

---

## Best Practices

### Naming Conventions

Use consistent naming for cloned databases:

```
{ENV}_{DATABASE}_{USERNAME}

Examples:
- DEV_ANALYTICS_RSERRANO
- QA_ANALYTICS_SPRINT42
- STAGING_ANALYTICS_20240115
```

### Development Workflow

1. **Morning refresh**: Clone prod at start of day
   ```bash
   dbt run-operation clone_database --args '{
     "source_db": "ANALYTICS",
     "target_db": "DEV_ANALYTICS_RSERRANO",
     "role": "DEV_ROLE"
   }'
   ```

2. **Test against known state**: Use time travel for reproducible tests
   ```bash
   dbt run-operation clone_database --args '{
     "source_db": "ANALYTICS",
     "target_db": "TEST_ANALYTICS_REGRESSION",
     "role": "QA_ROLE",
     "clone_timestamp": "2024-01-15 00:00:00"
   }'
   ```

3. **Minimal clones**: Only clone schemas you need
   ```bash
   dbt run-operation clone_database --args '{
     "source_db": "ANALYTICS",
     "target_db": "DEV_ANALYTICS_RSERRANO",
     "role": "DEV_ROLE",
     "schemas": ["MARTS"]
   }'
   ```

### Cost Optimization

Snowflake clones use zero-copy cloning, meaning:
- Initial clone is nearly instant and free
- Storage costs only accrue when data diverges from source
- Dropping a clone reclaims divergent storage immediately

**Tip:** Clean up unused dev clones regularly to minimize storage costs from divergent data.

---

## Troubleshooting

### Common Errors

**"Insufficient privileges"**

The executing role needs:
- `USAGE` on the source database
- `CREATE DATABASE` privilege (typically from `SYSADMIN` or custom role)

**"Object does not exist" (time travel)**

The requested timestamp may be outside the retention period. Check:
```sql
SHOW PARAMETERS LIKE 'DATA_RETENTION_TIME_IN_DAYS' IN DATABASE ANALYTICS;
```

**"Schema already exists" (schema-specific clone)**

When cloning specific schemas with `drop_if_exists: false`, the target database may already contain those schemas. Either:
- Set `drop_if_exists: true`
- Manually drop the conflicting schemas
- Use a different target database name

### Validation Queries

After running the generated DDL, validate the clone:

```sql
-- Check database exists
SHOW DATABASES LIKE 'DEV_ANALYTICS_RSERRANO';

-- Compare object counts
SELECT 
    'SOURCE' as db,
    COUNT(*) as table_count 
FROM ANALYTICS.INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
UNION ALL
SELECT 
    'TARGET' as db,
    COUNT(*) as table_count 
FROM DEV_ANALYTICS_RSERRANO.INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE';

-- Verify grants
SHOW GRANTS ON DATABASE DEV_ANALYTICS_RSERRANO;
```

---

## Quick Reference Card

```bash
# Basic clone
dbt run-operation clone_database --args '{"source_db": "PROD_DB", "target_db": "DEV_DB", "role": "MY_ROLE"}'

# With warehouse
... "warehouse": "MY_WH" ...

# Time travel
... "clone_timestamp": "2024-01-15 10:30:00" ...

# Specific schemas
... "schemas": ["SCHEMA1", "SCHEMA2"] ...

# Read-only roles
... "read_only_roles": ["ROLE1", "ROLE2"] ...

# Read-write roles
... "read_write_roles": ["ROLE1", "ROLE2"] ...

# Don't drop existing
... "drop_if_exists": false ...
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-XX | Initial release with basic cloning |
| 1.1.0 | 2024-01-XX | Added time travel, schema filtering, multi-role support |

---

## Support

For issues or feature requests, contact your data platform team or submit a request through your standard channels.
