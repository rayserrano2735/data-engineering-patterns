# Quick Reference - Python Analytics Engineering Syntax

Rapid lookup during interviews. Results shown for verification without running code.

## Lists

```python
# Starting with: lst = [1, 2, 3]
lst.append(4)                 # [1, 2, 3, 4]
lst.extend([5, 6])            # [1, 2, 3, 5, 6]
lst.insert(0, 0)              # [0, 1, 2, 3]
lst.remove(3)                 # [1, 2] (removes first 3)
lst.pop()                     # Returns 3, lst = [1, 2]
lst.pop(0)                    # Returns 1, lst = [2, 3]
lst.clear()                   # []
lst.index(2)                  # 1 (index of first 2)
lst.count(2)                  # Number of 2s
lst.sort()                    # [1, 2, 3] (in place)
lst.reverse()                 # [3, 2, 1] (in place)
sorted(lst)                   # [1, 2, 3] (new list)
list(reversed(lst))           # [3, 2, 1] (new list)
lst[:]                        # [1, 2, 3] (shallow copy)
lst[1:3]                      # [2, 3] (slice elements 1-2)
lst[::2]                      # [1, 3] (every 2nd element)
lst[::-1]                     # [3, 2, 1] (reverse)
```

**Note:** "Ordered" means maintains insertion position. "Sorted" means arranged by value.

## Dictionaries

```python
# Starting with: d = {'a': 1, 'b': 2}
d['c'] = 3                    # {'a': 1, 'b': 2, 'c': 3}
d.get('a')                    # 1
d.get('x', 0)                 # 0 (default when missing)
d.pop('a')                    # Returns 1, d = {'b': 2}
d.popitem()                   # Returns ('b', 2), d = {}
d.clear()                     # {}
list(d.keys())                # ['a', 'b']
list(d.values())              # [1, 2]
list(d.items())               # [('a', 1), ('b', 2)]
d.update({'c': 3})            # {'a': 1, 'b': 2, 'c': 3}
d.setdefault('d', 4)          # {'a': 1, 'b': 2, 'd': 4}
'a' in d                      # True
dict.fromkeys(['a','b'], 0)   # {'a': 0, 'b': 0}
```

## Sets

```python
# Starting with: s = {1, 2, 3}
s.add(4)                      # {1, 2, 3, 4}
s.update([5, 6])              # {1, 2, 3, 5, 6}
s.remove(2)                   # {1, 3} (error if missing)
s.discard(2)                  # {1, 3} (no error if missing)
s.pop()                       # Returns arbitrary element
s.clear()                     # set()
{1,2} | {3,4}                 # {1, 2, 3, 4} union
{1,2,3} & {2,3,4}             # {2, 3} intersection
{1,2,3} - {2,3}               # {1} difference
{1,2} ^ {2,3}                 # {1, 3} symmetric difference
```

## Iteration

```python
# For loops
for item in [1, 2, 3]:        # Iterate list
    print(item)

for key in {'a': 1}:          # Iterate dict keys
    print(key)

for key, val in {'a': 1}.items():  # Iterate key-value pairs
    print(key, val)

for val in {'a': 1}.values(): # Iterate dict values
    print(val)

# Range
for i in range(5):            # 0, 1, 2, 3, 4
for i in range(1, 5):         # 1, 2, 3, 4
for i in range(0, 10, 2):     # 0, 2, 4, 6, 8

# Enumerate (index + value)
for i, val in enumerate(['a', 'b']):
    print(i, val)             # 0 a, 1 b

# Zip (parallel iteration)
for x, y in zip([1,2], ['a','b']):
    print(x, y)               # 1 a, 2 b

# While loop
i = 0
while i < 5:
    print(i)
    i += 1                    # Don't forget increment!

# Break and continue
for i in range(10):
    if i == 5:
        break                 # Exit loop
    if i % 2 == 0:
        continue              # Skip to next iteration
    print(i)                  # Prints odd numbers < 5

# For-else (runs if loop completes without break)
for i in range(5):
    if i == 10:
        break
else:
    print("Loop completed")   # Executes
```

## Strings

```python
# Starting with: s = "Hello World"
s.lower()                     # "hello world"
s.upper()                     # "HELLO WORLD"
s.title()                     # "Hello World"
s.strip()                     # "Hello World" (remove whitespace)
s.split()                     # ["Hello", "World"]
s.split(',')                  # Split on comma
",".join(['a','b'])           # "a,b"
s.replace('H', 'h')           # "hello World"
s.startswith('Hello')         # True
s.endswith('World')           # True
s.find('World')               # 6 (index or -1)
s.count('l')                  # 3
s[0]                          # "H" (access by index)
s[0:5]                        # "Hello" (slice)
```

