# Repository Tools

This folder contains utilities for maintaining and extending the data engineering patterns repository.

## Quick Start

### Adding a New Pattern (Easiest Method)
```bash
# Run the interactive pattern selector
tools\add_pattern.bat

# Select from menu or create new structure
```

### Generate Folder Documentation
```bash
# Interactive tree generator
tools\generate_tree.bat

# Creates markdown-ready folder structure views
```

## Available Tools

### 📁 add_pattern.bat
**Purpose:** Interactive pattern structure selector  
**Usage:** Double-click or run from command line
- Lists all available pattern templates
- Create new patterns from templates
- No need to type file paths

### 🏗️ create_structure.py / create_structure.bat
**Purpose:** Generate folder structures from YAML definitions  
**Usage:** 
```bash
# Using batch wrapper
tools\create_structure.bat

# Direct Python usage
python tools\create_structure.py tools\structures\[pattern].yaml
```
**Safety Features:**
- Won't overwrite existing non-empty files
- Protected paths (tools folder)
- Warning messages for skipped files

### 🌳 generate_tree.py / generate_tree.bat
**Purpose:** Create visual folder structure documentation  
**Usage:**
```bash
# Interactive mode
tools\generate_tree.bat

# Command line
python tools\generate_tree.py --folders-only
python tools\generate_tree.py -o structure.txt
```

### 📝 add-gitkeep-to-empty-folders.bat
**Purpose:** Add .gitkeep files to empty directories for Git tracking  
**Usage:** Run when you have empty folders that need to be committed
```bash
tools\add-gitkeep-to-empty-folders.bat
```

## Structure Definitions

The `structures/` subfolder contains YAML templates for patterns:

### Available Templates
- `structure_full_repo.yaml` - Complete repository structure
- `structure_table_comparison.yaml` - Table comparison pattern
- `structure_pivot_pattern.yaml` - SQL pivot pattern  
- `structure_example_project.yaml` - Template for new patterns

### Creating New Structure Templates
1. Copy `structure_example_project.yaml`
2. Rename to `structure_[your_pattern].yaml`
3. Modify the structure as needed
4. Run `add_pattern.bat` to generate

### YAML Structure Format
```yaml
# Basic folder with files
pattern-category:
  pattern-name:
    __files__:
      - README.md
      - solution.sql
    examples: null  # Empty folder
    tests: null     # Empty folder

# Files with content
pattern-name:
  README.md:
    __content__: |
      # Documentation here
```

## Safety Notes

⚠️ **IMPORTANT:** Never include `tools:` in structure YAMLs - it can overwrite the tools themselves!

The tools have built-in safety features:
- Protected paths (won't overwrite tools folder)
- Skip existing non-empty files
- Warning messages for dangerous operations

## Workflow Examples

### Adding a New SQL Pattern
```bash
1. Run: tools\add_pattern.bat
2. Select: [Create new structure file]
3. Enter: pattern name
4. Edit: the generated YAML if needed
5. Run: tools\add_pattern.bat again
6. Select: your new structure
7. Add: your code files to created folders
8. Commit: git add & push
```

### Document Current Structure
```bash
1. Run: tools\generate_tree.bat
2. Select: Option 1 (folders only)
3. Copy: the output
4. Paste: into your README.md
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No output from tools | Check Python installation: `python --version` |
| YAML not found | Ensure file is in `tools\structures\` |
| Files overwritten | Use updated create_structure.py with safety features |
| Permission denied | Run command prompt as administrator |

## Tool Dependencies

- Python 3.6+ 
- PyYAML (`pip install pyyaml`)
- Windows for .bat files (or use Python directly on Mac/Linux)

---

*These tools make pattern management easy and consistent!* 🛠️