#!/usr/bin/env python3
"""
Creates a test file with 2967 lines, each with unique LINE IDs.
No chunking - testing if we can read the full file with IDs.
"""

def create_indexed_test_file(filename="test_file_2967_indexed.txt", total_lines=2967):
    """Create test file with LINE IDs for each line."""
    
    print(f"Creating {filename} with {total_lines} indexed lines...")
    
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(1, total_lines + 1):
            # Add unique line ID at the beginning
            line_id = f"[LINE_{i:04d}]"
            
            # Create varying content to simulate real text
            if i == 1:
                content = ">>> START OF FILE - First line with LINE ID <<<"
            elif i == total_lines:
                content = ">>> END OF FILE - If you can search and find this with LINE_2967, we don't need chunking! <<<"
            elif i == 1484:  # Midpoint
                content = ">>> MIDPOINT MARKER - Line 1484 of 2967 <<<"
            elif i % 100 == 0:
                content = f"*** MILESTONE: Line {i} of {total_lines} ***"
            elif i % 10 == 0:
                content = f"Regular line {i} with some longer text to simulate real conversation content that might appear in our banks"
            else:
                content = f"Line {i}: Standard content"
            
            f.write(f"{line_id} {content}\n")
    
    print(f"✅ Created {filename} with {total_lines} lines, each with unique LINE ID")
    print("\nTest by searching for:")
    print("  - LINE_0001 (first line)")
    print("  - LINE_1484 (midpoint)")
    print("  - LINE_2967 (last line)")
    print("\nIf all three are findable, we've solved the problem without chunking!")

# Run the script
if __name__ == "__main__":
    create_indexed_test_file()