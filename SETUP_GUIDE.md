# Setup Guide - Repository Tools & Structure

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Tool Overview](#tool-overview)
3. [Creating New Pattern Structures](#creating-new-pattern-structures)
4. [Maintaining Repository Structure](#maintaining-repository-structure)
5. [Documentation Tools](#documentation-tools)
6. [Workflow Examples](#workflow-examples)

---

## Initial Setup

### Prerequisites
- **Python 3.6+** - Required for tools
- **Git** - Version control
- **pip** - Python package manager

### First-Time Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/data-engineering-patterns.git
cd data-engineering-patterns

# Install Python dependencies
pip install pyyaml  # For YAML structure definitions

# Verify tools are working
python tools/create_structure.py --examples
python tools/generate_tree.py --help
```

### Windows Users
All tools have batch file wrappers for convenience:
- Double-click any `.bat` file to run interactively
- Or use from command line: `tool_name.bat [arguments]`

---

## Tool Overview

### 🏗️ Structure Generator (`create_structure.py`)
**Purpose**: Create folder structures from YAML/JSON definitions

**Location**: `tools/create_structure.py`

**Features**:
- Data-driven folder creation
- Automatic `.gitkeep` for empty folders
- File creation with content
- Template support

### 🌳 Tree Generator (`generate_tree.py`)
**Purpose**: Create visual folder structure documentation

**Location**: `tools/generate_tree.py`

**Features**:
- Multiple view options (folders only, with files, custom)
- Excludes common directories (.git, node_modules, etc.)
- Cross-platform compatible
- Markdown-ready output

### 📁 GitKeep Manager (`add-gitkeep-to-empty-folders.bat`)
**Purpose**: Add `.gitkeep` files to empty directories for Git tracking

**Location**: `tools/add-gitkeep-to-empty-folders.bat`

**Features**:
- Scans entire repository
- Only adds where needed
- Shows progress
- Safe to run multiple times

---

## Creating New Pattern Structures

### Method 1: Using YAML Definitions (Recommended)

#### Step 1: Create a structure definition
```yaml
# structures/my_new_pattern.yaml
spark-patterns:
  optimization:
    __files__:
      - README.md
      - broadcast_joins.py
      - partition_tuning.py
    examples:
      __files__:
        - large_dataset_example.py
    benchmarks: null  # Empty folder
```

#### Step 2: Generate the structure
```bash
# Using Python directly
python tools/create_structure.py structures/my_new_pattern.yaml

# Using batch wrapper (Windows)
create_structure.bat structures/my_new_pattern.yaml

# Interactive mode
python tools/create_structure.py -i
```

### Method 2: Quick Inline Creation

```bash
# Create simple structure quickly
python tools/create_structure.py --inline '{"new-pattern": {"src": null, "tests": null}}'
```

### Method 3: Using the Full Repository Template

```bash
# Generate entire repository structure
python tools/create_structure.py structure_full_repo.yaml
```

### Structure Definition Syntax

#### Basic Folders
```yaml
parent-folder:
  subfolder1: null  # Empty folder
  subfolder2: null
```

#### Folders with Files
```yaml
parent-folder:
  __files__:
    - file1.py
    - file2.sql
  subfolder:
    __files__:
      - README.md
```

#### Files with Content
```yaml
parent-folder:
  README.md:
    __content__: |
      # Pattern Name
      
      ## Overview
      This pattern does...
  
  main.py:
    __content__: |
      def main():
          print("Pattern implementation")
```

---

## Maintaining Repository Structure

### Adding .gitkeep Files

Empty directories need `.gitkeep` files for Git tracking:

```bash
# Windows
add-gitkeep-to-empty-folders.bat

# The script will:
# 1. Find all empty directories
# 2. Add .gitkeep where missing
# 3. Report what was added
```

### Documenting Structure

Generate tree views for documentation:

```bash
# Interactive mode - choose options
python tools/generate_tree.py -i

# Folders only (clean overview)
python tools/generate_tree.py --folders-only

# Include specific file types
python tools/generate_tree.py -e .sql,.py,.md

# Save to file
python tools/generate_tree.py -o structure.txt

# Then paste into your README.md:
```
repository/
├── folder1/
│   ├── subfolder/
│   └── file.txt
└── folder2/
```
```

---

## Documentation Tools

### Creating Pattern Documentation

Each pattern should have a README following this template:

```markdown
# Pattern Name

## Problem Statement
What challenge does this solve?

## Solution Overview
High-level approach

## Usage
How to implement this pattern

## Code Explanation
Detailed walkthrough

## Examples
Real-world applications

## Best Practices
Tips and considerations

## Database-Specific Notes
Variations for different systems
```

### Generating Documentation Structure

```yaml
# structures/pattern_template.yaml
new-pattern:
  README.md:
    __content__: |
      # Pattern Name
      
      ## Problem Statement
      
      ## Solution Overview
      
      ## Usage
      
      ## Examples
  
  solution.sql: null
  examples:
    example1.sql: null
  tests:
    test_cases.sql: null
```

---

## Workflow Examples

### Workflow 1: Adding a New SQL Pattern

```bash
# 1. Create structure definition
cat > structures/new_sql_pattern.yaml << EOF
sql-patterns:
  my-new-pattern:
    __files__:
      - README.md
      - solution.sql
    examples: null
    tests: null
EOF

# 2. Generate structure
python tools/create_structure.py structures/new_sql_pattern.yaml

# 3. Add your code files
# ... edit files ...

# 4. Generate tree for documentation
python tools/generate_tree.py sql-patterns/my-new-pattern --folders-only

# 5. Commit to Git
git add sql-patterns/my-new-pattern/
git commit -m "Add new SQL pattern: my-new-pattern"
```

### Workflow 2: Setting Up Table Comparison Pattern

```bash
# 1. Generate the structure
python tools/create_structure.py structure_table_comparison.yaml

# 2. Copy in the solution files
copy compare_tables_dynamic.sql sql-patterns/table-comparison/
copy column_mapper.py sql-patterns/table-comparison/
copy TABLE_COMPARISON_USER_GUIDE.md sql-patterns/table-comparison/README.md

# 3. Add example files
# ... create examples ...

# 4. Ensure Git tracking
add-gitkeep-to-empty-folders.bat

# 5. Document the structure
python tools/generate_tree.py sql-patterns/table-comparison -o structure.txt

# 6. Commit everything
git add .
git commit -m "Add table comparison pattern with column mapping"
```

### Workflow 3: Initializing Full Repository

```bash
# 1. Start with the complete structure
python tools/create_structure.py structure_full_repo.yaml

# 2. Verify structure
python tools/generate_tree.py --folders-only

# 3. Add .gitkeep files
add-gitkeep-to-empty-folders.bat

# 4. Commit initial structure
git add .
git commit -m "Initialize repository structure"

# 5. Start adding patterns
# Follow Workflow 1 for each new pattern
```

---

## Best Practices

### 1. Structure Definition Files
- Keep all structure definitions in `tools/structures/`
- Name them descriptively: `structure_[pattern_name].yaml`
- Version control all structure definitions

### 2. Consistency
- Always use the structure generator for new patterns
- Follow the same folder organization for each pattern type
- Include README.md in every pattern folder

### 3. Documentation
- Generate tree views after structural changes
- Update main README.md when adding patterns
- Keep pattern READMEs comprehensive but focused

### 4. Git Workflow
```bash
# Before committing new structures
1. Run add-gitkeep-to-empty-folders.bat
2. Generate tree documentation
3. Update relevant README files
4. Commit with clear message
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Python not found" | Ensure Python is in PATH, or use `python3` |
| "yaml module not found" | Run: `pip install pyyaml` |
| Folders not created | Check YAML syntax, ensure proper indentation |
| .gitkeep not added | Run the gitkeep script after creating structures |
| Tree output too verbose | Use `--folders-only` flag |

### Getting Help

1. Check tool help: `python tools/[tool_name].py --help`
2. Review example structures: `python tools/create_structure.py --examples`
3. Examine existing patterns for reference

---

## Summary

These tools transform repository management from a chore into an automated, consistent process:

- **Define** structures in YAML → **Generate** with one command
- **Document** automatically → **Maintain** consistency
- **Scale** effortlessly → **Share** knowledge

The investment in tooling pays dividends as your pattern library grows!

---

*Make the tools work for you, not the other way around.* 🛠️