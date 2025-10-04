#!/usr/bin/env python3
"""
Setup Python Analytics Interview Prep Repository
VERSION: 0.5

Smart installer with runtime merge intelligence.
Detects existing state and applies appropriate updates.

USAGE:
    cd to your GitHub directory (or wherever you want the repo)
    python path/to/setup_python_interview_prep.py [options]
    
OPTIONS:
    --mode local   : Create/update local repository only (default)
    --mode docker  : Build Docker image only
    --mode all     : Create repository and build Docker image

PRESERVES:
    Your work in practice_work/, notes/, mock_interviews/ is never overwritten
    
UPDATES:
    All course materials to latest version
    Migrates flat structure to organized if needed
    Removes obsolete files automatically
"""

import os
import sys
import argparse
import base64
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Repository name
REPO_NAME = "python-analytics-interview-prep"

# Version
VERSION = "0.5"

# ============================================================================
# EMBEDDED CONTENT DEFINITIONS
# All learning materials are defined here
# ============================================================================

# Course content files
COURSE_CONTENT = {
    'docs/course_with_schedule.md': '''# Python Analytics Engineering Interview Prep Course

## Course Overview

This comprehensive course teaches Python from fundamentals through interview-ready patterns in 21 days.

**Structure:**
- 6 Learning Modules (concepts with examples)
- 60 Progressive Exercises (10 per module)
- 70 Flashcards (aligned with modules)
- 21-Day Study Schedule

**Daily Commitment:** 90-120 minutes

---

# Module 1: Python Data Structures & Operations

## Lists and List Operations

Lists are ordered, mutable collections - the foundation of data manipulation in Python.

```python
# Creating and accessing lists
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# Indexing and slicing
first = numbers[0]         # 1
last = numbers[-1]         # 5
subset = numbers[1:3]      # [2, 3]
reversed = numbers[::-1]   # [5, 4, 3, 2, 1]
```

[Content continues...]
''',

    'docs/talking_points.md': '''# Talking Points - How to Discuss Your Solutions Professionally

## The Meta-Strategy

Remember: They're not just evaluating your code. They're evaluating whether they want to work with you for the next 2+ years.

[Content continues...]
''',

    'docs/quick_reference.md': '''# Quick Reference - Python Analytics Engineering Syntax

Rapid lookup during interviews. No explanations, just syntax.

## Lists

```python
lst = [1, 2, 3]
lst.append(4)                 # Add single item
lst.extend([5, 6])            # Add multiple items
[Content continues...]
```
''',

    # Note: README.md will be in root, not docs/

    'docs/GETTING_STARTED.md': '''# Getting Started - Python Analytics Interview Prep Platform

## Quick Start (5 Minutes)

[Full getting started content...]
''',

    # README goes in root, not docs
    'README.md': '''# Python Analytics Interview Prep Platform

## Quick Start

1. Review the Pattern Matcher for problem recognition
2. Study Group A patterns (critical for interviews)  
3. Practice with exercises.py
4. Drill flashcards daily

## Repository Structure

```
python-analytics-interview-prep/
├── README.md              # This file (in root)
├── src/                   # Python source code
├── docs/                  # Documentation
├── data/                  # Data files
├── docker/                # Docker configuration
├── practice_work/         # Your work (preserved)
├── notes/                 # Your notes (preserved)
└── docker-compose.yml
```

[Content continues...]
''',
}

# Python source files
PYTHON_SOURCE = {
    'src/exercises.py': '''#!/usr/bin/env python3
"""
Python Analytics Interview Prep - Progressive Exercises
60 exercises mapped to course modules with solutions
"""

import pandas as pd
import numpy as np

# Module 1 Exercises: Data Structures
def exercise_1_1():
    """EASY: Create a list of numbers 1-10 and return only even numbers."""
    numbers = list(range(1, 11))
    evens = [x for x in numbers if x % 2 == 0]
    return evens

[Content continues with all 60 exercises...]
''',

    'src/patterns_and_gotchas.py': '''#!/usr/bin/env python3
"""
Patterns and Gotchas - Complete Implementation Reference
Analytics Engineering Interview Patterns
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple

class CorePatterns:
    """The 20 patterns that solve 80% of interview problems."""
    
    @staticmethod
    def top_n_by_group(df: pd.DataFrame, group_col: str, value_col: str, n: int = 5) -> pd.DataFrame:
        """Find top N items by value within each group."""
        return (df
                .sort_values(value_col, ascending=False)
                .groupby(group_col)
                .head(n))

[Content continues with all patterns...]
''',
}

