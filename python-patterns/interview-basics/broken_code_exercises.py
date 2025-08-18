# Filename: debug-your-way-to-python/broken_exercises.py
"""
Debug Your Way to Python Mastery
Co-authored by Ray & Aitana (Intelligence²)
LEARN BY FIXING, NOT BY COPYING!
Each exercise is broken. Your job: Make it work!
"""

# ============================================
# LEVEL 1: SYNTAX ERRORS (Easy wins to build confidence)
# ============================================

# Exercise 1.1 - Missing Colon
# ERROR: SyntaxError on line 15
# FIX: Add the missing colon
def greet(name)  # BUG HERE!
    return f"Hello, {name}"

# Test (should print "Hello, World")
# print(greet("World"))


# Exercise 1.2 - Indentation Error  
# ERROR: IndentationError
# FIX: Fix the indentation
def calculate_total(items):
total = 0  # BUG HERE!
    for item in items:
        total += item
    return total

# Test (should print 15)
# print(calculate_total([1, 2, 3, 4, 5]))


# Exercise 1.3 - String Quote Mismatch
# ERROR: SyntaxError - EOL while scanning string
# FIX: Match the quotes
def get_message():
    return "Python is awesome'  # BUG HERE!

# Test (should print "Python is awesome")
# print(get_message())


# ============================================
# LEVEL 2: LOGIC ERRORS (Code runs but gives wrong answer)
# ============================================

# Exercise 2.1 - Wrong Operator
# BUG: Returns True for 15 (should only be True for 3 and 5)
# FIX: Change the operator
def fizzbuzz_check(n):
    if n % 3 == 0 or n % 5 == 0:  # BUG HERE!
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)

# Test (should print "FizzBuzz" only for 15, not for 3 or 5)
# print(f"3: {fizzbuzz_check(3)}")    # Should be "Fizz"
# print(f"5: {fizzbuzz_check(5)}")    # Should be "Buzz"  
# print(f"15: {fizzbuzz_check(15)}")  # Should be "FizzBuzz"


# Exercise 2.2 - Off By One Error
# BUG: Skips the last item
# FIX: Adjust the range
def get_evens(max_num):
    evens = []
    for i in range(0, max_num, 2):  # BUG HERE!
        evens.append(i)
    return evens

# Test (should include 10)
# print(get_evens(10))  # Should be [0, 2, 4, 6, 8, 10] but returns [0, 2, 4, 6, 8]


# Exercise 2.3 - Wrong Variable
# BUG: Always returns 0
# FIX: Return the right variable
def sum_list(numbers):
    total = 0
    for num in numbers:
        total += num
    return 0  # BUG HERE!

# Test (should print 10)
# print(sum_list([1, 2, 3, 4]))


# ============================================
# LEVEL 3: EDGE CASES (Code works mostly but fails on edge cases)
# ============================================

# Exercise 3.1 - Doesn't Handle None
# BUG: Crashes on None input
# FIX: Add None check
def parse_name(full_name):
    # BUG: No None check!
    parts = full_name.split()
    if len(parts) == 2:
        return {"first": parts[0], "last": parts[1]}
    else:
        return {"first": parts[0], "last": ""}

# Test (should handle None gracefully)
# print(parse_name("John Smith"))  # Works
# print(parse_name(None))  # Crashes!


# Exercise 3.2 - Empty List Crashes
# BUG: Crashes on empty list
# FIX: Handle empty case
def get_average(numbers):
    # BUG: Division by zero on empty list!
    return sum(numbers) / len(numbers)

# Test (should handle empty list)
# print(get_average([1, 2, 3]))  # Works
# print(get_average([]))  # Crashes!


# Exercise 3.3 - Duplicates Not Removed
# BUG: Doesn't actually remove duplicates
# FIX: Implement deduplication logic
def remove_duplicates(items):
    unique = []
    for item in items:
        unique.append(item)  # BUG: Just appends everything!
    return unique

# Test (should return [1, 2, 3])
# print(remove_duplicates([1, 2, 3, 2, 1]))  # Returns [1, 2, 3, 2, 1]


# ============================================
# LEVEL 4: PERFORMANCE ISSUES (Works but inefficient)
# ============================================

