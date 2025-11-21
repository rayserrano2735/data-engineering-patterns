# Modern Multi-Engine, Multi-Cloud Warehouse Architecture (Text Spec)

> **Scope:** This document captures our *current architectural alignments* in text form only (no diagrams), plus explicitly lists any **open issues / questions** that remain. It is intended as a precise handoff that another system can use to generate diagrams.

---

## 1. Core Vision

We are designing a **modern, SQL-first, multi-engine, multi-cloud warehouse** with these defining properties:

1. **DW Layers on Iceberg**  
   - All internal warehouse data is stored as **Apache Iceberg tables** on object storage (S3, ADLS, GCS).  
   - There are **no raw file swamps**; even Landing is Iceberg.

2. **Universal Catalog (Single Source of DW Truth)**  
   - One **engine-agnostic catalog** exposes all DW tables and metadata, and serves as the **DW dictionary**.  
   - Multiple engines interrogate the *same* catalog to discover and query the *same* Iceberg-backed DW layers.

3. **Multi-Engine Compute Mesh**  
   - Multiple SQL engines (e.g., **Snowflake**, **Databricks SQL**, **BigQuery**, **Redshift**, and “others”) operate as **peers**.  
   - No engine is treated as "the heavy engine" or "the BI engine" by ideology; each must **earn workloads empirically**.

4. **dbt as Control Plane; dbt Mesh as Sky**  
   - **dbt projects** define models/tests/contracts and use engines to materialize DW layers.  
   - **dbt Mesh** coordinates multiple dbt projects across domains and engines.  
   - dbt Mesh is conceptually the **Sky** (control and governance plane) above engines and clouds.

5. **Semantic Layer as Kimball Killer**  
   - The **Semantic Layer** is **metric-oriented, dimension-flexible**, and can **eliminate the need for physical marts**.  
   - It provides governed metrics to both BI and MCP, and is the **primary consumer of the DW Consumption layer**.

6. **MCP + Agentic**  
   - A **dbt MCP server** exposes the semantic model to agentic/LLM clients.  
   - **Agentic systems** call MCP (not Semantic directly).  
   - BI tools consume the **Semantic Layer** directly.

---

## 2. Data Warehouse Layers (DW Layers)

DW Layers are **roles**, not schemas. They are implemented as Iceberg tables and surfaced in the catalog as namespaces, but conceptually they are lifecycle stages:

1. **Landing Layer**  
   - First structured checkpoint after sources.  
   - Data is typed, lightly cleaned, and stored as Iceberg tables.  
   - Close to source schemas, but queryable; no raw, unstructured file dumps.

2. **Historical Vault Layer**  
   - Stores **full history** of entities and events (SCDs, soft deletes, audit columns).  
   - Source-faithful but **time-aware** and analytics-safe.  
   - Enables auditing, recon, and historical replay.

3. **Integration Layer** (EDW replacement)  
   - Conforms and integrates entities across domains (Inmon/UDM style).  
   - This is effectively the **Enterprise Data Warehouse** but we call it the **Integration layer** to avoid overloading “EDW” as both product and component.  
   - Provides clean business entities ready for wide reuse.

4. **Consumption Layer**  
   - The **primary input** to the Semantic Layer.  
   - Contains:
     - **Atomic, consumption-ready tables** (flattened or denormalized where appropriate).  
     - **Optional marts / star schemas** as transitional components.  
   - Over time, the goal is that **only atomic consumption structures remain**, with marts becoming unnecessary because the Semantic Layer can dynamically join dims and facts.

**Lifecycle Flow (conceptual):**

- `Sources → Landing → Historical Vault → Integration → Consumption → Semantic`

---

## 3. Catalog: Universal DW Dictionary

### 3.1 Role of the Catalog

The Catalog is:

- The **authoritative DW dictionary**  
- Engine-agnostic and multi-cloud  
- Responsible for:
  - Table and view registration  
  - Column and schema metadata  
  - Locations of Iceberg table data files  
  - Snapshots / versions / branches (if using something like Nessie)  

### 3.2 Relationships

Using “source → target” semantics:

- **`Catalog → Engine`**  
  - The Catalog **provides** DW metadata to Engines.  
  - Engines **interrogate** the Catalog to discover tables, schemas, and physical locations.

- **Logical dependency:**  
  - dbt Projects **logically depend** on the Catalog (for schema, refs, tests), but access it **through the Engine**.  
  - This may be represented in diagrams as a **dotted arrow** `Catalog …→ dbt Project`.

### 3.3 Catalog Choice

Architectural intent (not yet finalized as a brand):