# Documentation files (already embedded above in COURSE_CONTENT, but separating key platform docs)
PLATFORM_DOCS = {
    'docs/RELEASE_NOTES.md': '''# RELEASE NOTES - Python Analytics Interview Prep Platform

## Current Production Version: 3.2.6

### Version 3.2.6 - Base64 Fix
- Fixed: Handle placeholder text in binary files
- Fixed: Proper error handling for invalid base64 content
- Added: Skip binary files with placeholder content

[Full release notes content...]
''',

    'docs/PLATFORM_ARCHITECTURE.md': '''# Platform Architecture - Python Analytics Interview Prep

Technical architecture of the interview prep platform.

[Full content from the file we just created]
''',
}

# Docker configuration
DOCKER_CONFIG = {
    'docker/requirements.txt': '''numpy==2.3.3
pandas==2.3.3
python-dateutil==2.9.0.post0
pytz==2025.2
six==1.17.0
tzdata==2025.2
openpyxl==3.1.2
''',

    'docker/Dockerfile': '''FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York

# Install desktop environment and dependencies
RUN apt-get update && apt-get install -y \\
    xfce4 xfce4-terminal xfce4-goodies \\
    tightvncserver novnc websockify \\
    supervisor sudo wget curl git nano \\
    build-essential software-properties-common \\
    && apt-get clean

[Full Dockerfile content...]
''',

    'docker-compose.yml': '''version: '3.8'

services:
  interview-prep:
    build:
      context: .
      dockerfile: docker/Dockerfile
    image: interview-prep:latest
    container_name: python-interview-prep
    ports:
      - "5901:5901"
      - "6901:6901"
    volumes:
      - ./practice_work:/home/student/interview-prep/practice_work
      - ./notes:/home/student/interview-prep/notes
    environment:
      - DISPLAY=:1
      - VNC_PASSWORD=student
    restart: unless-stopped
''',
}

