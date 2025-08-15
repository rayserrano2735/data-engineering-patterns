#!/usr/bin/env python3
# Filename: create_structure.py
"""
Data-driven folder structure generator
Define your structure in YAML or JSON and generate it automatically
"""

import os
import json
import yaml
import argparse
import fnmatch
from pathlib import Path
from typing import Dict, List, Union, Any

class StructureGenerator:
    def __init__(self, add_gitkeep: bool = True):
        self.add_gitkeep = add_gitkeep
        self.created_dirs = []
        self.created_files = []
        # SAFETY: Forbidden paths that should never be overwritten
        self.forbidden_patterns = [
            '**/tools/*.py',
            '**/tools/*.bat', 
            '**/tools/structures/*.yaml',
            '**/tools/structures/*.yml',
            '**/.git/**'
        ]
    
    def is_forbidden_path(self, path: Path) -> bool:
        """Check if a path matches forbidden patterns"""
        import fnmatch
        path_str = str(path).replace('\\', '/')
        for pattern in self.forbidden_patterns:
            if fnmatch.fnmatch(path_str, pattern):
                return True
        return False
    
    def create_structure(self, structure: Union[Dict, List, str], base_path: Path = Path(".")):
        """
        Recursively create folder structure from dictionary/list definition
        
        Structure format:
        - String: Create empty directory
        - List: Create multiple directories at same level
        - Dict: Keys are directories, values are subdirectories/files
        - Dict with special keys:
          - "__files__": List of files to create
          - "__content__": Content for a file
          - "__template__": Template file to copy
        """
        
        if isinstance(structure, str):
            # Simple directory
            dir_path = base_path / structure
            self._create_directory(dir_path)
            
        elif isinstance(structure, list):
            # Multiple items at same level
            for item in structure:
                self.create_structure(item, base_path)
                
        elif isinstance(structure, dict):
            for key, value in structure.items():
                if key == "__files__":
                    # Create files in current directory
                    for filename in value:
                        self._create_file(base_path / filename)
                        
                elif key == "__content__":
                    # This is file content (used with parent key as filename)
                    continue
                    
                elif key.startswith("__"):
                    # Skip other special keys
                    continue
                    
                else:
                    # Check if this is a file with content
                    if isinstance(value, dict) and "__content__" in value:
                        # This is a file with content
                        file_path = base_path / key
                        self._create_file(file_path, value["__content__"])
                    else:
                        # This is a directory
                        dir_path = base_path / key
                        self._create_directory(dir_path)
                        
                        # Recursively create subdirectories/files
                        if value is not None:
                            self.create_structure(value, dir_path)
    
    def _create_directory(self, path: Path):
        """Create a directory and optionally add .gitkeep"""
        path.mkdir(parents=True, exist_ok=True)
        self.created_dirs.append(path)
        
        if self.add_gitkeep:
            gitkeep_path = path / ".gitkeep"
            if not gitkeep_path.exists():
                gitkeep_path.touch()
                self.created_files.append(gitkeep_path)
        
        print(f"📁 Created: {path}")
    
    def _create_file(self, path: Path, content: str = ""):
        """Create a file with optional content"""
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # SAFETY CHECK: Never overwrite existing files with empty content
        if path.exists() and content == "":
            print(f"⚠️  Skipped (exists): {path}")
            return
        
        # SAFETY CHECK: Warn before overwriting non-empty files
        if path.exists() and path.stat().st_size > 0 and content == "":
            print(f"⚠️  WARNING: Skipping overwrite of non-empty file: {path}")
            return
            
        path.write_text(content)
        self.created_files.append(path)
        print(f"📄 Created: {path}")
    
    def print_summary(self):
        """Print summary of what was created"""
        print("\n" + "="*50)
        print(f"✅ Created {len(self.created_dirs)} directories")
        print(f"✅ Created {len(self.created_files)} files")
        print("="*50)


def load_structure_file(filepath: str) -> Dict:
    """Load structure definition from YAML or JSON file"""
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"Structure file not found: {filepath}")
    
    with open(path, 'r') as f:
        if path.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(f)
        elif path.suffix == '.json':
            return json.load(f)
        else:
            # Try JSON first, then YAML
            content = f.read()
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return yaml.safe_load(content)


