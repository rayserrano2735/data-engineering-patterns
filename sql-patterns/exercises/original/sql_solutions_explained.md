# SQL Window Functions - Solutions Explained

## Exercise 1: ROW_NUMBER() for Deduplication
**Goal:** Keep only the most recent version of each movie

**Key Concepts:**
- `ROW_NUMBER()` assigns sequential integers within each partition
- `PARTITION BY title_code` restarts numbering for each movie
- `ORDER BY ingestion_ts_utc DESC` ensures newest gets row_number = 1
- Filter WHERE part_row = 1 keeps only the latest version

**Why This Matters:**
- Common pattern for deduplication
- Often used in data warehousing for slowly changing dimensions

---

## Exercise 2: RANK() vs DENSE_RANK()
**Goal:** Understand the difference when handling ties

**Key Concepts:**
- `RANK()`: Skips numbers after ties (1, 2, 2, 4)
- `DENSE_RANK()`: No gaps in sequence (1, 2, 2, 3)
- Both give same rank to tied values

**Interview Tip:**
- Always clarify which behavior is wanted when ranking with possible ties

---

## Exercise 3: Top N per Group
**Goal:** Find top 3 longest movies per genre

**Pattern:**
```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY group ORDER BY metric DESC) as rn
)
SELECT * FROM ranked WHERE rn <= N
```

**Why ROW_NUMBER() instead of RANK():**
- ROW_NUMBER() guarantees exactly N results per group
- RANK() might return more than N if there are ties

---

## Exercise 4: Running Totals
**Goal:** Cumulative sum over time