# Data files (text format)
# Data files (pipe-delimited flashcards - ready for Cram.com)
# Note: Flashcards are generated dynamically to handle multi-line code properly
def generate_flashcards():
    """Generate flashcard content with proper formatting"""
    cards = []
    cards.append(("Front", "Back", "Category"))
    
    # Pattern Recognition cards (20)
    cards.append(("Find top 5 products by revenue in each region", "df.sort_values('revenue', ascending=False).groupby('region').head(5)", "Pattern Recognition"))
    cards.append(("Get bottom 3 items by score per category", "df.sort_values('score').groupby('category').head(3)", "Pattern Recognition"))
    cards.append(("Remove duplicates keeping first occurrence", "df.drop_duplicates(keep='first')", "Pattern Recognition"))
    cards.append(("Remove duplicates based on specific columns", "df.drop_duplicates(subset=['col1', 'col2'])", "Pattern Recognition"))
    cards.append(("Calculate 7-day rolling average", "df['metric'].rolling(window=7).mean()", "Pattern Recognition"))
    cards.append(("Calculate cumulative sum by group", "df.groupby('group')['value'].cumsum()", "Pattern Recognition"))
    cards.append(("Group by category and sum values", "df.groupby('category')['value'].sum()", "Pattern Recognition"))
    cards.append(("Group by multiple columns with multiple aggregations", "df.groupby(['cat1', 'cat2']).agg({'val': 'sum', 'qty': 'mean'})", "Pattern Recognition"))
    cards.append(("Filter rows where column > threshold", "df[df['column'] > threshold]", "Pattern Recognition"))
    cards.append(("Filter rows with multiple conditions", "df[(df['col1'] > 5) & (df['col2'] == 'value')]", "Pattern Recognition"))
    cards.append(("Merge two dataframes on a key", "pd.merge(df1, df2, on='key', how='left')", "Pattern Recognition"))
    cards.append(("Merge with different column names", "pd.merge(df1, df2, left_on='id', right_on='user_id')", "Pattern Recognition"))
    cards.append(("Fill missing values with a constant", "df['column'].fillna(0)", "Pattern Recognition"))
    cards.append(("Fill missing values with mean", "df['column'].fillna(df['column'].mean())", "Pattern Recognition"))
    cards.append(("Forward fill missing values", "df.fillna(method='ffill')", "Pattern Recognition"))
    cards.append(("Find rows with any null values", "df[df.isnull().any(axis=1)]", "Pattern Recognition"))
    cards.append(("Count null values per column", "df.isnull().sum()", "Pattern Recognition"))
    cards.append(("Pivot table with values and aggregation", "df.pivot_table(values='sales', index='region', columns='product', aggfunc='sum')", "Pattern Recognition"))
    cards.append(("Rank items within groups", "df.groupby('group')['value'].rank(method='dense', ascending=False)", "Pattern Recognition"))
    cards.append(("Get year-over-year change", "df.groupby('category')['sales'].pct_change(periods=12)", "Pattern Recognition"))
    
    # Gotchas cards (15) - with multi-line code
    cards.append(("Sort a list WITHOUT using .sort() or sorted()", "for i in range(len(arr)):\\n    for j in range(i+1, len(arr)):\\n        if arr[i] > arr[j]:\\n            arr[i], arr[j] = arr[j], arr[i]", "Gotchas"))
    cards.append(("Group data WITHOUT using .groupby()", "result = {}\\nfor row in df.itertuples():\\n    key = row.category\\n    if key not in result:\\n        result[key] = []\\n    result[key].append(row.value)", "Gotchas"))
    cards.append(("Remove duplicates WITHOUT .drop_duplicates()", "seen = set()\\nresult = []\\nfor item in items:\\n    if item not in seen:\\n        seen.add(item)\\n        result.append(item)", "Gotchas"))
    cards.append(("Find max WITHOUT using max()", "max_val = float('-inf')\\nfor val in values:\\n    if val > max_val:\\n        max_val = val", "Gotchas"))
    cards.append(("Count occurrences WITHOUT value_counts()", "counts = {}\\nfor val in series:\\n    counts[val] = counts.get(val, 0) + 1", "Gotchas"))
    cards.append(("Reverse a list WITHOUT [::-1] or reverse()", "reversed_list = []\\nfor i in range(len(lst)-1, -1, -1):\\n    reversed_list.append(lst[i])", "Gotchas"))
    cards.append(("Flatten nested list WITHOUT itertools", "flat = []\\nfor sublist in nested:\\n    for item in sublist:\\n        flat.append(item)", "Gotchas"))
    cards.append(("Join strings WITHOUT .join()", "result = ''\\nfor i, s in enumerate(strings):\\n    result += s\\n    if i < len(strings) - 1:\\n        result += delimiter", "Gotchas"))
    cards.append(("Filter list WITHOUT list comprehension or filter()", "result = []\\nfor item in items:\\n    if condition(item):\\n        result.append(item)", "Gotchas"))
    cards.append(("Create dict from two lists WITHOUT zip()", "d = {}\\nfor i in range(len(keys)):\\n    d[keys[i]] = values[i]", "Gotchas"))
    cards.append(("Check if all elements true WITHOUT all()", "all_true = True\\nfor val in values:\\n    if not val:\\n        all_true = False\\n        break", "Gotchas"))
    cards.append(("Check if any element true WITHOUT any()", "any_true = False\\nfor val in values:\\n    if val:\\n        any_true = True\\n        break", "Gotchas"))
    cards.append(("Find index WITHOUT .index()", "idx = -1\\nfor i, val in enumerate(lst):\\n    if val == target:\\n        idx = i\\n        break", "Gotchas"))
    cards.append(("Sum values WITHOUT sum()", "total = 0\\nfor val in values:\\n    total += val", "Gotchas"))
    cards.append(("Get unique values WITHOUT set()", "unique = []\\nfor val in values:\\n    if val not in unique:\\n        unique.append(val)", "Gotchas"))
    
    # Syntax Essentials cards (15)
    cards.append(("Read CSV file with pandas", "pd.read_csv('file.csv')", "Syntax Essentials"))
    cards.append(("Read CSV with specific delimiter", "pd.read_csv('file.csv', sep='|')", "Syntax Essentials"))
    cards.append(("Save dataframe to CSV", "df.to_csv('output.csv', index=False)", "Syntax Essentials"))
    cards.append(("Create empty dataframe with columns", "pd.DataFrame(columns=['col1', 'col2', 'col3'])", "Syntax Essentials"))
    cards.append(("Add new column to dataframe", "df['new_col'] = values", "Syntax Essentials"))
    cards.append(("Rename columns", "df.rename(columns={'old': 'new'})", "Syntax Essentials"))
    cards.append(("Drop columns", "df.drop(columns=['col1', 'col2'])", "Syntax Essentials"))
    cards.append(("Reset index after operations", "df.reset_index(drop=True)", "Syntax Essentials"))
    cards.append(("Apply function to column", "df['col'].apply(lambda x: x * 2)", "Syntax Essentials"))
    cards.append(("Convert string to datetime", "pd.to_datetime(df['date_string'])", "Syntax Essentials"))
    cards.append(("Get value counts", "df['column'].value_counts()", "Syntax Essentials"))
    cards.append(("Check data types", "df.dtypes", "Syntax Essentials"))
    cards.append(("Get dataframe shape", "df.shape", "Syntax Essentials"))
    cards.append(("Get first n rows", "df.head(n)", "Syntax Essentials"))
    cards.append(("Sample random rows", "df.sample(n=100)", "Syntax Essentials"))
    
    # Comprehensions cards (5)
    cards.append(("Basic list comprehension syntax", "[expression for item in iterable if condition]", "Comprehensions"))
    cards.append(("List comprehension with conditional expression", "['even' if x % 2 == 0 else 'odd' for x in range(5)]", "Comprehensions"))
    cards.append(("Nested list comprehension for flattening", "[item for sublist in matrix for item in sublist]", "Comprehensions"))
    cards.append(("Dictionary comprehension", "{key: value for key, value in items.items() if condition}", "Comprehensions"))
    cards.append(("Set comprehension to get unique values", "{x**2 for x in numbers}", "Comprehensions"))
    
    # Lambda Functions cards (5)
    cards.append(("Lambda function basic syntax", "lambda arguments: expression", "Lambda Functions"))
    cards.append(("Sort with lambda by specific key", "sorted(data, key=lambda x: x['age'])", "Lambda Functions"))
    cards.append(("Apply lambda to pandas column", "df['col'].apply(lambda x: x * 2 if x > 0 else 0)", "Lambda Functions"))
    cards.append(("Map with lambda function", "list(map(lambda x: x**2, numbers))", "Lambda Functions"))
    cards.append(("Filter with lambda function", "list(filter(lambda x: x % 2 == 0, numbers))", "Lambda Functions"))
    
    # Error Handling cards (5)
    cards.append(("Basic try-except structure", "try:\\n    risky_operation()\\nexcept Exception as e:\\n    handle_error(e)", "Error Handling"))
    cards.append(("Handle multiple exception types", "try:\\n    code\\nexcept ValueError:\\n    handle_value\\nexcept KeyError:\\n    handle_key", "Error Handling"))
    cards.append(("Try-except with finally clause", "try:\\n    open_file()\\nexcept:\\n    handle_error()\\nfinally:\\n    close_file()", "Error Handling"))
    cards.append(("Retry logic with exponential backoff", "for i in range(retries):\\n    try:\\n        operation()\\n        break\\n    except:\\n        sleep(2**i)", "Error Handling"))
    cards.append(("Using context manager for files", "with open('file.txt', 'r') as f:\\n    data = f.read()", "Error Handling"))
    
    # Functions cards (5)
    cards.append(("Function with default arguments", "def func(data, method='mean', nulls=True):\\n    process(data)", "Functions"))
    cards.append(("Avoid mutable default arguments", "def func(item, target=None):\\n    if target is None:\\n        target = []", "Functions"))
    cards.append(("Function with *args and **kwargs", "def func(*args, **kwargs):\\n    positional = args\\n    keyword = kwargs", "Functions"))
    cards.append(("Return multiple values from function", "def func():\\n    return value1, value2, value3", "Functions"))
    cards.append(("Closure - function returning function", "def outer(x):\\n    def inner(y):\\n        return x + y\\n    return inner", "Functions"))
    
    # Convert to pipe-delimited format (replace \\n with actual newlines in output)
    result = []
    for front, back, category in cards:
        # Replace \\n with actual newlines for the output file
        back = back.replace('\\n', '\n')
        result.append(f"{front}|{back}|{category}")
    
    return '\n'.join(result)

