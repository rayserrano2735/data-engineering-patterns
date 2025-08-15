#!/usr/bin/env python3
# Filename: generate_tree.py
"""
Cross-platform folder tree generator for documentation
Works on Windows, Linux, and macOS

USAGE EXAMPLES:
--------------
# Interactive mode (with menu)
python generate_tree.py -i

# Basic usage (current directory)
python generate_tree.py

# Folders only
python generate_tree.py --folders-only
python generate_tree.py -f

# Custom extensions
python generate_tree.py -e .sql,.py,.md
python generate_tree.py --extensions .sql,.py,.md

# All files
python generate_tree.py --all
python generate_tree.py -a

# Limited depth
python generate_tree.py -d 3
python generate_tree.py --max-depth 3

# Show hidden files/folders
python generate_tree.py --show-hidden

# Save to file
python generate_tree.py -o structure.txt
python generate_tree.py --output structure.txt

# Combine options
python generate_tree.py --folders-only -d 5 -o folders.txt
python generate_tree.py -f -d 5 -o folders.txt

# Specific directory
python generate_tree.py /path/to/directory
python generate_tree.py ../another-project

MAKING IT EXECUTABLE:
--------------------
Linux/Mac:
  chmod +x generate_tree.py
  ./generate_tree.py -i

Windows batch wrapper (save as generate_tree.bat):
  @echo off
  python generate_tree.py -i
  pause

OUTPUT FORMAT:
-------------
The script generates an ASCII tree structure that can be copied
directly into README.md files inside markdown code blocks:

```
project-root/
├── folder1/
│   ├── subfolder/
│   └── file.txt
└── folder2/
    └── another_file.md
```
"""

import os
import sys
from pathlib import Path
import argparse

# Directories to always exclude
EXCLUDE_DIRS = {
    '.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env',
    '.idea', '.vscode', 'dist', 'build', 'target', '.pytest_cache',
    '.mypy_cache', '.tox', 'htmlcov', '.coverage', 'site-packages'
}

# Files to always exclude
EXCLUDE_FILES = {
    '.gitkeep', '.DS_Store', 'Thumbs.db', '.gitignore'
}

# Common file extensions for data engineering projects
DATA_EXTENSIONS = {
    '.md', '.yml', '.yaml', '.sql', '.py', '.json', '.ini', '.cfg',
    '.conf', '.properties', '.txt', '.csv', '.parquet', '.avro',
    '.sh', '.bat', '.ps1', '.toml', '.rst', '.ipynb'
}

def generate_tree(path=".", prefix="", max_depth=10, current_depth=0, 
                  folders_only=False, file_extensions=None, show_hidden=False):
    """Generate a tree structure of directories and files."""
    
    if current_depth >= max_depth:
        return
    
    path = Path(path)
    
    # Get all items in the directory
    try:
        items = list(path.iterdir())
    except PermissionError:
        return
    
    # Filter directories
    dirs = [item for item in items if item.is_dir() 
            and item.name not in EXCLUDE_DIRS
            and (show_hidden or not item.name.startswith('.'))]
    
    # Filter files
    files = []
    if not folders_only:
        for item in items:
            if item.is_file():
                # Skip excluded files
                if item.name in EXCLUDE_FILES:
                    continue
                # Skip hidden files unless requested
                if not show_hidden and item.name.startswith('.'):
                    continue
                # Check file extensions if specified
                if file_extensions:
                    if '*' in file_extensions or item.suffix.lower() in file_extensions:
                        files.append(item)
                else:
                    files.append(item)
    
    # Sort items
    dirs.sort(key=lambda x: x.name.lower())
    files.sort(key=lambda x: x.name.lower())
    all_items = dirs + files
    
    for i, item in enumerate(all_items):
        is_last = (i == len(all_items) - 1)
        
        # Determine the prefix characters
        current_prefix = "└── " if is_last else "├── "
        next_prefix = "    " if is_last else "│   "
        
        # Add folder indicator
        name = f"{item.name}/" if item.is_dir() else item.name
        
        print(f"{prefix}{current_prefix}{name}")
        
        # Recurse into directories
        if item.is_dir():
            generate_tree(
                item, 
                prefix + next_prefix, 
                max_depth, 
                current_depth + 1,
                folders_only,
                file_extensions,
                show_hidden
            )

