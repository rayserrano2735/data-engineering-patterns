# Filename: interview-prep/fix_these_for_practice.py
"""
Broken Code Exercises

"""

#import pandas as pd

# ============================================
# STRING MANIPULATION (They love this)
# ============================================

# BROKEN 1: Name Parser - Crashes on edge cases
def parse_name(full_name):
    """
    BUG: Doesn't handle None, empty string, or single names
    FIX: Add proper checks
    """
    #full_name = full_name.strip()
    
    # Normalize full_name
    match full_name:
        case None:
            full_name = "N/A"
        case "":
            full_name = "N/A"
        case "  ":
            full_name = "N/A"
        
    parts = full_name.split()  # BUG: Will crash on None!
    first = parts[0]  # BUG: Will crash if parts is empty!
    last = parts[1] if len(parts) > 1 else ""   # BUG: Will crash if only one name!
    return {"first": first, "last": last}

# Test cases (some will crash):
print(parse_name("John Smith"))    # Works
print(parse_name("Cher"))          # Crashes - single name
print(parse_name(None))            # Crashes - None
print(parse_name(""))              # Crashes - empty string
print(parse_name("  "))            # Crashes - just spaces


# BROKEN 2: Phone Number Cleaner
def clean_phone(phone):
    """
    BUG: Should return only digits, but doesn't handle None or actually remove non-digits
    FIX: Handle None and actually clean the phone number
    """
    # BUG: No None check!
    # BUG: This doesn't actually remove anything!
    return phone.replace("-", "")  

# Test cases:
# print(clean_phone("123-456-7890"))   # Partially works
# print(clean_phone("(123) 456-7890")) # Fails - parentheses remain
# print(clean_phone(None))             # Crashes


# ============================================
# LIST OPERATIONS (Must know basics)
# ============================================

# BROKEN 3: Find Second Highest
def second_highest(numbers):
    """
    BUG: Doesn't handle duplicates or short lists
    FIX: Remove duplicates and check length
    """
    numbers.sort()
    return numbers[-2]  # BUG: What if list has less than 2 items?
                       # BUG: What if highest number appears twice?

# Test cases:
# print(second_highest([1, 2, 3, 4, 5]))    # Works
# print(second_highest([5, 5, 4, 3]))       # Wrong - returns 5 instead of 4
# print(second_highest([1]))                # Crashes
# print(second_highest([]))                 # Crashes


# BROKEN 4: Remove Duplicates
def remove_duplicates(items):
    """
    BUG: Doesn't actually remove duplicates
    FIX: Track what you've seen
    """
    result = []
    for item in items:
        result.append(item)  # BUG: Just appends everything!
    return result

# Test cases:
# print(remove_duplicates([1, 2, 3, 2, 1]))  # Should return [1, 2, 3]
# print(remove_duplicates([]))               # Should handle empty


# ============================================
# PANDAS OPERATIONS (They ALWAYS test this)
# ============================================

# BROKEN 5: Group By Average
def avg_salary_by_dept(df):
    """
    BUG: Wrong syntax for pandas groupby
    FIX: Use correct pandas syntax
    """
    # BUG: This isn't how pandas groupby works!
    return df.group('department').average('salary')

# Test with:
# df = pd.DataFrame({
#     'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
#     'department': ['Sales', 'IT', 'Sales', 'IT'],
#     'salary': [50000, 60000, 55000, 65000]
# })
# print(avg_salary_by_dept(df))


# BROKEN 6: Filter DataFrame
def get_high_earners(df, threshold):
    """
    BUG: Wrong filtering syntax
    FIX: Use correct boolean indexing
    """
    # BUG: This isn't how you filter a DataFrame!
    return df.where('salary' > threshold)

# Test with same df as above:
# print(get_high_earners(df, 55000))


# BROKEN 7: Add Calculated Column
def add_bonus_column(df):
    """
    BUG: Wrong syntax for adding column
    FIX: Use correct column assignment
    """
    # BUG: This doesn't actually add the column to df!
    bonus = df['salary'] * 0.1
    return df

# Test with same df:
# result = add_bonus_column(df)
# print(result.columns)  # Should include 'bonus'