DATA_FILES = {
    'data/flashcards_complete.txt': generate_flashcards(),
}

# ============================================================================
# RUNTIME MERGE ENGINE
# ============================================================================

class SmartMergeEngine:
    """Intelligent merge engine that makes runtime decisions."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.repo_path = base_path / REPO_NAME
        self.existing_structure = None
        self.user_modifications = set()
        
    def detect_structure(self) -> str:
        """Detect current repository structure."""
        if not self.repo_path.exists():
            return 'none'
        
        # Check for organized structure markers
        if (self.repo_path / 'src').exists() and (self.repo_path / 'docs').exists():
            return 'organized'
        
        # Check for flat structure markers
        if (self.repo_path / 'exercises.py').exists():
            return 'flat'
            
        return 'unknown'
    
    def scan_user_modifications(self):
        """Identify files that user has modified."""
        # For now, preserve all files in protected directories
        protected_dirs = ['practice_work', 'notes', 'mock_interviews']
        for dir_name in protected_dirs:
            dir_path = self.repo_path / dir_name
            if dir_path.exists():
                for file_path in dir_path.rglob('*'):
                    if file_path.is_file():
                        self.user_modifications.add(str(file_path.relative_to(self.repo_path)))
    
    def should_update_file(self, relative_path: str) -> bool:
        """Determine if a file should be updated."""
        # Never update user work
        protected_dirs = ['practice_work', 'notes', 'mock_interviews']
        for protected in protected_dirs:
            if relative_path.startswith(protected):
                return False
        
        # Update everything else
        return True
    
    def create_file_with_subdirs(self, relative_path: str, content: str, binary: bool = False):
        """
        Create a file, ensuring all subdirectories exist.
        
        FIXED: Handles placeholder text in binary files
        """
        full_path = self.repo_path / relative_path
        
        # Ensure parent directories exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content
        if binary:
            # Check if content is just a placeholder
            if '[BASE64_ENCODED' in content or 'PLACEHOLDER' in content.upper():
                print(f"  ⚠ Skipping {relative_path} (placeholder content)")
                return
                
            try:
                # Decode base64 for binary files
                import base64
                # Clean up any whitespace
                content = ''.join(content.split())
                # Add padding if needed
                while len(content) % 4:
                    content += '='
                decoded_content = base64.b64decode(content)
                full_path.write_bytes(decoded_content)
            except Exception as e:
                print(f"  ⚠ Skipping {relative_path} (invalid base64: {e})")
                return
        else:
            full_path.write_text(content, encoding='utf-8')
    
    def migrate_flat_to_organized(self):
        """Migrate from flat structure to organized structure."""
        print("  → Migrating from flat to organized structure...")
        
        migrations = {
            'exercises.py': 'src/exercises.py',
            'patterns_and_gotchas.py': 'src/patterns_and_gotchas.py',
            'flashcards_complete.xlsx': 'data/flashcards_complete.xlsx',
            'course_with_schedule.md': 'docs/course_with_schedule.md',
            'talking_points.md': 'docs/talking_points.md',
            'quick_reference.md': 'docs/quick_reference.md',
            'README.md': 'docs/README.md',
        }
        
        for old_path, new_path in migrations.items():
            old_file = self.repo_path / old_path
            if old_file.exists():
                new_file = self.repo_path / new_path
                new_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_file), str(new_file))
                print(f"    Moved {old_path} → {new_path}")
    
    def clean_obsolete_files(self):
        """Remove files that no longer exist in the platform."""
        obsolete = [
            'ARCHITECTURE.md',  # Old, replaced by PLATFORM_ARCHITECTURE.md
            'consolidator.py',  # Old approach, no longer used
            'docs/ARCHITECTURE.md',  # Might be in docs folder
            'setup_complete.py',  # Old generated file
            'docs/SETUP.md',  # Duplicate - using GETTING_STARTED.md
            'SETUP.md',  # Old location
            'docs/README.md',  # README should be in root
            'PROJECT_STATUS.md',  # Renamed to RELEASE_NOTES.md
            'docs/PROJECT_STATUS.md',  # Old name
            'docs/SETUP_GUIDE.md',  # Replaced by GETTING_STARTED.md
            'SETUP_GUIDE.md',  # Old location
            'data/flashcards_complete.xlsx',  # Replaced with .txt for Cram.com
        ]
        
        for file_path in obsolete:
            full_path = self.repo_path / file_path
            if full_path.exists():
                full_path.unlink()
                print(f"  ✓ Removed obsolete file: {file_path}")
    
    def apply_updates(self):
        """Apply all updates based on runtime analysis."""
        
        # Detect current state
        structure = self.detect_structure()
        print(f"\n📁 Detected structure: {structure}")
        
        if structure == 'none':
            print("\n🚀 Performing fresh installation...")
            self.fresh_install()
        else:
            print("\n🔄 Updating existing repository...")
            
            # Scan for user modifications
            self.scan_user_modifications()
            
            # Migrate if needed
            if structure == 'flat':
                self.migrate_flat_to_organized()
            
            # Update files
            self.update_files()
            
            # Clean obsolete
            self.clean_obsolete_files()
        
        # Ensure user directories exist
        self.ensure_user_directories()
        
        # Create .gitignore
        self.create_gitignore()
        
        # Create requirements.txt
        self.create_requirements()
        
        print("\n✅ Platform setup complete!")
    
    def fresh_install(self):
        """Perform a fresh installation."""
        self.repo_path.mkdir(parents=True, exist_ok=True)
        
        # Create all files
        all_content = {
            **COURSE_CONTENT,
            **PYTHON_SOURCE,
            **PLATFORM_DOCS,
            **DOCKER_CONFIG,
            **DATA_FILES,
        }
        
        for relative_path, content in all_content.items():
            self.create_file_with_subdirs(relative_path, content)
            print(f"  ✓ Created {relative_path}")
    
    def update_files(self):
        """Update existing files selectively."""
        all_content = {
            **COURSE_CONTENT,
            **PYTHON_SOURCE,
            **PLATFORM_DOCS,
            **DOCKER_CONFIG,
            **DATA_FILES,
        }
        
        for relative_path, content in all_content.items():
            if self.should_update_file(relative_path):
                self.create_file_with_subdirs(relative_path, content)
                print(f"  ✓ Updated {relative_path}")
    
    def ensure_user_directories(self):
        """Ensure user work directories exist."""
        user_dirs = [
            'practice_work',
            'notes',
            'mock_interviews',
        ]
        
        for dir_name in user_dirs:
            dir_path = self.repo_path / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                # Add .gitkeep
                (dir_path / '.gitkeep').write_text('')
                print(f"  ✓ Created user directory: {dir_name}/")
    
    def create_gitignore(self):
        """Create .gitignore file."""
        gitignore_content = """# Python
