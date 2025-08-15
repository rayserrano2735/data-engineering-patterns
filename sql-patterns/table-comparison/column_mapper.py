#!/usr/bin/env python3
# Filename: column_mapper.py
"""
Interactive Column Mapper for Table Comparison
Maps columns between two tables with different column names
Generates SQL comparison queries with proper column mappings
"""

import json
import sys
from typing import Dict, List, Tuple, Optional
import re
from difflib import SequenceMatcher
from pathlib import Path

class ColumnMapper:
    def __init__(self):
        self.mappings = {}
        self.table1_columns = []
        self.table2_columns = []
        self.join_key_mapping = {}
        
    def similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings."""
        # Normalize strings
        str1 = str1.lower().replace('_', '').replace('-', '')
        str2 = str2.lower().replace('_', '').replace('-', '')
        return SequenceMatcher(None, str1, str2).ratio()
    
    def suggest_mappings(self, table1_cols: List[str], table2_cols: List[str]) -> Dict[str, str]:
        """Suggest column mappings based on name similarity."""
        suggestions = {}
        used_cols = set()
        
        for col1 in table1_cols:
            best_match = None
            best_score = 0
            
            for col2 in table2_cols:
                if col2 in used_cols:
                    continue
                    
                score = self.similarity_score(col1, col2)
                
                # Boost score for common patterns
                if self.common_pattern_match(col1, col2):
                    score += 0.3
                
                if score > best_score and score > 0.6:  # Threshold of 60% similarity
                    best_score = score
                    best_match = col2
            
            if best_match:
                suggestions[col1] = best_match
                used_cols.add(best_match)
        
        return suggestions
    
    def common_pattern_match(self, col1: str, col2: str) -> bool:
        """Check for common column naming patterns."""
        patterns = [
            # Common abbreviations
            (r'cust(omer)?', r'cust(omer)?'),
            (r'prod(uct)?', r'prod(uct)?'),
            (r'qty|quantity', r'qty|quantity'),
            (r'amt|amount', r'amt|amount'),
            (r'desc(ription)?', r'desc(ription)?'),
            (r'addr(ess)?', r'addr(ess)?'),
            (r'num(ber)?', r'num(ber)?|no'),
            (r'dt|date', r'dt|date'),
            (r'ts|timestamp', r'ts|timestamp'),
            # Common prefixes/suffixes
            (r'(.+)_id$', r'(.+)_id$'),
            (r'(.+)_code$', r'(.+)_code$'),
            (r'(.+)_name$', r'(.+)_name$'),
            (r'is_(.+)', r'is_(.+)'),
            (r'has_(.+)', r'has_(.+)'),
        ]
        
        col1_lower = col1.lower()
        col2_lower = col2.lower()
        
        for pattern1, pattern2 in patterns:
            if re.search(pattern1, col1_lower) and re.search(pattern2, col2_lower):
                return True
        return False
    
    def interactive_mapping(self, table1_name: str, table1_cols: List[str], 
                          table2_name: str, table2_cols: List[str]) -> Dict[str, str]:
        """Interactive CLI for mapping columns."""
        print("\n" + "="*60)
        print(f"COLUMN MAPPING: {table1_name} -> {table2_name}")
        print("="*60)
        
        # Get join key mapping first
        print("\n1. JOIN KEY MAPPING")
        print("-" * 40)
        print(f"\n{table1_name} columns: {', '.join(table1_cols)}")
        print(f"{table2_name} columns: {', '.join(table2_cols)}")
        
        join_key1 = input(f"\nEnter join key column for {table1_name}: ").strip()
        join_key2 = input(f"Enter join key column for {table2_name}: ").strip()
        
        self.join_key_mapping = {join_key1: join_key2}
        
        # Get automatic suggestions
        suggestions = self.suggest_mappings(table1_cols, table2_cols)
        
        print("\n2. COLUMN MAPPINGS")
        print("-" * 40)
        print("\nSuggested mappings based on similarity:")
        print(f"{'Table1 Column':<25} {'Table2 Column':<25} {'Similarity':<10}")
        print("-" * 60)
        
        for col1, col2 in suggestions.items():
            score = self.similarity_score(col1, col2)
            print(f"{col1:<25} {col2:<25} {score:.0%}")
        
        use_suggestions = input("\nUse these suggestions? (y/n/edit): ").lower()
        
        if use_suggestions == 'y':
            mappings = suggestions
        elif use_suggestions == 'edit':
            mappings = self.edit_mappings(suggestions, table1_cols, table2_cols)
        else:
            mappings = self.manual_mapping(table1_cols, table2_cols)
        
        # Add join key to mappings
        mappings.update(self.join_key_mapping)
        
        return mappings
    
    def edit_mappings(self, suggestions: Dict[str, str], 
                     table1_cols: List[str], table2_cols: List[str]) -> Dict[str, str]:
        """Edit suggested mappings."""
        mappings = suggestions.copy()
        
        print("\nEdit mappings (press Enter to keep suggestion, '-' to skip column):")
        print("-" * 60)
        
        for col1 in table1_cols:
            if col1 in self.join_key_mapping:
                continue
                
            current = mappings.get(col1, '')
            prompt = f"{col1} -> [{current}]: "
            new_mapping = input(prompt).strip()
            
            if new_mapping == '-':
                mappings.pop(col1, None)
            elif new_mapping:
                mappings[col1] = new_mapping
            elif not current:
                mappings.pop(col1, None)
        
        return mappings
    
    def manual_mapping(self, table1_cols: List[str], table2_cols: List[str]) -> Dict[str, str]:
        """Manual column mapping."""
        mappings = {}
        
        print("\nAvailable columns in table2:")
        for i, col in enumerate(table2_cols, 1):
            print(f"  {i}. {col}")
        
        print("\nMap columns (enter number or column name, '-' to skip):")
        print("-" * 60)
        
        for col1 in table1_cols:
            if col1 in self.join_key_mapping:
                continue
                
            mapping = input(f"{col1} -> ").strip()
            
            if mapping == '-':
                continue
            elif mapping.isdigit():
                idx = int(mapping) - 1
                if 0 <= idx < len(table2_cols):
                    mappings[col1] = table2_cols[idx]
            elif mapping in table2_cols:
                mappings[col1] = mapping
        
        return mappings
    
    def save_mapping(self, mappings: Dict[str, str], filename: str):
        """Save mappings to JSON file."""
        output = {
            "join_key_mapping": self.join_key_mapping,
            "column_mappings": {k: v for k, v in mappings.items() 
                              if k not in self.join_key_mapping}
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\nMappings saved to {filename}")
    
    def load_mapping(self, filename: str) -> Dict[str, str]:
        """Load mappings from JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        mappings = data.get("column_mappings", {})
        mappings.update(data.get("join_key_mapping", {}))
        return mappings
    
    def generate_comparison_sql(self, table1_name: str, table2_name: str, 
                               mappings: Dict[str, str]) -> str:
        """Generate SQL comparison query with column mappings."""
        
        # Separate join key from other mappings
        join_keys = [(k, v) for k, v in mappings.items() 
                     if k in self.join_key_mapping]
        column_mappings = [(k, v) for k, v in mappings.items() 
                          if k not in self.join_key_mapping]
        
        if not join_keys:
            raise ValueError("No join key mapping found!")
        
        join_key1, join_key2 = join_keys[0]
        
        # Build UNION ALL statements for each column
        union_parts = []
        for col1, col2 in column_mappings:
            union_part = f"""
    SELECT 
        COALESCE(t1.{join_key1}, t2.{join_key2}) as key_value,
        '{col1}' as column_name,
        CAST(t1.{col1} AS VARCHAR) as table1_value,
        CAST(t2.{col2} AS VARCHAR) as table2_value
    FROM {table1_name} t1
    FULL OUTER JOIN {table2_name} t2 
        ON t1.{join_key1} = t2.{join_key2}
    WHERE t1.{col1} != t2.{col2}
       OR (t1.{col1} IS NULL AND t2.{col2} IS NOT NULL)
       OR (t1.{col1} IS NOT NULL AND t2.{col2} IS NULL)"""
            union_parts.append(union_part)
        
        sql = f"""-- Table Comparison with Column Mapping
-- Comparing: {table1_name} vs {table2_name}
-- Join Key: {table1_name}.{join_key1} = {table2_name}.{join_key2}

WITH comparison_data AS (
{' UNION ALL '.join(union_parts)}
)
SELECT 
    key_value,
    column_name,
    table1_value,
    table2_value
FROM comparison_data
ORDER BY key_value, column_name;"""
        
        return sql


