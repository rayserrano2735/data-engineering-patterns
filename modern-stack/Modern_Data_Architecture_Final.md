# Modern Multi-Engine, Multi-Cloud Data Architecture (Final Text-Only Specification)

## 0. Purpose
This document defines the **canonical, metals-free** modern data architecture we designed.  
It is written **without diagrams** so it can be provided directly to Claude for diagram generation.

This is the authoritative textual specification.

---

## 1. Guiding Principles

### 1.1 No Metals  
We explicitly **reject** the obsolete "bronze/silver/gold" lakehouse model.  
It is a legacy artifact of the data-lake swamp era.

### 1.2 Iceberg Everywhere  
All data storage uses **Apache Iceberg** as the universal open table format, enabling:

- Multi-engine compute (Snowflake, Databricks, BigQuery, Redshift, others)
- Multi-cloud storage (AWS S3, Azure ADLS, GCP GCS)
- ACID, time travel, versioning, schema evolution

### 1.3 dbt Mesh = Sky  
dbt Mesh acts as the **coordinating plane** across all engines and clouds.  
This is the “Sky layer” that unifies transformation logic across environments.

### 1.4 Semantic Layer is the Kimball Killer  
The semantic layer provides **metrics + dimensions** as composable elements.  
It enables BI and agentic consumers to work directly off standardized metrics.

### 1.5 MCP Feeds Agentics  
The Model Context Protocol server draws from the semantic layer, enabling **agents** to consume the same metric definitions as BI tools.

---

## 2. Architectural Layers

### 2.1 Source Systems  
Operational systems that generate data.  
Examples: EHR, finance, CRM, ERP, web events, APIs.

### 2.2 Land Layer (Iceberg-Based Ingestion Layer)  
**Name: land**  
This is the first stop after ingestion.

Characteristics:
- Iceberg tables (not raw files)
- Schema-on-write, strongly typed
- Handles all forms of ingestion
- Supports multi-cloud & multi-engine access

### 2.3 Vault Layer  
Name: **vault**  
A historical, immutable layer.

Characteristics:
- Stores change history
- Models raw business entities
- Full fidelity retention
- Iceberg-based

### 2.4 Integration Layer  
Name: **integrate**  
This is the **EDW** in the modern architecture.

Characteristics:
- Conformed dimensions
- Clean business entities
- Domain integration
- The replacement for legacy Inmon/Kimball patterns

### 2.5 Consumption Layer  
Name: **consume**  
Where flattened, ready-to-query analytic objects live.

Characteristics:
- Simplified, performant structures
- Still Iceberg tables
- Supports both BI and agentic consumption
- Eventually minimized as semantic layer takes over

---

## 3. Logical Flow (Arrows)

Below is the directional flow using source → target notation.

```
sources -> land
land -> vault
vault -> integrate
integrate -> consume
consume -> semantic
semantic -> mcp
mcp -> agentic
semantic -> bi
```

### 3.1 Engines & Catalog

```
catalog -> engine
dbt project -> engine (solid line)
catalog -> dbt project (dotted line, metadata-level)
engine -> iceberg (read/write)
```

dbt Mesh orchestrates transformations across engines.

---

## 4. Multi-Engine Positioning

### 4.1 Snowflake  
SQL-first, cost-optimized, reliable, strong governance.

### 4.2 Databricks  
Notebook-first, data-science friendly.  
Not a “superior heavy-load engine”—that bias is legacy and incorrect.

### 4.3 BigQuery / Redshift (Optional)  
Additional engines reading from the same Iceberg tables.

### 4.4 Positioning Philosophy  
**Engines are collaborators, not competitors.**  
Iceberg enables parallel, concurrent compute access.

---

## 5. dbt Mesh (“Sky”)  

### 5.1 Responsibilities
- Orchestrates transformations across engines
- Manages cross-project lineage
- Enforces governance
- Acts as the unifying layer above compute

### 5.2 Position in Flow

```
dbt project -> engine -> iceberg -> dw layers
```

---

## 6. Semantic Layer (Kimball Killer)

### 6.1 Role
- Defines metrics (e.g., revenue, active patients)
- Defines dimensions (e.g., date, region, provider)
- Supports dynamic, combinatorial metric assembly

### 6.2 BI Connections

```
bi -> semantic
```

### 6.3 Agentic Connections (via MCP)

```
agentic -> mcp -> semantic
```

The agentic layer never queries raw tables.

---

## 7. MCP (Model Context Protocol)

### 7.1 Role
- Gateway for agents
- Exposes standardized metrics from the semantic layer
- Removes the need for agents to understand SQL or schemas

### 7.2 Flow

```
semantic -> mcp -> agentic
```

---

## 8. Catalog (Engine-Agnostic Metadata Layer)

### 8.1 Role
- Provides metadata access (schema, lineage, Iceberg manifests)
- Informs engines how to interact with Iceberg tables

### 8.2 Flow

```
catalog -> engine
catalog -> dbt project (dotted)
```

---

## 9. Core Guarantees

### 9.1 Multi-Engine Concurrency  
Iceberg ensures Snowflake and Databricks can read/write concurrently.

### 9.2 Multi-Cloud Flexibility  
Iceberg works with S3, ADLS, and GCS.

### 9.3 Python-Minimized Architecture  
We avoid Python where SQL/dbt/Iceberg suffice.  
APIs can be ingested using Snowflake external functions or dbx notebooks when required.

### 9.4 No Forward References  
Each layer depends only on the one below it.

---

## 10. Summary (Claude-Ready)

### **Layer Stack**
1. sources  
2. land  
3. vault  
4. integrate  
5. consume  
6. semantic  
7. mcp  
8. agentic  

### **Compute & Catalog**
- engines ↔ iceberg  
- catalog → engines  
- dbt Mesh → engines  
- dbt Mesh (dotted) → catalog  

### **Consumption**
- bi → semantic  
- agentic → mcp → semantic  

### **Storage**
- everything persists to Iceberg  

---

## Appendix A: Naming Conventions

- land = ingestion layer  
- vault = history layer  
- integrate = EDW layer  
- consume = analytic layer  
- semantic = metrics/dimensions layer  
- mcp = agentic gateway  

---

This is the complete, final, metals-free architecture document.  
Ready for Claude to produce diagrams.