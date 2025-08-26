# SQL Window Functions - Pattern Recognition Textbook

## Introduction: Think in Patterns, Not Functions

Window functions solve recurring data patterns. Master the pattern first, then apply the appropriate function. This textbook presents 15 patterns that correspond directly to Exercises 1-15.

---

## Pattern 1: Deduplication - "Keep Only the Latest"

### The Problem
You have multiple versions of the same record (due to updates, ingestion times, or duplicates). You need exactly one version per entity.

### The Pattern Recognition
- Multiple rows with same ID
- Timestamp or version column exists
- Need: Most recent/relevant version only

### The Solution
```sql
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY entity_id 
            ORDER BY timestamp DESC
        ) as rn
    FROM table
)
SELECT * FROM ranked WHERE rn = 1
```

### Visual Example
```
Before:                After:
ID  Version  Date      ID  Version  Date
A   1        Jan       A   3        Mar
A   2        Feb       B   2        Apr
A   3        Mar
B   1        Mar
B   2        Apr
```

---

## Pattern 2: Ranking with Ties - "Olympics vs Dense Competition"

### The Problem
You need to rank items but must decide how to handle ties.

### The Pattern Recognition
- Competition or ordering scenario
- Ties are possible
- Decision: Skip ranks after ties (Olympics) or continuous ranks (dense)?

### The Solution
```sql
-- Olympics style (1,2,2,4):
RANK() OVER (ORDER BY score DESC)

-- Continuous (1,2,2,3):
DENSE_RANK() OVER (ORDER BY score DESC)

-- Unique positions (1,2,3,4):
ROW_NUMBER() OVER (ORDER BY score DESC)
```

### Visual Example
```
Score: 100, 90, 90, 80
RANK:        1, 2, 2, 4  (no bronze medal!)
DENSE_RANK:  1, 2, 2, 3  (bronze exists)
ROW_NUMBER:  1, 2, 3, 4  (arbitrary tie-breaking)
```

---

## Pattern 3: Top N per Group - "Best in Each Category"

### The Problem
Find top performers within each category, not overall.

### The Pattern Recognition
- Groups/categories exist
- Need top N within EACH group
- Overall top N won't work

### The Solution
```sql
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY category 
            ORDER BY metric DESC
        ) as rn
    FROM table
)
SELECT * FROM ranked WHERE rn <= 3
```

### Visual Example
```
Genre    Movie         Runtime   Rank
Action   Die Hard      132       1
Action   Matrix        136       2  ← Top 3 Action
Action   Terminator    107       3
Comedy   Airplane      88        1
Comedy   Ghostbusters  105       2  ← Top 3 Comedy
```

---

## Pattern 4: Running Totals - "Cumulative Progress"

### The Problem
Track cumulative values over time (bank balance, YTD sales, progressive sum).

### The Pattern Recognition
- Time-ordered data
- Each row adds to previous total
- Need: Running sum at each point

