# Learning Guide - Python Analytics Interview Prep

## Table of Contents

- [Why This Course Exists](#why-this-course-exists-the-analytics-engineering-paradox)
- [What This Course Actually Teaches](#what-this-course-actually-teaches)
- [How Patterns and Concepts Work Together](#how-patterns-and-concepts-work-together)
- [Learning Framework](#learning-framework)
- [Python Prerequisites](#python-prerequisites)
- [Interview Mode](#interview-mode)
- [Pattern Library](#pattern-library)
  - [Categories 1-8: Data Manipulation Patterns](#category-1-selection--filtering)
  - [Category 9: Testing & Validation](#category-9-testing--validation)

---

Comprehensive guide for studying effectively with the interview prep platform.

## Why This Course Exists: The Analytics Engineering Paradox

### The Guiding Principle

**This course exists because the skills companies test in interviews have nothing to do with the skills required for the job.**

You're an Analytics Engineer. You know dbt. You know SQL. You understand semantic modeling, data governance, and the modern data stack. These are the skills you'll use every day in your role. But you're being filtered out of interviews because you can't write pandas groupby operations from memory in 15 minutes.

This isn't about your competency. It's about broken hiring processes testing obsolete skills while banning the tools you'd actually use in production.

**This course is your way through the gatekeeping test.**

### The Modern Data Stack Reality

**Python is obsolete in the Analytics Engineering workflow.**

Here's what the modern data stack actually looks like:

**The Architecture:**
1. **Ingestion:** Fivetran, Airbyte (no code, just configuration)
2. **Storage:** Snowflake, Databricks (SQL interface)
3. **Transformation:** dbt (SQL with Jinja templating)
4. **Semantic Layer:** dbt metrics, Cube (declarative YAML)
5. **BI Tools:** Tableau, Looker, PowerBI (drag-and-drop + SQL)
6. **Orchestration:** Airflow (managed by Data Engineers, not you)

**Notice what's missing?** Python. Nowhere in this stack do Analytics Engineers write Python scripts.

**The Historical Context:**

The data lake era (2015-2018) was a disaster. Companies thought they could skip data warehouses and go straight from source to insight using S3 files and Python scripts. The result was the "data swamp"—unmaintainable pipelines, no governance, broken transformations, and Data Engineers drowning in imperative code.

The industry learned its lesson. SQL reasserted its rightful place as the primary data language because:
- SQL is declarative (describe what you want, not how to get it)
- dbt made transformation code testable, version-controlled, and maintainable
- Cloud warehouses made storage cheap and compute fast
- Semantic layers solved the "metrics everywhere" problem

**Python lost because it was the wrong tool for the job.**

### The Role Confusion Problem

**There are two different roles with different skill requirements:**

**Data Engineer (dying role):**
- Works in the swamp/lake infrastructure
- Writes Python/Spark pipelines
- Manages Kafka, streaming, infrastructure
- Deals with raw data ingestion at scale

**Analytics Engineer (modern role):**
- Works in the data warehouse
- Writes dbt models and tests
- Builds semantic layers and metrics
- Enables self-service analytics
- Never touches infrastructure

**The problem:** Hiring managers and HR teams are stuck in a data swamp mindset. They post "Analytics Engineer" roles with job descriptions mentioning dbt, SQL, and semantic modeling—then interview you with Python pandas questions meant for Data Engineers.

**You're being tested on the wrong role's skills.**

### The AI Reality: The Final Absurdity

**Here's what makes this especially ridiculous:**

**In actual production work, everyone uses AI.**

When you need to manipulate data in your Analytics Engineer role:
1. You describe the problem to Cursor, Claude, or ChatGPT
2. AI generates the dbt SQL (or pandas if somehow needed)
3. You review the code, test it, and ship

**Nobody writes pandas from memory in production.** Nobody. That would be inefficient and error-prone.

**But in interviews:**
- "Write a function to find top N by group without looking anything up"
- "No AI, no documentation, no Google"
- "You have 15 minutes"

**This is the "no calculator" nonsense all over again.**

It's like testing engineers on slide rule proficiency in 2024, or testing writers on spelling without spellcheck, or testing mathematicians on arithmetic speed instead of problem-solving ability.

**The interview tests memorization of syntax you'd never write from scratch in the actual job.**

### The Economic Irrationality

**Here's the business case that makes this even more absurd:**

Analytics Engineers in the modern data stack need Python for approximately **1% of scenarios**—rare edge cases that fall outside standard dbt/SQL workflows.

**Basic economics question:** Should companies maintain full-time Python expertise for 1% utilization?

**No.** You wouldn't:
- Hire a full-time lawyer for 1% legal work → Use a law firm when needed
- Hire a full-time designer for 1% design work → Contract specialists
- Hire a full-time DBA for 1% database tuning → Use managed cloud services

**For that 1% of Python scenarios, companies should:**
- Outsource to contractors/specialists
- Use AI code generation (Cursor, Claude, ChatGPT)
- Consult with Data Engineers (different role entirely)
- Build partnerships with external teams

**Maintaining in-house Python expertise as a required skill for Analytics Engineers is economically irrational.**

Yet companies filter candidates based on Python competency—optimizing hiring for the 1% instead of the 99%. They're rejecting qualified candidates who excel at the actual job (dbt, SQL, semantic modeling) because they can't write pandas from memory.

**What about orchestration tools like Airflow?**

Even orchestration has evolved beyond Python:
- dbt Cloud schedules and orchestrates transformation runs natively
- Fivetran triggers dbt jobs automatically after data sync
- dbt's lineage graph defines dependency execution order
- No Python DAGs needed for standard Analytics Engineering workflows

The 1% of edge cases requiring custom orchestration logic? Outsource it or use AI to generate it when needed.

**That said, many companies still use Airflow and test basic DAG knowledge in Analytics Engineer interviews.** While this reflects outdated architecture understanding, it's market reality. We can't filter out every company that hasn't fully adopted the modern stack—that would eliminate most job opportunities.

**This course includes basic Airflow orchestration patterns** (reading DAGs, writing simple task dependencies, understanding scheduling) because they appear in interviews. We teach the orchestration aspect only—not data transformation in Airflow, which would be a Data Engineer responsibility.

If an interview heavily focuses on complex Airflow development (custom operators, XComs, dynamic DAGs, Spark integration), that signals the company may not understand the Analytics Engineer role. But basic orchestration knowledge is a reasonable gatekeeping test we can prepare for efficiently—just like the pandas patterns.

**This course exists because hiring hasn't caught up to this economic reality.** We can't fix company hiring practices, but we can get you past the gatekeeping so you can do the actual job.

### What This Course Actually Teaches

**Given this reality, what should you learn?**

**Not this:**
- Deep Python expertise
- Production best practices
- How to build data pipelines
- Computer Science algorithms

**But this:**
- Pattern recognition (which approach solves which problem)
- 20 core patterns that appear in interviews
- Quick recall of pattern implementations
- How to execute under time pressure
- Communication skills for explaining your approach

**The valuable skill is pattern recognition.** AI can generate syntax, but AI can't tell you "this is a top-N-by-group problem" or "use merge-with-indicator for data quality validation."

**Interviews test pattern execution** (even though it's artificial). **Your job requires pattern recognition** (which is actually valuable).

**This course bridges that gap.**

### How Patterns and Concepts Work Together

**The Two-Dimensional Teaching Methodology**

This course uses a sophisticated two-dimensional approach to ensure patterns are introduced as early as possible while maintaining conceptual understanding:

**Dimension 1 (Horizontal): Concept Progression**
- Week 1: Python fundamentals (lists, dicts, functions, comprehensions)
- Week 2: DataFrame basics (creation, selection, filtering)
- Week 3: Aggregation (groupby, merge, transform)
- Week 4: Ranking/windows (sort, rank, rolling, shift)
- Week 5: Advanced operations (strings, categorical, multi-index)
- Week 6: Integration (file I/O, Airflow orchestration)
- Week 7: Meta-knowledge (performance, gotchas)

**Dimension 2 (Vertical): Pattern Complexity**
- Level 1: Simple version using basic concepts
- Level 2: Intermediate version with additional concepts
- Level 3: Advanced version with optimization/edge cases

**The Critical Principle: Early Introduction with Progressive Expansion**

We do NOT wait until all prerequisite concepts are mastered before introducing patterns. Instead:

1. **Introduce patterns as early as possible** using whatever concepts are available
2. **Expand pattern complexity** as more concepts are mastered
3. **Revisit patterns** at increasing sophistication levels across multiple weeks

**Example: The "Top N" Pattern Evolution**

This single pattern appears THREE times across the course, each time more sophisticated:

**Week 2 (Basic concepts available: DataFrames, sort, head):**
```python
# Pattern: Get top 5 records
df.sort_values('revenue', ascending=False).head(5)
```
**Concept level:** Basic sorting
**Pattern level:** Simple top N

**Week 3 (New concepts: groupby):**
```python
# Pattern: Get top 5 records BY GROUP
df.sort_values('revenue', ascending=False).groupby('region').head(5)
```
**Concept level:** Sorting + grouping
**Pattern level:** Top N by group

**Week 4 (New concepts: nlargest, rank, optimization awareness):**
```python
# Pattern: Efficient top N by group with ties handling
df.groupby('region').apply(lambda x: x.nlargest(5, 'revenue'))
# Or with ranking
df['rank'] = df.groupby('region')['revenue'].rank(method='dense', ascending=False)
df[df['rank'] <= 5]
```
**Concept level:** Optimization + edge cases
**Pattern level:** Production-ready top N by group

**Why This Works:**

1. **Early pattern exposure** - Students see the "top N" concept in Week 2, building mental framework early
2. **Incremental complexity** - Each week adds one new concept to the pattern, not overwhelming
3. **Reinforcement through repetition** - Same pattern practiced multiple times at different levels
4. **Real mastery** - By Week 4, students understand the pattern at three complexity levels
5. **Interview flexibility** - Can adapt pattern to whatever constraints interviewer imposes

**The Two-Dimensional Matrix**

Every pattern in the course maps to this matrix:

| Pattern | Week 2 (Simple) | Week 3 (Intermediate) | Week 4 (Advanced) |
|---------|-----------------|----------------------|-------------------|
| Top N | sort + head | + groupby | + nlargest/rank |
| Aggregation | mean/sum | + multiple aggs | + named aggs/transform |
| Filtering | boolean index | + query/isin | + complex conditions |
| Missing values | fillna | + strategy by type | + forward/back fill |

**This is different from traditional linear teaching** where you learn sort in Week 2, groupby in Week 3, and "maybe someday" combine them. We combine them immediately, then expand sophistication.

**Our curriculum structure reflects this:**
- **Week 1:** Python fundamentals (foundation - no pandas patterns yet)
- **Week 2:** DataFrame basics + FIRST versions of core patterns
- **Week 3:** Aggregation concepts + EXPANDED versions of Week 2 patterns + new patterns
- **Week 4:** Ranking/windows + ADVANCED versions of previous patterns + new patterns
- **Week 5:** Advanced operations + specialized patterns
- **Week 6:** Integration + orchestration patterns
- **Week 7:** Meta-patterns (how to use all previous patterns correctly)

**Each week:**
- Introduces 1-3 new concepts
- Introduces simple versions of 2-3 new patterns (using current + prior concepts)
- Expands 2-3 previous patterns with newly learned concepts
- Reinforces all prior patterns through varied exercises

**This scaffolding ensures:**
- You're never copying code you don't understand (concepts always precede pattern complexity)
- Patterns are introduced as early as possible (don't wait for "complete" understanding)
- Repetition builds mastery (same pattern, increasing sophistication)
- Interview readiness (can execute patterns at multiple complexity levels)

**Why This Matters for Gatekeeping Interviews:**

Interviewers don't all ask for the same complexity level. Some want:
- "Just get top 5 records" (Week 2 version)
- "Get top 5 per region" (Week 3 version)  
- "Handle ties and explain efficiency" (Week 4 version)

By learning each pattern at multiple levels, you can match whatever the interviewer asks for without over-engineering or under-delivering.


### This Course's Mission

**Help Analytics Engineers proficient in the modern data stack pass Python gatekeeping tests, land the job, and return to the work that actually matters.**

**Our content strategy:**
- Teach only patterns that appear in Analytics Engineer interviews
- Focus on quick recall, not deep mastery
- Provide ready-to-adapt implementations
- Train pattern recognition speed
- Build communication skills
- Acknowledge this is test prep, not career skill development

**Our design philosophy:**
- Time-boxed exercises (interviews are time-boxed)
- Pattern-based learning (memorize 20 patterns, not 200 methods)
- Spaced repetition (flashcards for recall under pressure)
- Mock interviews (practice the absurd constraints)

**Think of this as exam prep for a broken certification system.** You need the certification to get hired, even though it doesn't measure actual competence. We'll get you certified efficiently, then you can go back to building semantic layers and dbt models.

### What Success Looks Like

**Short term:**
- Pass Python interviews for Analytics Engineer roles
- Demonstrate "I can manipulate data" competency
- Get past the gatekeeping filters
- Land the role you're qualified for

**Long term:**
- Never write Python again (you'll use dbt and SQL)
- Use AI when Python is actually needed
- Focus on the skills that matter (data modeling, metrics, governance)
- Help fix hiring from the inside (once you're hired)

### Evaluating Companies During Interviews

**While preparing for interviews, also evaluate if the company understands the modern data stack.**

You're not just trying to pass their test—you're also testing whether you want to work there. A company stuck in the data swamp mindset may have you maintaining legacy Python pipelines instead of building modern semantic layers.

**Green flags (company gets it):**
- Questions focus on SQL, dbt, semantic modeling, and metrics
- Python questions are basic gatekeeping (top N, groupby, merge—reasonable)
- They mention dbt, semantic layers, metrics catalogs, or data contracts
- Orchestration questions are about understanding DAGs, not building custom operators
- They acknowledge AI use in production workflows
- They distinguish between Analytics Engineer and Data Engineer roles clearly

**Yellow flags (proceed with caution):**
- Heavy focus on Python pandas optimization and performance tuning
- Questions about building ETL pipelines from scratch
- No mention of dbt or modern transformation tools in tech stack discussion
- Airflow questions go deep into custom operators, XComs, or complex DAG patterns
- They seem surprised or concerned you use AI for code generation
- Vague boundaries between Analytics Engineer and Data Engineer responsibilities

**Red flags (seriously consider running):**
- Role says "Analytics Engineer" but interviews like "Data Engineer"
- Questions about Spark, Kafka, streaming infrastructure (wrong role entirely)
- They want you to build or maintain data lakes
- No semantic layer, metrics strategy, or data governance mentioned
- Python is described as "primary language" for the role (should be SQL)
- They're hiring "Analytics Engineer" but the work is clearly data engineering
- Infrastructure concerns dominate over analytics/metrics concerns

**Remember:** You're interviewing them too. If they don't understand the modern stack, you may end up in the data swamp, maintaining unmaintainable Python scripts, instead of building clean dbt models and semantic layers.

The goal is to pass their Python test AND verify they'll let you do actual Analytics Engineering work once hired.

---

## Interview Mode: AI-Powered Practice for Mastery

Interview Mode is the platform's AI-driven practice system that generates unlimited, context-aware scenarios for active learning. Instead of static problem sets, it simulates realistic situations where you apply knowledge under pressure.

### What is Interview Mode?

Interview Mode uses AI to act as interviewer, code reviewer, colleague, or challenger—generating unique practice scenarios tailored to your current learning objectives. Every practice session is different, preventing pattern memorization and forcing genuine understanding.

**Traditional Practice vs Interview Mode:**

| Traditional | Interview Mode |
|------------|----------------|
| Fixed 20-50 problems | Infinite unique scenarios |
| Abstract exercises | Realistic contexts |
| Right/wrong feedback | Teaching-focused explanations |
| Static difficulty | Adapts to your responses |
| Predictable patterns | Unpredictable challenges |

### How It Works

```
Interview Mode Session Flow:

1. CONTEXT SETTING
   AI establishes realistic scenario
   
2. CHALLENGE PRESENTATION  
   Problem posed within context
   
3. YOUR RESPONSE
   You attempt to solve/answer
   
4. AI EVALUATION
   Assesses response quality
   
5. FOLLOW-UP / PROBING
   AI asks clarifying questions, challenges reasoning
   
6. FEEDBACK & LEARNING
   Contextual explanation of concepts
   
7. NEXT SCENARIO
   Process repeats with new variation
```

### The AI's Role

The AI adapts its persona based on learning objectives:

- **The Interviewer** - Asks technical questions, probes understanding
- **The Code Reviewer** - Evaluates your code, suggests improvements
- **The Colleague** - Presents problems requiring collaboration  
- **The Challenger** - Questions decisions, forces justification
- **The Mentor** - Guides learning, provides hints when stuck

### Why It's Effective

**Active Recall Under Pressure:**
Interview Mode creates psychological pressure similar to real interviews. Memory consolidation improves under moderate stress—you're practicing how knowledge will actually be tested.

**Contextual Application:**
Knowledge isn't tested in isolation. You apply concepts within realistic scenarios requiring synthesis and judgment.

**Example:**
- ❌ Bad: "What is a dictionary in Python?"
- ✅ Good: "You're building user authentication. A colleague suggests using a list to store usernames and passwords. What data structure would you recommend and why?"

**Infinite Variability:**
AI generates unique scenarios every session. You can't memorize solutions—you must genuinely understand concepts.

### Extended Thinking Mode

Interview Mode uses Claude's extended thinking capability to:
- Plan more effective scenarios before presenting them
- Evaluate responses more thoroughly  
- Decide optimal hint timing and difficulty adjustments
- Maintain consistent difficulty progression

This produces higher-quality practice sessions with better-calibrated challenges.

### Voice Mode

**Bidirectional voice enhances realism:**
- **You speak responses** - Practice articulating solutions verbally
- **Claude speaks questions** - Hear interview questions naturally
- **Natural conversation flow** - More realistic than text chat
- **Builds verbal skills** - Forces clear explanation without editing

Voice mode simulates actual interview conditions where you must think aloud and communicate clearly under pressure.

**When to use voice:**
- Final prep before real interviews
- Building verbal communication confidence
- Practicing "think aloud" habits
- Simulating interview pressure

**When to use text:**
- Learning new concepts (easier to reference)
- Working through complex code
- When environment doesn't allow voice


### Using Interview Mode

**When to Practice:**
After completing each day's textbook content, practice with Interview Mode for 30-45 minutes. Continue until confident applying that day's concepts.

**Week-Specific Instructions:**
Each week has dedicated Interview Mode guidelines telling the AI what to focus on:
- **Week 1:** INTERVIEW_MODE_WEEK1.md (Python fundamentals practice)
- **Week 2+:** Additional IM docs (pattern application practice)

**How to Start:**
1. Complete a textbook section
2. Open Interview Mode for that week
3. Tell the AI which topic you just studied
4. Practice until concepts feel natural
5. Request hints if stuck, new scenarios when ready

**Practice Until Proficient:**
There's no fixed number of problems. Practice as long as needed. Some concepts click in 3 scenarios, others need 10. The AI adapts—if you're struggling, it provides scaffolding; if you're excelling, it increases difficulty.

### Example Session

**Scenario Type:** Real-World Application (Day 2: Dictionaries)

```
AI: You're working at an e-commerce company. Your manager asks 
    you to write a function that calculates total revenue from 
    a list of orders.

    Each order is a dictionary: {'quantity': 2, 'price': 29.99}
    
    How would you approach this?

You: I would loop through the list and multiply quantity by 
     price for each order, then sum them up.

AI: Good thinking! Can you write the code for that?

You: [writes code]

AI: [evaluates code] Your logic is correct, but what happens 
    if the list is empty? Also, what if an order has a 
    negative quantity? Let's handle those edge cases...
```

The AI continues probing, teaching error handling, asking about alternative approaches, and reinforcing concepts through realistic application.

### Integration with Learning Path

Interview Mode sits between guided practice and assessment:

```
Learning Progression:

1. INTRODUCTION - Watch/read content
2. UNDERSTANDING - Work through examples  
3. APPLICATION - Standard exercises
4. MASTERY - Interview Mode ← You are here
5. ASSESSMENT - Quizzes, projects
```

**Week 1 Schedule with Interview Mode:**
- Day 1-2: Study data structures (2 hours) + IM practice (30 min)
- Day 3: Study comprehensions (1.5 hours) + IM practice (30 min)
- Day 4: Study functions (1.5 hours) + IM practice (45 min)
- Day 5: Study lambda/sorting (1.5 hours) + IM practice (45 min)
- Day 6: Study strings (1 hour) + IM practice (30 min)
- Day 7: Review + IM mixed practice (1 hour)

### Benefits for Analytics Engineers

**Mirrors Real Interviews:**
You'll face technical interviews with time pressure, follow-up questions, and challenges to your reasoning. Interview Mode simulates this environment safely.

**Builds Confidence:**
Unlimited practice means you can't "run out" of problems. Practice until concepts feel natural, not just memorized.

**No Pattern Memorization:**
Can't game the system by memorizing solutions. Must genuinely understand to succeed.

**Immediate Feedback:**
Unlike homework graded later, you get instant teaching-focused feedback tied to your specific approach.

**Adapts to You:**
AI adjusts difficulty based on your responses. Struggling? Gets more scaffolding. Excelling? Gets harder challenges.

### Interview Mode vs Static Exercises

The platform includes both:

**Static Exercises (week1_exercises.py):**
- Fixed problems with known solutions
- Good for initial concept validation
- 20 problems covering Week 1 topics
- Use first, before Interview Mode

**Interview Mode:**
- Infinite unique scenarios
- Realistic contexts and follow-ups  
- Adaptive difficulty
- Use after exercises for mastery practice

Both are valuable. Exercises verify basic understanding; Interview Mode builds fluency and application skill.

### For Course Designers: Creating Week-Specific IM Documents

Each week requires an INTERVIEW_MODE_WEEK[X].md document that instructs the AI on how to conduct practice sessions. These documents are critical for maintaining consistency and quality.

**Required Elements:**

1. **Learning Objectives** - What concepts the week covers
2. **Difficulty Level** - Beginner/intermediate/advanced for that week
3. **Scenario Types** - Categories of practice situations (code review, debugging, design challenge, etc.)
4. **Key Concepts to Assess** - Specific topics the AI should probe
5. **Common Mistakes** - Typical errors learners make at this stage
6. **Evaluation Criteria** - How to determine response quality

**Template Structure:**

```markdown
# Interview Mode: Week [X] - [Topic]

## Context
Students have completed Week [X] covering [topics]. They should be able to [learning objectives].

## AI Role
Act as [interviewer/code reviewer/colleague] evaluating practical understanding of [topics].

## Scenario Types

### Type 1: [Scenario Category]
**Focus:** [What to assess]
**Approach:** [How to present challenge]
**Example:** [Brief scenario example]

### Type 2: [Scenario Category]
[Repeat structure]

## Key Concepts to Assess
- Concept 1 with specific probing questions
- Concept 2 with edge cases to introduce
- Concept 3 with common misconceptions to test

## Common Mistakes to Probe
- Mistake pattern 1 and how to address
- Mistake pattern 2 and teaching approach

## Difficulty Progression
- Start with: [Basic level challenge]
- If successful: [Intermediate level challenge]  
- If struggling: [Provide hint type]
- Advanced: [Complex scenarios for strong students]

## Evaluation Guidelines
**Strong Response:**
- Demonstrates [specific criteria]
- Can explain [reasoning]

**Weak Response:**
- Missing [key elements]
- Needs guidance on [concepts]

## Teaching Approach
- Use Socratic method for [situations]
- Provide direct instruction for [situations]
- Offer hints when [conditions]
```

**Example from Week 1:**

```markdown
# Interview Mode: Week 1 - Python Fundamentals

## Context
Students completed Week 1: lists, dicts, sets, comprehensions, functions, lambda, strings. They should be able to manipulate data structures, write functions with parameters, use comprehensions for filtering/transformation.

## AI Role
Technical interviewer evaluating junior developer candidate on Python basics.

## Scenario Types

### Code Review
**Focus:** Identify issues in provided code using Week 1 concepts
**Example:** "Review this function that processes order data. What could be improved?"

### Real-World Application  
**Focus:** Design solution for business problem
**Example:** "Build a function that calculates revenue from orders list using dicts"

### Debugging
**Focus:** Find and fix bugs in code
**Example:** "This dictionary merge isn't working correctly. Debug it."

## Key Concepts to Assess
- Dictionary operations (creation, access, methods)
- List comprehensions for filtering
- Function parameters and return values
- When to use which data structure

## Common Mistakes
- Using mutable default arguments
- Confusing dict access methods (.get() vs [])
- Inefficient nested loops instead of comprehensions
- Not handling edge cases (empty lists, None values)

## Difficulty Progression
Start: "Write a function that counts word frequency in a list"
Success → "Now handle punctuation and case-insensitivity"
Struggling → "Let's start with just counting. What data structure stores counts?"

## Evaluation Guidelines
Strong: Clean code, handles edge cases, explains choices
Weak: Works but inefficient, missing error handling, can't explain why

## Teaching Approach
- Guide with questions, don't give answers immediately
- If stuck for 2 minutes, provide hint
- Always explain WHY the solution works, not just WHAT the code does
```

This framework ensures AI-generated scenarios remain consistent with learning objectives and provide appropriate challenge level. See interview_mode_concept.md in project root for complete implementation guide.

---
## Python Prerequisites

**Extracted from 24 patterns - everything you need, nothing you don't.**

This section lists all Python/pandas concepts required to master the pattern library. Learn these fundamentals, then apply them through patterns.

### Core Python (Week 1)

**Data Structures:**
- Lists: creation, indexing, slicing, append, extend, comprehensions
- Dicts: creation, access (.get(), []), keys(), values(), items(), dict comprehension
- Sets: creation, add(), union, intersection, set comprehension
- Tuples: immutable sequences, unpacking

**Control Flow:**
- if/elif/else conditionals
- for loops (including enumerate, zip)
- while loops
- List/dict/set comprehensions with conditions

**Functions:**
- def, parameters, return values
- Default parameters
- *args, **kwargs
- Lambda expressions

**String Operations:**
- split(), join(), strip(), lower(), upper()
- f-strings for formatting
- String methods: replace(), startswith(), endswith()
- Basic regex (re.search, re.match, re.findall)

**Built-in Functions:**
- len(), sum(), min(), max(), sorted()
- filter(), map(), zip()
- range(), enumerate()
- any(), all()

**Operators:**
- Comparison: ==, !=, <, >, <=, >=
- Logical: and, or, not
- Membership: in, not in
- Arithmetic: +, -, *, /, //, %, **

### Pandas Fundamentals (Week 2+)

**DataFrame Basics:**
- pd.DataFrame() creation
- df.head(), df.tail(), df.info(), df.describe()
- df.shape, df.columns, df.dtypes
- df['col'] column selection
- df[['col1', 'col2']] multiple columns
- df.loc[], df.iloc[] row selection

**Boolean Indexing:**
- df[df['col'] > value]
- df[df['col'].isin(values)]
- df[df['col'].between(a, b)]
- Combining conditions with & | ~

**Sorting & Selection:**
- df.sort_values()
- df.nlargest(), df.nsmallest()
- df.head(n)

**Aggregation:**
- df.groupby().agg()
- df.groupby().sum(), mean(), count(), etc.
- Multiple aggregation functions
- Named aggregations

**Column Operations:**
- df['new_col'] = expression
- df.assign()
- df.apply(), df.applymap()
- df['col'].map()

**Reshaping:**
- df.pivot_table()
- df.melt()
- df.stack(), df.unstack()

**Merging & Joining:**
- pd.merge()
- df.merge()
- pd.concat()
- join types: inner, left, right, outer

**Time Series:**
- pd.to_datetime()
- df['date'].dt accessor
- df.resample()
- df.rolling(), df.expanding()

**String Operations:**
- df['col'].str accessor
- str.contains(), str.replace(), str.split()
- str.extract() with regex

**Missing Data:**
- df.isna(), df.notna()
- df.fillna(), df.dropna()
- df.interpolate()

**Data Quality:**
- df.duplicated()
- df.drop_duplicates()
- df.unique(), df.nunique()

### NumPy (As Needed)

**Conditional Logic:**
- np.where(condition, if_true, if_false)
- np.select(conditions, choices)

**Basic Operations:**
- np.sum(), np.mean(), np.std()
- np.arange(), np.linspace()

### Testing Concepts

**Assertions:**
- assert statement
- assertEqual, assertTrue, assertRaises

**Test Structure:**
- Test functions
- Test data generation
- Expected vs actual comparison

**DataFrame Testing:**
- pd.testing.assert_frame_equal()
- Shape validation
- Column validation
- Value range checks

---

**Learning Strategy:**
1. Week 1: Master core Python fundamentals
2. Week 2+: Learn pandas through patterns
3. Reference this list when stuck on syntax
4. Use external Python resources for deeper explanations

**This is your scope.** Everything needed for analytics engineer interviews, nothing extra.

---

## The Complete Pattern Library: 24 Problem Types

**This is the heart of the course.** These 24 patterns represent every problem type you'll face in Analytics Engineer Python interviews. Master these, and you can solve any interview question by recognizing which pattern applies.

### How to Use This Reference

**During study:**
- Each pattern has a name (e.g., "Top N Selection")
- Learn to recognize the problem type from interview questions
- Understand when each pattern applies
- Study implementations in `patterns_and_gotchas.py`

**During interviews:**
- Interviewer asks: "Find the top 3 products by revenue in each region"
- You recognize: "This is a Top N Selection problem"
- You recall: "sort + groupby + head, or groupby + nlargest"
- You implement the pattern adapted to the specific question

**Pattern recognition is the valuable skill.** Syntax can be looked up (or AI-generated), but recognizing "this is a top-N problem" requires understanding.

---

### Pattern Categories

**Selection & Filtering (3 patterns)**
Problems about choosing subsets of data

**Aggregation & Summarization (3 patterns)**
Problems about calculating statistics and summaries

**Time-Based Analysis (4 patterns)**
Problems involving dates and sequential data

**Ranking & Ordering (2 patterns)**
Problems about sorting and assigning ranks

**Data Quality (3 patterns)**
Problems about cleaning and validating data

**Data Combination (2 patterns)**
Problems about joining multiple datasets

**Advanced Transformations (3 patterns)**
Problems requiring complex calculations

**Performance & Integration (4 patterns)**
Optimization and operational patterns

---

## CATEGORY 1: Selection & Filtering

### Pattern 1: Basic Filtering
**Problem:** "Show me records that meet certain criteria"

**Interview examples:**
- "Find all transactions over $1000"
- "Get customers in the Northeast region who are active"
- "Select products with price between $50 and $100"

**Week progression:**
- **Week 2:** Boolean indexing `df[df['value'] > 100]`
- **Week 3:** Multiple conditions `df[(df['value'] > 100) & (df['category'] == 'A')]`
- **Week 4:** Query syntax `df.query('value > 100 and category == "A"')`

**Interview frequency:** Very High (80%+)

---

### Pattern 2: Top N Selection
**Problem:** "Find the best or worst N items"

**Interview examples:**
- "What are the top 5 products by revenue?"
- "Show me the 3 highest-paid employees in each department"
- "Find the 10 worst-performing stores"

**Week progression:**
- **Week 2:** Simple top N `df.sort_values('revenue', ascending=False).head(5)`
- **Week 3:** Top N by group `df.sort_values('revenue', ascending=False).groupby('region').head(3)`
- **Week 4:** With ties and optimization `df.groupby('region').apply(lambda x: x.nlargest(3, 'revenue'))`

**Why it matters:** This is THE most common interview pattern. Master it at all three levels.

**Interview frequency:** Very High (90%+)

---

### Pattern 3: Outlier Detection
**Problem:** "Find unusual or anomalous values"

**Interview examples:**
- "Identify transactions that are statistical outliers"
- "Flag orders with unusually high amounts"
- "Find customers in the top 5% by spending"

**Week progression:**
- **Week 4:** Statistical outliers `df[df['amount'] > df['amount'].mean() + 3*df['amount'].std()]`
- **Week 4:** Quantile-based `df[df['amount'] > df['amount'].quantile(0.95)]`
- **Week 5:** Business rules combined with statistics

**Interview frequency:** Medium (20-50%)

---

## CATEGORY 2: Aggregation & Summarization

### Pattern 4: Simple Aggregation
**Problem:** "Calculate overall statistics"

**Interview examples:**
- "What's the total revenue?"
- "Calculate average order value"
- "How many unique customers?"

**Week progression:**
- **Week 2:** Basic aggregations `df['revenue'].sum()`, `df['price'].mean()`
- **Week 3:** Multiple metrics at once
- **Week 4:** With filtering and conditions

**Interview frequency:** Very High (80%+)

---

### Pattern 5: GroupBy Aggregation
**Problem:** "Calculate statistics by category"

**Interview examples:**
- "Show revenue by region"
- "Calculate average salary by department and level"
- "Total sales by product category and month"

**Week progression:**
- **Week 2:** Single metric `df.groupby('category')['value'].sum()`
- **Week 3:** Multiple metrics `df.groupby('category').agg({'value': ['sum', 'mean', 'count']})`
- **Week 4:** Named aggregations `df.groupby('category').agg(total=('value', 'sum'), avg=('value', 'mean'))`

**Why it matters:** GroupBy is the foundation of most analytics. This pattern appears in 80%+ of interviews.

**Interview frequency:** Very High (85%+)

---

### Pattern 6: Percentage of Total
**Problem:** "Calculate each item as percentage of total"

**Interview examples:**
- "What percentage of revenue comes from each region?"
- "Show market share by product"
- "Calculate each category's contribution to total sales"

**Week progression:**
- **Week 3:** Simple percentage `df['pct'] = df['value'] / df['value'].sum() * 100`
- **Week 4:** By group `df['pct'] = df.groupby('category')['value'].transform(lambda x: x / x.sum() * 100)`
- **Week 4:** Cumulative percentage

**Interview frequency:** Medium (30-50%)

---

## CATEGORY 3: Time-Based Analysis

### Pattern 7: Period Comparison
**Problem:** "Compare values across time periods"

**Interview examples:**
- "Calculate month-over-month revenue growth"
- "Show year-over-year change for each product"
- "Compare this quarter to same quarter last year"

**Week progression:**
- **Week 4:** Basic comparison using shift
- **Week 5:** Percentage change `df['pct_change'] = df.groupby('product')['sales'].pct_change()`
- **Week 5:** Custom period logic (YoY, QoQ)

**Why it matters:** Time comparisons are fundamental to analytics. Every dashboard has MoM or YoY metrics.

**Interview frequency:** High (60%+)

---

### Pattern 8: Moving Calculations
**Problem:** "Calculate rolling averages or windows"

**Interview examples:**
- "Show 7-day moving average of sales"
- "Calculate 30-day rolling sum"
- "Find the maximum value in the last 90 days"

**Week progression:**
- **Week 4:** Basic rolling `df['rolling_avg'] = df['value'].rolling(window=7).mean()`
- **Week 4:** With min_periods `df['rolling_avg'] = df['value'].rolling(window=7, min_periods=1).mean()`
- **Week 5:** By group `df['rolling_avg'] = df.groupby('category')['value'].rolling(window=7).mean()`

**Interview frequency:** Medium (40-60%)

---

### Pattern 9: Cumulative Values
**Problem:** "Calculate running totals"

**Interview examples:**
- "Show cumulative revenue by month"
- "Calculate running count of customers"
- "Display year-to-date sales"

**Week progression:**
- **Week 4:** Basic cumsum `df['cumulative'] = df['value'].cumsum()`
- **Week 4:** By group `df['cumulative'] = df.groupby('category')['value'].cumsum()`
- **Week 5:** Multiple cumulative operations (cummax, cummin)

**Interview frequency:** Medium (30-50%)

---

### Pattern 10: Date Operations
**Problem:** "Parse and extract information from dates"

**Interview examples:**
- "Extract year and month from transaction date"
- "Flag weekend transactions"
- "Calculate days since last purchase"
- "Group by fiscal quarter"

**Week progression:**
- **Week 4:** Parse dates `df['date'] = pd.to_datetime(df['date_string'])`
- **Week 4:** Extract components `df['month'] = df['date'].dt.month`
- **Week 5:** Date arithmetic and business logic

**Why it matters:** Almost every analytics dataset has dates. This pattern appears in 70%+ of interviews.

**Interview frequency:** Very High (75%+)

---

## CATEGORY 4: Ranking & Ordering

### Pattern 11: Sorting
**Problem:** "Order records by one or more criteria"

**Interview examples:**
- "Sort customers by revenue descending"
- "Order by region, then by sales within region"
- "Sort by date, handling nulls appropriately"

**Week progression:**
- **Week 2:** Single column `df.sort_values('revenue', ascending=False)`
- **Week 3:** Multiple columns `df.sort_values(['region', 'sales'], ascending=[True, False])`
- **Week 4:** Custom sort logic

**Interview frequency:** High (60%+)

---

### Pattern 12: Ranking
**Problem:** "Assign ranks to items"

**Interview examples:**
- "Rank employees by salary within each department"
- "Assign percentile ranks to test scores"
- "Create dense ranks (1, 2, 2, 3) for tied values"

**Week progression:**
- **Week 4:** Simple ranking `df['rank'] = df['value'].rank(ascending=False)`
- **Week 4:** By group `df['rank'] = df.groupby('category')['value'].rank(ascending=False)`
- **Week 5:** Different rank methods (dense, min, max), percentiles

**Interview frequency:** Medium-High (50-70%)

---

## CATEGORY 5: Data Quality

### Pattern 13: Missing Value Handling
**Problem:** "Handle nulls and missing data"

**Interview examples:**
- "Clean dataset by filling missing values appropriately"
- "Remove records with too many nulls"
- "Fill missing prices with category average"

**Week progression:**
- **Week 2:** Basic fill `df['column'].fillna(0)` or drop `df.dropna()`
- **Week 3:** Strategy by column type (mean for numeric, "Unknown" for categorical)
- **Week 4:** Forward/backward fill for time series

**Why it matters:** Every real dataset has missing values. Interviewers test how you handle data quality.

**Interview frequency:** Very High (80%+)

---

### Pattern 14: Deduplication
**Problem:** "Remove duplicate records"

**Interview examples:**
- "Remove duplicate customer records"
- "Keep only the most recent transaction per customer"
- "Find and investigate duplicate orders"

**Week progression:**
- **Week 2:** Simple dedupe `df.drop_duplicates()`
- **Week 3:** By subset `df.drop_duplicates(subset=['customer_id'], keep='first')`
- **Week 4:** Strategic deduplication (sort first, then keep best)

**Interview frequency:** High (60%+)

---

### Pattern 15: Data Validation
**Problem:** "Check data quality and flag issues"

**Interview examples:**
- "Validate that all prices are positive"
- "Check for expected values in status column"
- "Flag records with suspicious patterns"

**Week progression:**
- **Week 4:** Range checks and value validation
- **Week 5:** Complex validation rules
- **Week 5:** Quality scoring

**Interview frequency:** Medium-Low (20-40%)

---

## CATEGORY 6: Data Combination

### Pattern 16: Merging/Joining
**Problem:** "Combine data from multiple sources"

**Interview examples:**
- "Join customer data with order data"
- "Merge product information with sales records"
- "Find customers who haven't placed orders (anti-join)"
- "Track which records matched during merge"

**Week progression:**
- **Week 3:** Basic merge `df1.merge(df2, on='key', how='left')`
- **Week 3:** Different join types (inner, left, right, outer)
- **Week 4:** With indicator `df1.merge(df2, on='key', how='outer', indicator=True)`

**Why it matters:** Real analytics requires combining multiple data sources. This appears in 80%+ of interviews.

**Interview frequency:** Very High (85%+)

---

### Pattern 17: Reshaping (Pivot)
**Problem:** "Transform data structure between long and wide formats"

**Interview examples:**
- "Create a pivot table showing sales by region and product"
- "Convert wide data to long format for analysis"
- "Reshape for reporting"

**Week progression:**
- **Week 5:** Basic pivot `df.pivot_table(values='sales', index='region', columns='product')`
- **Week 5:** Multiple aggregations in pivot
- **Week 5:** Unpivot with melt

**Interview frequency:** Medium (40-60%)

---

## CATEGORY 7: Advanced Transformations

### Pattern 18: Lag/Lead Operations
**Problem:** "Access previous or next row values"

**Interview examples:**
- "Calculate change from previous month"
- "Compare each transaction to customer's prior transaction"
- "Find first-time vs repeat purchases"

**Week progression:**
- **Week 4:** Basic shift `df['prev_value'] = df['value'].shift(1)`
- **Week 5:** By group `df['prev_value'] = df.groupby('category')['value'].shift(1)`
- **Week 5:** Percentage change `df['pct_change'] = df.groupby('customer')['amount'].pct_change()`

**Why it matters:** Sequential analysis is common in time series and user behavior analytics.

**Interview frequency:** Medium-High (50-70%)

---

### Pattern 19: Window Functions
**Problem:** "Calculate values using a window of rows"

**Interview examples:**
- "Find first purchase date for each customer"
- "Get the last known status for each account"
- "Retrieve nth transaction"

**Week progression:**
- **Week 5:** First/last in group using groupby + transform
- **Week 5:** Nth value patterns
- **Week 5:** Complex window logic

**Interview frequency:** Medium (30-50%)

---

### Pattern 20: Text Operations
**Problem:** "Clean, parse, and manipulate string data"

**Interview examples:**
- "Clean email addresses (lowercase, trim whitespace)"
- "Extract domain from email"
- "Standardize phone numbers"
- "Parse log entries"

**Week progression:**
- **Week 5:** Basic string methods `df['email'] = df['email'].str.lower().str.strip()`
- **Week 5:** String contains for filtering `df[df['description'].str.contains('keyword')]`
- **Week 5:** Extract patterns `df['domain'] = df['email'].str.split('@').str[1]`

**Why it matters:** Real data is messy. String cleaning appears in most analytics workflows.

**Interview frequency:** High (60%+)

---

## CATEGORY 8: Performance & Integration

### Pattern 21: Vectorization
**Problem:** "Optimize slow code using vectorized operations"

**Interview examples:**
- "This code is too slow, optimize it"
- "Explain why iterrows is slow and how to fix it"
- "Rewrite this loop as vectorized operation"

**Week progression:**
- **Week 7:** Replace loops with numpy.where
- **Week 7:** Use map instead of apply
- **Week 7:** Understand when to vectorize

**Why it matters:** Demonstrates understanding of pandas performance. Common follow-up question after solving a problem.

**Interview frequency:** Medium (40-60%)

---

### Pattern 22: File I/O
**Problem:** "Read and write data files"

**Interview examples:**
- "Load this CSV handling encoding issues"
- "Read large file in chunks"
- "Export results to Excel"

**Week progression:**
- **Week 6:** Basic CSV `pd.read_csv('file.csv')`
- **Week 6:** Options (encoding, parse_dates, dtype)
- **Week 6:** Chunked reading for large files

**Interview frequency:** High (60%+)

---

### Pattern 23: Basic Orchestration (Airflow)
**Problem:** "Define task dependencies and scheduling"

**Interview examples:**
- "Create a simple DAG with 3 tasks"
- "Define task dependencies"
- "Explain DAG scheduling"

**Week progression:**
- **Week 6:** Basic DAG structure
- **Week 6:** Task dependencies (A >> B >> C)
- **Week 6:** Simple scheduling parameters

**Why it matters:** Many companies still use Airflow. Basic knowledge expected even for Analytics Engineers.

**Interview frequency:** Medium (varies by company, 30-50%)

**Note:** Complex Airflow (custom operators, XComs, dynamic DAGs) is NOT tested for Analytics Engineers. That's Data Engineer territory.

---

### Pattern 24: Common Gotchas
**Problem:** "Avoid common pandas mistakes"

**Interview examples:**
- "Fix this SettingWithCopyWarning"
- "Why is this chained indexing unreliable?"
- "Explain copy vs view behavior"

**Week progression:**
- **Week 7:** SettingWithCopyWarning and how to fix
- **Week 7:** Chained indexing and why it fails
- **Week 7:** When to use .copy()

**Why it matters:** Shows deeper pandas understanding. Demonstrates you've written production code.

**Interview frequency:** Low-Medium (20-40%)

---

## Using This Pattern Library

### During Study

**Week by week approach:**
- Week 1: Focus on Python fundamentals (no patterns yet)
- Week 2-7: Each week introduces 2-3 patterns at simple level, expands 2-3 previous patterns

**For each pattern:**
1. Read the problem description here
2. Study implementation in `patterns_and_gotchas.py`
3. Practice with exercises
4. Memorize pattern name and when to use it
5. Drill with flashcards until instant recall

### During Interviews

**Pattern recognition process:**
1. Interviewer describes problem
2. Identify: "This is a [pattern name] problem"
3. Recall: General approach (sort + groupby, merge with indicator, etc.)
4. Implement: Adapt pattern to specific requirements
5. Explain: Why this pattern solves the problem

**Example:**
- Question: "Find the 3 best-selling products in each region for Q4"
- Recognition: "Top N Selection pattern, with filtering by date"
- Approach: Filter for Q4, then sort + groupby + head
- Implementation: `df_q4.sort_values('sales', ascending=False).groupby('region').head(3)`
- Explanation: "This is a top-N-by-group problem. I filter first, then sort by sales, then use groupby with head to get top 3 per region."

### Mastery Checklist

Before interviews, you should be able to:
- [ ] Name all 24 patterns from memory
- [ ] Recognize pattern type from problem description
- [ ] Recall general solution approach for each pattern
- [ ] Explain when each pattern applies
- [ ] Implement simple version without looking up syntax
- [ ] Explain trade-offs between different implementation methods

**The 80/20 rule:** Master the 6 very high frequency patterns first (Filtering, Top N, GroupBy Aggregation, Merging, Missing Values, Date Operations). These appear in 80%+ of interviews. Then expand to the rest.

---

### After You're Hired

Once you pass the gatekeeping and land the role:

**First 30 days:**
- Focus on learning the company's dbt models and semantic layer (or help build one)
- Understand their data governance, testing, and documentation practices
- Build relationships with stakeholders and data consumers
- You likely won't write Python (and that's perfectly fine)
- If Python comes up, you'll use AI to generate it and your pattern knowledge to review it

**First 90 days:**
- Contribute to dbt model development and refactoring
- Improve data quality through tests and contracts
- Help build out the semantic layer and metrics definitions
- Document transformation logic and business rules
- Identify opportunities to replace legacy Python with SQL/dbt

**Long term:**
- Advocate for modern data stack practices within the organization
- Share knowledge about dbt, semantic layers, and declarative approaches
- When hiring decisions come your way, push for relevant skill assessment
- Help fix the broken interview process from the inside
- Mentor other Analytics Engineers in the modern stack

**The ultimate goal:** Get more Analytics Engineers hired based on SQL/dbt/semantic layer competency, not arbitrary Python gatekeeping. Once you're inside and respected, you'll be in a position to influence how your company assesses candidates.

Every Analytics Engineer who gets hired and demonstrates the modern stack's effectiveness helps shift the industry away from obsolete Python-focused interviews.

### The Uncomfortable Truth

**Most Python courses pretend interviews test valuable skills.**

We're honest: **Interviews test arbitrary gatekeeping skills. Here's how to pass anyway.**

This isn't cynicism. It's accurate market analysis.

You don't need to love Python. You don't need to plan a Python career. You just need to demonstrate competency for 45 minutes so you can get hired and do the actual job.

**Master these 20 patterns. Pass the test. Get back to work that matters.**

---

## Learning Philosophy

This platform uses **active learning** with immediate application:
1. **Learn** - Read concept (20%)
2. **Practice** - Code solution (50%)
3. **Retain** - Flashcard drilling (30%)

## 7-Week Curriculum Overview

This course follows a carefully structured 7-week progression, where each week builds on previous concepts. Patterns are introduced only when you have the foundational knowledge to understand them.

### Week 1: Python Fundamentals (Days 1-5)
**Concepts:** Lists, dictionaries, sets, list comprehensions, dict comprehensions, functions, lambda expressions, basic string operations

**Patterns introduced:**
- Filter and transform operations
- Basic data cleaning with comprehensions

**Why these concepts:** You need solid Python basics before touching pandas. Every pattern you'll learn builds on these fundamentals.

### Week 2: DataFrame Basics (Days 6-10)
**Concepts:** DataFrame creation and structure, column selection, boolean indexing, query method, sorting, missing value handling, basic aggregations

**Patterns introduced:**
- DataFrame filtering pattern
- Simple data cleaning pattern
- Basic aggregation pattern

**Why these concepts:** You must understand what DataFrames are and how to select/filter data before applying any advanced patterns.

### Week 3: Aggregation Patterns (Days 11-15)
**Concepts:** GroupBy mechanics, multiple aggregations, named aggregations, transform vs apply, merge operations (inner/outer), merge validation, concat operations

**Patterns introduced:**
- GroupBy aggregation pattern
- Named aggregations pattern
- Merge with indicator pattern (data quality validation)
- Transform for group calculations

**Why these concepts:** Aggregations are the foundation of analytics. Top N by group, rolling calculations, and other advanced patterns require solid groupby understanding.

### Week 4: Ranking & Window Patterns (Days 16-20)
**Concepts:** Sorting methods, ranking (dense, min, average), deduplication strategies, rolling windows, shift operations (lag/lead), cumulative calculations, date/time operations

**Patterns introduced:**
- Top N by group pattern (most common interview question)
- Deduplication pattern
- Rolling average pattern
- Lag/lead pattern
- Cumulative sum by group pattern

**Why these concepts:** These patterns appear in 70% of Analytics Engineer interviews. They require everything from Weeks 1-3.

### Week 5: Advanced Patterns (Days 21-25)
**Concepts:** String operations (str accessor methods), regex basics, categorical dtype, ordered categories, multi-level indexing, pivot tables, melt/stack/unstack, complex filtering (between, quantiles)

**Patterns introduced:**
- Text cleaning and extraction pattern
- Category optimization pattern
- Multi-index selection pattern
- Pivot table pattern
- Reshape pattern (wide to long)

**Why these concepts:** These differentiate strong candidates. They're less common than Week 4 patterns but still appear regularly.

### Week 6: Integration Patterns (Days 26-30)
**Concepts:** File I/O (CSV, JSON, Excel options), safe file reading, chunking large files, basic SQL reading, Airflow DAG structure, task dependencies, scheduling

**Patterns introduced:**
- Safe file read pattern
- Large file chunking pattern
- Basic Airflow orchestration pattern

**Why these concepts:** Practical patterns for take-home assignments. Also demonstrates you understand data integration (even if Fivetran handles it in production).

### Week 7: Interview Readiness (Days 31-35)
**Concepts:** SettingWithCopyWarning, chained indexing, vectorization vs loops, performance optimization, common gotchas, communication strategies

**Patterns introduced:**
- Vectorization pattern
- Avoiding copy warnings pattern
- Mock interview problem-solving patterns

**Why these concepts:** Meta-knowledge about using all previous patterns correctly and efficiently. Plus full mock interview practice.

---

**Total: 47 exercises across 7 weeks, organized into ~20 core patterns you'll memorize.**

## Daily Study Schedule (90-120 minutes)

### Morning Session (30 min)
- **10 min**: Review flashcards (spaced repetition)
- **20 min**: Read new concepts in course_with_schedule.md

### Main Session (60-90 min)
- **30 min**: Complete daily exercises
- **20 min**: Review and understand solutions
- **20 min**: Practice variations
- **20 min**: Code from memory

### Evening Review (Optional, 30 min)
- Update notes on challenging concepts
- Extra flashcard drilling for weak areas
- Prepare questions for next day

## Using the Materials

### 1. Course Content (`docs/course_with_schedule.md`)
Your primary reference for daily learning. Read the concept explanations that introduce patterns and their applications.

### 2. Weekly Exercise Files (`src/week1_exercises.py` through `week7_exercises.py`)

Each week has its own exercise file aligned with the curriculum:

```python
# Import exercises from the week you're studying
from week1_exercises import exercise_1_1, run_all_week1
from week2_exercises import exercise_2_1, run_all_week2

# Run individual exercises
exercise_1_1()  # List filtering pattern

# Or run all exercises for a week
run_all_week1()  # Runs all 7 Week 1 exercises in sequence
```

**Each exercise docstring shows:**
- **Pattern name** (e.g., "Pattern: Top N by Group")
- **Pattern reference** (e.g., "CorePatterns.top_n_by_group")
- **Concepts used** (e.g., "Week 3: groupby, Week 4: nlargest")
- **Problem description**
- **Time estimate** (match interview pressure)

**Exercise workflow:**
1. Read the problem statement
2. Note which pattern it teaches
3. Try solving without looking
4. Check the solution
5. Understand why this approach works
6. Implement a variation to cement understanding

### 3. Flashcards (`data/flashcards_complete.txt`)

Spaced repetition for recall under pressure.

- **Upload to Cram.com** for best spaced repetition experience
- **Categories:** Python syntax, pandas operations, pattern names, common gotchas
- **Frequency:** 2x daily minimum (morning and evening)
- **Target:** 95% recall before interviews

**What's in the flashcards:**
- Python syntax (list methods, dict operations, comprehension patterns)
- Pandas operations (groupby syntax, merge parameters, method signatures)
- **Pattern names and use cases** ("When to use top_n_by_group?" → "Finding top/bottom N items per group")
- Common gotchas (SettingWithCopyWarning, chained indexing, mutable defaults)

**The 20/50/30 learning split:**
- **20% reading:** Understand the pattern and concepts (LEARNING_GUIDE, pattern library, course_with_schedule)
- **50% practice:** Apply patterns to exercises (week exercise files)
- **30% retention:** Drill for recall under pressure (flashcards)

Flashcards ensure you can recall patterns quickly during interviews when time pressure and nerves affect memory. You're not just learning—you're training for performance under constraints.

### 4. Patterns Reference (`src/patterns_and_gotchas.py`)

Your pattern library—the core of the course.

```python
# Quick lookup when stuck on an exercise
from patterns_and_gotchas import CorePatterns
help(CorePatterns.top_n_by_group)

# Common gotchas to memorize
- reset_index() after groupby
- merge vs join differences  
- copy() vs view behavior
```

### Pattern Library Organization

The `patterns_and_gotchas.py` file contains ~20 core patterns organized in the `CorePatterns` class:

**Example patterns (full list in the file):**
- `top_n_by_group()` - Find top/bottom N items per group
- `groupby_multiple_agg()` - Multiple aggregations per group
- `merge_with_indicator()` - Track merge sources for data quality
- `handle_missing_values()` - Comprehensive null handling strategies
- `deduplication_strategies()` - Remove duplicates with various keep options
- `rolling_calculations()` - Moving averages and windows
- `lag_lead_operations()` - Shift for time series analysis
- ...and more

**Each pattern includes:**
- Clean implementation ready to copy and adapt
- Multiple solution methods (when multiple approaches exist)
- Comments explaining when to use this pattern
- Common variations and edge cases
- Performance notes (when relevant)

**How to use patterns during exercises:**

1. **Exercise docstring** says: "Pattern: Top N by Group"
2. **You look up** `CorePatterns.top_n_by_group` in the pattern library
3. **You study** the implementation and comments
4. **You adapt** it to the specific exercise problem
5. **You practice** until you can write it from memory
6. **You memorize** the pattern name and use case

**During actual interviews:**
- You won't have the file, but you'll have the patterns memorized
- **Pattern names become mental shortcuts:** "Oh, this is a top-N-by-group problem"
- You recall the general approach: sort then groupby head, or groupby then nlargest
- You implement from memory, adapting to specifics
- You can explain why you chose this pattern

**This is pattern-based learning:** Recognize problem type → Recall relevant pattern → Execute implementation.

## Practice Strategies

### Active Coding
```python
# Don't copy-paste! Type everything
# practice_work/day01.py
def my_groupby_solution(df):
    # Type from memory first
    # Then check solution
    return df.groupby('category').agg({'value': 'sum'})
```

### Progressive Difficulty
1. **Solve with hints** (look at pattern library)
2. **Solve without hints** (only documentation)
3. **Solve under time pressure** (15 min limit)
4. **Solve while explaining** (mock interview)

### Error Learning
Keep an error log:
```python
# notes/errors.md
## Day 3: KeyError
Problem: df['column'] failed
Solution: Check df.columns first
Learning: Always validate assumptions
```

## Communication Practice

### The STAR Method
- **Situation**: "Given a DataFrame with..."
- **Task**: "I need to find..."
- **Action**: "I'll use groupby because..."
- **Result**: "This gives us..."

### Think Aloud Protocol
```python
# Practice narrating your thought process
"First, I'll examine the data structure..."
"I notice there might be duplicates, so..."
"Let me verify my assumption by..."
"The time complexity would be..."
```

## Mock Interview Schedule

### Week 1: Foundation Check
- 10 min: Basic DataFrame operations
- Focus: Correct syntax

### Week 2: Concept Application
- 20 min: Medium difficulty problem
- Focus: Choosing right approach

### Week 3: Complex Problems
- 30 min: Multi-step solution
- Focus: Breaking down problem

### Week 4: Full Simulation
- 45 min: Complete interview
- Focus: Communication + code

## Success Metrics

### Daily
- ✅ Complete all exercises
- ✅ <5 min for basic problems
- ✅ Flashcard streak maintained

### Weekly
- ✅ Mock interview improvement
- ✅ Solve new problems without help
- ✅ Explain solutions clearly

### Pre-Interview
- ✅ 95% flashcard recall
- ✅ Solve medium problems in <10 min
- ✅ Comfortable with edge cases

## Common Pitfalls to Avoid

### 1. Passive Reading
❌ Just reading solutions
✅ Code everything yourself

### 2. Skipping Foundations
❌ Jumping to hard problems
✅ Master basics first

### 3. Not Timing Yourself
❌ Taking unlimited time
✅ Set timer for each problem

### 4. Silent Coding
❌ Coding without explaining
✅ Always narrate approach

## Weak Area Diagnosis

### Can't Start?
- Review patterns library
- Break problem into steps
- Start with data exploration

### Syntax Errors?
- Drill flashcards more
- Use quick_reference.md
- Type more, copy less

### Logic Errors?
- Draw data transformations
- Test with simple examples
- Use print debugging

### Too Slow?
- Practice common patterns
- Learn keyboard shortcuts
- Prepare code templates

## Study Tools Integration

### Wing IDE Setup (Included with Platform)

The platform comes pre-configured with Wing IDE project files:

- **Automatic environment:** Virtual environment at `~/.venvs/paip` activated automatically
- **Import support:** Can import from pattern library: `from patterns_and_gotchas import CorePatterns`
- **Debugging:** Set breakpoints, inspect variables, step through code
- **Interactive console:** Test patterns quickly with Python shell
- **Desktop shortcut:** "PAIP - Wing IDE" launches directly into project

**Using Wing for exercises:**
1. Open Wing via desktop shortcut or `Open-Wing` command
2. Create practice files in `study/practice_work/`
3. Import patterns to test: `from patterns_and_gotchas import CorePatterns`
4. Run exercises: `from week1_exercises import exercise_1_1; exercise_1_1()`
5. Debug when stuck: Set breakpoints, inspect DataFrames

### Version Control (Already Configured)

The platform repository is already set up with git:
- **Wing project files tracked:** `.wpr` file is version controlled (shared settings)
- **Your work tracked:** Everything in `study/` directory is tracked
- **Practice progress saved:** Commit your work as you complete exercises

```bash
# Track your progress
cd ~/python-analytics-interview-prep
git add study/practice_work/day01.py
git commit -m "Completed Week 1 exercises"
git push  # If you've set up a remote
```

**Pro tip:** Commit after completing each week. This creates checkpoints you can review before interviews.

## Pre-Interview Checklist

### 1 Week Before
- [ ] Complete all 47 exercises (7 weeks of content)
- [ ] 95% flashcard accuracy across all categories
- [ ] 3 mock interviews completed (Week 7 exercises)
- [ ] Pattern names memorized (can name the ~20 core patterns)
- [ ] Can recognize which pattern applies to which problem type

### 1 Day Before
- [ ] Review error log and weak areas
- [ ] Quick flashcard review (focus on patterns, not syntax details)
- [ ] Test Wing IDE environment (imports work, can run code)
- [ ] Prepare questions for interviewer
- [ ] Review talking_points.md for communication strategies

### Day Of
- [ ] Warm up with 2-3 easy problems (Week 1-2 exercises)
- [ ] Review communication tips (STAR method, think-aloud protocol)
- [ ] Test audio/video/screen share if remote
- [ ] Have water ready
- [ ] Remember: You know the patterns. Trust your preparation.

## Continuous Improvement

### After Each Session
1. What was challenging?
2. What pattern helped most?
3. What would I do differently?

### After Each Week
1. Which concepts need review?
2. Are flashcards effective?
3. Is pace sustainable?

### After Mock Interviews
1. Where did I struggle?
2. Was explanation clear?
3. Did I manage time well?

---

Remember: **Consistency > Intensity**. Daily practice beats weekend cramming every time.

For technical details about the platform, see [PLATFORM_ARCHITECTURE.md](PLATFORM_ARCHITECTURE.md)

---

## Category 9: Testing & Validation

### Pattern 25: Edge Case Testing

**Interview signal:** "How would you test this function?"

**The pattern:**
```python
# Test boundary conditions, empty inputs, None values
def test_edge_cases():
    # Empty input
    assert process([]) == expected_empty
    
    # None handling
    assert process(None) == expected_none
    
    # Boundary values
    assert process([0]) == expected_single
    assert process([-1, 0, 1]) == expected_boundaries
    
    # Large input
    assert process(range(10000)) == expected_large
```

**When to use:** Every function needs edge case validation

**Common gotchas:**
- Forgetting empty list/None cases
- Not testing boundary values (0, -1, max)
- Missing large input performance tests

---

### Pattern 26: Assertion Patterns

**Interview signal:** "Write tests to validate your solution"

**The pattern:**
```python
# Standard assertions
assert result == expected  # Equality
assert len(result) == 5    # Length
assert 'key' in result     # Membership
assert result > threshold  # Comparison

# DataFrame assertions
assert df.shape == (100, 5)
assert list(df.columns) == ['col1', 'col2']
assert df['col'].isna().sum() == 0  # No nulls
```

**When to use:** Validating function outputs, DataFrame operations

**Common gotchas:**
- Float comparison without tolerance (use `math.isclose()`)
- Not checking DataFrame dtypes
- Assuming column order

---

### Pattern 27: Test Data Generation

**Interview signal:** "Create test data for this scenario"

**The pattern:**
```python
# List-based test data
test_nums = list(range(1, 11))
test_nulls = [1, None, 3, None, 5]
test_edge = []  # empty case

# DataFrame test data
test_df = pd.DataFrame({
    'id': range(1, 101),
    'category': ['A', 'B'] * 50,
    'value': range(100, 0, -1)
})

# Dictionary test data
test_dict = {f'key{i}': i*10 for i in range(5)}
```

**When to use:** Setting up test scenarios, validating transformations

**Common gotchas:**
- Test data doesn't represent real edge cases
- Missing null/duplicate/negative values
- Test data too small to catch issues

---

### Pattern 28: Parametrized Testing

**Interview signal:** "Test this with multiple inputs"

**The pattern:**
```python
# Test multiple scenarios efficiently
test_cases = [
    ([1, 2, 3], 6),      # simple case
    ([], 0),             # empty
    ([1], 1),            # single
    ([-1, 1], 0),        # negatives
]

for inputs, expected in test_cases:
    result = sum_list(inputs)
    assert result == expected, f"Failed for {inputs}"
```

**When to use:** Testing function with various input combinations

**Common gotchas:**
- Not covering enough scenarios
- Test cases too similar (redundant)
- Missing failure cases

---

### Pattern 29: Testing Pandas Operations

**Interview signal:** "Validate this DataFrame transformation"

**The pattern:**
```python
# DataFrame equality
pd.testing.assert_frame_equal(result, expected)

# Column validation
assert set(result.columns) == {'col1', 'col2'}

# Value validation
assert result['col'].between(0, 100).all()
assert result['id'].is_unique

# Shape validation
assert result.shape[0] == expected_rows
```

**When to use:** Validating DataFrame operations, data quality checks

**Common gotchas:**
- `==` doesn't work for DataFrames (use `equals()` or `assert_frame_equal`)
- Float precision issues
- Not checking for NaN values
- Index differences causing false failures

---

### Pattern 30: Orchestration Task Dependencies

**Interview signal:** "How would you coordinate these pipeline steps?" or "Design a workflow for multiple data sources"

**The pattern:**
Task dependencies define execution order in orchestration frameworks. Common in Airflow interviews even for Analytics Engineers.

```python
# Sequential execution
sync_salesforce >> run_dbt >> send_notification

# Parallel then converge
[sync_salesforce, sync_stripe, sync_zendesk] >> run_dbt_models

# Complex dependencies
sync_tasks >> validate_syncs >> run_transformations >> quality_checks
quality_checks >> [success_notification, failure_alert]
```

**Real example from modern stack:**
```python
from airflow.decorators import dag
from airflow.providers.fivetran.operators.fivetran import FivetranOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.providers.slack.operators.slack import SlackWebhookOperator

@dag(schedule="@daily", start_date=datetime(2024, 1, 1))
def data_pipeline():
    # Sync multiple sources in parallel
    sync_sf = FivetranOperator(task_id="sync_salesforce", connector_id="sf_prod")
    sync_stripe = FivetranOperator(task_id="sync_stripe", connector_id="stripe_prod")
    
    # Transform after all syncs complete
    run_dbt = DbtCloudRunJobOperator(task_id="run_dbt", job_id=12345)
    
    # Notify on completion
    notify = SlackWebhookOperator(task_id="notify", message="Pipeline complete")
    
    # Define dependencies
    [sync_sf, sync_stripe] >> run_dbt >> notify
```

**When to use:** Questions about workflow coordination, multi-step pipelines, or "how do you ensure order?"

**Common gotchas:**
- Circular dependencies cause failures (A → B → A won't work)
- Forgetting to handle failures (use trigger rules)
- Not considering parallel execution when possible
- Confusing orchestration (Airflow) with transformation (dbt/SQL)

**Interview talking point:**
"Task dependencies map to data lineage. If `marts.customers` depends on `staging.orders`, then the dbt task that creates staging must complete before the marts task runs. Airflow's `>>` enforces this execution order."

**SQL mental model:**
```sql
-- Data dependencies in warehouse
CREATE TABLE staging.orders AS SELECT * FROM raw.orders;  -- Must exist first

CREATE TABLE marts.customer_summary AS 
SELECT customer_id, SUM(amount)
FROM staging.orders  -- Depends on staging existing
GROUP BY customer_id;
```

**Orchestration equivalent:**
```python
load_staging_orders >> create_customer_summary
```