def main():
    """Main interactive workflow."""
    mapper = ColumnMapper()
    
    print("\n" + "="*60)
    print("  TABLE COLUMN MAPPER & COMPARISON GENERATOR")
    print("="*60)
    
    # Get table information
    table1_name = input("\nEnter first table name: ").strip()
    table1_cols_input = input("Enter columns for table1 (comma-separated): ").strip()
    table1_cols = [col.strip() for col in table1_cols_input.split(',')]
    
    table2_name = input("\nEnter second table name: ").strip()
    table2_cols_input = input("Enter columns for table2 (comma-separated): ").strip()
    table2_cols = [col.strip() for col in table2_cols_input.split(',')]
    
    # Check for existing mapping file
    mapping_file = f"mapping_{table1_name}_{table2_name}.json"
    if Path(mapping_file).exists():
        use_existing = input(f"\nFound existing mapping file: {mapping_file}. Use it? (y/n): ").lower()
        if use_existing == 'y':
            mappings = mapper.load_mapping(mapping_file)
            print("\nLoaded mappings:")
            for k, v in mappings.items():
                print(f"  {k} -> {v}")
        else:
            mappings = mapper.interactive_mapping(table1_name, table1_cols, 
                                                 table2_name, table2_cols)
    else:
        mappings = mapper.interactive_mapping(table1_name, table1_cols, 
                                             table2_name, table2_cols)
    
    # Save mappings
    save = input("\nSave these mappings? (y/n): ").lower()
    if save == 'y':
        mapper.save_mapping(mappings, mapping_file)
    
    # Generate SQL
    print("\n" + "="*60)
    print("GENERATED SQL")
    print("="*60)
    
    sql = mapper.generate_comparison_sql(table1_name, table2_name, mappings)
    print(sql)
    
    # Save SQL to file
    sql_file = f"compare_{table1_name}_{table2_name}.sql"
    save_sql = input(f"\nSave SQL to {sql_file}? (y/n): ").lower()
    if save_sql == 'y':
        with open(sql_file, 'w') as f:
            f.write(sql)
        print(f"SQL saved to {sql_file}")
    
    print("\n✓ Complete! You can now run the generated SQL to compare your tables.")


if __name__ == "__main__":
    main()