# ============================================
# CLASSIC ALGORITHMS (Interview favorites)
# ============================================

# BROKEN 8: FizzBuzz
def fizzbuzz(n):
    """
    BUG: Logic is in wrong order
    FIX: Check divisible by 15 FIRST
    """
    result = []
    for i in range(1, n + 1):
        if i % 3 == 0:  # BUG: This catches 15 before we check for FizzBuzz!
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        elif i % 15 == 0:  # BUG: This will never execute!
            result.append("FizzBuzz")
        else:
            result.append(str(i))
    return result

# Test:
# print(fizzbuzz(15))  # 15 should be "FizzBuzz" not "Fizz"


# BROKEN 9: Check Palindrome
def is_palindrome(s):
    """
    BUG: Doesn't handle spaces or case
    FIX: Clean string first
    """
    # BUG: Doesn't handle "A man a plan a canal Panama"
    return s == s[::-1]

# Test cases:
# print(is_palindrome("racecar"))                    # Works
# print(is_palindrome("A man a plan a canal Panama")) # Should be True
# print(is_palindrome("race a car"))                 # Should be False


# BROKEN 10: Find Common Elements
def find_common(list1, list2):
    """
    BUG: Inefficient nested loop and doesn't handle duplicates properly
    FIX: Use sets
    """
    common = []
    for item1 in list1:
        for item2 in list2:  # BUG: O(n²) complexity!
            if item1 == item2:
                common.append(item1)  # BUG: Will add duplicates!
    return common

# Test:
# print(find_common([1, 2, 2, 3], [2, 2, 3, 4]))  # Should return [2, 3] not [2, 2, 2, 2, 3]


# ============================================
# BONUS: SQL to Python (Your strength!)
# ============================================

# BROKEN 11: Implement SQL's COALESCE
def coalesce(*args):
    """
    BUG: Should return first non-None value, but doesn't
    FIX: Actually check for None
    """
    # BUG: This just returns the first argument always!
    return args[0] if args else None

# Test:
# print(coalesce(None, None, "first", "second"))  # Should return "first"
# print(coalesce(None, 0, 1))                     # Should return 0 (0 is not None!)


# ============================================
# ANSWER KEY (DON'T LOOK UNTIL YOU TRY!)
# ============================================

"""
HINTS (if you're stuck):

1. Name Parser: Check if full_name exists before calling .split()
2. Phone Cleaner: Use list comprehension with .isdigit()
3. Second Highest: Convert to set first, then sort
4. Remove Duplicates: Check "if item not in result" before appending
5. Pandas GroupBy: df.groupby('department')['salary'].mean()
6. Pandas Filter: df[df['salary'] > threshold]
7. Add Column: df['bonus'] = df['salary'] * 0.1
8. FizzBuzz: Check % 15 first, then % 3, then % 5
9. Palindrome: clean = s.lower().replace(" ", "")
10. Common Elements: list(set(list1) & set(list2))
11. Coalesce: for arg in args: if arg is not None: return arg

FULL SOLUTIONS:
(Write your solutions first, then compare!)

def parse_name_fixed(full_name):
    if not full_name:
        return {"first": "", "last": ""}
    full_name = full_name.strip()
    if not full_name:
        return {"first": "", "last": ""}
    parts = full_name.split()
    if len(parts) == 0:
        return {"first": "", "last": ""}
    elif len(parts) == 1:
        return {"first": parts[0], "last": ""}
    else:
        return {"first": parts[0], "last": " ".join(parts[1:])}

def clean_phone_fixed(phone):
    if not phone:
        return ""
    return "".join(c for c in phone if c.isdigit())

def second_highest_fixed(numbers):
    if len(numbers) < 2:
        return None
    unique = sorted(set(numbers), reverse=True)
    return unique[1] if len(unique) > 1 else None

# ... etc
"""

# ============================================
# YOUR PRACTICE STRATEGY
# ============================================

"""

FOCUS ORDER:
1. String manipulation (1-2) - They ALWAYS ask
2. Classic algorithms (8-10) - Common filters
3. Pandas operations (5-7) - Required for data roles
4. List operations (3-4) - Basic competency

"""