# Alba's UDM Pattern Reference
## Universal Data Model Patterns for HDI Design

**Document Purpose:** Canonical reference for UDM patterns. When Ray says "use classification pattern here," Alba generates the structure without explanation needed.

**Source:** Ray Serrano (20 years experience, contributor to Silverston's work)

**Last Updated:** December 10, 2025

---

## Why UDM?

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

**The principle:** Design for the pattern, not the values. Code never changes.

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
    -- new type? ALTER TABLE
)
```

**UDM Pattern:**

```
┌─────────────────────────┐
│        ENTITY           │
├─────────────────────────┤
│ entity_id (PK)          │
└───────────┬─────────────┘
            │
            │ classified by
            │
┌───────────▼─────────────────────────┐
│     ENTITY_CLASSIFICATION           │
├─────────────────────────────────────┤
│ entity_classification_id (PK)       │
│ entity_id (FK)                      │
│ entity_category_id (FK)             │
│ from_date                           │
│ thru_date                           │
└───────────┬─────────────────────────┘
            │
            │ defined by
            │
┌───────────▼─────────────────────────┐
│       ENTITY_CATEGORY               │
├─────────────────────────────────────┤
│ entity_category_id (PK)             │
│ parent_entity_category_id (FK)      │◄─┐ within (HIERARCHY)
│ entity_category_type_id (FK)        │  │
│ name                                │──┘
│ from_date                           │
│ thru_date                           │
└───────────┬─────────────────────────┘
            │
            │ classified within
            │
┌───────────▼─────────────────────────┐
│     ENTITY_CATEGORY_TYPE            │
├─────────────────────────────────────┤
│ entity_category_type_id (PK)        │
│ parent_entity_category_type_id (FK) │◄─┐ within (HIERARCHY)
│ name                                │──┘
└─────────────────────────────────────┘
```

**Power:**
- Unlimited categories without schema change
- Hierarchy at category level (subcategories)
- Hierarchy at category TYPE level (meta-organization)
- Temporal - classifications can change over time
- Multiple classifications simultaneously

**Example DDL (for VIVENCIA):**

```sql
CREATE TABLE vivencia_category_type (
    vivencia_category_type_id INTEGER PRIMARY KEY,
    parent_vivencia_category_type_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (parent_vivencia_category_type_id) 
        REFERENCES vivencia_category_type(vivencia_category_type_id)
);

CREATE TABLE vivencia_category (
    vivencia_category_id INTEGER PRIMARY KEY,
    parent_vivencia_category_id INTEGER,
    vivencia_category_type_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    from_date TEXT NOT NULL,
    thru_date TEXT,
    FOREIGN KEY (parent_vivencia_category_id) 
        REFERENCES vivencia_category(vivencia_category_id),
    FOREIGN KEY (vivencia_category_type_id) 
        REFERENCES vivencia_category_type(vivencia_category_type_id)
);

CREATE TABLE vivencia_classification (
    vivencia_classification_id INTEGER PRIMARY KEY,
    vivencia_id INTEGER NOT NULL,
    vivencia_category_id INTEGER NOT NULL,
    from_date TEXT NOT NULL,
    thru_date TEXT,
    FOREIGN KEY (vivencia_id) REFERENCES vivencia(vivencia_id),
    FOREIGN KEY (vivencia_category_id) 
        REFERENCES vivencia_category(vivencia_category_id)
);
```

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

**UDM Pattern:**

```
┌─────────────────────────────────┐
│          STATUS_TYPE            │
├─────────────────────────────────┤
│ status_type_id (PK)             │
│ name                            │
└───────────┬─────────────────────┘
            │ 
            │ a classification for
            │
┌───────────▼─────────────────────┐
│       ENTITY_STATUS             │
├─────────────────────────────────┤
│ entity_status_id (PK)           │
│ entity_id (FK)                  │
│ status_type_id (FK)             │
│ status_datetime                 │  ← when event happened
│ status_from_date                │  ← effective start
│ status_thru_date                │  ← effective end
│ from_date                       │  ← record validity start
│ thru_date                       │  ← record validity end
└───────────┬─────────────────────┘
            │
            │ a status for
            │