- Prefer an **Iceberg-native, engine-agnostic, versioned catalog** (e.g., **Apache Nessie** or a REST catalog class of system).  
- Explicitly **avoid vendor-/cloud-specific catalogs** (e.g., Unity Catalog-only, Glue-only) as the *sole* catalog, to preserve neutrality.

---

## 4. Compute Mesh (Engines)

The **compute mesh** is the set of SQL engines that can execute dbt models and query DW Layers through the Catalog.

Key properties:

- **Peers, not hierarchy**: engines are not pre-assigned “roles” like “heavy ETL” or “BI only.”  
- **Empirical selection**: engine choice per workload is driven by performance, cost, and operational characteristics.  
- **Multi-cloud**: different engines may run in different clouds, all pointing at the same logical DW via the catalog.

Example engines within the mesh:

- Snowflake  
- Databricks SQL  
- BigQuery  
- Redshift  
- Others (future engines)  

**Direct relationships:**

- `Catalog → Engine` (metadata & dictionary)  
- `dbt Project → Engine` (SQL execution)  
- `Engine → DW Layers` (reads/writes Iceberg-backed tables)

---

## 5. dbt Projects and dbt Mesh

### 5.1 dbt Projects

Each **dbt project**:

- Targets **one engine** (per runtime configuration).  
- Contains:
  - Models (SQL + Jinja)  
  - Tests (data quality, referential integrity)  
  - Contracts (schema expectations)  
  - Documentation and lineage  
- Materializes DW layers as Iceberg tables via the Engine and Catalog.

**Relationship:**

- `dbt Project → Engine`  
  - The dbt project **uses** the Engine to execute SQL.  
- Logical: `Catalog …→ dbt Project` (through the Engine).

### 5.2 dbt Mesh

**dbt Mesh** is the **coordination and governance layer** over multiple dbt projects:

- Manages **cross-project dependencies** (e.g., Integration layer produced by one project feeding another).  
- Enforces **contracts and governance** across domains.  
- Does **not** talk to Iceberg or Catalog directly; it orchestrates at the project level.

**Relationship:**

- `dbt Mesh → dbt Project`  
  - Mesh coordinates and governs projects, not engines or storage.

Conceptually, this is the **Sky** over the compute mesh and DW layers.

---

## 6. Information & Semantic Plane

This is the **data/meaning flow**, independent of how it is executed.

### 6.1 Sources and DW Layers

- `Sources → Landing Layer`  
- `Landing Layer → Historical Vault Layer`  
- `Historical Vault Layer → Integration Layer`  
- `Integration Layer → Consumption Layer`  

Each arrow denotes that the downstream layer **depends on and is derived from** the upstream layer.

### 6.2 Semantic Layer – the Kimball Killer

The **Semantic Layer**:

- Consumes the **Consumption Layer** (primarily atomic tables; transitional marts if present).  
- Defines:
  - **Metrics** as first-class objects  
  - **Dimensions** as flexible, combinable entities  
  - **Relationships** between entities  
- Dynamically generates correct SQL for queries combining any metrics with any compatible dimensions.

This is why it is the **Kimball Killer**:

- Traditional Kimball marts pre-join facts and dims, fixing schema and grain in advance.  
- The Semantic Layer **virtualizes** these joins and grains, so we no longer need to pre-materialize all combinations as physical marts.  
- Over time, physical marts can be removed or reduced to performance-optimized materializations, not the primary semantic surface.

### 6.3 MCP and Agentic

- **`Consumption Layer → Semantic Layer`**  
  - Semantic definitions are built over Consumption data structures.

- **`Semantic Layer → MCP`**  
  - The **dbt MCP server** uses the semantic model as its source-of-truth for metrics, dims, and relationships.  
  - MCP exposes this to agentic/LLM clients.

- **`MCP → Agentic`**  
  - Agentic systems (LLMs, digital agents) issue queries via MCP, not by directly querying Semantic or engines.

### 6.4 BI Tools

- **`Semantic Layer → BI Tools`**  
  - BI tools (Tableau, Power BI, etc.) consume **Semantic metrics and dimensions**, not raw tables.  
  - The Semantic Layer is the **governed interface** for BI, keeping metrics consistent.

---

## 7. Arrow Semantics (for future diagramming)

To avoid ambiguity in any future diagrams, we lock in the arrow rule:

- **Arrows point from source → target.**
- **Source** = provider / prerequisite / dependency.  
- **Target** = consumer / dependent.

Examples:

