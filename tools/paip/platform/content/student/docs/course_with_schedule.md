# Python for Analytics Engineering - Complete Course with Schedule
**Version: 1.0.5-RC1

## Course Overview
**Duration:** 8 weeks (40 hours total)
**Target:** Analytics Engineers preparing for technical interviews
**Format:** Self-paced with daily assignments

## Week 1: Python Fundamentals - Foundation for Pattern Learning (7 hours)

**Week 1 Mission:** Build Python fundamentals that enable pattern-based learning starting Week 2. No pandas patterns yet - just the building blocks patterns are made from.

**Learning Objectives:**
- Master core data structures (lists, dicts, sets)
- Write comprehensions for filtering and transformation  
- Define and use functions with parameters and return values
- Use lambda expressions for sorting and filtering
- Perform basic string operations

### Day 1-2: Data Structures (2 hours)

**Lists: Ordered Collections**
```python
# Creating and accessing
numbers = [1, 2, 3, 4, 5]
first = numbers[0]
last = numbers[-1]

# Common operations
numbers.append(6)
numbers.remove(3)
len(numbers)
3 in numbers
```

**When to use:** Ordered data, duplicates allowed, access by index

**Dictionaries: Key-Value Mappings**
```python
# Creating and accessing
person = {'name': 'Alice', 'age': 30, 'dept': 'Analytics'}
name = person['name']
salary = person.get('salary', 0)  # Default if missing

# Modifying
person['age'] = 31
person['salary'] = 75000
```

**When to use:** Look up by key, structured data, count/aggregate

**Sets: Unique Collections**
```python
# Creating and operations
unique_ids = {1, 2, 3, 4, 5}
a = {1, 2, 3}
b = {3, 4, 5}
a | b  # Union
a & b  # Intersection
```

**When to use:** Unique values, fast membership testing, set operations

**Interview connection:** Lists become DataFrame rows. Dicts become DataFrame records. Understanding these now makes pandas intuitive later.

**Practice:**
- Exercise 1.1: Create list, filter evens
- Exercise 1.2: Remove duplicates preserving order
- Exercise 1.3: Merge dicts keeping higher values
- Exercise 1.4: Debug list modification during iteration
- Exercise 1.5: Word frequency counter using dict

### Day 3: Comprehensions (1.5 hours)

**List Comprehensions: Filter and Transform**
```python
# Without comprehension (verbose)
evens = []
for n in range(10):
    if n % 2 == 0:
        evens.append(n)

# With comprehension (Pythonic)
evens = [n for n in range(10) if n % 2 == 0]
```

**Pattern:** `[transform(item) for item in sequence if condition]`

**Dict Comprehensions:**
```python
names = ['Alice', 'Bob', 'Charlie']
name_lengths = {name: len(name) for name in names}
```

**Interview use case:**
```python
# Extract specific data
transactions = [
    {'id': 1, 'amount': 100, 'status': 'completed'},
    {'id': 2, 'amount': 50, 'status': 'pending'}
]
completed_amounts = [t['amount'] for t in transactions if t['status'] == 'completed']
```

**Interview connection:** Comprehensions → DataFrame boolean indexing. Same filter/transform logic, cleaner syntax in pandas.

**Practice:**
- Exercise 2.1: Squares of positive numbers only
- Exercise 2.2: Name to length dictionary
- Exercise 2.3: Flatten nested lists
- Exercise 2.4: Debug character vs word iteration
- Exercise 2.5: Clean and validate emails

### Day 4: Functions and Parameters (1.5 hours)

**Function Basics**
```python
def calculate_total(price, quantity, tax_rate=0.08):
    subtotal = price * quantity
    tax = subtotal * tax_rate
    return subtotal + tax

# Multiple return values
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)
```

**Critical gotcha - Mutable defaults:**
```python
# WRONG: Mutable default argument
def add_item(item, items=[]):    # BAD!
    items.append(item)
    return items

# RIGHT: Use None as default
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

**Type hints for clarity:**
```python
from typing import List, Dict, Optional

def process_data(
    records: List[Dict[str, any]], 
    min_value: float,
    max_results: Optional[int] = None
) -> List[Dict[str, any]]:
    """Filter records by value range."""
    filtered = [r for r in records if r['value'] >= min_value]
    if max_results:
        filtered = filtered[:max_results]
    return filtered
```

**Interview connection:** Breaking problems into functions shows logical thinking. Type hints show production-quality code.

**Practice:**
- Exercise 3.1: Currency formatter with defaults
- Exercise 3.2: Sort list of tuples by second element
- Exercise 3.3: Function returning function (closure)
- Exercise 3.4: Fix mutable default bug
- Exercise 3.5: Process transactions with map/filter/reduce

### Day 5: Lambda and Sorting (1.5 hours)

**Lambda: Anonymous Functions**
```python
# Regular function
def double(x):
    return x * 2

# Lambda equivalent
double = lambda x: x * 2

