# Filename: python-essentials/fundamentals_for_sql_experts.py
"""
Python Fundamentals for SQL Experts
Co-authored by Ray & Aitana (Intelligence²)
Everything you need before touching Pandas or Airflow
Run this file section by section to build muscle memory
"""

# ============================================
# LEVEL 0: THE ABSOLUTE BASICS (10 minutes)
# ============================================

# Variables (like SQL parameters)
name = "Ray"                    # String (VARCHAR)
years_experience = 20           # Integer (INT)
hourly_rate = 250.00           # Float (DECIMAL)
is_expert = True               # Boolean (BOOL)
nothing = None                 # NULL in SQL

# Print (your debugging friend)
print(f"Name: {name}, Years: {years_experience}, Rate: ${hourly_rate}")

# ============================================
# LEVEL 1: STRINGS (They LOVE testing this)
# ============================================

# String basics
full_name = "Ray Serrano"
upper_name = full_name.upper()        # UPPER() in SQL
lower_name = full_name.lower()        # LOWER() in SQL
name_length = len(full_name)          # LENGTH() in SQL

# String splitting (THE classic interview question)
parts = full_name.split()             # Splits on space by default
first_name = parts[0]                 # Arrays are 0-indexed!
last_name = parts[1] if len(parts) > 1 else ""

# String methods they test
text = "  Hello World  "
cleaned = text.strip()                # TRIM() in SQL
replaced = text.replace("World", "Python")  # REPLACE() in SQL
contains = "World" in text            # LIKE '%World%' in SQL

# F-strings (modern Python formatting)
output = f"{name} has {years_experience} years experience"

# THE NAME PARSER THEY ALWAYS ASK FOR
def parse_name(full_name):
    """Every interview has some version of this"""
    if not full_name:  # Handle NULL/empty
        return {"first": "", "last": ""}
    
    # Clean up spaces
    full_name = full_name.strip()
    
    # Split into parts
    parts = full_name.split()
    
    # Handle different cases
    if len(parts) == 0:
        return {"first": "", "last": ""}
    elif len(parts) == 1:
        return {"first": parts[0], "last": ""}
    elif len(parts) == 2:
        return {"first": parts[0], "last": parts[1]}
    else:
        # Handle middle names
        return {"first": parts[0], "last": " ".join(parts[1:])}

# Test the name parser
test_names = ["John Smith", "Cher", "Mary Jane Watson", None, ""]
for test_name in test_names:
    result = parse_name(test_name)
    print(f"{test_name:20} -> {result}")

# ============================================
# LEVEL 2: LISTS (Like SQL arrays)
# ============================================

# Creating lists
scores = [95, 87, 92, 88, 90]         # Like ARRAY in SQL
names = ["Alice", "Bob", "Charlie"]    # List of strings
mixed = [1, "two", 3.0, True]         # Python allows mixed types

# Accessing elements (0-indexed!)
first_score = scores[0]               # Gets 95
last_score = scores[-1]               # Gets 90 (negative indexes!)
middle_scores = scores[1:3]           # Gets [87, 92] (slicing)

# List operations
scores.append(93)                     # Add to end
scores.remove(87)                     # Remove specific value
scores.insert(0, 100)                 # Insert at position
popped = scores.pop()                 # Remove and return last item

# Common operations
total = sum(scores)                   # SUM() in SQL
count = len(scores)                   # COUNT() in SQL
average = sum(scores) / len(scores)   # AVG() in SQL
maximum = max(scores)                 # MAX() in SQL
minimum = min(scores)                 # MIN() in SQL

# Checking membership
has_90 = 90 in scores                 # IN clause in SQL
not_in = 75 not in scores            # NOT IN clause

# List comprehension (Pythonic way - bonus points!)
# This is like: SELECT score * 1.1 FROM scores WHERE score > 90
curved_scores = [score * 1.1 for score in scores if score > 90]
print(f"Curved scores: {curved_scores}")

# ============================================
# LEVEL 3: DICTIONARIES (Like JSON/key-value)
# ============================================

# Creating dictionaries
employee = {
    "id": 1001,
    "name": "Ray",
    "department": "Data",
    "skills": ["SQL", "Python", "dbt"]  # Can nest lists!
}

# Accessing values
emp_name = employee["name"]           # Will error if key doesn't exist
emp_dept = employee.get("department") # Returns None if missing
emp_salary = employee.get("salary", 0)  # Default value if missing

# Adding/updating
employee["salary"] = 150000           # Add new key
employee["department"] = "Analytics"  # Update existing

# Dictionary operations
keys = employee.keys()                # All keys
values = employee.values()            # All values
items = employee.items()              # Key-value pairs

# Checking existence
has_salary = "salary" in employee     # Check if key exists

# Nested access (like JSON)
first_skill = employee["skills"][0]   # Gets "SQL"

# ============================================
# LEVEL 4: CONTROL FLOW (Logic)
# ============================================

# If/elif/else (like CASE WHEN in SQL)
def categorize_experience(years):
    if years < 2:
        return "Junior"
    elif years < 5:
        return "Mid-level"
    elif years < 10:
        return "Senior"
    else:
        return "Principal"

# For loops (iteration)
for score in scores:
    if score >= 90:
        print(f"A grade: {score}")
    elif score >= 80:
        print(f"B grade: {score}")
    else:
        print(f"Below B: {score}")

# While loops (less common in data work)
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1

# ============================================
# LEVEL 5: FUNCTIONS (Reusable code)
# ============================================

def calculate_stats(numbers):
    """Function with multiple returns"""
    if not numbers:  # Handle empty list
        return {
            "count": 0,
            "sum": 0,
            "avg": 0,
            "min": None,
            "max": None
        }
    
    return {
        "count": len(numbers),
        "sum": sum(numbers),
        "avg": sum(numbers) / len(numbers),
        "min": min(numbers),
        "max": max(numbers)
    }