- `Catalog → Engine` (Catalog provides DW dictionary to Engine).  
- `dbt Project → Engine` (dbt uses Engine to run models).  
- `Integration → Consumption` (Consumption derived from Integration).  
- `Consumption → Semantic` (Semantic built on Consumption).  
- `Semantic → MCP` (MCP relies on semantic definitions).  
- `MCP → Agentic` (Agentic relies on MCP API).  
- `Semantic → BI` (BI relies on Semantic).

Additionally:

- **Solid arrows** in future diagrams should represent **direct technical interaction**.  
- **Dotted arrows** should represent **logical / indirect dependency** (e.g., `Catalog …→ dbt Project`).

---

## 8. Multi-Engine, Shared-Catalog Paradigm Shift

This is a critical conceptual pillar that emerged from the II-driven analysis:

1. There is **one universal Catalog** for the warehouse.  
2. Multiple **Engines** (Snowflake, DBX, etc.) use that same Catalog.  
3. Multiple **dbt Projects** target those Engines.  
4. All Engines operate on the **same Iceberg-backed DW Layers** through that Catalog.

This means:

- No engine “owns” the data.  
- No project “owns” the catalog.  
- The catalog is the **shared spine** of the architecture.  
- dbt Mesh operates above this as the **Sky**, coordinating projects that, via engines, share the same DW.

---

## 9. Open Issues / Questions

These are deliberate **open points** we have *not* fully locked down and are left for further exploration (e.g., in another system that will generate diagrams):

1. **Catalog Implementation Choice**  
   - We conceptually favor something like **Apache Nessie** or an Iceberg REST catalog, but have not yet:  
     - Selected a specific implementation  
     - Defined branching/versioning policies  
     - Specified how cross-environment promotion (dev → test → prod) is handled via branches/tags.

2. **Exact Consumption Structures**  
   - We know the **Consumption Layer** will contain:  
     - Atomic consumption tables  
     - Transitional marts (while Kimball is being phased out)  
   - Open details:  
     - Naming conventions for atomic vs mart-like tables  
     - Criteria for when a mart is allowed / deprecated  
     - Performance strategies (e.g., selective materialized views vs pure semantic virtualization).

3. **Semantic Layer Implementation**  
   - We have defined its **role** and **impact (Kimball Killer)**, but not:  
     - The concrete technology (dbt Semantic Layer vs another metric store)  
     - How cross-engine query routing will work in detail  
     - How semantic caching / performance optimization is managed.

4. **Agentic Use Cases and Patterns**  
   - We know that **Agentic systems consume MCP**, which consumes Semantic.  
   - Open questions include:  
     - Standard prompt/interaction patterns for agents.  
     - Guardrails and governance for agent-generated queries.  
     - How agents choose among multiple engines (if MCP is multi-engine aware).

5. **Engine Selection Strategy**  
   - Principle is: **“Let the best engine win per workload.”**  
   - Open items:  
     - Standard benchmarks and metrics (latency, cost, concurrency, operational simplicity).  
     - How dbt Mesh expresses engine selection and fallback at the project or model level.  
     - Whether certain domains default to certain engines (with overrides), or everything is fully dynamic.

6. **Platform Product Naming & Packaging**  
   - We have **not yet named** the overall **platform product type** that includes:  
     - DW Layers  
     - Catalog  
     - Compute Mesh  
     - dbt Mesh & Projects  
     - Semantic / MCP / BI / Agentic surface  
   - “EDW” is no longer accurate, because the Integration layer is just one part of the system.  
   - We still need a **clear product name and external-facing concept** (e.g., “Modern Analytics Fabric,” “Sky Warehouse,” etc.).

7. **Governance & Security Topology**  
   - High-level idea:  
     - Centralized policies at Catalog and Semantic level  
   - Still pending:  
     - Detailed RBAC model across Catalog, Engines, dbt, and Semantic  
     - Cross-cloud identity mapping  
     - How governance metadata is surfaced to BI and Agentic consumers.

---

## 10. Handoff Notes for Diagramming

For any system (like Claude or a drawing tool) that will turn this into diagrams:

- **Start with two views** (Zachman-style):
  1. **Information Architecture (IA)** view:  
     - Components: Sources, DW Layers, Semantic, MCP, BI, Agentic.  
     - Arrows: data & meaning flow only.
  2. **Execution Architecture (EA)** view:  
     - Components: Catalog, Engines, dbt Projects, dbt Mesh, DW Layers.  
     - Arrows: control & execution flow, plus metadata direction.

- **Then, optionally, a third “integration” view** that shows:  
  - IA and EA layered together, but with great care to avoid clutter.  
  - Solid vs dotted arrows to distinguish direct vs logical dependency.

- **Follow the arrow semantics and open issues section strictly**; do not invent relationships not described here.

---

_End of Text Spec_
