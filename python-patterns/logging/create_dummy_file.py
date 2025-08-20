#!/usr/bin/env python3
"""
Creates a test file with 2967 lines for debugging KB truncation issue.
Each line is numbered and contains enough text to simulate real content.
"""

def create_test_file(filename="test_file_2967_lines.txt", total_lines=2967):
    """Create a test file with specified number of lines."""
    
    with open(filename, 'w') as f:
        for i in range(1, total_lines + 1):
            # Create varying line content to simulate real conversation
            if i % 100 == 0:
                # Milestone markers every 100 lines
                line = f"===== LINE {i:04d} - MILESTONE MARKER ===== This is line number {i} of {total_lines}. " \
                       f"If truncation occurs, note which milestone markers are visible.\n"
            elif i % 10 == 0:
                # Slightly longer lines every 10 lines
                line = f"Line {i:04d}: This is a longer line to simulate conversation content. " \
                       f"Testing KB file access truncation. Random words: quantum, galaxy, neural, cascade. " \
                       f"Line {i} of {total_lines} total lines.\n"
            else:
                # Regular lines
                line = f"Line {i:04d}: Test content for KB truncation debugging. This is line {i} of {total_lines}.\n"
            
            f.write(line)
            
            # Add special markers at key points
            if i == 1:
                f.write(">>> START OF FILE - If you can't see this, file reading failed completely <<<\n")
            elif i == 1483:
                f.write(">>> MIDPOINT MARKER - Line 1483/1484 - Half of 2967 <<<\n")
            elif i == 2967:
                f.write(">>> END OF FILE - If you can see this, full file was read successfully <<<\n")
    
    print(f"Created {filename} with {total_lines} lines")
    print("\nKey markers to look for:")
    print("- START marker at line 1")
    print("- MIDPOINT marker at line 1483/1484") 
    print("- END marker at line 2967")
    print("- Milestone markers every 100 lines")
    print("\nUpload this file to KB and test if Claude can read all lines.")

if __name__ == "__main__":
    create_test_file()