**Critical Frame Clause:**
```sql
SUM(value) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

**Why Specify ROWS BETWEEN:**
- Makes intent explicit
- Some databases have different defaults
- Shows you understand frame clauses

---

## Exercise 5: Moving Average (3-Year Window)
**Goal:** Smooth out yearly variations

**The Frame:**
```sql
AVG(value) OVER (ORDER BY year ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
```

**Breakdown:**
- 1 PRECEDING = previous year
- CURRENT ROW = this year  
- 1 FOLLOWING = next year
- Results in 3-year average

**Edge Cases:**
- First row: only current + next (2-year avg)
- Last row: only previous + current (2-year avg)

---

## Exercise 6: LAG and LEAD
**Goal:** Access previous/next row values

**Key Points:**
- No need for self-joins!
- `LAG(column, offset, default)` looks backward
- `LEAD(column, offset, default)` looks forward
- Default offset is 1

**Pro Tip for Actor Timeline:**
- Filter for primary roles (ORDERING = 1) to avoid duplicates
- ORDER BY should match business logic (year, then title for ties)

---

## Exercise 7: PERCENT_RANK()
**Goal:** Find percentile position

**Formula:** (rank - 1) / (total_rows - 1)
- Returns value between 0 and 1
- 0 = minimum value
- 1 = maximum value
- 0.5 = median position

**Use DISTINCT:**
- Prevents duplicate runtime values from skewing percentiles

---

## Exercise 8: Multiple Window Functions ⚠️ CRITICAL TRAP ⚠️
**Goal:** Rank and running total together

**THE TRAP - RANGE vs ROWS:**

```sql
-- WRONG (uses default RANGE):
SUM(movie_count) OVER (ORDER BY movie_count DESC, PRIMARY_NAME)

-- CORRECT (explicit ROWS):
SUM(movie_count) OVER (ORDER BY movie_count DESC, PRIMARY_NAME 
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

**Why This Matters:**
- **RANGE** (default): Groups all rows with same ORDER BY values
  - If 5 actors have 75 movies, all get same running total!
- **ROWS**: Counts individual rows regardless of ties
  - Each actor gets unique running total even if counts match

**Example with Ties:**
```
With ROWS:
Actor A: 75 movies → Total: 75
Actor B: 75 movies → Total: 150
Actor C: 75 movies → Total: 225

With RANGE (default):
Actor A: 75 movies → Total: 225 (includes all three!)
Actor B: 75 movies → Total: 225 (same!)
Actor C: 75 movies → Total: 225 (same!)
```

**Interview Gold:** If interviewer asks about running totals with ties, this shows deep understanding!

---

## Exercise 9: Gap and Island Problem
**Goal:** Find consecutive sequences, identify gaps

**Pattern:**
```sql
ROW_NUMBER() OVER (ORDER BY sequence_value) - sequence_value AS group_id
```

**The Trick:**
- If values are consecutive, (row_number - value) stays constant
- When gap occurs, this difference changes
- GROUP BY this difference to find islands

---

## Exercise 10: FIRST_VALUE and LAST_VALUE
**Goal:** Get first and last values in a window

**CRITICAL: Frame clause for LAST_VALUE!**
```sql
FIRST_VALUE(col) OVER (PARTITION BY group ORDER BY date)  -- Works with default frame

LAST_VALUE(col) OVER (PARTITION BY group ORDER BY date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)  -- NEEDS full frame!
```

**Why LAST_VALUE Needs Special Frame:**
- Default frame is UNBOUNDED PRECEDING to CURRENT ROW
- So LAST_VALUE with default only sees up to current row!
- Must specify UNBOUNDED FOLLOWING to see all rows

---

## Exercise 11: NTILE - Dividing Data into Buckets
**Goal:** Split movies into quartiles by runtime

**Key Concepts:**
- `NTILE(n)` divides ordered rows into n groups of equal size (or as close as possible)
- Each row gets a bucket number from 1 to n
- Useful for percentile analysis, A/B testing groups, etc.

**Example:**
```sql
NTILE(4) OVER (ORDER BY runtime_minutes)
```
- Quartile 1: Shortest 25% of movies
- Quartile 2: 25-50th percentile
- Quartile 3: 50-75th percentile
- Quartile 4: Longest 25%

**Interview Tip:** If row count isn't evenly divisible, earlier buckets get the extra rows

---

## Exercise 12: Finding Second/Nth Highest Value
**Goal:** Find second highest runtime per genre

**Pattern:**
```sql
WITH ranked AS (
    SELECT *, DENSE_RANK() OVER (PARTITION BY group ORDER BY value DESC) as dr
)
SELECT * FROM ranked WHERE dr = 2  -- or any nth position
```

**Why DENSE_RANK() not ROW_NUMBER():**
- DENSE_RANK() handles ties properly
- If two movies tie for longest, we still get a true "second highest"
- ROW_NUMBER() might skip the actual second highest value

---

## Exercise 13: Median Calculation with PERCENTILE_CONT
**Goal:** Find median (50th percentile) runtime

**Syntax:**
```sql
PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY column)
```

**Key Points:**
- PERCENTILE_CONT = continuous (interpolates between values)
- PERCENTILE_DISC = discrete (returns actual value from dataset)
- 0.5 = median, 0.25 = Q1, 0.75 = Q3
- This is an aggregate function, not a window function!

**Median vs Mean:**
- Median: Less affected by outliers
- Mean: Can be skewed by extreme values
- Include both to show distribution understanding

---

## Exercise 14: Complex Date-Based Rolling Windows
**Goal:** 3-year rolling movie count

**The Pattern:**
```sql
SUM(movies) OVER (
    PARTITION BY actor 
    ORDER BY year 
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

**Breakdown:**
- 2 PRECEDING = two years before
- CURRENT ROW = this year
- Total = 3-year window

**Real-World Use:**
- Rolling revenue calculations
- Moving average of sales
- Trend analysis over time periods

---

## Exercise 15: Self-Join with Window Functions
**Goal:** Find top actor collaborations

**Complex Pattern Combining:**
1. Self-join to find pairs
2. Aggregation to count collaborations
3. Window function to rank pairs

**Key Tricks:**
- `tp1.PERSON_CODE < tp2.PERSON_CODE` prevents duplicates (A-B vs B-A)
- HAVING filters after GROUP BY
- RANK() assigns same rank to ties
- Can add actor names with additional joins

**Interview Gold:** Shows you can combine multiple SQL concepts elegantly

---

## Debugging Exercises - Common Pitfalls

### Debug 1: Window Functions in WHERE Clause
**Why it fails:** WHERE is evaluated before window functions

**The Rule:** Window functions can only be in SELECT or ORDER BY

**Solution:** Use CTE or subquery:
```sql
WITH windowed AS (SELECT *, ROW_NUMBER() OVER(...) as rn)
SELECT * FROM windowed WHERE rn = 1
```

### Debug 2: Wrong Direction Frame Clause
**The Mistake:** Using FOLLOWING for historical aggregation

**Remember:**
- Running totals look BACKWARD (UNBOUNDED PRECEDING)
- Future projections look FORWARD (UNBOUNDED FOLLOWING)

### Debug 3: Confused PARTITION BY and ORDER BY
**Common Confusion:**
- PARTITION BY = groups to separate
- ORDER BY = sorting within each group

**Think:** "I want to PARTITION my data by genre, then ORDER by runtime"

---

## Advanced Interview Topics

### When to Use RANGE vs ROWS
- **ROWS:** Physical row count (most common, predictable)
- **RANGE:** Logical value range (tricky with ties, know the gotcha!)

### Optimization Tips They Love to Hear
1. "Window functions often outperform self-joins"
2. "One pass through data vs multiple"
3. "But check execution plan - sometimes optimizer surprises you"

### The "Median Without PERCENTILE_CONT" Trick
If they say the database doesn't support PERCENTILE_CONT:
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

## Quick Reference for Tuesday

**When to use each function:**
- **ROW_NUMBER()**: Deduplication, Top N per group (no ties)
- **RANK()**: Competition-style ranking (with gaps)
- **DENSE_RANK()**: Ranking without gaps
- **PERCENT_RANK()**: Percentile position
- **NTILE()**: Divide into equal buckets
- **LAG/LEAD**: Compare to previous/next rows
- **SUM() OVER**: Running totals (remember ROWS BETWEEN!)
- **AVG() OVER**: Moving averages
- **FIRST/LAST_VALUE**: Endpoints of windows (frame clause!)
- **PERCENTILE_CONT**: Median and other percentiles

**Frame Clause Cheat Sheet:**
- `UNBOUNDED PRECEDING`: From start of partition
- `N PRECEDING`: N rows before
- `CURRENT ROW`: Current row
- `N FOLLOWING`: N rows after
- `UNBOUNDED FOLLOWING`: To end of partition

**Remember:** 
- ROWS = physical rows
- RANGE = logical values (beware of ties!)
- Default frame: RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

Good luck Tuesday! You've got this! 💙