def create_example_structures():
    """Create example structure definition files"""
    
    # Example 1: Simple structure (YAML)
    yaml_example = """# Simple folder structure
sql-patterns:
  - window-functions
  - joins
  - ctes
  - optimization

spark-patterns:
  - transformations
  - optimizations
  - udfs

airflow-patterns:
  - dags
  - operators
  - sensors
"""
    
    # Example 2: Complex structure with files (YAML)
    yaml_complex = """# Complex structure with files
sql-patterns:
  table-comparison:
    __files__:
      - README.md
      - compare_tables_dynamic.sql
      - compare_tables_with_mapping.sql
      - column_mapper.py
    examples:
      __files__:
        - customer_migration_example.sql
        - mapping_customers.json
        - sample_output.txt
    database-specific:
      __files__:
        - snowflake_version.sql
        - bigquery_version.sql
        - postgres_version.sql
        - mysql_version.sql
  
  window-functions:
    __files__:
      - README.md
      - ranking_examples.sql
      - rolling_aggregates.sql
    examples: null  # Empty folder
    
dbt-patterns:
  macros:
    __files__:
      - generate_alias_name.sql
      - test_helpers.sql
  models:
    staging: null
    intermediate: null
    marts: null
  tests: null
"""
    
    # Example 3: JSON format
    json_example = {
        "data-engineering-patterns": {
            "sql-patterns": {
                "table-comparison": {
                    "__files__": ["README.md", "main.sql"],
                    "examples": None,
                    "database-specific": ["snowflake.sql", "bigquery.sql"]
                },
                "optimization": None
            },
            "spark-patterns": {
                "transformations": None,
                "ml-pipelines": None
            }
        }
    }
    
    # Example 4: Structure with file content
    yaml_with_content = """# Structure with file content
project-template:
  README.md:
    __content__: |
      # Project Name
      
      ## Overview
      This is a template project.
      
      ## Usage
      Add your documentation here.
  
  src:
    __init__.py:
      __content__: |
        # Package initialization
        __version__ = '0.1.0'
    
    main.py:
      __content__: |
        def main():
            print("Hello, World!")
        
        if __name__ == "__main__":
            main()
  
  tests:
    __files__:
      - test_main.py
  
  docs: null  # Empty folder with .gitkeep
"""
    
    # Save examples
    Path("structure_simple.yaml").write_text(yaml_example)
    Path("structure_complex.yaml").write_text(yaml_complex)
    Path("structure_with_content.yaml").write_text(yaml_with_content)
    Path("structure_example.json").write_text(json.dumps(json_example, indent=2))
    
    print("📝 Created example structure files:")
    print("  - structure_simple.yaml")
    print("  - structure_complex.yaml")
    print("  - structure_with_content.yaml")
    print("  - structure_example.json")


def main():
    parser = argparse.ArgumentParser(
        description='Generate folder structures from YAML/JSON definitions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate structure from file
  python create_structure.py structure.yaml
  
  # Generate structure without .gitkeep files
  python create_structure.py structure.yaml --no-gitkeep
  
  # Generate in specific directory
  python create_structure.py structure.yaml --base-path ./my-project
  
  # Create example structure files
  python create_structure.py --examples
  
  # Use inline JSON
  python create_structure.py --inline '{"src": {"models": null, "utils": null}}'

Structure Definition Format:
  Simple list:
    folder1:
      - subfolder1
      - subfolder2
    folder2: null
  
  With files:
    folder:
      __files__:
        - file1.py
        - file2.sql
      subfolder: null
  
  With content:
    folder:
      README.md:
        __content__: |
          # Title
          Content here
        """
    )
    
    parser.add_argument('structure_file', nargs='?', help='YAML or JSON file defining the structure')
    parser.add_argument('--no-gitkeep', action='store_true', help="Don't add .gitkeep files to empty directories")
    parser.add_argument('--base-path', default='.', help='Base path where structure will be created (default: current directory)')
    parser.add_argument('--examples', action='store_true', help='Create example structure definition files')
    parser.add_argument('--inline', help='Inline JSON structure definition')
    
    args = parser.parse_args()
    
    if args.examples:
        create_example_structures()
        return
    
    if args.inline:
        # Use inline JSON structure
        try:
            structure = json.loads(args.inline)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            return
    elif args.structure_file:
        # Load structure from file
        try:
            structure = load_structure_file(args.structure_file)
        except Exception as e:
            print(f"❌ Error loading structure file: {e}")
            return
    else:
        print("❌ Please provide a structure file, use --inline, or use --examples")
        parser.print_help()
        return
    
    # Create the structure
    generator = StructureGenerator(add_gitkeep=not args.no_gitkeep)
    base_path = Path(args.base_path)
    
    print(f"\n🚀 Creating structure in: {base_path.absolute()}")
    print("="*50)
    
    generator.create_structure(structure, base_path)
    generator.print_summary()
    
    print("\n✨ Structure created successfully!")


if __name__ == "__main__":
    main()