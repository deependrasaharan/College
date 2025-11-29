#!/usr/bin/env python3
"""
🚀 QUICK START - BFS Traversal GUI
Launch this for immediate demo!
"""

import os
import sys

def print_banner():
    """Print welcome banner."""
    print("\n" + "="*60)
    print("🌐 BFS TRAVERSAL - GRAPH BUILDER GUI".center(60))
    print("="*60)
    print("\n✨ Complete Graph Theory Learning Tool ✨\n")

def print_menu():
    """Print quick start menu."""
    print("📋 Quick Start Options:")
    print("-" * 60)
    print("1. Launch GUI (Main Program) ⭐")
    print("2. Launch CLI (Text Version)")
    print("3. View Demo Guide")
    print("4. Show Feature List")
    print("5. Show Help")
    print("6. Exit")
    print("-" * 60)

def launch_gui():
    """Launch the GUI application."""
    print("\n🚀 Launching GUI...")
    print("💡 Tip: Click canvas to add nodes, click 2 nodes to connect!")
    print("\n")
    os.system("python3 bfs-traversal-gui.py")

def launch_cli():
    """Launch the CLI application."""
    print("\n🚀 Launching CLI...")
    print("💡 Tip: Use menu options to build your graph!")
    print("\n")
    os.system("python3 bfs-traversal.py")

def show_demo_guide():
    """Show quick demo guide."""
    print("\n" + "="*60)
    print("🎬 QUICK DEMO GUIDE".center(60))
    print("="*60)
    print("\n🎯 30-Second Demo:")
    print("   1. Launch GUI")
    print("   2. Click 'Generate Nodes Auto' → 8 nodes → Yes")
    print("   3. Click 'Generate Edges Auto' → 12 edges")
    print("   4. Click 'Run BFS' → Enter any node value")
    print("   5. Watch the animation! 🎨")
    
    print("\n🎯 2-Minute Manual Demo:")
    print("   1. Click canvas 5 times (add nodes 1,2,3,4,5)")
    print("   2. Click node pairs to connect them")
    print("   3. Click 'Show Adjacency List'")
    print("   4. Click 'Run BFS' from node 1")
    print("   5. Enjoy the visualization! ✨")
    
    print("\n💡 Pro Tips:")
    print("   • Orange nodes = selected")
    print("   • Green nodes = processed by BFS")
    print("   • Use 'Reorganize Layout' for clean circles")
    print("   • All operations are validated!")
    print()

def show_features():
    """Show feature list."""
    print("\n" + "="*60)
    print("✅ COMPLETE FEATURE LIST".center(60))
    print("="*60)
    print("\n🔢 Automatic Generation:")
    print("   ✓ Generate nodes (random or manual values)")
    print("   ✓ Generate edges (random connections)")
    
    print("\n✏️ Manual Operations:")
    print("   ✓ Add node (click canvas or button)")
    print("   ✓ Add edge (click nodes or enter values)")
    
    print("\n🗑️ Deletion:")
    print("   ✓ Delete node (removes connected edges)")
    print("   ✓ Delete edge (between two nodes)")
    
    print("\n🔍 Traversal:")
    print("   ✓ BFS with animation")
    print("   ✓ Color-coded visualization")
    print("   ✓ Step-by-step display")
    
    print("\n📊 Display & Info:")
    print("   ✓ Graph statistics")
    print("   ✓ Adjacency list popup")
    print("   ✓ Visual canvas")
    
    print("\n🔧 Utilities:")
    print("   ✓ Reorganize layout (circular)")
    print("   ✓ Reset colors")
    print("   ✓ Clear graph")
    
    print("\n🛡️ Validation:")
    print("   ✓ No duplicate nodes")
    print("   ✓ No duplicate edges")
    print("   ✓ No self-loops")
    print("   ✓ Integer-only values")
    print("   ✓ Complete error checking")
    print()

def show_help():
    """Show help information."""
    print("\n" + "="*60)
    print("❓ HELP & DOCUMENTATION".center(60))
    print("="*60)
    print("\n📁 Available Files:")
    print("   • bfs-traversal-gui.py      - Main GUI program ⭐")
    print("   • bfs-traversal.py          - CLI alternative")
    print("   • GUI_USER_GUIDE.md         - Complete GUI guide")
    print("   • README_BFS.md             - CLI documentation")
    print("   • FEATURE_COMPARISON.md     - Feature comparison")
    print("   • PROJECT_SUMMARY.md        - Complete summary")
    print("   • demo_guide.py             - Demo scenarios")
    print("   • test_cases.py             - Test inputs")
    
    print("\n🎓 For Learning:")
    print("   1. Start with GUI (visual & intuitive)")
    print("   2. Read GUI_USER_GUIDE.md")
    print("   3. Try all 14 features")
    print("   4. Experiment with different graphs")
    
    print("\n🏃 Quick Commands:")
    print("   Launch GUI:  python3 bfs-traversal-gui.py")
    print("   Launch CLI:  python3 bfs-traversal.py")
    print("   View demo:   python3 demo_guide.py")
    
    print("\n💬 Need Help?")
    print("   • Read the documentation files")
    print("   • Try the demo sequences")
    print("   • Check feature comparison")
    
    print("\n🐛 Troubleshooting:")
    print("   Problem: Nodes overlap")
    print("   Solution: Click 'Reorganize Layout'")
    print()
    print("   Problem: Can't see BFS colors")
    print("   Solution: Click 'Reset Colors' first")
    print()
    print("   Problem: Edge creation not working")
    print("   Solution: Ensure 2+ nodes exist, click 2 different nodes")
    print()

def main():
    """Main function."""
    try:
        while True:
            print_banner()
            print_menu()
            
            try:
                choice = input("\n👉 Enter your choice (1-6): ").strip()
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                sys.exit(0)
            
            if choice == '1':
                launch_gui()
            elif choice == '2':
                launch_cli()
            elif choice == '3':
                show_demo_guide()
                input("\nPress Enter to continue...")
            elif choice == '4':
                show_features()
                input("\nPress Enter to continue...")
            elif choice == '5':
                show_help()
                input("\nPress Enter to continue...")
            elif choice == '6':
                print("\n👋 Thank you for using BFS Traversal Tool!")
                print("🎓 Happy learning and exploring graphs!\n")
                break
            else:
                print("\n❌ Invalid choice! Please enter 1-6.")
                input("Press Enter to continue...")
            
            # Clear screen for better UX (works on Unix-like systems)
            if choice not in ['3', '4', '5']:
                os.system('clear' if os.name != 'nt' else 'cls')
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please ensure all required files are in the current directory.")
        sys.exit(1)

if __name__ == "__main__":
    # Check if we're in the right directory
    required_files = ['bfs-traversal-gui.py', 'bfs-traversal.py']
    missing = [f for f in required_files if not os.path.exists(f)]
    
    if missing:
        print("\n❌ Error: Required files not found!")
        print("Missing files:", ', '.join(missing))
        print("\nPlease run this script from the correct directory:")
        print("/home/geralt/Desktop/Repositories/College/AI-Lab/practical-1/")
        sys.exit(1)
    
    main()
