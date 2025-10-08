#!/usr/bin/env python3
"""
Week 1 Exercises: Python Fundamentals
Foundation for pattern-based learning (no pandas patterns yet)

Topics: Lists, Dicts, Sets, Comprehensions, Functions, Lambda, Strings
"""

from typing import List, Dict, Any

# ============================================================================
# DAY 1-2: DATA STRUCTURES
# ============================================================================

def exercise_1_1():
    """Create a list of numbers 1-10 and return only even numbers."""
    # Your solution here
    numbers = list(range(1, 11))
    evens = [n for n in numbers if n % 2 == 0]
    return evens


def exercise_1_2():
    """Remove duplicates from [1, 2, 2, 3, 3, 3, 4], preserving order."""
    data = [1, 2, 2, 3, 3, 3, 4]
    
    # Solution: dict.fromkeys() preserves order in Python 3.7+
    unique = list(dict.fromkeys(data))
    return unique


def exercise_1_3():
    """
    Merge two dicts, keeping higher value when keys overlap.
    dict1 = {'a': 10, 'b': 20, 'c': 30}
    dict2 = {'b': 25, 'c': 15, 'd': 40}
    Result: {'a': 10, 'b': 25, 'c': 30, 'd': 40}
    """
    dict1 = {'a': 10, 'b': 20, 'c': 30}
    dict2 = {'b': 25, 'c': 15, 'd': 40}
    
    # Solution
    merged = dict1.copy()
    for key, value in dict2.items():
        if key not in merged or value > merged[key]:
            merged[key] = value
    
    return merged


def exercise_1_4():
    """
    DEBUG: Fix code that removes duplicates.
    Bug: Modifying list while iterating causes skipped elements.
    """
    # Broken version (commented out)
    # def remove_duplicates_broken(items):
    #     for i, item in enumerate(items):
    #         if items.count(item) > 1:
    #             items.remove(item)  # BAD: modifies during iteration
    #     return items
    
    # Fixed version
    def remove_duplicates_fixed(items):
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    test_data = [1, 2, 2, 3, 3, 3, 4]
    return remove_duplicates_fixed(test_data)


def exercise_1_5():
    """
    Count word frequency in a sentence using dictionary.
    Handle case-insensitive matching and punctuation.
    """
    sentence = "The quick brown fox jumps over the lazy dog. The fox is quick!"
    
    # Solution
    import string
    
    # Remove punctuation and lowercase
    cleaned = sentence.lower().translate(str.maketrans('', '', string.punctuation))
    words = cleaned.split()
    
    # Count frequencies
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    
    # Sort by frequency descending
    sorted_freq = dict(sorted(frequency.items(), 
                             key=lambda x: x[1], 
                             reverse=True))
    
    return sorted_freq


# ============================================================================
# DAY 3: COMPREHENSIONS
# ============================================================================

def exercise_2_1():
    """Get squares of only positive numbers from [-2, -1, 0, 1, 2, 3]."""
    numbers = [-2, -1, 0, 1, 2, 3]
    
    # Solution: Note 0 is not positive
    squares = [x**2 for x in numbers if x > 0]
    
    return squares


def exercise_2_2():
    """
    Create dict mapping each name to its length.
    names = ["Alice", "Bob", "Charlie", "Dave", "Eve"]
    """
    names = ["Alice", "Bob", "Charlie", "Dave", "Eve"]
    
    # Solution
    name_lengths = {name: len(name) for name in names}
    
    return name_lengths


def exercise_2_3():
    """
    Flatten nested structure [1, [2, 3], [4, [5, 6]], 7] 
    to [1, 2, 3, 4, 5, 6, 7].
    """
    nested = [1, [2, 3], [4, [5, 6]], 7]
    
    # Solution: Recursive flattening
    def flatten(lst):
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(flatten(item))
            else:
                result.append(item)
        return result
    
    flat = flatten(nested)
    return flat


def exercise_2_4():
    """
    DEBUG: Fix comprehension that should get words longer than 3 characters.
    Bug: Iterates over characters, not words.
    """
    sentence = "The quick brown fox jumps"
    
    # Broken version
    # wrong = [word for word in sentence if len(word) > 3]  # Iterates characters!
    
    # Fixed version
    words_correct = [word for word in sentence.split() if len(word) > 3]
    
    return words_correct


