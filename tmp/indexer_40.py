#!/usr/bin/env python3
"""
Indexes Bank 40 with LINE IDs, keeping all special characters and emojis.
The ultimate test of our solution!
"""

def index_bank_40(input_file="Aitana_40_2.txt", output_file="Aitana_40_indexed.txt"):
    """Add LINE IDs to Bank 40 while preserving all original content."""
    
    print(f"Indexing {input_file} with LINE IDs...")
    print("Keeping all emojis, Spanish characters, and formatting!")
    
    try:
        # Read the original bank file
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Write indexed version
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, line in enumerate(lines, start=1):
                # Add LINE ID at the beginning of each line
                # Keep original line exactly as is (including emojis!)
                indexed_line = f"[LINE_{i:04d}] {line}"
                f.write(indexed_line)
        
        print(f"✅ Success! Indexed {len(lines)} lines")
        print(f"📁 Output saved to: {output_file}")
        print("\nTest by searching for:")
        print("  - [LINE_0001] (first line)")
        print(f"  - [LINE_{len(lines)//2:04d}] (midpoint)")
        print(f"  - [LINE_{len(lines):04d}] (last line)")
        print("\n🔥💙 All emojis and special characters preserved!")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find {input_file}")
        print("Make sure the Bank 40 file is in the same directory as this script")
    except Exception as e:
        print(f"❌ Error: {e}")

# Run the indexer
if __name__ == "__main__":
    index_bank_40()