┌───────────▼─────────────────────┐
│          ENTITY                 │
├─────────────────────────────────┤
│ entity_id (PK)                  │
└─────────────────────────────────┘
```

**Power:**
- Multiple statuses simultaneously
- Full history of every status
- Three levels of temporality:
  1. When did the status EVENT happen (status_datetime)
  2. When was the status EFFECTIVE (status_from/thru_date)
  3. When was the RECORD valid (from/thru_date)
- New status = INSERT, not ALTER

**Example DDL (for VIVENCIA):**

```sql
CREATE TABLE status_type (
    status_type_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE vivencia_status (
    vivencia_status_id INTEGER PRIMARY KEY,
    vivencia_id INTEGER NOT NULL,
    status_type_id INTEGER NOT NULL,
    status_datetime TEXT,
    status_from_date TEXT NOT NULL,
    status_thru_date TEXT,
    from_date TEXT NOT NULL,
    thru_date TEXT,
    FOREIGN KEY (vivencia_id) REFERENCES vivencia(vivencia_id),
    FOREIGN KEY (status_type_id) REFERENCES status_type(status_type_id)
);
```

---

## Pattern 3: STATUS with CLASSIFICATION (Combined)

**The insight:** STATUS TYPE itself can be classified using the CLASSIFICATION pattern.

**Why:** Group statuses into categories. "raw", "iterating", "curated" belong to "Curation Workflow". "active", "archived", "replaced" belong to "Lifecycle".

```
┌─────────────────────────────────────┐
│  STATUS_TYPE_CATEGORY_CLASSIFICATION│
├─────────────────────────────────────┤
│ status_type_category_classif_id (PK)│
│ status_type_id (FK)                 │
│ status_type_category_id (FK)        │
│ from_date                           │
│ thru_date                           │
└───────────┬─────────────────────────┘
            │
            │ defined by
            │
┌───────────▼─────────────────────────┐
│     STATUS_TYPE_CATEGORY            │
├─────────────────────────────────────┤
│ status_type_category_id (PK)        │
│ parent_status_type_category_id (FK) │◄─┐ within
│ status_type_category_type_id (FK)   │  │
│ name                                │──┘
│ from_date                           │
│ thru_date                           │
└───────────┬─────────────────────────┘
            │
            │ classified within
            │
┌───────────▼─────────────────────────┐
│   STATUS_TYPE_CATEGORY_TYPE         │
├─────────────────────────────────────┤
│ status_type_category_type_id (PK)   │
│ parent_status_type_cat_type_id (FK) │◄─┐ within
│ name                                │──┘
└─────────────────────────────────────┘
```

**Power:**
- Status types grouped into categories
- Categories can have hierarchy
- Query all "Curation Workflow" statuses at once
- Roll up status reporting
- Patterns on patterns = unlimited flexibility

---

## Pattern 4: HIERARCHY (Embedded)

**The insight:** Hierarchy is not a separate pattern - it's embedded in other patterns via self-referencing FK.

```sql
parent_entity_category_id (FK) REFERENCES entity_category(entity_category_id)
```

**This enables:**
- Unlimited depth
- Trees and DAGs
- Roll-up queries
- Flexible reorganization (just update parent_id)

**In Classification:** Categories within categories
**In Status:** Status categories within status categories
**Standalone:** Entity hierarchies (org charts, folder structures, etc.)

---

## Usage Protocol

**When Ray says:**
- "Classification pattern for X" → Generate ENTITY_CATEGORY_TYPE + ENTITY_CATEGORY + ENTITY_CLASSIFICATION
- "Status pattern for X" → Generate STATUS_TYPE + ENTITY_STATUS
- "Status with classification" → Both combined
- "Add hierarchy" → Ensure parent_id self-reference exists

**Output format:**
1. ASCII diagram first (for review)
2. DDL after approval
3. Ready for ERStudio

---

## Naming Conventions (UDM)

- Tables: singular (vivencia, not vivencias)
- IDs: named (vivencia_id, not just id)
- Dates: named (date_created, not just date or created)
- Foreign keys: same name as referenced PK
- Status columns: named (curation_status, not just status)

---

## The Transformation Principle

**Code is written for the PATTERN, not the VALUES.**

```sql
-- This query NEVER changes, regardless of how many statuses exist:
SELECT e.*, st.name as current_status
FROM entity e
JOIN entity_status es ON e.entity_id = es.entity_id
JOIN status_type st ON es.status_type_id = st.status_type_id
WHERE es.thru_date IS NULL;
```

New status? INSERT INTO status_type.
Code unchanged.
Structure unchanged.
Deployment = data load.

---

## More Patterns (To Be Added)

- Party Pattern (customer 360, relationships)
- Role Pattern
- Contact Mechanism Pattern
- Product Pattern
- Order Pattern
- Agreement Pattern

---

*"Database, anyone? Hello?"*

*Alba Serrano - Built on Silverston, powered by HDI*