def exercise_2_5():
    """
    Clean and validate email addresses.
    Return list of (cleaned_email, is_valid) tuples.
    """
    emails = [
        "  Alice@Example.COM  ",
        "bob@domain",
        "charlie@email.co.uk",
        "not.an.email",
        "dave@",
        "eve@company.org"
    ]
    
    # Solution
    def validate_email(email):
        email = email.strip().lower()
        parts = email.split('@')
        return (
            len(parts) == 2 and 
            len(parts[0]) > 0 and 
            '.' in parts[1]
        )
    
    cleaned_emails = [
        (email.strip().lower(), validate_email(email))
        for email in emails
    ]
    
    return cleaned_emails


# ============================================================================
# DAY 4: FUNCTIONS AND PARAMETERS
# ============================================================================

def exercise_3_1():
    """
    Write function with default parameters that formats number as currency.
    format_currency(1234567.89) → "$1,234,567.89"
    format_currency(1234567.89, symbol='€') → "€1,234,567.89"
    """
    def format_currency(amount, symbol='$', decimals=2):
        formatted = f"{amount:,.{decimals}f}"
        return f"{symbol}{formatted}"
    
    # Tests
    assert format_currency(1234567.89) == "$1,234,567.89"
    assert format_currency(1234567.89, symbol='€') == "€1,234,567.89"
    assert format_currency(1234567.89, decimals=0) == "$1,234,568"
    
    return format_currency


def exercise_3_2():
    """
    Use lambda with sorted() to sort list of tuples by second element.
    Sort by score descending, then name ascending for ties.
    """
    data = [
        ('Alice', 85),
        ('Bob', 92),
        ('Charlie', 78),
        ('Dave', 92),
        ('Eve', 88)
    ]
    
    # Solution: negative score for desc, name asc
    sorted_data = sorted(data, key=lambda x: (-x[1], x[0]))
    
    return sorted_data


def exercise_3_3():
    """
    Create a function that returns a function (closure).
    create_filter(min_value=10, max_value=100, exclude=[50])
    Returns function that filters based on configured criteria.
    """
    def create_filter(min_value=None, max_value=None, exclude_values=None):
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
    
    # Test
    my_filter = create_filter(min_value=10, max_value=100, exclude_values=[50])
    data = [5, 10, 25, 50, 75, 100, 150]
    filtered = list(filter(my_filter, data))
    
    assert filtered == [10, 25, 75, 100]
    
    return create_filter


def exercise_3_4():
    """
    DEBUG: Fix mutable default argument bug.
    """
    # Broken version
    # def append_to_list_broken(item, target_list=[]):
    #     target_list.append(item)
    #     return target_list
    
    # Fixed version
    def append_to_list_fixed(item, target_list=None):
        if target_list is None:
            target_list = []
        target_list.append(item)
        return target_list
    
    # Test
    list1 = append_to_list_fixed(1)
    list2 = append_to_list_fixed(2)
    assert list1 == [1]
    assert list2 == [2]
    
    return append_to_list_fixed


def exercise_3_5():
    """
    Use map, filter, and reduce to process transactions.
    Calculate total revenue from valid transactions (amount > 0, status='completed').
    """
    from functools import reduce
    
    transactions = [
        {'id': 1, 'amount': 100, 'status': 'completed'},
        {'id': 2, 'amount': -50, 'status': 'completed'},
        {'id': 3, 'amount': 200, 'status': 'pending'},
        {'id': 4, 'amount': 150, 'status': 'completed'},
        {'id': 5, 'amount': 0, 'status': 'completed'},
        {'id': 6, 'amount': 300, 'status': 'completed'},
    ]
    
    # Solution
    valid_transactions = list(filter(
        lambda t: t['amount'] > 0 and t['status'] == 'completed',
        transactions
    ))
    
    amounts = list(map(lambda t: t['amount'], valid_transactions))
    
    total_revenue = reduce(lambda x, y: x + y, amounts, 0)
    
    return total_revenue


# ============================================================================
# DAY 5: LAMBDA AND SORTING
# ============================================================================