# Common use: inline operations
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
```

**Lambda with Sorting (Most Interview-Relevant)**
```python
# Sort list of tuples by second element
data = [('Alice', 85), ('Bob', 92), ('Charlie', 78)]
sorted_by_score = sorted(data, key=lambda x: x[1], reverse=True)

# Sort list of dicts
employees = [
    {'name': 'Alice', 'salary': 50000},
    {'name': 'Bob', 'salary': 75000}
]
by_salary = sorted(employees, key=lambda e: e['salary'], reverse=True)

# Multiple sort keys: score desc, then name asc
sorted_complex = sorted(data, key=lambda x: (-x[1], x[0]))
```

**Interview connection:** Lambda sorting → DataFrame sort_values(). Same logic, cleaner pandas syntax.

**Practice:**
- Exercise: Sort products by price desc, name asc
- Exercise: Get top 3 highest salaries using sorted + lambda

### Day 6: String Operations (1 hour)

**Basic String Methods**
```python
text = "  Hello, World!  "
text.lower()                 # "  hello, world!  "
text.strip()                 # "Hello, World!"
text.replace("World", "Python")
"Hello" in text              # True
text.split()                 # ['Hello,', 'World!']
```

**String Formatting**
```python
name = "Alice"
age = 30
f"Name: {name}, Age: {age}"        # "Name: Alice, Age: 30"

value = 1234567.89
f"{value:,.2f}"                    # "1,234,567.89"
```

**Data Cleaning Example**
```python
# Clean email
email = "  Alice@Example.COM  "
clean = email.strip().lower()  # "alice@example.com"

# Validate
is_valid = '@' in clean and '.' in clean.split('@')[1]
```

**Interview connection:** String cleaning → pandas str accessor. Same operations, vectorized in pandas.

**Practice:**
- Exercise: Clean phone numbers to XXX-XXX-XXXX format
- Exercise: Parse log entries extracting ERROR messages

### Day 7: Review and Integration (0.5 hours)

**Putting It All Together**

Scenario: Calculate summary statistics by category from transaction data (list of dicts).

```python
transactions = [
    {'category': 'Food', 'amount': 45.50},
    {'category': 'Transport', 'amount': 12.00},
    {'category': 'Food', 'amount': 38.75}
]

def summarize_transactions(transactions):
    # Group by category (manual groupby)
    grouped = {}
    for t in transactions:
        cat = t['category']
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(t['amount'])
    
    # Calculate summary stats
    summary = {
        cat: {
            'total': sum(amounts),
            'average': sum(amounts) / len(amounts),
            'count': len(amounts)
        }
        for cat, amounts in grouped.items()
    }
    
    # Sort by total descending
    return dict(sorted(summary.items(), 
                      key=lambda x: x[1]['total'], 
                      reverse=True))