# Using the function
stats = calculate_stats(scores)
print(f"Statistics: {stats}")

# Function with default parameters
def greet(name, title="Mr."):
    return f"Hello, {title} {name}"

print(greet("Smith"))              # Uses default
print(greet("Johnson", "Dr."))    # Override default

# ============================================
# LEVEL 6: COMMON INTERVIEW PATTERNS
# ============================================

# Pattern 1: FizzBuzz (They STILL ask this)
def fizzbuzz(n):
    """Print 1 to n, but:
    - 'Fizz' for multiples of 3
    - 'Buzz' for multiples of 5
    - 'FizzBuzz' for multiples of both
    """
    result = []
    for i in range(1, n + 1):  # range is exclusive of end
        if i % 15 == 0:        # Divisible by both 3 and 5
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result

print(f"FizzBuzz(15): {fizzbuzz(15)}")

# Pattern 2: Find duplicates
def find_duplicates(items):
    """Find all duplicate values in a list"""
    seen = set()
    duplicates = set()
    
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    
    return list(duplicates)

test_list = [1, 2, 3, 2, 4, 3, 5]
print(f"Duplicates in {test_list}: {find_duplicates(test_list)}")

# Pattern 3: Reverse a string (another classic)
def reverse_string(s):
    """Multiple ways to reverse"""
    # Method 1: Slicing (Pythonic)
    return s[::-1]
    
    # Method 2: Using reversed()
    # return ''.join(reversed(s))
    
    # Method 3: Manual (what they might want to see)
    # result = ""
    # for char in s:
    #     result = char + result
    # return result

print(f"Reversed 'Python': {reverse_string('Python')}")

# Pattern 4: Check palindrome
def is_palindrome(s):
    """Check if string reads same forwards and backwards"""
    # Clean the string (remove spaces, lowercase)
    cleaned = s.lower().replace(" ", "")
    # Compare with reverse
    return cleaned == cleaned[::-1]

test_palindromes = ["racecar", "hello", "A man a plan a canal Panama"]
for word in test_palindromes:
    print(f"'{word}' is palindrome: {is_palindrome(word)}")

# ============================================
# LEVEL 7: ERROR HANDLING (Professional touch)
# ============================================

def safe_divide(a, b):
    """Division with error handling"""
    try:
        return a / b
    except ZeroDivisionError:
        return None  # or could return 0 or raise custom error
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Test error handling
print(f"10 / 2 = {safe_divide(10, 2)}")
print(f"10 / 0 = {safe_divide(10, 0)}")

# ============================================
# YOUR INTERVIEW STRATEGY
# ============================================

"""
1. ALWAYS test with edge cases:
   - Empty list/string
   - None/NULL values
   - Single element
   - Duplicates

2. When stuck, think "How would I do this in SQL?"
   - GROUP BY -> dictionary to accumulate
   - WHERE -> if statements or list comprehension
   - JOIN -> nested loops or dictionary lookups

3. Name your variables clearly:
   - Not 'x', 'y', 'z'
   - Use 'employee_name', 'total_sales', etc.

4. Add comments for complex logic

5. If they ask for optimization:
   "In production, I'd handle this at the database level"

COMMON MISTAKES TO AVOID:
- Forgetting Python is 0-indexed (SQL is 1-indexed)
- Modifying list while iterating over it
- Not handling None/empty cases
- Using '==' for None (use 'is None')

YOUR POWER PHRASES:
- "Let me handle the edge cases first..."
- "In SQL this would be..., here's the Python equivalent"
- "I'd normally use pandas for this, but in pure Python..."
"""

# ============================================
# PRACTICE EXERCISES (Do these!)
# ============================================

# Exercise 1: Count word frequency
def word_frequency(text):
    """Count how many times each word appears"""
    # YOUR CODE HERE
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

# Exercise 2: Find common elements in two lists
def find_common(list1, list2):
    """Find elements that appear in both lists"""
    # YOUR CODE HERE
    return list(set(list1) & set(list2))

# Exercise 3: Flatten nested list
def flatten(nested_list):
    """Convert [[1,2], [3,4]] to [1,2,3,4]"""
    # YOUR CODE HERE
    result = []
    for sublist in nested_list:
        result.extend(sublist)
    return result

# Exercise 4: Group by key
def group_by_key(records, key):
    """Group list of dicts by a key (like SQL GROUP BY)"""
    # YOUR CODE HERE
    grouped = {}
    for record in records:
        key_value = record.get(key)
        if key_value not in grouped:
            grouped[key_value] = []
        grouped[key_value].append(record)
    return grouped

# Test your solutions!
print("\n=== Testing Exercises ===")
print(f"Word frequency: {word_frequency('the quick brown fox jumps over the lazy dog')}")
print(f"Common elements: {find_common([1,2,3,4], [3,4,5,6])}")
print(f"Flattened: {flatten([[1,2], [3,4], [5]])}")

employees = [
    {"name": "Alice", "dept": "Sales"},
    {"name": "Bob", "dept": "IT"},
    {"name": "Charlie", "dept": "Sales"}
]
print(f"Grouped: {group_by_key(employees, 'dept')}")

# ============================================
# NEXT STEPS
# ============================================

"""
1. Run this ENTIRE file to see all outputs
2. Modify each function to understand how it works
3. Break things on purpose to see error messages
4. Practice the exercises until they're natural
5. Then move on to Pandas (which builds on these)

Remember: This is just your entry ticket.
Your SQL expertise is your real value.

Time estimate: 2-3 hours to be comfortable with all of this.
Then you're ready for Pandas!
"""