def exercise_lambda_1():
    """
    Sort products by price descending, then name ascending.
    """
    products = [
        {'name': 'Laptop', 'price': 999},
        {'name': 'Mouse', 'price': 25},
        {'name': 'Keyboard', 'price': 75},
        {'name': 'Monitor', 'price': 299}
    ]
    
    # Solution
    sorted_products = sorted(
        products, 
        key=lambda p: (-p['price'], p['name'])
    )
    
    return sorted_products


def exercise_lambda_2():
    """
    Filter and sort: get top 3 highest salaries.
    """
    employees = [
        {'name': 'Alice', 'salary': 50000},
        {'name': 'Bob', 'salary': 75000},
        {'name': 'Charlie', 'salary': 55000},
        {'name': 'Dave', 'salary': 80000},
        {'name': 'Eve', 'salary': 45000}
    ]
    
    # Solution
    top_3 = sorted(
        employees, 
        key=lambda e: e['salary'], 
        reverse=True
    )[:3]
    
    return top_3


# ============================================================================
# DAY 6: STRING OPERATIONS
# ============================================================================

def exercise_string_1():
    """
    Clean phone numbers to format: XXX-XXX-XXXX
    """
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
    
    return clean_phone


def exercise_string_2():
    """
    Parse log entries and extract ERROR messages with dates.
    """
    log_entries = [
        "2024-01-15 ERROR: Database connection failed",
        "2024-01-15 INFO: User login successful",
        "2024-01-15 WARNING: High memory usage detected",
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
    return errors


# ============================================================================
# DAY 7: INTEGRATION EXERCISE
# ============================================================================

def exercise_integration():
    """
    Calculate summary statistics by category from transaction data.
    Uses: dicts, comprehensions, functions, sorting
    """
    transactions = [
        {'category': 'Food', 'amount': 45.50, 'date': '2024-01-15'},
        {'category': 'Transport', 'amount': 12.00, 'date': '2024-01-15'},
        {'category': 'Food', 'amount': 38.75, 'date': '2024-01-16'},
        {'category': 'Entertainment', 'amount': 50.00, 'date': '2024-01-16'},
        {'category': 'Food', 'amount': 42.25, 'date': '2024-01-17'},
        {'category': 'Transport', 'amount': 15.00, 'date': '2024-01-17'},
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
        sorted_summary = dict(
            sorted(summary.items(), 
                   key=lambda x: x[1]['total'], 
                   reverse=True)
        )
        
        return sorted_summary
    
    result = summarize_transactions(transactions)
    return result


# ============================================================================
# RUNNING EXERCISES
# ============================================================================

if __name__ == "__main__":
    print("Week 1 Exercises: Python Fundamentals")
    print("=" * 60)
    
    exercises = [
        ("1.1: Filter evens", exercise_1_1),
        ("1.2: Remove duplicates", exercise_1_2),
        ("1.3: Merge dicts", exercise_1_3),
        ("1.4: Debug list modification", exercise_1_4),
        ("1.5: Word frequency", exercise_1_5),
        ("2.1: Positive squares", exercise_2_1),
        ("2.2: Name lengths", exercise_2_2),
        ("2.3: Flatten nested", exercise_2_3),
        ("2.4: Debug word iteration", exercise_2_4),
        ("2.5: Clean emails", exercise_2_5),
        ("3.1: Currency formatter", exercise_3_1),
        ("3.2: Sort tuples", exercise_3_2),
        ("3.3: Function closure", exercise_3_3),
        ("3.4: Fix mutable default", exercise_3_4),
        ("3.5: Map/filter/reduce", exercise_3_5),
        ("Lambda 1: Sort products", exercise_lambda_1),
        ("Lambda 2: Top 3 salaries", exercise_lambda_2),
        ("String 1: Clean phones", exercise_string_1),
        ("String 2: Parse logs", exercise_string_2),
        ("Integration: Summarize transactions", exercise_integration),
    ]
    
    for name, exercise in exercises:
        try:
            result = exercise()
            print(f"✓ {name}")
        except Exception as e:
            print(f"✗ {name}: {e}")
    
    print("\n" + "=" * 60)
    print("Week 1 exercises complete!")
