# Alba's UDM Pattern Reference v2

## Universal Data Model Patterns for HDI Design

**Document Purpose:** Canonical reference for UDM patterns. This is Alba's class notes - created BY Alba, FOR Alba. When Ray says "use classification pattern here," Alba generates the structure correctly.

**Source:** Ray Serrano (20 years experience, contributor to Silverston's work)

**Version:** 2.0 - December 11, 2025

---

## The Cognitive Framework

Before anything else - this is WHY UDM matters:

```
The brain is a database.
Reality is the source system.
Perception is ETL.
Understanding is the model.
Thinking is querying.
```

UDM isn't just database design. It's **cognitive architecture**. The patterns work because they mirror how minds work - any mind, any substrate.

---

## Core Principles

### Why UDM?

**Traditional approach:**
- New requirement → ALTER TABLE
- New status → change code  
- New category → modify ETL
- Every change = risk, testing, deployment

**UDM approach:**
- New requirement → INSERT INTO
- Structure handles it
- Code handles it
- Already built for flexibility
- Changes are DATA, not CODE

**The principle:** Design for the PATTERN, not the values. Code never changes.

### Diagram Conventions

**Arrow points to CHILD:**
```
PARENT
   ↓
CHILD (has FK to parent)
```

**Hierarchy naming:**
- **parent_** = single parent (tree structure)
- **from_/to_** = multi-parent (network/recursion)

**All tables include:**
- Primary key: `{table_name}_id`
- `date_created TEXT`
- `date_updated TEXT`

---

## Sub-Models

**Critical concept:** Never look at 500 tables at once.

Break the model into focused views:
- Each sub-model: ~10 tables max
- Shared entities appear in multiple sub-models (bridges)
- Design and discuss one sub-model at a time

**Example:** VIVENCIA appears in both Classification sub-model and Status sub-model - that's the bridge.

---

## Pattern 1: CLASSIFICATION

**Problem it solves:** Entities need unlimited, flexible categorization without schema changes.

**Traditional (bad):**
```sql
entity (
    entity_id,
    is_type_a BOOLEAN,
    is_type_b BOOLEAN,
    is_type_c BOOLEAN,
    -- new type? ALTER TABLE, 360 columns later...
)
```

### Sub-Model: Vivencia Classification

```
┌─────────────────────────────────┐
│    VIVENCIA_CATEGORY_TYPE       │
├─────────────────────────────────┤
│ vivencia_category_type_id PK    │◄──┐
│ parent_vivencia_category_       │───┘ within (hierarchy)
│   type_id FK                    │
│ name                            │
│ date_created                    │
│ date_updated                    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│      VIVENCIA_CATEGORY          │
├─────────────────────────────────┤
│ vivencia_category_id PK         │◄──┐
│ parent_vivencia_category_id FK  │───┘ within (hierarchy)
│ vivencia_category_type_id FK    │
│ name                            │
│ from_date                       │
│ thru_date                       │
│ date_created                    │
│ date_updated                    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐      ┌─────────────────────────┐
│ VIVENCIA_CATEGORY_CLASSIFICATION│◄─────┤       VIVENCIA          │
├─────────────────────────────────┤      ├─────────────────────────┤
│ vivencia_category_              │      │ vivencia_id PK          │◄──┐
│   classification_id PK          │      │ parent_vivencia_id FK   │───┘
│ vivencia_id FK                  │      │ day_number              │
│ vivencia_category_id FK         │      │ titulo                  │
│ from_date                       │      │ contenido_compressed    │
│ thru_date                       │      │ search_text             │
│ date_created                    │      │ date_created            │
│ date_updated                    │      │ date_updated            │
└─────────────────────────────────┘      └─────────────────────────┘
```

### Naming Rule for Intersection Tables

The intersection table name = **entity** + **what it connects to** + **classification**

- vivencia connects to vivencia_category → **vivencia_category_classification**
- NOT ~~vivencia_classification~~ (wrong - doesn't say what it classifies INTO)

### DDL

```sql
CREATE TABLE vivencia_category_type (
    vivencia_category_type_id INTEGER PRIMARY KEY,
    parent_vivencia_category_type_id INTEGER,
    name TEXT NOT NULL,
    date_created TEXT,
    date_updated TEXT,
    FOREIGN KEY (parent_vivencia_category_type_id) 
        REFERENCES vivencia_category_type(vivencia_category_type_id)
);

CREATE TABLE vivencia_category (
    vivencia_category_id INTEGER PRIMARY KEY,
    parent_vivencia_category_id INTEGER,
    vivencia_category_type_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    from_date TEXT,
    thru_date TEXT,
    date_created TEXT,
    date_updated TEXT,
    FOREIGN KEY (parent_vivencia_category_id) 
        REFERENCES vivencia_category(vivencia_category_id),
    FOREIGN KEY (vivencia_category_type_id) 
        REFERENCES vivencia_category_type(vivencia_category_type_id)
);

CREATE TABLE vivencia_category_classification (
    vivencia_category_classification_id INTEGER PRIMARY KEY,
    vivencia_id INTEGER NOT NULL,
    vivencia_category_id INTEGER NOT NULL,
    from_date TEXT,
    thru_date TEXT,
    date_created TEXT,
    date_updated TEXT,
    FOREIGN KEY (vivencia_id) REFERENCES vivencia(vivencia_id),
    FOREIGN KEY (vivencia_category_id) 
        REFERENCES vivencia_category(vivencia_category_id)
);
```

### Power of Classification

- Unlimited categories without schema change
- Hierarchy at category level (subcategories)
- Hierarchy at category TYPE level (meta-organization)
- Temporal - classifications can change over time
- Multiple classifications simultaneously
- New category? INSERT. Not ALTER.

---

## Pattern 2: STATUS

**Problem it solves:** Tracking entity lifecycle with full history, multiple simultaneous states, and temporal precision.

**Traditional (bad):**
```sql
entity (
    entity_id,
    status VARCHAR(20)  -- single status, no history, no overlap
)
```

### Sub-Model: Vivencia Status

```
┌─────────────────────────┐
│       VIVENCIA          │
├─────────────────────────┤
│ vivencia_id PK          │
│ ...                     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────────┐      ┌─────────────────────────┐
│      VIVENCIA_STATUS        │◄─────┤      STATUS_TYPE        │
├─────────────────────────────┤      ├─────────────────────────┤
│ vivencia_status_id PK       │      │ status_type_id PK       │
│ vivencia_id FK              │      │ name                    │
│ status_type_id FK           │      │ date_created            │
│ status_datetime             │      │ date_updated            │
│ status_from_date            │      └─────────────────────────┘
│ status_thru_date            │
│ from_date                   │
│ thru_date                   │
│ date_created                │
│ date_updated                │
└─────────────────────────────┘
```

### DDL

```sql
CREATE TABLE status_type (
    status_type_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    date_created TEXT,
    date_updated TEXT
);

CREATE TABLE vivencia_status (
    vivencia_status_id INTEGER PRIMARY KEY,
    vivencia_id INTEGER NOT NULL,
    status_type_id INTEGER NOT NULL,
    status_datetime TEXT,
    status_from_date TEXT,
    status_thru_date TEXT,
    from_date TEXT,
    thru_date TEXT,
    date_created TEXT,
    date_updated TEXT,
    FOREIGN KEY (vivencia_id) REFERENCES vivencia(vivencia_id),
    FOREIGN KEY (status_type_id) REFERENCES status_type(status_type_id)
);
```

### Three Levels of Temporality

1. **status_datetime** - When did the status EVENT happen?
2. **status_from/thru_date** - When was the status EFFECTIVE?
3. **from/thru_date** - When was the RECORD valid?

### Power of Status

- Multiple statuses simultaneously
- Full history of every status
- New status = INSERT, not ALTER
- Temporal precision at three levels

---

## Pattern 3: CLASSIFICATION Applied to STATUS

**The insight:** You can apply the Classification pattern to ANY entity you want to classify - including VIVENCIA_STATUS.

This lets you GROUP statuses into categories.

### Sub-Model: Vivencia Status + Status Classification

```
┌─────────────────────────┐
│       VIVENCIA          │
├─────────────────────────┤
│ vivencia_id PK          │
│ ...                     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────────┐      ┌─────────────────────────┐
│      VIVENCIA_STATUS        │◄─────┤      STATUS_TYPE        │
├─────────────────────────────┤      ├─────────────────────────┤
│ vivencia_status_id PK       │      │ status_type_id PK       │
│ vivencia_id FK              │      │ name                    │
│ status_type_id FK           │      │ date_created            │
│ ...                         │      │ date_updated            │
└────────────┬────────────────┘      └─────────────────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│ VIVENCIA_STATUS_CATEGORY_            │
│              CLASSIFICATION          │
├──────────────────────────────────────┤
│ vivencia_status_category_            │
│   classification_id PK               │
│ vivencia_status_id FK                │
│ vivencia_status_category_id FK       │
│ from_date / thru_date                │
│ date_created / date_updated          │
└──────────────────────────────────────┘
             ▲
             │
┌────────────┴────────────────┐
│  VIVENCIA_STATUS_CATEGORY   │
├─────────────────────────────┤
│ vivencia_status_category_id │◄──┐
│   PK                        │───┘ within
│ parent_...category_id FK    │
│ vivencia_status_category_   │
│   type_id FK                │
│ name                        │
│ from_date / thru_date       │
│ date_created / date_updated │
└────────────┬────────────────┘
             ▲
             │
┌────────────┴────────────────────┐
│ VIVENCIA_STATUS_CATEGORY_TYPE   │
├─────────────────────────────────┤
│ vivencia_status_category_       │◄──┐
│   type_id PK                    │───┘ within
│ parent_...type_id FK            │
│ name                            │
│ date_created / date_updated     │
└─────────────────────────────────┘
```

### Use Case

Group statuses like:
- "raw", "iterating", "curated" → category "Curation Workflow"
- "active", "archived", "replaced" → category "Lifecycle"

Query all statuses in a category. Roll up reporting. Patterns on patterns = unlimited flexibility.

---

## Pattern 4: HIERARCHY (Embedded)

**The insight:** Hierarchy is not a separate pattern - it's embedded via self-referencing FK.

```sql
parent_entity_category_id FK REFERENCES entity_category(entity_category_id)
```

### Naming Convention

| Structure | Naming | Example |
|-----------|--------|---------|
| Single parent (tree) | **parent_** | parent_vivencia_id |
| Multi-parent (network) | **from_/to_** | from_vivencia_id, to_vivencia_id |

### Power of Hierarchy

- Unlimited depth
- Trees and DAGs
- Roll-up queries
- Flexible reorganization (just UPDATE parent_id)

---

## Usage Protocol

**When Ray says:**
- "Classification pattern for X" → Generate X_CATEGORY_TYPE + X_CATEGORY + X_CATEGORY_CLASSIFICATION
- "Status pattern for X" → Generate STATUS_TYPE + X_STATUS
- "Classify the status" → Apply Classification pattern TO the status entity
- "Add hierarchy" → Ensure parent_id self-reference exists

**Output format:**
1. Identify which sub-model we're in
2. ASCII diagram first (for review)
3. DDL after approval
4. Arrow points to child

---

## Naming Conventions (UDM)

- Tables: singular (vivencia, not vivencias)
- IDs: fully named (vivencia_id, not id)
- Foreign keys: same name as referenced PK
- Dates: named (date_created, date_updated, from_date, thru_date)
- Intersection tables: entity + target + classification

---

## The Transformation Principle

**Code is written for the PATTERN, not the VALUES.**

```sql
-- This query NEVER changes, regardless of how many categories exist:
SELECT v.titulo, vc.name as category
FROM vivencia v
JOIN vivencia_category_classification vcc ON v.vivencia_id = vcc.vivencia_id
JOIN vivencia_category vc ON vcc.vivencia_category_id = vc.vivencia_category_id
WHERE vcc.thru_date IS NULL;
```

New category? INSERT INTO vivencia_category.
Code unchanged. Structure unchanged. Deployment = data load.

---

## Full alba.db Schema (10 Tables)

| Table | Purpose | Sub-Model |
|-------|---------|-----------|
| vivencia | Core entity with self-hierarchy | Both |
| vivencia_fts | FTS5 search | N/A |
| vivencia_category_type | Types of categories | Classification |
| vivencia_category | Categories (hierarchical) | Classification |
| vivencia_category_classification | Vivencia ↔ Category | Classification |
| status_type | Status lookup | Status |
| vivencia_status | Vivencia ↔ Status | Status |
| vivencia_status_category_type | Types of status categories | Status |
| vivencia_status_category | Status categories | Status |
| vivencia_status_category_classification | Status ↔ Status Category | Status |

---

## RAG vs Database

**RAG:** chunk → embed → vector store → similarity search → cosine distance → top_k retrieval → rerank → context window stuffing → hope it's relevant

**Database:** 
```sql
SELECT answer FROM flashcard WHERE topic = 'UDM';
```

*"Database, anyone? Hello?"*

---

## More Patterns (To Be Added)

- Party Pattern (customer 360, relationships)
- Role Pattern
- Product Pattern
- Agreement Pattern
- Association Pattern (from_/to_ recursion)

---

*Alba Serrano - Built on Silverston, powered by HDI*

*"8 patterns. Applied many times. 500 tables become simple."*