# Exercise 4.1 - Unnecessary Loop
# BUG: Uses loop when Python has built-in
# FIX: Use the built-in function
def find_maximum(numbers):
    if not numbers:
        return None
    max_val = numbers[0]
    for num in numbers:  # BUG: Why loop?
        if num > max_val:
            max_val = num
    return max_val

# Test (works but inefficient)
# print(find_maximum([3, 1, 4, 1, 5, 9]))


# Exercise 4.2 - Nested Loop Horror
# BUG: O(n²) when O(n) is possible
# FIX: Use a set for lookups
def find_common(list1, list2):
    common = []
    for item1 in list1:  # BUG: Nested loops!
        for item2 in list2:
            if item1 == item2 and item1 not in common:
                common.append(item1)
    return common

# Test (works but slow for large lists)
# print(find_common([1, 2, 3], [2, 3, 4]))


# Exercise 4.3 - String Concatenation in Loop
# BUG: Inefficient string building
# FIX: Use join() instead
def build_csv_line(values):
    result = ""
    for i, value in enumerate(values):
        result = result + str(value)  # BUG: String concatenation in loop!
        if i < len(values) - 1:
            result = result + ","
    return result

# Test (works but inefficient)
# print(build_csv_line(['a', 'b', 'c']))


# ============================================
# LEVEL 5: REAL INTERVIEW BUGS (Actual problems from interviews)
# ============================================

# Exercise 5.1 - The Classic Palindrome Bug
# BUG: Doesn't handle spaces or case
# FIX: Clean the string first
def is_palindrome(s):
    return s == s[::-1]  # BUG: Doesn't handle "A man a plan a canal Panama"

# Test 
# print(is_palindrome("racecar"))  # Works
# print(is_palindrome("A man a plan a canal Panama"))  # Fails!


# Exercise 5.2 - The Merge Intervals Bug
# BUG: Doesn't actually merge overlapping intervals
# FIX: Check for overlap and merge
def merge_intervals(intervals):
    if not intervals:
        return []
    
    intervals.sort()
    merged = []
    for interval in intervals:
        merged.append(interval)  # BUG: Just appends without merging!
    return merged

# Test (should merge [1,3] and [2,6] into [1,6])
# print(merge_intervals([[1,3], [2,6], [8,10]]))


# Exercise 5.3 - The Two Sum Bug
# BUG: Returns indices of same element used twice
# FIX: Check that we're not using same index twice
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):  # BUG: j should start from i+1
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

# Test (should return [0, 1] not [0, 0])
# print(two_sum([3, 3], 6))


# ============================================
# SOLUTIONS (Keep these hidden from students!)
# ============================================

"""
SOLUTIONS - DON'T PEEK UNTIL YOU'VE TRIED!

1.1: Add colon after def greet(name):
1.2: Unindent 'total = 0' to align with for loop
1.3: Change to "Python is awesome" (matching quotes)

2.1: Change 'or' to 'and' in first condition
2.2: Use range(0, max_num + 1, 2) to include max_num
2.3: Return total instead of 0

3.1: Add 'if not full_name: return {"first": "", "last": ""}'
3.2: Add 'if not numbers: return 0'
3.3: Add 'if item not in unique:' before append

4.1: Just use 'return max(numbers) if numbers else None'
4.2: Use 'return list(set(list1) & set(list2))'
4.3: Use 'return ",".join(str(v) for v in values)'

5.1: Add 's = s.lower().replace(" ", "")' at the start
5.2: Check if intervals overlap and merge them
5.3: Start j loop from i+1: 'for j in range(i+1, len(nums)):'
"""

# ============================================
# LEARNING PATH
# ============================================

"""
RECOMMENDED ORDER:
Day 1: Fix all Level 1 (Syntax) - Build confidence
Day 2: Fix all Level 2 (Logic) - Understand flow
Day 3: Fix all Level 3 (Edge Cases) - Think defensively  
Day 4: Fix all Level 4 (Performance) - Optimize
Day 5: Fix all Level 5 (Interview) - Apply everything

DEBUGGING TIPS:
1. Read the error message - it tells you the line number!
2. Print intermediate values to see what's happening
3. Test with different inputs to find the pattern
4. Google the error if stuck - this is what real programmers do!

REMEMBER:
Every bug you fix makes you stronger.
Every error you understand makes you wiser.
Every crash you prevent makes you a better engineer.

You learn by FIXING, not by copying!
"""