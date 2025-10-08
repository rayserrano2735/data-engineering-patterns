#!/usr/bin/env python3
"""
Week 1 Exercises: Python Fundamentals
Students write solutions and validate with test_week1_exercises.py

Topics: Lists, Dicts, Sets, Comprehensions, Functions, Lambda, Strings
"""

from typing import List, Dict, Any

# ============================================================================
# DAY 1-2: DATA STRUCTURES
# ============================================================================

def exercise_1_1():
    """Create a list of numbers 1-10 and return only even numbers."""
    pass


def exercise_1_2():
    """Remove duplicates from [1, 2, 2, 3, 3, 3, 4], preserving order."""
    pass


def exercise_1_3():
    """
    Merge two dicts, keeping higher value when keys overlap.
    dict1 = {'a': 10, 'b': 20, 'c': 30}
    dict2 = {'b': 25, 'c': 15, 'd': 40}
    Result: {'a': 10, 'b': 25, 'c': 30, 'd': 40}
    """
    pass


def exercise_1_4():
    """
    Count word frequency in ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
    Return: {'apple': 3, 'banana': 2, 'cherry': 1}
    """
    pass


def exercise_1_5():
    """
    Given list of dicts with 'name' and 'score' keys,
    return dict mapping name to score.
    Input: [{'name': 'Alice', 'score': 85}, {'name': 'Bob', 'score': 92}]
    Output: {'Alice': 85, 'Bob': 92}
    """
    pass


# ============================================================================
# DAY 3: COMPREHENSIONS
# ============================================================================

def exercise_2_1():
    """
    From [-2, -1, 0, 1, 2, 3], return squares of only positive numbers.
    Result: [1, 4, 9]
    """
    pass


def exercise_2_2():
    """
    From ['Alice', 'Bob', 'Charlie'], create dict mapping name to length.
    Result: {'Alice': 5, 'Bob': 3, 'Charlie': 7}
    """
    pass


def exercise_2_3():
    """
    Flatten [1, [2, 3], 4, [5, 6]] to [1, 2, 3, 4, 5, 6].
    Handle one level of nesting.
    """
    pass


def exercise_2_4():
    """
    From ['test@email.com', '  user@domain.org  ', 'invalid-email', 'admin@site.net'],
    return list of cleaned (stripped, lowercase) valid emails (has @ and . after @).
    Result: ['test@email.com', 'user@domain.org', 'admin@site.net']
    """
    pass


def exercise_2_5():
    """
    From sentence "The quick brown fox jumps over the lazy dog",
    return dict of word lengths.
    Result: {'The': 3, 'quick': 5, 'brown': 5, ...}
    """
    pass


# ============================================================================
# DAY 4: FUNCTIONS
# ============================================================================

def exercise_3_1(amount, symbol='$', decimals=2):
    """
    Format number as currency with optional symbol and decimal places.
    exercise_3_1(1234567.89) → '$1,234,567.89'
    exercise_3_1(1234567.89, symbol='€') → '€1,234,567.89'
    exercise_3_1(1234567.89, decimals=0) → '$1,234,568'
    """
    pass


def exercise_3_2(data):
    """
    Sort list of tuples by second element descending, then first element ascending.
    Input: [('Alice', 85), ('Bob', 92), ('Charlie', 78), ('Dave', 92)]
    Output: [('Bob', 92), ('Dave', 92), ('Alice', 85), ('Charlie', 78)]
    """
    pass


def exercise_3_3(employees):
    """
    From list of employee dicts with 'name' and 'salary',
    return highest paid employee dict. Handle empty list.
    Input: [{'name': 'Alice', 'salary': 75000}, {'name': 'Bob', 'salary': 85000}]
    Output: {'name': 'Bob', 'salary': 85000}
    """
    pass


def exercise_3_4(numbers, threshold):
    """
    Return list of numbers above threshold.
    Input: ([10, 25, 30, 5, 40], 20)
    Output: [25, 30, 40]
    """
    pass


def exercise_3_5(text):
    """
    Count word frequency in text (case-insensitive, ignore punctuation).
    Input: "Hello world! Hello Python."
    Output: {'hello': 2, 'world': 1, 'python': 1}
    """
    pass


# ============================================================================
# DAY 5: LAMBDA & SORTING
# ============================================================================

def exercise_4_1(products):
    """
    Sort list of product dicts by price descending, then name ascending.
    Input: [{'name': 'Widget', 'price': 25}, {'name': 'Gadget', 'price': 25}, {'name': 'Tool', 'price': 30}]
    Output: [{'name': 'Tool', 'price': 30}, {'name': 'Gadget', 'price': 25}, {'name': 'Widget', 'price': 25}]
    """
    pass


def exercise_4_2(data):
    """
    From [{'category': 'A', 'value': 10}, {'category': 'B', 'value': 5}, {'category': 'A', 'value': 15}],
    return top 2 values overall.
    Output: [15, 10]
    """
    pass


def exercise_4_3(numbers):
    """
    Use filter() and lambda to get numbers divisible by both 3 and 5.
    Input: [15, 30, 10, 45, 25, 60]
    Output: [15, 30, 45, 60]
    """
    pass


def exercise_4_4(words):
    """
    Use map() and lambda to get length of each word.
    Input: ['apple', 'banana', 'cherry']
    Output: [5, 6, 6]
    """
    pass


def exercise_4_5(scores):
    """
    From list of score dicts with 'student' and 'score',
    return list of students who scored above 80, sorted by score descending.
    Input: [{'student': 'Alice', 'score': 85}, {'student': 'Bob', 'score': 72}, {'student': 'Charlie', 'score': 90}]
    Output: ['Charlie', 'Alice']
    """
    pass