__pycache__/
*.pyc
.pytest_cache/

# Virtual Environment
venv/
env/
.env

# IDE
.idea/
.vscode/
*.swp
*.swo
.DS_Store

# Wing IDE
*.wpr
*.wpu

# Jupyter
.ipynb_checkpoints/
*.ipynb

# User work (preserved but not committed)
practice_work/*
!practice_work/.gitkeep
notes/*
!notes/.gitkeep
mock_interviews/*
!mock_interviews/.gitkeep
"""
        gitignore_path = self.repo_path / '.gitignore'
        gitignore_path.write_text(gitignore_content)
        print("  ✓ Created .gitignore")
    
    def create_requirements(self):
        """Create requirements.txt file."""
        requirements_content = """# Python Analytics Interview Prep - Requirements
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.0.0  # For Excel file handling
"""
        requirements_path = self.repo_path / 'requirements.txt'
        requirements_path.write_text(requirements_content)
        print("  ✓ Created requirements.txt")

# ============================================================================
# DOCKER BUILDER
# ============================================================================

class DockerBuilder:
    """Handles Docker image building."""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        
    def find_wing_deb(self) -> Path:
        """Search for Wing Pro .deb file."""
        search_locations = [
            Path.home() / 'Downloads',
            Path.cwd(),
            Path(__file__).parent,
        ]
        
        for location in search_locations:
            if location.exists():
                for file in location.glob('wing-pro*.deb'):
                    return file
        
        return None
    
    def build_image(self):
        """Build Docker image."""
        print("\n🐳 Building Docker image...")
        
        # Check if Wing .deb exists
        wing_deb = self.find_wing_deb()
        if wing_deb:
            # Copy to docker directory
            docker_wing = self.repo_path / 'docker' / wing_deb.name
            shutil.copy2(wing_deb, docker_wing)
            print(f"  ✓ Found Wing Pro: {wing_deb.name}")
        else:
            print("  ⚠ Wing Pro not found, will use JupyterLab instead")
        
        # Build image
        os.chdir(self.repo_path)
        result = os.system('docker compose build')
        
        if result == 0:
            print("\n✅ Docker image built successfully!")
            print("\nTo start the container:")
            print("  docker compose up")
            print("\nThen access at: http://localhost:6901")
            print("  Password: student")
        else:
            print("\n⚠ Docker build failed. Check Docker is running.")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point for setup script."""
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Setup Python Analytics Interview Prep Platform')
    parser.add_argument('--mode', 
                       choices=['local', 'docker', 'all'],
                       default='local',
                       help='Setup mode: local (default), docker, or all')
    
    args = parser.parse_args()
    
    # Display header
    print("=" * 60)
    print(f"Python Analytics Interview Prep Platform Setup v{VERSION}")
    print("=" * 60)
    
    # Determine base path
    base_path = Path.cwd()
    repo_path = base_path / REPO_NAME
    
    # Initialize merge engine
    merger = SmartMergeEngine(base_path)
    
    # Apply updates based on mode
    if args.mode in ['local', 'all']:
        merger.apply_updates()
    
    # Build Docker if requested
    if args.mode in ['docker', 'all']:
        if not repo_path.exists():
            print("\n⚠ Repository must exist before building Docker image.")
            print("  Run with --mode local first.")
            sys.exit(1)
        
        builder = DockerBuilder(repo_path)
        builder.build_image()
    
    # Final instructions
    if args.mode == 'local':
        print(f"\n📂 Repository ready at: {repo_path}")
        print("\nNext steps:")
        print("  1. cd python-analytics-interview-prep")
        print("  2. pip install -r requirements.txt")
        print("  3. Start with README.md")
    
    print("\n" + "=" * 60)
    print("🎯 Ready for interview prep!")
    print("=" * 60)

if __name__ == "__main__":
    main()