def interactive_mode():
    """Interactive mode with menu options."""
    print("=" * 50)
    print("    Folder Tree Generator")
    print("=" * 50)
    print("\nChoose what to display:")
    print("  1. Folders only (no files)")
    print("  2. Folders and important files")
    print("  3. Everything except hidden/system files")
    print("  4. Custom (you'll be prompted for options)")
    print()
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == '1':
        return {
            'folders_only': True,
            'max_depth': 10,
            'file_extensions': None,
            'show_hidden': False
        }
    elif choice == '2':
        return {
            'folders_only': False,
            'max_depth': 10,
            'file_extensions': DATA_EXTENSIONS,
            'show_hidden': False
        }
    elif choice == '3':
        return {
            'folders_only': False,
            'max_depth': 10,
            'file_extensions': {'*'},
            'show_hidden': False
        }
    elif choice == '4':
        # Custom options
        depth = input("\nMaximum depth (default 10): ").strip()
        max_depth = int(depth) if depth else 10
        
        include_files = input("Include files? (y/n, default y): ").strip().lower()
        folders_only = include_files == 'n'
        
        file_extensions = None
        if not folders_only:
            ext_input = input("File extensions to include (comma-separated, e.g., .md,.sql,.py or * for all): ").strip()
            if ext_input and ext_input != '*':
                file_extensions = set()
                for ext in ext_input.split(','):
                    ext = ext.strip()
                    if not ext.startswith('.'):
                        ext = '.' + ext
                    file_extensions.add(ext.lower())
            elif ext_input == '*':
                file_extensions = {'*'}
            else:
                file_extensions = DATA_EXTENSIONS
        
        show_hidden = input("Show hidden files/folders? (y/n, default n): ").strip().lower() == 'y'
        
        return {
            'folders_only': folders_only,
            'max_depth': max_depth,
            'file_extensions': file_extensions,
            'show_hidden': show_hidden
        }
    else:
        print("Invalid choice, using default (folders and important files)")
        return {
            'folders_only': False,
            'max_depth': 10,
            'file_extensions': DATA_EXTENSIONS,
            'show_hidden': False
        }

def main():
    parser = argparse.ArgumentParser(description='Generate a tree view of directory structure')
    parser.add_argument('path', nargs='?', default='.', help='Path to generate tree for (default: current directory)')
    parser.add_argument('--folders-only', '-f', action='store_true', help='Show only folders, no files')
    parser.add_argument('--max-depth', '-d', type=int, default=10, help='Maximum depth to traverse (default: 10)')
    parser.add_argument('--extensions', '-e', help='Comma-separated list of file extensions to include (e.g., .md,.py,.sql)')
    parser.add_argument('--all', '-a', action='store_true', help='Show all files')
    parser.add_argument('--show-hidden', action='store_true', help='Show hidden files and folders')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode with menu')
    parser.add_argument('--output', '-o', help='Output to file instead of console')
    
    args = parser.parse_args()
    
    # If interactive mode, get options from menu
    if args.interactive:
        options = interactive_mode()
        print("\nGenerating tree structure...\n")
    else:
        # Parse file extensions
        file_extensions = None
        if args.all:
            file_extensions = {'*'}
        elif args.extensions:
            file_extensions = set()
            for ext in args.extensions.split(','):
                ext = ext.strip()
                if not ext.startswith('.'):
                    ext = '.' + ext
                file_extensions.add(ext.lower())
        elif not args.folders_only:
            file_extensions = DATA_EXTENSIONS
        
        options = {
            'folders_only': args.folders_only,
            'max_depth': args.max_depth,
            'file_extensions': file_extensions,
            'show_hidden': args.show_hidden
        }
    
    # Redirect output if specified
    if args.output if not args.interactive else False:
        sys.stdout = open(args.output, 'w', encoding='utf-8')
    
    # Print root directory
    root_name = Path(args.path).resolve().name
    print(root_name + "/")
    
    # Generate tree
    generate_tree(args.path, **options)
    
    # Print footer
    print("\nTree structure generated!")
    
    if not args.interactive:
        print("\nTip: Use -i for interactive mode with menu options")
    else:
        print("\n" + "=" * 50)
        print("Copy the tree above and paste into README.md")
        print("=" * 50)
        print("\nYou can also save directly to a file:")
        print(f"  python {sys.argv[0]} -o structure.txt")

if __name__ == "__main__":
    main()