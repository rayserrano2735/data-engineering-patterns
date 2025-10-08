# Python Analytics Interview Prep - Complete Textbook
**Version: 1.0.5-RC4

## Table of Contents

- [Course Structure](#course-structure)
- [Week 1: Python Fundamentals](#week-1-python-fundamentals---foundation-for-pattern-learning)
  - [Day 1-2: Data Structures](#day-1-2-data-structures-2-hours)
  - [Day 3: Comprehensions](#day-3-comprehensions-15-hours)
  - [Day 4: Functions and Parameters](#day-4-functions-and-parameters-15-hours)
  - [Day 5: Lambda and Sorting](#day-5-lambda-and-sorting-15-hours)
  - [Day 6: String Operations](#day-6-string-operations-1-hour)
  - [Day 7: Review and Integration](#day-7-review-and-integration-05-hours)
- [Week 2: DataFrame Basics + First Pattern Versions](#week-2-dataframe-basics--first-pattern-versions)
  - [Day 1: Modern Python Patterns](#day-1-modern-python-patterns-1-hour)
- [Week 3: Aggregation + Pattern Expansion](#week-3-aggregation--pattern-expansion)
- [Week 4: Ranking/Windows + Advanced Patterns](#week-4-rankingwindows--advanced-patterns)
- [Week 5: Advanced Operations + Specialized Patterns](#week-5-advanced-operations--specialized-patterns)
- [Week 6: Integration Patterns](#week-6-integration-patterns)
- [Week 7: Meta-Patterns + Performance](#week-7-meta-patterns--performance)

---

## Course Structure

This textbook contains detailed content for all 7 weeks of the Python Analytics Interview Prep course. Each week builds on the previous, following a pattern-based learning approach.

**Week 1:** Python Fundamentals (Foundation - 0 patterns)
**Week 2:** DataFrame Basics + First Pattern Versions (6 patterns introduced)
**Week 3:** Aggregation + Pattern Expansion (1 new + 6 expanded patterns)
**Week 4:** Ranking/Windows + Advanced Patterns (5 new + 7 expanded patterns)
**Week 5:** Advanced Operations + Specialized Patterns (3 new + 5 expanded patterns)
**Week 6:** Integration Patterns (2 new patterns)
**Week 7:** Meta-Patterns + Performance (3 new patterns)

---

## Week 1: Python Fundamentals - Foundation for Pattern Learning

**Week 1 Mission:** Build Python fundamentals that enable pattern-based learning starting Week 2. No pandas patterns yet - just the building blocks patterns are made from.

**Learning Objectives:**
- Master core data structures (lists, dicts, sets)
- Write comprehensions for filtering and transformation  
- Define and use functions with parameters and return values
- Use lambda expressions for sorting and filtering
- Perform basic string operations

**Time Allocation:** 7 hours total
- Day 1-2: Data Structures (2 hours)
- Day 3: Comprehensions (1.5 hours)
- Day 4: Functions and Parameters (1.5 hours)
- Day 5: Lambda and Sorting (1.5 hours)
- Day 6: String Operations (1 hour)
- Day 7: Review and Integration (0.5 hours)

---

### Day 1-2: Data Structures (2 hours)

#### Python Built-in Types and Functions

Python includes many types and functions that are always available without importing:

**Built-in Types:**
- `int`, `str`, `list`, `dict`, `set`, `tuple`, `bool`

**Built-in Functions:**
- `print()`, `len()`, `range()`, `enumerate()`, `zip()`, `sorted()`, `sum()`, `max()`, `min()`

**Example - No Import Needed:**
```python
numbers = [1, 2, 3]  # list is built-in
my_dict = {}         # dict is built-in  
print(len(numbers))  # print() and len() are built-in
```

**When Imports ARE Needed:**
```python
import pandas as pd   # pandas not built-in
import string         # string module not built-in
```

#### Lists: Ordered Collections

**Important:** "Ordered" means maintains insertion position, NOT sorted by value.
```python
[3, 1, 2]  # Ordered (preserves position) but not sorted
[1, 2, 3]  # Both ordered AND sorted
```

**Creating and Accessing:**
```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
names = ['Alice', 'Bob', 'Charlie']
mixed = [1, 'hello', 3.14, True]

# Accessing elements
first = numbers[0]        # 1
last = numbers[-1]        # 5
middle = numbers[1:4]     # [2, 3, 4]
```

**Common Operations:**
```python
# Adding elements
numbers.append(6)         # Add to end
numbers.insert(0, 0)      # Add at position
numbers.extend([7, 8])    # Add multiple

# Removing elements
numbers.remove(3)         # Remove first occurrence of value
popped = numbers.pop()    # Remove and return last item
popped = numbers.pop(0)   # Remove and return item at index

# Other operations
len(numbers)              # Length
3 in numbers              # Membership test
numbers.count(2)          # Count occurrences
numbers.index(4)          # Find index of value
```

**When to use lists:**
- Ordered data where position matters
- Duplicates are allowed
- Need to access by index
- Iterating in sequence

**Interview connection:** Lists often represent tables when you have a list of lists (each inner list = row) or a list of dicts (each dict = row). Understanding list operations now makes pandas intuitive later.

---

#### Dictionaries: Key-Value Mappings

**Creating and Accessing:**
```python
# Creating dictionaries
person = {'name': 'Alice', 'age': 30, 'dept': 'Analytics'}

# Accessing values
name = person['name']              # Direct access (KeyError if missing)
salary = person.get('salary', 0)   # Safe access with default

# Checking existence
'salary' in person                 # False
```

**Modifying Dictionaries:**
```python
# Adding/updating
person['age'] = 31
person['salary'] = 75000

# Removing
del person['age']
salary = person.pop('salary', 0)   # Remove and return with default

# Merging (Python 3.9+)
defaults = {'status': 'active', 'level': 1}
person = defaults | person         # Merge, person values override
```

**Iterating Over Dictionaries:**
```python
# Keys only
for key in person:
    print(key)

# Keys explicitly
for key in person.keys():
    print(key)

# Values only
for value in person.values():
    print(value)

# Keys and values
for key, value in person.items():
    print(f"{key}: {value}")
```

**When to use dictionaries:**
- Look up by key (not position)
- Structured data with named fields
- Counting/aggregating (key = category, value = count)
- Fast membership testing (key existence)

**Interview connection:** In Analytics Engineering, data often arrives as a list of dicts (JSON from APIs). Mental model: List = Table, Dict = Row. Each transaction/record is a dict with key-value pairs that become column names and values. Understanding dict operations prepares you for groupby logic.

---

#### Sets: Unique Collections

**Creating and Operations:**
```python
# Creating sets
unique_ids = {1, 2, 3, 4, 5}
colors = set(['red', 'blue', 'green', 'blue'])  # Duplicates removed

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b          # Union: {1, 2, 3, 4, 5, 6} - all elements from both
a & b          # Intersection: {3, 4} - only elements in both
a - b          # Difference: {1, 2} - in a, NOT in b
a ^ b          # Symmetric difference: {1, 2, 5, 6}
               # Elements in EITHER but NOT BOTH

# Visual examples:
# a = {1, 2, 3, 4}, b = {3, 4, 5, 6}
#
# a - b: Remove b's elements from a
#   {1, 2, 3, 4} - {3, 4, 5, 6} = {1, 2}
#   (3,4 removed because they're in b; 5,6 ignored because not in a)
#
# a ^ b: Elements appearing in only ONE set (XOR logic)
#   {1, 2, 3, 4} ^ {3, 4, 5, 6} = {1, 2, 5, 6}
#   (3,4 removed because in BOTH; 
#    1,2,5,6 kept because in only one)
#
# Use cases:
# a - b: "What's unique to a?" (e.g., customers who bought A but not B)
# a ^ b: "What's different between sets?" (e.g., either added OR removed, not both)

# SQL equivalents:
# a - b (set difference)
customers_a = {1, 2, 3, 4}
customers_b = {3, 4, 5, 6}
only_a = customers_a - customers_b  # {1, 2}
# SQL: SELECT customer_id FROM tab_a EXCEPT SELECT customer_id FROM tab_b

# a ^ b (symmetric difference)  
changed = customers_a ^ customers_b  # {1, 2, 5, 6}
# SQL: (SELECT customer_id FROM tab_a EXCEPT SELECT customer_id FROM tab_b)
#      UNION
#      (SELECT customer_id FROM tab_b EXCEPT SELECT customer_id FROM tab_a)

# Membership
3 in a         # True (very fast - O(1))

# Modifying
a.add(5)
a.remove(1)    # KeyError if not present
a.discard(1)   # No error if not present
```

**When to use sets:**
- Unique values only
- Fast membership testing
- Set operations (union, intersection, difference)
- Removing duplicates from list: `list(set(items))`

**Common Interview Gotcha - Empty Set:**
```python
empty_dict = {}      # Creates empty DICT, not set!
empty_set = set()    # Correct way to create empty set

# Why? Dict came first in Python, gets precedence for {}
type({})             # <class 'dict'>
type(set())          # <class 'set'>

# Non-empty is clear:
my_set = {1, 2, 3}   # Set (values only)
my_dict = {'a': 1}   # Dict (key-value pairs)
```

**Interview connection:** Sets used for deduplication, finding unique values, checking membership. Understanding sets now prepares you for pandas unique() and duplicated() methods. The `{}` edge case is a classic gotcha question testing Python fundamentals.

---

#### Essential Built-in Functions

Before working with examples, understand these fundamental Python functions:

**range() - Generate Number Sequences:**
```python
range(5)           # 0, 1, 2, 3, 4 (start at 0, end before 5)
range(1, 6)        # 1, 2, 3, 4, 5 (start at 1, end before 6)
range(0, 10, 2)    # 0, 2, 4, 6, 8 (start at 0, step by 2)
range(10, 0, -1)   # 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 (countdown)

# Note: range() returns a range object, not a list
# Use list() to convert to actual list
```

**list() - Convert to List:**
```python
list(range(5))          # [0, 1, 2, 3, 4]
list("hello")           # ['h', 'e', 'l', 'l', 'o']
list({1, 2, 3})         # [1, 2, 3] from set
list({'a': 1, 'b': 2})  # ['a', 'b'] keys only
```

**Other Common Built-ins:**
```python
len([1, 2, 3])      # 3 (length)
sum([1, 2, 3])      # 6 (sum of numbers)
min([3, 1, 2])      # 1 (minimum value)
max([3, 1, 2])      # 3 (maximum value)
sorted([3, 1, 2])   # [1, 2, 3] (sorted copy)
```

**dict.fromkeys() - Create Dict from Sequence:**
```python
# Remove duplicates while preserving order (Python 3.7+)
data = [1, 2, 2, 3, 3, 3, 4]
unique_dict = dict.fromkeys(data)  # {1: None, 2: None, 3: None, 4: None}
unique_list = list(dict.fromkeys(data))  # [1, 2, 3, 4]

# With default values
keys = ['a', 'b', 'c']
initialized = dict.fromkeys(keys, 0)  # {'a': 0, 'b': 0, 'c': 0}
```

**Why fromkeys preserves order:** Python 3.7+ dictionaries maintain insertion order. fromkeys adds each unique key in sequence order, automatically removing duplicates.

**zip() - Create Dict from Keys and Values:**
```python
# Pairing separate key and value lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
paired_dict = dict(zip(keys, values))  # {'a': 1, 'b': 2, 'c': 3}

# Comparison:
dict.fromkeys(keys)           # {'a': None, 'b': None, 'c': None} - keys only
dict(zip(keys, values))       # {'a': 1, 'b': 2, 'c': 3} - keys paired with values
```

**Functions vs Methods:**
- `zip()` is a **function** - standalone, called as `zip(keys, values)`
- `dict.fromkeys()` is a **method** - attached to dict object, called as `dict.fromkeys(keys)`
- Functions: `zip()`, `len()`, `sorted()`, `print()`
- Methods: `list.append()`, `dict.fromkeys()`, `str.upper()`

**Understanding Evaluation Order:**

Python evaluates code inside-out, like math:
```python
list(range(5))
# Step 1: range(5) creates sequence 0,1,2,3,4
# Step 2: list() converts to [0, 1, 2, 3, 4]

sum([x*2 for x in range(3)])
# Step 1: range(3) → 0,1,2
# Step 2: [x*2 for x in ...] → [0,2,4]
# Step 3: sum(...) → 6
```

**List Comprehension Basics:**

You'll see square brackets with `for` inside in the examples below. This is called a list comprehension - a compact way to build lists.

Basic pattern: `[expression for item in sequence]`

Execution order (inside-out):
1. Loop through sequence: `for item in sequence`
2. Apply expression: `expression` to each item
3. Collect results into new list

Example:
```python
[n for n in numbers if n % 2 == 0]
# Execution: Loop through numbers → Check if even → Collect evens into list
# Syntax looks backwards but executes left-to-right
```

You'll learn full comprehension details in Day 3. For now, just recognize the pattern: "build a list by looping through something and optionally filtering items."

---

#### Practice Examples: Data Structures

**Example 1.1: Filter odds**
Create a list of numbers 1-10 and return only even numbers.
```python
numbers = list(range(1, 11))
evens = [n for n in numbers if n % 2 == 0]
# Result: [2, 4, 6, 8, 10]
```

**Example 1.2: Remove duplicates preserving order**
Given `[1, 2, 2, 3, 3, 3, 4]`, remove duplicates while preserving order.
```python
data = [1, 2, 2, 3, 3, 3, 4]
unique = list(dict.fromkeys(data))  # Python 3.7+ preserves order
# Result: [1, 2, 3, 4]
```

**Example 1.3: Merge dicts keeping higher values**
```python
dict1 = {'a': 10, 'b': 20, 'c': 30}
dict2 = {'b': 25, 'c': 15, 'd': 40}

# Copy dict1 to preserve original for validation
merged = dict1.copy()
for key, value in dict2.items():
    if key not in merged or value > merged[key]:
        merged[key] = value

# Result: {'a': 10, 'b': 25, 'c': 30, 'd': 40}

# Validation: Verify higher values were kept
assert merged['b'] == 25  # 25 > 20, kept higher value
assert merged['c'] == 30  # 30 > 15, kept higher value
assert merged['d'] == 40  # New key added
print(f"Original dict1: {dict1}")  # Still intact
print(f"Merged result: {merged}")
```

**Example 1.4: Debug - modifying list during iteration**
```python
# WRONG: Modifying list while iterating causes skipped elements
def remove_duplicates_broken(items):
    for i, item in enumerate(items):
        if items.count(item) > 1:
            items.remove(item)  # BAD!
    return items

# RIGHT: Build new list
def remove_duplicates_fixed(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```

**Example 1.5: Word frequency counter**
Count word frequency in a sentence using dictionary.
```python
sentence = "The quick brown fox jumps over the lazy dog. The fox is quick!"

# Solution
import string
cleaned = sentence.lower().translate(str.maketrans('', '', string.punctuation))
words = cleaned.split()

frequency = {}
for word in words:
    frequency[word] = frequency.get(word, 0) + 1

# Sort by frequency descending
sorted_freq = dict(sorted(frequency.items(), 
                         key=lambda x: x[1], 
                         reverse=True))
```

---

**Learning Activities:**

After completing Day 1-2 content, practice with these activities:

1. **Exercises:** Complete Exercises 1.1-1.5 in `week1_exercises.py`
   - Test your solutions: `python test_week1_exercises.py`
   - Check reference solutions in `week1_solutions.py` if stuck

2. **Flashcards:** Review `day1-2_flashcards.txt`
   - Focus on list, dict, and set operations
   - Practice until you can recall syntax from memory

3. **Interview Mode:** Practice with `INTERVIEW_MODE_WEEK1.md`
   - Focus areas: Dictionary operations, list manipulation, set usage
   - Practice explaining your code choices aloud
   - 30-45 minutes of interactive scenarios

---

### Day 3: Comprehensions (1.5 hours)

#### List Comprehensions: Filter and Transform

**Basic Syntax:**
```python
# Pattern: [expression for item in sequence if condition]

# Without comprehension (verbose)
evens = []
for n in range(10):
    if n % 2 == 0:
        evens.append(n)

# With comprehension (Pythonic)
evens = [n for n in range(10) if n % 2 == 0]
```

**Why This Confuses People:**

The syntax order doesn't match execution order:

```python
[n for n in numbers if n % 2 == 0]
#↑     ↑              ↑
#3rd   1st            2nd
```

**Execution order:** Loop → Filter → Collect
1. `for n in numbers` - iterate through numbers
2. `if n % 2 == 0` - check condition
3. `n` - collect result

**Syntax order:** Collect → Loop → Filter
1. `n` - what to collect (written first)
2. `for n in numbers` - loop source
3. `if n % 2 == 0` - filter condition

**SQL Mapping (matches execution order):**
```sql
SELECT n              -- what to collect (3rd)
FROM numbers          -- loop source (1st)
WHERE n % 2 = 0       -- filter (2nd)
```

**Design Rationale:** Python mimics mathematical set-builder notation: {x² | x ∈ numbers, x even}

**Design Evaluation:** Questionable choice for a procedural language. Math notation optimization conflicts with how programmers think about loops and filters. Creates cognitive load for SQL/procedural programmers.

**Interview Strategy:** Explain both syntax AND execution order. Show you understand the distinction. This backwards pattern is a common gatekeeping question.

**Different Bracket Types:**

Comprehension is the pattern; brackets determine collection type:
```python
# List comprehension
[x for x in range(5)]    # [0, 1, 2, 3, 4]

# Generator expression (lazy evaluation)
(x for x in range(5))    # generator object

# Set comprehension
{x for x in range(5)}    # {0, 1, 2, 3, 4}

# Dict comprehension
{x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```


**Common Patterns:**
```python
# Transform only
doubled = [x * 2 for x in numbers]

# Filter only
positives = [x for x in numbers if x > 0]

# Transform and filter
positive_squares = [x**2 for x in numbers if x > 0]

# Nested comprehension (flatten)
nested = [[1, 2], [3, 4], [5, 6]]
flat = [item for sublist in nested for item in sublist]
# Result: [1, 2, 3, 4, 5, 6]
```

**Interview Use Case:**
```python
# Extract specific data from list of dicts
transactions = [
    {'id': 1, 'amount': 100, 'status': 'completed'},
    {'id': 2, 'amount': 50, 'status': 'pending'},
    {'id': 3, 'amount': 200, 'status': 'completed'}
]

# Get amounts of completed transactions
completed_amounts = [t['amount'] for t in transactions 
                     if t['status'] == 'completed']
# Result: [100, 200]
```

**Interview connection:** Comprehensions are the Python equivalent of DataFrame filtering. The logic `[x for x in items if condition]` becomes `df[df['col'] > value]` in pandas.

---

#### Dict Comprehensions

**Syntax:**
```python
# Pattern: {key_expr: value_expr for item in sequence if condition}

# Create dict from lists
names = ['Alice', 'Bob', 'Charlie']
name_lengths = {name: len(name) for name in names}
# Result: {'Alice': 5, 'Bob': 3, 'Charlie': 7}

# Transform existing dict
prices = {'apple': 1.50, 'banana': 0.75, 'orange': 2.00}
discounted = {item: price * 0.9 for item, price in prices.items()}

# Filter dict
expensive = {item: price for item, price in prices.items() if price > 1.00}
```

---

#### Set Comprehensions

**Syntax:**
```python
# Pattern: {expression for item in sequence if condition}

# Get unique lengths
words = ['apple', 'banana', 'cherry', 'date']
unique_lengths = {len(word) for word in words}
# Result: {4, 5, 6}
```

---

#### Practice Examples: Comprehensions

**Example 2.1: Squares of positive numbers**
```python
numbers = [-2, -1, 0, 1, 2, 3]
squares = [x**2 for x in numbers if x > 0]
# Result: [1, 4, 9]
```

**Example 2.2: Name to length dictionary**
```python
names = ["Alice", "Bob", "Charlie", "Dave", "Eve"]
name_lengths = {name: len(name) for name in names}
# Result: {'Alice': 5, 'Bob': 3, 'Charlie': 7, 'Dave': 4, 'Eve': 3}
```

**Example 2.3: Flatten nested lists**
```python
nested = [1, [2, 3], [4, [5, 6]], 7]

def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

flat = flatten(nested)
# Result: [1, 2, 3, 4, 5, 6, 7]
```

**Example 2.4: Debug - character vs word iteration**
```python
sentence = "The quick brown fox jumps"

# WRONG: Iterates over characters, not words
wrong = [word for word in sentence if len(word) > 3]

# RIGHT: Split into words first
correct = [word for word in sentence.split() if len(word) > 3]
# Result: ['quick', 'brown', 'jumps']
```

**Example 2.5: Clean and validate emails**
```python
emails = [
    "  Alice@Example.COM  ",
    "bob@domain",
    "charlie@email.co.uk",
    "not.an.email"
]

def validate_email(email):
    email = email.strip().lower()
    parts = email.split('@')
    return len(parts) == 2 and len(parts[0]) > 0 and '.' in parts[1]

cleaned = [(email.strip().lower(), validate_email(email)) 
           for email in emails]
# Result: [('alice@example.com', True), ('bob@domain', False), ...]
```

---


---

**Learning Activities:**

After completing Day 3 content, practice with these activities:

1. **Exercises:** Complete Exercises 2.1-2.5 in `week1_exercises.py`
   - Focus on list/dict comprehensions
   - Test: `python test_week1_exercises.py`

2. **Flashcards:** Review `day3_flashcards.txt`
   - List comprehension syntax and evaluation order
   - Dict/set comprehensions

3. **Interview Mode:** Practice with `INTERVIEW_MODE_WEEK1.md`
   - Focus: Comprehension patterns, filter/transform operations
   - 30-45 minutes practice

---

### Day 4: Functions and Parameters (1.5 hours)

#### Function Basics

**Defining Functions:**
```python
def calculate_total(price, quantity, tax_rate=0.08):
    """Calculate total with tax."""
    subtotal = price * quantity
    tax = subtotal * tax_rate
    return subtotal + tax

# Using the function
total = calculate_total(10.00, 3)              # Uses default tax_rate
total = calculate_total(10.00, 3, tax_rate=0.10)  # Custom tax_rate
```

**Multiple Return Values:**
```python
def get_stats(numbers):
    """Return min, max, and average."""
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

# Unpack return values
min_val, max_val, avg_val = get_stats([1, 2, 3, 4, 5])
```

**Type Hints:**
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

**Interview benefit:** Type hints show production-quality code and make your intent clear to interviewers.

---

#### Critical Gotcha: Mutable Default Arguments

**The Problem:**
```python
# WRONG: Mutable default argument
def add_item(item, items=[]):    # BAD!
    items.append(item)
    return items

# First call
list1 = add_item(1)  # [1]

# Second call - SURPRISE!
list2 = add_item(2)  # [1, 2] - not [2]!

# Why: The empty list is created ONCE at function definition
# All calls share the same list object
```

**The Solution:**
```python
# RIGHT: Use None as default
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Now each call gets a fresh list
list1 = add_item(1)  # [1]
list2 = add_item(2)  # [2]
```

**Why this matters in interviews:** This is a classic Python gotcha. Knowing it shows you understand Python's object model and have written real code.

---

#### Practice Examples: Functions

**Example 3.1: Currency formatter with defaults**
```python
def format_currency(amount, symbol='$', decimals=2):
    """Format number as currency."""
    formatted = f"{amount:,.{decimals}f}"
    return f"{symbol}{formatted}"

# Tests
assert format_currency(1234567.89) == "$1,234,567.89"
assert format_currency(1234567.89, symbol='€') == "€1,234,567.89"
assert format_currency(1234567.89, decimals=0) == "$1,234,568"
```

**Example 3.2: Sort with lambda**
```python
# Sort by score descending, then name ascending
data = [
    ('Alice', 85),
    ('Bob', 92),
    ('Charlie', 78),
    ('Dave', 92)
]

sorted_data = sorted(data, key=lambda x: (-x[1], x[0]))
# Result: [('Bob', 92), ('Dave', 92), ('Alice', 85), ('Charlie', 78)]
```

**Example 3.3: Function returning function (closure)**
```python
def create_filter(min_value=None, max_value=None, exclude_values=None):
    """Create a filter function with configured criteria."""
    exclude_set = set(exclude_values) if exclude_values else set()
    
    def filter_func(value):
        if value in exclude_set:
            return False
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True
    
    return filter_func

# Usage
my_filter = create_filter(min_value=10, max_value=100, exclude_values=[50])
data = [5, 10, 25, 50, 75, 100, 150]
filtered = list(filter(my_filter, data))
# Result: [10, 25, 75, 100]
```

**Example 3.4: Fix mutable default bug**
```python
# BROKEN
def append_to_list_broken(item, target_list=[]):
    target_list.append(item)
    return target_list

# FIXED
def append_to_list_fixed(item, target_list=None):
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list
```

**Example 3.5: Map, filter, reduce**
```python
from functools import reduce

transactions = [
    {'id': 1, 'amount': 100, 'status': 'completed'},
    {'id': 2, 'amount': -50, 'status': 'completed'},
    {'id': 3, 'amount': 200, 'status': 'pending'},
    {'id': 4, 'amount': 150, 'status': 'completed'}
]

# Filter valid transactions
valid = list(filter(
    lambda t: t['amount'] > 0 and t['status'] == 'completed',
    transactions
))

# Extract amounts
amounts = list(map(lambda t: t['amount'], valid))

# Calculate total
total = reduce(lambda x, y: x + y, amounts, 0)
# Result: 250
```

---


---

**Learning Activities:**

1. **Exercises:** Complete Exercises 3.1-3.5 in `week1_exercises.py`
   - Practice function parameters and return values
   - Test: `python test_week1_exercises.py`

2. **Flashcards:** Review `day4_flashcards.txt`
   - Function definition and calling syntax
   - Parameters, defaults, return values

3. **Interview Mode:** Practice with `INTERVIEW_MODE_WEEK1.md`
   - Focus: Writing functions, parameter handling
   - 30-45 minutes practice

---

### Day 5: Lambda and Sorting (1.5 hours)

#### Lambda Functions

**Basic Syntax:**
```python
# Regular function
def double(x):
    return x * 2

# Lambda equivalent
double = lambda x: x * 2

# Most common use: inline with map, filter, sorted
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
```

**When to use lambda vs def:**
- **Lambda:** One-line operations, sorting keys, callbacks
- **def:** Everything else (multiple lines, complex logic, docstrings)

---

#### Lambda with Sorting (Most Interview-Relevant)

**Sorting Lists of Tuples:**
```python
# Sort by second element (score)
data = [('Alice', 85), ('Bob', 92), ('Charlie', 78)]
sorted_by_score = sorted(data, key=lambda x: x[1], reverse=True)
# Result: [('Bob', 92), ('Alice', 85), ('Charlie', 78)]
```

**Sorting Lists of Dicts:**
```python
employees = [
    {'name': 'Alice', 'salary': 50000},
    {'name': 'Bob', 'salary': 75000},
    {'name': 'Charlie', 'salary': 55000}
]

# Sort by salary descending
by_salary = sorted(employees, key=lambda e: e['salary'], reverse=True)
```

**Multiple Sort Keys:**
```python
# Sort by score descending, then name ascending (for ties)
data = [
    ('Alice', 85),
    ('Bob', 92),
    ('Charlie', 78),
    ('Dave', 92)
]

# Trick: Use negative for descending, positive for ascending
sorted_complex = sorted(data, key=lambda x: (-x[1], x[0]))
# Result: [('Bob', 92), ('Dave', 92), ('Alice', 85), ('Charlie', 78)]
```

**Interview connection:** Lambda sorting prepares you for DataFrame.sort_values(). Same logic:
- `sorted(items, key=lambda x: x['field'])` → `df.sort_values('field')`
- `sorted(items, key=lambda x: -x['field'])` → `df.sort_values('field', ascending=False)`

---

#### Practice Examples: Lambda and Sorting

**Exercise: Sort products by price desc, name asc**
```python
products = [
    {'name': 'Laptop', 'price': 999},
    {'name': 'Mouse', 'price': 25},
    {'name': 'Keyboard', 'price': 75},
    {'name': 'Monitor', 'price': 299}
]

sorted_products = sorted(
    products, 
    key=lambda p: (-p['price'], p['name'])
)
# Result: Laptop(999), Monitor(299), Keyboard(75), Mouse(25)
```

**Exercise: Get top 3 highest salaries**
```python
employees = [
    {'name': 'Alice', 'salary': 50000},
    {'name': 'Bob', 'salary': 75000},
    {'name': 'Charlie', 'salary': 55000},
    {'name': 'Dave', 'salary': 80000},
    {'name': 'Eve', 'salary': 45000}
]

top_3 = sorted(
    employees, 
    key=lambda e: e['salary'], 
    reverse=True
)[:3]
# Result: Dave(80000), Bob(75000), Charlie(55000)
```

---


---

**Learning Activities:**

1. **Exercises:** Complete Exercises 4.1-4.5 in `week1_exercises.py`
   - Focus on lambda and sorting patterns
   - Test: `python test_week1_exercises.py`

2. **Flashcards:** Review `day5_flashcards.txt`
   - Lambda syntax and use cases
   - sorted(), sort(), key parameters

3. **Interview Mode:** Practice with `INTERVIEW_MODE_WEEK1.md`
   - Focus: Lambda expressions, custom sorting
   - 30-45 minutes practice

---

### Day 6: String Operations (1 hour)

#### Basic String Methods

**Cleaning and Case:**
```python
text = "  Hello, World!  "

# Case conversion
text.lower()                 # "  hello, world!  "
text.upper()                 # "  HELLO, WORLD!  "
text.title()                 # "  Hello, World!  "

# Whitespace removal
text.strip()                 # "Hello, World!"
text.lstrip()                # "Hello, World!  "
text.rstrip()                # "  Hello, World!"

# Replacement
text.replace("World", "Python")  # "  Hello, Python!  "
```

**Searching and Testing:**
```python
# Membership
"Hello" in text              # True
text.startswith("  Hello")   # True
text.endswith("!")           # True

# Finding
text.find("World")           # 9 (index) or -1 if not found
text.index("World")          # 9 (raises ValueError if not found)
```

**Splitting and Joining:**
```python
# Split
words = "apple,banana,cherry".split(',')
# Result: ['apple', 'banana', 'cherry']

# Join
joined = ','.join(['apple', 'banana', 'cherry'])
# Result: "apple,banana,cherry"
```

---

#### String Formatting

**f-strings (Python 3.6+):**
```python
name = "Alice"
age = 30

# Basic
f"Name: {name}, Age: {age}"  # "Name: Alice, Age: 30"

# With formatting
value = 1234567.89
f"{value:,.2f}"              # "1,234,567.89"
f"{value:>15,.2f}"           # "   1,234,567.89" (right-aligned, width 15)

# Expressions
f"{2 + 2}"                   # "4"
f"{name.upper()}"            # "ALICE"
```

---

#### Data Cleaning Example

**Clean and validate email:**
```python
def clean_email(email):
    # Clean
    cleaned = email.strip().lower()
    
    # Validate
    if '@' not in cleaned:
        return None, "Missing @"
    
    username, domain = cleaned.split('@')
    
    if len(username) == 0:
        return None, "Empty username"
    
    if '.' not in domain:
        return None, "Invalid domain"
    
    return cleaned, "Valid"

# Test
result, status = clean_email("  Alice@Example.COM  ")
# Result: ("alice@example.com", "Valid")
```

**Interview connection:** String operations in Python → pandas str accessor. The logic is identical:
- `text.strip()` → `df['col'].str.strip()`
- `text.lower()` → `df['col'].str.lower()`
- `text.split('@')` → `df['col'].str.split('@')`

---

#### Practice Examples: Strings

**Exercise: Clean phone numbers to XXX-XXX-XXXX**
```python
def clean_phone(phone):
    # Remove all non-digits
    digits = ''.join(c for c in phone if c.isdigit())
    
    # Validate length
    if len(digits) != 10:
        return None
    
    # Format
    return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

# Tests
assert clean_phone("(555) 123-4567") == "555-123-4567"
assert clean_phone("555.123.4567") == "555-123-4567"
assert clean_phone("5551234567") == "555-123-4567"
assert clean_phone("123") is None
```

**Exercise: Parse log entries**
```python
log_entries = [
    "2024-01-15 ERROR: Database connection failed",
    "2024-01-15 INFO: User login successful",
    "2024-01-15 ERROR: API timeout exceeded"
]

def parse_logs(entries):
    errors = []
    for entry in entries:
        if 'ERROR' in entry:
            parts = entry.split()
            date = parts[0]
            message = ' '.join(parts[2:])
            errors.append({'date': date, 'message': message})
    return errors

errors = parse_logs(log_entries)
# Result: [
#   {'date': '2024-01-15', 'message': 'Database connection failed'},
#   {'date': '2024-01-15', 'message': 'API timeout exceeded'}
# ]
```

---

**Learning Activities:**

1. **Exercises:** Complete Exercises 5.1-5.5 in `week1_exercises.py`
   - String manipulation and parsing
   - Test: `python test_week1_exercises.py`

2. **Flashcards:** Review `day6_flashcards.txt`
   - String methods (split, join, strip, replace, etc.)
   - Common string patterns

3. **Interview Mode:** Practice with `INTERVIEW_MODE_WEEK1.md`
   - Focus: String operations, text parsing
   - 30 minutes practice

---

### Day 7: Review and Integration (0.5 hours)

#### Putting It All Together

**Scenario:** Calculate summary statistics by category from transaction data (list of dicts).

This exercise combines all Week 1 concepts:
- Data structures (dicts, lists)
- Comprehensions (dict comprehension)
- Functions (clear input/output)
- Lambda (sorting by nested value)

```python
transactions = [
    {'category': 'Food', 'amount': 45.50, 'date': '2024-01-15'},
    {'category': 'Transport', 'amount': 12.00, 'date': '2024-01-15'},
    {'category': 'Food', 'amount': 38.75, 'date': '2024-01-16'},
    {'category': 'Entertainment', 'amount': 50.00, 'date': '2024-01-16'},
    {'category': 'Food', 'amount': 42.25, 'date': '2024-01-17'},
    {'category': 'Transport', 'amount': 15.00, 'date': '2024-01-17'},
]

def summarize_transactions(transactions):
    """Calculate summary statistics by category."""
    
    # Step 1: Group by category (manual groupby)
    grouped = {}
    for t in transactions:
        cat = t['category']
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(t['amount'])
    
    # Step 2: Calculate summary stats using dict comprehension
    summary = {
        cat: {
            'total': sum(amounts),
            'average': sum(amounts) / len(amounts),
            'count': len(amounts),
            'min': min(amounts),
            'max': max(amounts)
        }
        for cat, amounts in grouped.items()
    }
    
    # Step 3: Sort by total descending using lambda
    sorted_summary = dict(
        sorted(summary.items(), 
               key=lambda x: x[1]['total'], 
               reverse=True)
    )
    
    return sorted_summary

result = summarize_transactions(transactions)
# Result: {
#   'Food': {'total': 126.5, 'average': 42.17, 'count': 3, ...},
#   'Entertainment': {'total': 50.0, 'average': 50.0, 'count': 1, ...},
#   'Transport': {'total': 27.0, 'average': 13.5, 'count': 2, ...}
# }
```

**What this demonstrates:**
1. **Data structures:** Dicts for grouping, lists for amounts
2. **Comprehensions:** Dict comprehension for calculating stats
3. **Functions:** Clear function with docstring
4. **Lambda:** Custom sorting by nested dict value
5. **Integration:** Combining multiple concepts to solve real problem

**Why this matters:** This is essentially a manual implementation of pandas groupby with aggregation. Understanding this logic makes pandas groupby intuitive - you'll see it's just a cleaner syntax for the same operation.

---

#### Week 1 Complete Checklist

Before moving to Week 2, ensure you can:

**Data Structures:**
- [ ] Choose appropriate structure (list vs dict vs set) for each scenario
- [ ] Access and modify lists, dicts, sets correctly
- [ ] Avoid common gotchas (modifying while iterating)

**Comprehensions:**
- [ ] Write list comprehensions with filter and transform
- [ ] Write dict comprehensions
- [ ] Flatten nested lists
- [ ] Debug common comprehension mistakes

**Functions:**
- [ ] Define functions with default parameters
- [ ] Return multiple values and unpack them
- [ ] Avoid mutable default argument bug
- [ ] Use type hints for clarity

**Lambda and Sorting:**
- [ ] Use lambda for custom sorting
- [ ] Sort by multiple keys (mix ascending/descending)
- [ ] Sort lists of tuples and dicts

**Strings:**
- [ ] Clean and validate strings
- [ ] Use f-strings for formatting
- [ ] Split and join strings
- [ ] Parse structured text

**Integration:**
- [ ] Combine concepts to solve real problems
- [ ] Implement manual groupby and aggregation
- [ ] Write clean, readable code

---

#### Connection to Week 2

**Week 1 concepts → Week 2 patterns:**

| Week 1 Concept | Week 2 Pattern |
|----------------|----------------|
| Lists | DataFrames (rows and columns) |
| Dicts | DataFrame rows as dicts |
| List comprehensions | Boolean indexing `df[df['col'] > value]` |
| Lambda sorting | `DataFrame.sort_values('col')` |
| String operations | `df['col'].str.strip()` |
| Manual groupby | `df.groupby('category')` |

**The pattern-based approach:**
- Week 1: Build the fundamentals (data structures, functions, comprehensions)
- Week 2: Learn first simple pattern versions (filtering, top N, aggregation)
- Week 3+: Expand patterns to intermediate and advanced levels

**You're ready for Week 2 when:**
- You can solve Week 1 exercises without looking up syntax
- You understand the logic behind manual groupby
- You can explain why comprehensions are Pythonic
- You recognize when to use lambda vs def

### Interview Mode Practice

After completing Week 1 exercises, practice applying Python fundamentals through Interview Mode. This AI-powered feature simulates realistic coding scenarios where you'll apply lists, dicts, functions, and comprehensions under interview-like conditions.

**What is Interview Mode?**  
Interview Mode generates unlimited unique practice scenarios. Instead of fixed problem sets, you engage with an AI interviewer who presents realistic coding challenges, asks follow-up questions, and provides contextual feedback. See the **Interview Mode** section in LEARNING_GUIDE.md for complete framework details.

**When to Practice:**
- After completing Week 1 exercises (day 7)
- Before moving to Week 2 DataFrame content
- Anytime you need additional Python fundamentals practice

**How to Use:**
1. Open a chat with Claude
2. Reference INTERVIEW_MODE_WEEK1.md (or say "Start Interview Mode for Week 1")
3. Claude will act as technical interviewer
4. Practice 5-10 scenarios minimum
5. Continue until you feel confident applying fundamentals

**What to Expect:**
- Real-world coding scenarios (building features, debugging code, explaining concepts)
- Probing questions that test understanding, not just memorization
- Immediate feedback that teaches the "why" behind solutions
- Adaptive difficulty based on your responses
- Infinite variations - you can't memorize patterns

**Example Scenario:**
```
AI: You're building an e-commerce system. Your manager asks 
    you to write a function that finds the top 3 products 
    by revenue from an orders list.
    
    Each order is a dict with 'product' and 'revenue' keys.
    How would you approach this?

You: [Your response using Week 1 concepts]

AI: [Evaluates, asks follow-ups, provides feedback]
```

Interview Mode is optional but highly recommended. Students who practice 5-10 scenarios report stronger confidence applying Python fundamentals in Week 2 DataFrame challenges.

**Learning Activities:**

Day 7 is review and consolidation - focus on integration:

1. **Review Exercises:** Revisit any incomplete exercises from Days 1-6
   - Work through week1_exercises.py comprehensively
   - Ensure all tests pass: `python test_week1_exercises.py`

2. **Flashcards:** Review `flashcards_complete.txt`
   - Complete Week 1 review (all 74 cards)
   - Focus on areas where you struggled

3. **Interview Mode:** Mixed practice with `INTERVIEW_MODE_WEEK1.md`
   - All Week 1 topics combined
   - 60 minutes comprehensive practice

---

## Week 2: DataFrame Basics + First Pattern Versions

**Week 2 Mission:** Bridge Python fundamentals to production data engineering patterns. Introduce modern Python patterns used in orchestration frameworks, then begin DataFrame operations.

**Time Allocation:** Day 1 (1 hour) + DataFrame content (TBD)

---

### Day 1: Modern Python Patterns (1 hour)

You've mastered Python fundamentals in Week 1. Before diving into pandas and DataFrames, you need to understand two patterns that appear everywhere in production data engineering code: **decorators** and **flexible function arguments**.

These aren't just Python trivia—they're the foundation of modern orchestration frameworks (Airflow, Prefect, Dagster) and appear in every data engineering interview.

---

#### Part 1: Decorators - The @ Symbol (45 minutes)

**Why this matters:** Open any production data engineering codebase and you'll see `@` everywhere:
```python
@dag(schedule="@daily")
@task
@pytest.fixture
@dataclass
```

You need to understand what's happening, even if you don't write decorators yourself.

---

##### Functions as Objects

**Core concept:** In Python, functions are objects—you can assign them to variables and pass them as arguments.

```python
def greet():
    return "Hello!"

# Assign function to variable
my_func = greet
print(my_func())  # "Hello!"

# Pass function as argument
def call_twice(func):
    func()
    func()

call_twice(greet)  # Prints "Hello!" twice
```

**Interview connection:** This is why pandas methods can take functions as parameters: `df.apply(my_function)`.

---

##### Closures - Functions That Remember

**The pattern:**
```python
def make_multiplier(x):
    def multiplier(y):
        return x * y  # 'x' is "closed over" from outer scope
    return multiplier

times_3 = make_multiplier(3)
print(times_3(4))  # 12
print(times_3(10)) # 30

times_5 = make_multiplier(5)
print(times_5(4))  # 20
```

**What's happening:**
1. `make_multiplier(3)` sets x=3
2. Returns the inner `multiplier` function
3. That inner function "remembers" x=3 even after `make_multiplier` returns
4. `times_3(4)` uses the remembered x=3 with new y=4

**Why "closure"?** The inner function "closes over" the variable `x`, capturing it from the outer scope.

**You can see the captured value:**
```python
print(times_3.__closure__)  # Shows closure object
print(times_3.__closure__[0].cell_contents)  # Shows 3
```

**Interview connection:** Closures enable configuration in data pipelines—create a function with specific settings, use it multiple times.

---

##### The @ Syntax - Decorator Basics

**Without decorators:**
```python
def say_hello():
    return "Hello"

def add_excitement(func):
    def wrapper():
        result = func()
        return result + "!!!"
    return wrapper

# Manual decoration
say_hello = add_excitement(say_hello)
print(say_hello())  # "Hello!!!"
```

**With decorators (cleaner):**
```python
@add_excitement
def say_hello():
    return "Hello"

print(say_hello())  # "Hello!!!"
```

**The @ is syntactic sugar:** `@add_excitement` means "replace `say_hello` with `add_excitement(say_hello)`"

**Mental model:** Decorators transform functions into enhanced versions.

---

##### Real-World Example: Airflow DAGs

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(schedule="@daily", start_date=datetime(2024, 1, 1))
def data_pipeline():
    
    @task
    def extract():
        return {"data": "extracted"}
    
    @task
    def transform(data):
        return {"transformed": data}
    
    data = extract()
    result = transform(data)

# The @ decorators transform these functions into Airflow components
my_pipeline = data_pipeline()
```

**What's happening:**
- `@dag` transforms `data_pipeline()` into an Airflow DAG object
- `@task` transforms `extract()` and `transform()` into Airflow Task objects
- These now have scheduling, retries, logging, UI visibility, etc.

**Interview talking point:** "Decorators add framework capabilities without changing core logic. Airflow uses `@dag` and `@task` to transform Python functions into orchestrated pipeline components."

---

#### Part 2: Flexible Arguments - *args and **kwargs (15 minutes)

**Why this matters:** Data engineering frameworks need to accept any combination of arguments. You'll see this pattern constantly in Airflow operators, pandas functions, and API wrappers.

---

##### The Pattern

```python
def universal_wrapper(*args, **kwargs):
    print(f"Positional args: {args}")
    print(f"Keyword args: {kwargs}")

# Try different calls:
universal_wrapper(1, 2, 3)
# Positional args: (1, 2, 3)
# Keyword args: {}

universal_wrapper(name='Ray', age=30)
# Positional args: ()
# Keyword args: {'name': 'Ray', 'age': 30}

universal_wrapper(1, 2, name='Ray', city='Boston')
# Positional args: (1, 2)
# Keyword args: {'name': 'Ray', 'city': 'Boston'}
```

**SQL analogy for understanding:**
- `*args` = SELECT * (captures all positional arguments)
- `**kwargs` = WHERE clauses (captures all keyword arguments as key=value pairs)

---

##### Real-World Example: Airflow Operators

```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

# PostgresOperator uses **kwargs to accept any parameter
task = PostgresOperator(
    task_id="run_query",
    sql="SELECT * FROM table",
    postgres_conn_id="warehouse",
    autocommit=True,           # Forwarded to psycopg2
    parameters={'date': '2024-01-01'}  # Forwarded to SQL
)
```

The operator doesn't need to know every possible parameter—`**kwargs` forwards everything to the underlying library.

**Interview talking point:** "The `*args/**kwargs` pattern enables flexible APIs. Operators accept any parameter and forward them to underlying connectors."

---

#### Part 3: Orchestration Concepts (15 minutes)

**Critical distinction for interviews:**

**Orchestration** = Scheduling and coordinating tools (Airflow's role)
**Transformation** = Actual data logic (dbt's role)

**Modern stack pattern:**
```
Fivetran (extract) → dbt (transform) → Airflow (schedule)
```

---

##### Task Dependencies in Airflow

**Sequential:**
```python
extract_task >> transform_task >> load_task
```

**Parallel convergence:**
```python
[extract_salesforce, extract_stripe] >> transform_all >> load_warehouse
```

**Complex:**
```python
sync_tasks >> validate >> [load_warehouse, send_alerts]
```

**Think of `>>` as:** "This must complete before that can start"

**SQL analogy:** Task dependencies map to table dependencies in your warehouse:
- `staging.orders` must exist before `marts.customer_summary`
- Foreign key relationships define data lineage
- Airflow `>>` enforces execution order

---

##### Interview Talking Point

When asked about workflow orchestration:

"I use Airflow for orchestration only—scheduling, dependencies, error handling. All transformation logic lives in dbt where it's testable and version-controlled. Airflow handles *when* and *what order*, dbt handles *how*."

**This shows you understand modern architecture.**

---

#### Week 2 Day 1 Summary

You now recognize:
- **Decorators (@)** - Transform functions into framework components
- ***args/**kwargs** - Capture flexible arguments
- **Orchestration** - Coordinate tools, don't replace them

These patterns appear throughout data engineering:
- Airflow uses decorators and flexible arguments
- pytest uses decorators for fixtures and parametrization
- pandas uses these patterns internally

**Next:** We'll apply these concepts while learning pandas DataFrames. You'll see decorators in testing frameworks and flexible arguments in DataFrame methods.

**You're ready for DataFrame content when you can:**
- Explain what `@dag` does in Airflow
- Understand why operators use `**kwargs`
- Distinguish orchestration from transformation in interviews

---

## Week 3: Aggregation + Pattern Expansion

*Content to be added in future RC*

---

## Week 4: Ranking/Windows + Advanced Patterns

*Content to be added in future RC*

---

## Week 5: Advanced Operations + Specialized Patterns

*Content to be added in future RC*

---

## Week 6: Integration Patterns

*Content to be added in future RC*

---

## Week 7: Meta-Patterns + Performance

*Content to be added in future RC*
