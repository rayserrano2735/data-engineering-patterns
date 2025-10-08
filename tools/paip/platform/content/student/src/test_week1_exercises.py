#!/usr/bin/env python3
"""
Week 1 Exercise Test Harness
Run: python test_week1_exercises.py
"""

import sys
from week1_exercises import *

def run_tests():
    """Run all exercise tests."""
    passed = 0
    failed = 0
    
    tests = [
        ("1.1", test_1_1),
        ("1.2", test_1_2),
        ("1.3", test_1_3),
        ("1.4", test_1_4),
        ("1.5", test_1_5),
        ("2.1", test_2_1),
        ("2.2", test_2_2),
        ("2.3", test_2_3),
        ("2.4", test_2_4),
        ("2.5", test_2_5),
        ("3.1", test_3_1),
        ("3.2", test_3_2),
        ("3.3", test_3_3),
        ("3.4", test_3_4),
        ("3.5", test_3_5),
        ("4.1", test_4_1),
        ("4.2", test_4_2),
        ("4.3", test_4_3),
        ("4.4", test_4_4),
        ("4.5", test_4_5),
    ]
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ Exercise {name} passed")
            passed += 1
        except AssertionError as e:
            print(f"✗ Exercise {name} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Exercise {name} error: {e}")
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    return failed == 0

# Test functions

def test_1_1():
    result = exercise_1_1()
    assert result == [2, 4, 6, 8, 10], f"Expected [2, 4, 6, 8, 10], got {result}"

def test_1_2():
    result = exercise_1_2()
    assert result == [1, 2, 3, 4], f"Expected [1, 2, 3, 4], got {result}"

def test_1_3():
    result = exercise_1_3()
    expected = {'a': 10, 'b': 25, 'c': 30, 'd': 40}
    assert result == expected, f"Expected {expected}, got {result}"

def test_1_4():
    result = exercise_1_4()
    expected = {'apple': 3, 'banana': 2, 'cherry': 1}
    assert result == expected, f"Expected {expected}, got {result}"

def test_1_5():
    result = exercise_1_5()
    expected = {'Alice': 85, 'Bob': 92}
    assert result == expected, f"Expected {expected}, got {result}"

def test_2_1():
    result = exercise_2_1()
    assert result == [1, 4, 9], f"Expected [1, 4, 9], got {result}"

def test_2_2():
    result = exercise_2_2()
    expected = {'Alice': 5, 'Bob': 3, 'Charlie': 7}
    assert result == expected, f"Expected {expected}, got {result}"

def test_2_3():
    result = exercise_2_3()
    assert result == [1, 2, 3, 4, 5, 6], f"Expected [1, 2, 3, 4, 5, 6], got {result}"

def test_2_4():
    result = exercise_2_4()
    expected = ['test@email.com', 'user@domain.org', 'admin@site.net']
    assert result == expected, f"Expected {expected}, got {result}"

def test_2_5():
    result = exercise_2_5()
    assert 'The' in result and result['The'] == 3, "Missing or incorrect 'The'"
    assert 'quick' in result and result['quick'] == 5, "Missing or incorrect 'quick'"

def test_3_1():
    assert exercise_3_1(1234567.89) == '$1,234,567.89'
    assert exercise_3_1(1234567.89, symbol='€') == '€1,234,567.89'
    assert exercise_3_1(1234567.89, decimals=0) == '$1,234,568'

def test_3_2():
    data = [('Alice', 85), ('Bob', 92), ('Charlie', 78), ('Dave', 92)]
    result = exercise_3_2(data)
    expected = [('Bob', 92), ('Dave', 92), ('Alice', 85), ('Charlie', 78)]
    assert result == expected, f"Expected {expected}, got {result}"

def test_3_3():
    employees = [{'name': 'Alice', 'salary': 75000}, {'name': 'Bob', 'salary': 85000}]
    result = exercise_3_3(employees)
    assert result == {'name': 'Bob', 'salary': 85000}

def test_3_4():
    result = exercise_3_4([10, 25, 30, 5, 40], 20)
    assert result == [25, 30, 40], f"Expected [25, 30, 40], got {result}"

def test_3_5():
    result = exercise_3_5("Hello world! Hello Python.")
    expected = {'hello': 2, 'world': 1, 'python': 1}
    assert result == expected, f"Expected {expected}, got {result}"

def test_4_1():
    products = [
        {'name': 'Widget', 'price': 25},
        {'name': 'Gadget', 'price': 25},
        {'name': 'Tool', 'price': 30}
    ]
    result = exercise_4_1(products)
    expected = [
        {'name': 'Tool', 'price': 30},
        {'name': 'Gadget', 'price': 25},
        {'name': 'Widget', 'price': 25}
    ]
    assert result == expected, f"Expected {expected}, got {result}"

def test_4_2():
    data = [
        {'category': 'A', 'value': 10},
        {'category': 'B', 'value': 5},
        {'category': 'A', 'value': 15}
    ]
    result = exercise_4_2(data)
    assert result == [15, 10], f"Expected [15, 10], got {result}"

def test_4_3():
    result = exercise_4_3([15, 30, 10, 45, 25, 60])
    assert result == [15, 30, 45, 60], f"Expected [15, 30, 45, 60], got {result}"

def test_4_4():
    result = exercise_4_4(['apple', 'banana', 'cherry'])
    assert result == [5, 6, 6], f"Expected [5, 6, 6], got {result}"

def test_4_5():
    scores = [
        {'student': 'Alice', 'score': 85},
        {'student': 'Bob', 'score': 72},
        {'student': 'Charlie', 'score': 90}
    ]
    result = exercise_4_5(scores)
    assert result == ['Charlie', 'Alice'], f"Expected ['Charlie', 'Alice'], got {result}"

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