```

**What this demonstrates:**
- Data structures (dicts, lists)
- Comprehensions (dict comprehension for summary)
- Functions (clear input/output)
- Lambda (sorting by nested value)

**Practice Problems:**
1. Which data structure for each scenario?
2. Write comprehensions with filter + transform
3. Function that returns highest-paid employee
4. Sort products by price, filter under $100
5. Clean and validate emails

**Week 1 Complete Checklist:**
- [ ] Know when to use list vs dict vs set
- [ ] Write list and dict comprehensions
- [ ] Define functions with default parameters
- [ ] Avoid mutable default gotcha
- [ ] Use lambda for custom sorting
- [ ] Clean and validate strings
- [ ] Combine concepts in integration problems

**Connection to Week 2:**

Week 1 concepts → Week 2 patterns:
- Lists → DataFrames (rows and columns)
- Dicts → DataFrame rows as dicts  
- Comprehensions → Boolean indexing
- Lambda sorting → DataFrame.sort_values()
- String operations → str accessor methods

Next week, these fundamentals become pandas patterns.

## Week 2: Pandas Basics (5 hours)

### Day 1: DataFrames & Series (1 hour)
- Creating DataFrames
- Selecting columns/rows
- Basic indexing
- Practice: Load and explore datasets

### Day 2: Filtering & Sorting (1 hour)
- Boolean indexing
- Query method
- sort_values, sort_index
- Practice: Customer segmentation

### Day 3: Missing Data (1 hour)
- isna, fillna, dropna
- Forward fill, backward fill
- Practice: Clean messy datasets

### Day 4: Groupby Basics (1 hour)
- Simple aggregations
- Multiple aggregations
- Named aggregations
- Practice: Sales analysis

### Day 5: Review & Mini-Project (1 hour)
- Combine filtering, grouping, aggregation
- Build a sales report
- Performance comparison

## Week 3: Advanced Pandas (5 hours)

### Day 1: Joins & Merges (1 hour)
- merge vs join
- Inner, outer, left, right joins
- Handling duplicates
- Practice: Customer-order analysis

### Day 2: Window Functions (1 hour)
- rolling, expanding
- shift, diff
- Practice: Time series analysis

### Day 3: Apply & Custom Functions (1 hour)
- apply, map, applymap
- When to use each
- Vectorization vs apply
- Practice: Custom transformations

### Day 4: MultiIndex & Pivot (1 hour)
- set_index, reset_index
- pivot_table, melt
- Practice: Reshaping data

### Day 5: Review & Mini-Project (1 hour)
- Complex data transformation pipeline
- Join multiple datasets
- Pivot and aggregate

## Week 4: Data Manipulation Patterns (5 hours)

### Day 1: Top N by Group (1 hour)
- sort_values + groupby + head
- rank within groups
- Practice: Top products per category

### Day 2: Deduplication (1 hour)
- drop_duplicates strategies
- Keep first vs last vs custom
- Practice: Customer deduplication

### Day 3: Date/Time Operations (1 hour)
- pd.to_datetime
- dt accessor
- Date arithmetic
- Practice: Event timeline analysis

### Day 4: String Operations (1 hour)
- str accessor
- Extract, replace, split
- Practice: Parse product codes

### Day 5: Review & Mini-Project (1 hour)
- E-commerce data analysis
- Combine all week's patterns
- Optimize for performance

## Week 5: SQL for Analysts (5 hours)

### Day 1: SELECT & WHERE (1 hour)
- Basic queries
- Filtering conditions
- LIKE, IN, BETWEEN
- Practice: Query exercise datasets

### Day 2: JOINs (1 hour)
- INNER, LEFT, RIGHT, FULL
- Multiple joins
- Self joins
- Practice: Multi-table queries

### Day 3: Aggregations (1 hour)
- GROUP BY
- HAVING
- COUNT, SUM, AVG, MIN, MAX
- Practice: Summary statistics

### Day 4: Window Functions (1 hour)
- ROW_NUMBER, RANK, DENSE_RANK
- PARTITION BY
- Running totals
- Practice: Ranking queries

### Day 5: Review & Mini-Project (1 hour)
- Complex analytical queries
- Subqueries and CTEs
- Query optimization

## Week 6: Integration & Workflows (5 hours)

### Day 1: Pandas ↔ SQL (1 hour)
- read_sql, to_sql
- Query construction
- Practice: Database operations

### Day 2: Data Validation (1 hour)
- Schema validation
- Data quality checks
- Assert statements
- Practice: Build validators

### Day 3: ETL Patterns (1 hour)
- Extract, Transform, Load
- Incremental updates
- Practice: Simple ETL pipeline

### Day 4: Error Handling & Logging (1 hour)
- Try/except in pipelines
- Logging best practices
- Practice: Robust data processing

### Day 5: Review & Mini-Project (1 hour)
- End-to-end data pipeline
- Error handling
- Logging and monitoring

## Week 7: Performance & Testing (5 hours)

### Day 1: Performance Optimization (1 hour)
- Vectorization
- Memory optimization
- Avoid iteration
- Practice: Speed up slow code

### Day 2: Profiling (1 hour)
- timeit, cProfile
- Memory profilers
- Practice: Identify bottlenecks

### Day 3: Unit Testing (1 hour)
- pytest basics
- Test data transformations
- Practice: Write test suite

### Day 4: Code Organization (1 hour)
- Functions vs classes
- Module structure
- Practice: Refactor messy code

### Day 5: Review & Mini-Project (1 hour)
- Optimize and test pipeline
- Performance benchmarks
- Code review

## Week 8: Interview Preparation (10 hours)

### Day 1-2: Pattern Practice (4 hours)
- Top N by group variations
- Join scenarios
- Aggregation challenges
- Deduplication edge cases

### Day 3-4: SQL Practice (3 hours)
- Complex joins
- Window function problems
- Subquery exercises

### Day 5-7: Mock Interviews (3 hours)
- Timed coding challenges
- Explain your approach
- Code review feedback
- Performance optimization

## Daily Study Routine

**Recommended Schedule:**
- 30 min: Review previous day
- 30 min: New concept learning
- 30 min: Coding practice
- 30 min: Pattern recognition

**Total:** 1 hour/day weekdays, catch-up on weekends

## Practice Datasets

All available in `platform/content/data/`:
- customers.csv
- orders.csv
- products.csv
- sales_transactions.csv
- web_logs.csv

## Assessment Milestones

**Week 2:** Basic pandas proficiency test
**Week 4:** Pattern recognition quiz
**Week 6:** ETL pipeline project
**Week 8:** Mock interview performance

## Success Metrics

By end of course, you should:
- Write efficient pandas code for common patterns
- Translate business questions to SQL
- Optimize slow data operations
- Handle edge cases gracefully
- Explain your code clearly

## Resources

- Platform exercises: `platform/content/src/`
- Pattern library: `platform/content/patterns/`
- Quick reference: `platform/content/docs/quick_reference.md`
- Interview tips: `platform/content/docs/talking_points.md`
