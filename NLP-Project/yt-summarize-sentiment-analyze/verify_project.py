#!/usr/bin/env python3
"""
Project verification script - checks project structure without requiring dependencies.
Run this BEFORE installing dependencies to verify everything is in place.
"""

import os
import sys

def check_file(filepath, description):
    """Check if a file exists."""
    exists = os.path.isfile(filepath)
    status = "✓" if exists else "✗"
    print(f"  [{status}] {description}: {os.path.basename(filepath)}")
    return exists

def check_files():
    """Verify all project files are present."""
    print("\n" + "="*70)
    print("PROJECT STRUCTURE VERIFICATION")
    print("="*70)
    
    all_good = True
    
    print("\nCore Application Files:")
    all_good &= check_file("youtube_nlp_analyzer.py", "Main application")
    all_good &= check_file("config.py", "Configuration module")
    all_good &= check_file("requirements.txt", "Dependencies list")
    
    print("\nDocumentation Files:")
    all_good &= check_file("README.md", "Main documentation")
    all_good &= check_file("QUICKSTART.md", "Quick start guide")
    all_good &= check_file("PROJECT_REPORT.md", "Academic report")
    all_good &= check_file("TESTING.md", "Testing guide")
    all_good &= check_file("START_HERE.txt", "Getting started")
    
    print("\nExample & Demo Files:")
    all_good &= check_file("example_usage.py", "Usage examples")
    all_good &= check_file("ARCHITECTURE.py", "Architecture docs")
    
    print("\nConfiguration Files:")
    all_good &= check_file(".env.example", "Environment template")
    all_good &= check_file(".gitignore", "Git ignore rules")
    
    print("\nProject Specification:")
    all_good &= check_file("project-description.txt", "Requirements")
    all_good &= check_file("project-guidelines.txt", "Guidelines")
    
    print("\n" + "="*70)
    
    if all_good:
        print("✓ ALL FILES PRESENT - Project structure is complete!")
    else:
        print("✗ MISSING FILES - Some files are missing!")
        return False
    
    print("="*70)
    return True

def check_file_sizes():
    """Display file sizes."""
    print("\nFile Sizes:")
    files = [
        "youtube_nlp_analyzer.py",
        "config.py",
        "example_usage.py",
        "README.md",
        "PROJECT_REPORT.md"
    ]
    
    total_size = 0
    for f in files:
        if os.path.isfile(f):
            size = os.path.getsize(f)
            total_size += size
            print(f"  {f}: {size:,} bytes")
    
    print(f"\nTotal size of main files: {total_size:,} bytes (~{total_size/1024:.1f} KB)")

def count_lines():
    """Count lines of code."""
    print("\nLines of Code:")
    files = {
        "youtube_nlp_analyzer.py": "Main application",
        "config.py": "Configuration",
        "example_usage.py": "Examples"
    }
    
    total_lines = 0
    for filepath, description in files.items():
        if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                lines = len(f.readlines())
                total_lines += lines
                print(f"  {description}: {lines} lines")
    
    print(f"\nTotal Python code: {total_lines} lines")

def show_next_steps():
    """Display next steps."""
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("\n1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n2. Configure API key:")
    print("   cp .env.example .env")
    print("   # Edit .env and add your OpenAI API key")
    print("\n3. Test the application:")
    print("   python youtube_nlp_analyzer.py --help")
    print("\n4. Read documentation:")
    print("   cat START_HERE.txt")
    print("   cat QUICKSTART.md")
    print("\n" + "="*70)

def main():
    """Main verification function."""
    print("\n" + "="*70)
    print("YOUTUBE NLP ANALYZER - PROJECT VERIFICATION")
    print("="*70)
    
    # Check we're in the right directory
    if not os.path.isfile("youtube_nlp_analyzer.py"):
        print("\n✗ Error: Not in project directory!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check files
    if not check_files():
        sys.exit(1)
    
    # Show file sizes
    check_file_sizes()
    
    # Count lines
    count_lines()
    
    # Show next steps
    show_next_steps()
    
    print("\n✓ PROJECT VERIFICATION COMPLETE")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