## List Comprehensions

```python
# Basic
[x for x in range(5)]         # [0, 1, 2, 3, 4]

# With condition
[x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# With transformation
[x**2 for x in range(5)]      # [0, 1, 4, 9, 16]

# Transform and filter
[x**2 for x in range(10) if x % 2 == 0]  # [0, 4, 16, 36, 64]

# Nested comprehension
[[i*j for j in range(3)] for i in range(3)]  # [[0,0,0],[0,1,2],[0,2,4]]

# Flatten
[item for sublist in nested for item in sublist]  # Flatten one level
```

## Dict Comprehensions

```python
# Basic
{x: x**2 for x in range(5)}   # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# From lists
{k: v for k, v in zip(keys, values)}  # Combine lists into dict

# From list of tuples
{k: v for k, v in [('a', 1), ('b', 2)]}  # {'a': 1, 'b': 2}

# With condition
{k: v for k, v in d.items() if v > 0}  # Filter dict by value
```

## Set Comprehensions

```python
{x for x in range(10) if x % 2 == 0}  # {0, 2, 4, 6, 8}
{x**2 for x in range(-3, 4)}          # {0, 1, 4, 9}
```

## Lambda & Sorting

```python
# Lambda basics
square = lambda x: x**2       # square(5) = 25
add = lambda x, y: x + y      # add(2, 3) = 5

# Sorting
sorted([3,1,2])               # [1, 2, 3]
sorted([3,1,2], reverse=True) # [3, 2, 1]

# Sort by key
data = [('Bob', 25), ('Alice', 30)]
sorted(data, key=lambda x: x[1])  # [('Bob', 25), ('Alice', 30)]
sorted(data, key=lambda x: x[0])  # [('Alice', 30), ('Bob', 25)]

# Sort with multiple keys
sorted(data, key=lambda x: (-x[1], x[0]))  # Desc by 2nd, asc by 1st
```

## Built-in Functions

```python
len([1,2,3])                  # 3
sum([1,2,3])                  # 6
min([3,1,2])                  # 1
max([3,1,2])                  # 3
range(5)                      # 0,1,2,3,4 (use list(range(5)))
list(range(1, 6))             # [1, 2, 3, 4, 5]
enumerate(['a','b'])          # [(0,'a'), (1,'b')]
zip([1,2], ['a','b'])         # [(1,'a'), (2,'b')]
filter(lambda x: x>0, lst)    # Iterator of filtered items
map(lambda x: x*2, lst)       # Iterator of transformed items
```

## Common Patterns

```python
# Dedup preserving order
list(dict.fromkeys(lst))      # [1, 2, 3] from [1,2,2,3]

# Dedup unordered
list(set(lst))                # [1, 2, 3] from [1,2,2,3] (faster)

# Count occurrences
from collections import Counter
Counter(lst)                  # {1: 2, 2: 3, 3: 1}

# Merge dicts (3.9+)
d1 | d2                       # Merge, d2 values override

# Flatten one level
[item for sublist in nested for item in sublist]

# Check all/any
all([True, True, False])      # False
any([False, False, True])     # True

# String formatting
f"Value: {x:.2f}"             # Format with 2 decimals
f"Name: {name:>10}"           # Right-align in 10 chars
```

## Pandas Quick Reference (Week 2+)

```python
# DataFrame basics
df.head(10)                   # First 10 rows
df.tail(10)                   # Last 10 rows
df.shape                      # (rows, cols)
df.columns                    # Column names
df.dtypes                     # Data types

# Selection
df['col']                     # Single column (Series)
df[['col1', 'col2']]          # Multiple columns (DataFrame)
df[df['col'] > 5]             # Boolean indexing
df.loc[0]                     # Row by label
df.iloc[0]                    # Row by position

# Sorting
df.sort_values('col')         # Sort by column
df.nlargest(10, 'col')        # Top 10
df.nsmallest(10, 'col')       # Bottom 10

# Groupby
df.groupby('col').sum()       # Sum by group
df.groupby('col').agg({'col2': 'mean', 'col3': 'sum'})

# Filtering
df[df['col'].isin([1,2,3])]   # Filter to values
df[df['col'].between(1, 10)]  # Filter to range
```

