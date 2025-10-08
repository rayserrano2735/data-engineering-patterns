# Interview Prep Template
**Version: 1.0.5-RC3**

Template for creating targeted interview prep documents based on specific job descriptions.

---

## Document Structure

### 1. Interview Context
- Company name
- Role title
- Interview type (technical screen, coding, system design, behavioral)
- Interviewer name/title (if known)
- Date and duration
- Key signals from JD (e.g., "dbt as plus" = Analytics Engineer despite DE title)

### 2. Python Focus Areas
**Rationale:** Student handles non-Python topics independently. Focus only on Python/PySpark gaps.

**Content principles:**
- Maintain content dependency directive (nothing used before explained)
- Assume PAIP Week 1 Days 1-2 knowledge: lists, dicts, sets, basic comprehensions, iteration
- Explain any concepts beyond Days 1-2
- Practical interview scenarios, not comprehensive coverage

**Typical Python topics:**
- PySpark DataFrame API
- Advanced pandas patterns
- Data pipeline design
- ETL/ELT patterns in Python
- Testing and validation

### 3. Quick Reference
Condensed syntax and patterns for rapid review. Examples:
- PySpark transformations
- Common operations with code samples
- Gotchas and edge cases

### 4. Interview Scenarios
Realistic problems based on JD requirements:
- Problem statement
- Expected approach
- Key concepts tested
- Solution pattern (not full code)

### 5. Supporting Materials
- Flashcards (platform/content/student/data/interview_preps/)
- Interview Mode document (platform/content/student/docs/interview_preps/)

---

## File Naming Convention

**Main prep document:**
`{company}_{role_shorthand}.md`

Examples:
- `danaher_staff_de.md`
- `stripe_analytics_engineer.md`
- `snowflake_data_engineer.md`

**Flashcards:**
`{company}_{topic}_flashcards.txt`

Examples:
- `danaher_pyspark_flashcards.txt`
- `stripe_sql_flashcards.txt`

**Interview Mode:**
`INTERVIEW_MODE_{COMPANY}_{ROLE}.md`

Examples:
- `INTERVIEW_MODE_DANAHER_STAFF_DE.md`
- `INTERVIEW_MODE_STRIPE_AE.md`

---

## Directory Structure

```
platform/content/student/
├── docs/
│   ├── INTERVIEW_PREP_TEMPLATE.md (this file)
│   └── interview_preps/
│       ├── danaher_staff_de.md
│       ├── INTERVIEW_MODE_DANAHER_STAFF_DE.md
│       └── [future preps...]
└── data/
    └── interview_preps/
        ├── danaher_pyspark_flashcards.txt
        └── [future flashcard decks...]
```

---

## Creating a New Interview Prep

1. **Extract JD signals:**
   - True role (DE vs AE despite title)
   - Required Python skills
   - Enterprise systems mentioned
   - Tools and frameworks

2. **Identify Python gaps:**
   - What's beyond Week 1 Days 1-2?
   - What's not in PAIP yet but needed?

3. **Create main document:**
   - Use this template structure
   - Focus only on Python topics
   - Include practical examples

4. **Build flashcards:**
   - Key syntax patterns
   - Common operations
   - Gotchas

5. **Create Interview Mode doc:**
   - Scenario-based questions
   - Aligned with JD requirements
   - CTO vs technical screen style

---

## Content Dependency Compliance

**Assumed knowledge (Days 1-2):**
- Lists, dicts, sets creation and access
- Basic iteration (for loops)
- List comprehensions (basic)
- Built-in functions: len(), range(), enumerate(), zip(), sorted()
- Dict methods: .get(), .keys(), .values(), .items()

**Must explain if used:**
- Lambda expressions (Day 5)
- Advanced comprehensions (Day 3)
- Function definitions (Day 4)
- String methods beyond basics (Day 6)
- Imports and modules
- Classes and objects
- Any PySpark-specific concepts

---

## Template Maintenance

Update this template as:
- New interview prep patterns emerge
- Content dependency rules evolve
- Platform structure changes
- Student feedback suggests improvements