### The Solution
```sql
SUM(amount) OVER (
    ORDER BY date 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

### ⚠️ CRITICAL: ROWS vs RANGE
```sql
Date    Amount  ROWS_Total  RANGE_Total
Jan-1   100     100         100
Jan-2   50      150         150
Jan-2   75      225         225  ← ROWS counts this separately
Jan-2   25      250         225  ← RANGE groups all Jan-2!
```

---

## Pattern 5: Moving Averages - "Smoothing the Noise"

### The Problem
Smooth out variations by averaging over rolling windows.

### The Pattern Recognition
- Time series with volatility
- Need smoothed trend
- Fixed window size (3-day, 7-day, etc.)

### The Solution
```sql
-- 3-period moving average (previous, current, next)
AVG(value) OVER (
    ORDER BY date 
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
)
```

### Visual Example
```
Day  Sales  3-Day-Avg
1    100    150        (100+200)/2
2    200    200        (100+200+300)/3
3    300    250        (200+300+200)/3
4    200    233        (300+200+100)/3
5    100    150        (200+100)/2
```

---

## Pattern 6: Previous/Next Values - "Context from Neighbors"

### The Problem
Compare current row to previous or next row (period-over-period change, sequential analysis).

### The Pattern Recognition
- Need previous/next value in same row
- Self-join would be complex
- Computing differences or trends

### The Solution
```sql
LAG(value, 1) OVER (ORDER BY date) as previous_value,
LEAD(value, 1) OVER (ORDER BY date) as next_value
```

### Visual Example
```
Month  Sales  Prev_Sales  Change
Jan    100    NULL        NULL
Feb    120    100         +20
Mar    115    120         -5
Apr    130    115         +15
```

---

## Pattern 7: Percentile Distribution - "Where Do I Stand?"

### The Problem
Find position within overall distribution (percentile rank).

### The Pattern Recognition
- Need relative position, not absolute
- "Top 10%" more meaningful than "rank 45"
- Statistical distribution analysis

### The Solution
```sql
-- Percentile rank (0 to 1)
PERCENT_RANK() OVER (ORDER BY value)
```

### Visual Example
```
Score  PERCENT_RANK  Interpretation
60     0.00          Minimum
70     0.25          25th percentile
80     0.50          Median position
90     0.75          75th percentile
100    1.00          Maximum
```

---

## Pattern 8: Multiple Windows with Tie Handling - "Complex Rankings"

### The Problem
Combine multiple window functions while properly handling tied values in running totals.

### The Pattern Recognition
- Need both ranking AND running totals
- Tied values exist in ORDER BY column
- RANGE vs ROWS behavior critical

### The Solution
```sql
SELECT 
    name,
    value,
    DENSE_RANK() OVER (ORDER BY value DESC) as rank,
    SUM(value) OVER (
        ORDER BY value DESC, name  -- Secondary sort
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
```

### ⚠️ The RANGE Trap
```sql
-- With ties at value=75:
ROWS:  Each row gets unique running total
RANGE: All value=75 rows get SAME running total
```

---

## Pattern 9: Gap and Island Detection - "Finding Sequences"

### The Problem
Identify consecutive sequences and gaps in sequential data.

### The Pattern Recognition
- Time series or sequential data
- Need to find continuous periods
- Gaps indicate new groups

### The Solution
```sql
-- CRITICAL: Start with DISTINCT to get one row per time period
WITH distinct_periods AS (
    SELECT DISTINCT value_column
    FROM table
),
grouped AS (
    SELECT *,
        value - ROW_NUMBER() OVER (ORDER BY value) as group_id
    FROM distinct_periods
)
SELECT 
    MIN(value) as start,
    MAX(value) as end,
    COUNT(*) as length
FROM grouped
GROUP BY group_id
```

### ⚠️ Critical: Why DISTINCT First?
Without DISTINCT, multiple records per year break the pattern:
```
Year  Movies  RowNum  Year-RowNum
2000  Movie1  1       1999
2000  Movie2  2       1998  ← Different group for same year!
2001  Movie3  3       1998
```

With DISTINCT first:
```
Year  RowNum  Year-RowNum
2000  1       1999  ← Consistent
2001  2       1999  ← Same group = consecutive
```

### Visual Breakdown
```
Year  RowNum  Year-RowNum  Group
1990  1       1989         A ← consecutive
1991  2       1989         A ← same difference
1992  3       1989         A ← same group
1994  4       1990         B ← gap detected!
1995  5       1990         B ← new group
```

---

## Pattern 10: First and Last Values - "Endpoints"

### The Problem
Get first and last values within a window or partition.

### The Pattern Recognition
- Need both endpoints in one query
- Grouping by some category
- Career start/end, first/last transaction

### The Solution
```sql
FIRST_VALUE(column) OVER (
    PARTITION BY group 
    ORDER BY sequence
    -- Default frame works for FIRST_VALUE
) as first,

LAST_VALUE(column) OVER (
    PARTITION BY group 
    ORDER BY sequence
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
) as last
```

### ⚠️ CRITICAL: LAST_VALUE needs full frame!
Default frame stops at CURRENT ROW, so LAST_VALUE returns current, not last!

---

## Pattern 11: Equal Distribution Buckets - "Quartiles and Percentiles"

### The Problem
Divide data into equal-sized groups (quartiles, deciles, percentiles).

### The Pattern Recognition
- Need to segment population
- Equal-sized buckets desired
- Statistical grouping required

### The Solution
```sql
-- Divide into N equal buckets
NTILE(4) OVER (ORDER BY value)  -- quartiles
NTILE(10) OVER (ORDER BY value) -- deciles
NTILE(100) OVER (ORDER BY value) -- percentiles
```

### Visual Example
```
With 10 rows and NTILE(4):
Rows 1-3:  Quartile 1 (extra row)
Rows 4-5:  Quartile 2
Rows 6-8:  Quartile 3 (extra row)
Rows 9-10: Quartile 4
```

---

## Pattern 12: Finding Nth Values - "Second Best"

### The Problem
Find specific positions (2nd highest, 3rd lowest) within groups.

### The Pattern Recognition
- Not just the top, but specific position
- Ties must be handled correctly
- Per group, not overall

### The Solution
```sql
WITH ranked AS (
    SELECT *,
        DENSE_RANK() OVER (
            PARTITION BY group 
            ORDER BY value DESC
        ) as dr
    FROM table
)
SELECT * FROM ranked WHERE dr = 2  -- second highest
```

### Why DENSE_RANK?
```
Values: 100, 100, 90, 80
RANK:        1, 1, 3, 4  (no 2nd highest!)
DENSE_RANK:  1, 1, 2, 3  (90 is truly 2nd highest)
```

---

## Pattern 13: Statistical Calculations - "Beyond Average"

### The Problem
Calculate median, quartiles, or other percentiles (not just mean).

### The Pattern Recognition
- Average skewed by outliers
- Need robust central tendency
- Percentile-based analysis

### The Solution
```sql
-- Median (50th percentile)
PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY value)

-- Quartiles
PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY value) as Q1,
PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY value) as Q3

-- Note: This is aggregate, not window function!
```

### Median Without PERCENTILE_CONT
```sql
WITH ranked AS (
    SELECT value,
        ROW_NUMBER() OVER (ORDER BY value) as rn,
        COUNT(*) OVER () as total
    FROM table
)
SELECT AVG(value) as median
FROM ranked
WHERE rn IN (FLOOR((total+1)/2), CEILING((total+1)/2))
```

---

## Pattern 14: Complex Date Windows - "Rolling Time Periods"

### The Problem
Calculate metrics over rolling date windows (3-year total, 30-day average).

### The Pattern Recognition
- Time-based calculations
- Not just cumulative but rolling window
- Window based on row count, not dates

### The Solution
```sql
-- 3-year rolling total (current + 2 previous)
SUM(value) OVER (
    ORDER BY year 
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)

-- Note: This is ROWS not date arithmetic!
```

### Visual Example
```
Year  Sales  3-Year-Total
2018  100    100          (only 2018)
2019  150    250          (2018-2019)
2020  200    450          (2018-2020)
2021  180    530          (2019-2021)
2022  220    600          (2020-2022)
```

---

## Pattern 15: Self-Join with Rankings - "Collaboration Analysis"

### The Problem
Find relationships between entities (actor collaborations, product co-purchases) and rank them.

### The Pattern Recognition
- Need pairs/combinations
- Self-join required
- Ranking the relationships

### The Solution
```sql
WITH pairs AS (
    -- Self-join to find pairs
    SELECT 
        a.id as id1,
        b.id as id2,
        COUNT(*) as frequency
    FROM table a
    JOIN table b ON a.key = b.key AND a.id < b.id
    GROUP BY a.id, b.id
),
ranked_pairs AS (
    -- Rank the pairs
    SELECT *,
        RANK() OVER (ORDER BY frequency DESC) as rank
    FROM pairs
)
SELECT * FROM ranked_pairs WHERE rank <= 10
```

### Key Tricks
- `a.id < b.id` prevents duplicates (A-B vs B-A)
- Window function ranks the aggregated results
- Combines aggregation + window functions

---

## Common Pitfalls and Solutions

### Pitfall 1: Window Functions in WHERE
```sql
-- WRONG:
WHERE ROW_NUMBER() OVER (...) = 1

-- RIGHT:
WITH cte AS (SELECT *, ROW_NUMBER() OVER (...) as rn)
SELECT * FROM cte WHERE rn = 1
```

### Pitfall 2: Wrong Frame Direction
```sql
-- WRONG for running total:
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING

-- RIGHT:
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

### Pitfall 3: Forgetting Frame for LAST_VALUE
```sql
-- WRONG (uses default frame):
LAST_VALUE(col) OVER (ORDER BY date)

-- RIGHT:
LAST_VALUE(col) OVER (
    ORDER BY date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

### Pitfall 4: RANGE vs ROWS with Ties
Always use ROWS for running totals unless you specifically want to group tied values!

---

## Quick Pattern Reference

| Exercise | Pattern | Key Function |
|----------|---------|--------------|
| 1 | Deduplication | ROW_NUMBER() |
| 2 | Ranking with ties | RANK() vs DENSE_RANK() |
| 3 | Top N per group | ROW_NUMBER() + PARTITION |
| 4 | Running totals | SUM() + frame |
| 5 | Moving averages | AVG() + frame |
| 6 | Previous/next values | LAG()/LEAD() |
| 7 | Percentile position | PERCENT_RANK() |
| 8 | Multiple windows + ties | ROWS vs RANGE |
| 9 | Gap detection | value - ROW_NUMBER() |
| 10 | First/last values | FIRST_VALUE()/LAST_VALUE() |
| 11 | Equal buckets | NTILE() |
| 12 | Nth highest | DENSE_RANK() = N |
| 13 | Median/percentiles | PERCENTILE_CONT() |
| 14 | Rolling date windows | Complex frames |
| 15 | Self-join rankings | Aggregation + RANK() |

---

## The Pattern Recognition Process

1. **Identify the pattern**: What problem am I solving?
2. **Choose the function**: Which window function fits this pattern?
3. **Determine partitioning**: Do I need groups?
4. **Set the ordering**: What sequence matters?
5. **Define the frame**: Which rows should be included?
6. **Handle edge cases**: What about ties, nulls, boundaries?

Master the patterns, and the functions become tools rather than mysteries.