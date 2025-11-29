"""
Test Examples for BFS Traversal Program
Copy and paste these test sequences to quickly test the program
"""

# Test 1: Basic Graph with Manual Nodes
# Creates nodes 1, 2, 3, 4, 5 and connects them
TEST_1_BASIC = """
1
5
n
1
2
3
4
5
4
1
2
4
2
3
4
3
4
4
1
5
5
6
1
8
"""

# Test 2: Random Graph Generation
# Creates 10 random nodes and 12 random edges
TEST_2_RANDOM = """
1
10
y
2
12
5
6
1
8
"""

# Test 3: Mixed Manual and Auto
# Manual nodes, automatic edges
TEST_3_MIXED = """
1
6
n
10
20
30
40
50
60
2
8
5
6
10
8
"""

# Test 4: Edge Cases Testing
# Test duplicate prevention, self-loops, etc.
TEST_4_EDGE_CASES = """
3
5
3
5
4
5
6
4
5
5
4
5
6
8
"""

# Test 5: Disconnected Graph
# Create nodes but don't connect all of them
TEST_5_DISCONNECTED = """
1
5
n
1
2
3
4
5
4
1
2
4
3
4
5
6
1
6
3
8
"""

# Test 6: Complete Graph (all nodes connected)
# 4 nodes, all possible edges (6 edges)
TEST_6_COMPLETE = """
1
4
n
1
2
3
4
2
6
5
6
1
8
"""

# Test 7: Linear Graph (chain)
# Creates a straight line: 1-2-3-4-5
TEST_7_LINEAR = """
1
5
n
1
2
3
4
5
4
1
2
4
2
3
4
3
4
4
4
5
5
6
1
6
3
8
"""

# Test 8: Star Graph (one center node)
# Node 1 is connected to all others
TEST_8_STAR = """
1
5
n
1
2
3
4
5
4
1
2
4
1
3
4
1
4
4
1
5
5
6
1
8
"""

# Test 9: Clear and Rebuild
# Test the clear functionality
TEST_9_CLEAR = """
1
3
y
2
2
5
7
y
1
4
n
10
20
30
40
2
4
5
6
10
8
"""

# Test 10: Maximum Edges Test
# Try to create more edges than possible
TEST_10_MAX_EDGES = """
1
4
y
2
10
5
6
1
8
"""

"""
How to use these tests:

METHOD 1 - Using echo (Linux/Mac):
echo "1
5
n
1
2
3
4
5" | python3 bfs-traversal.py

METHOD 2 - Using heredoc (Linux/Mac):
python3 bfs-traversal.py << 'EOF'
1
5
n
1
2
3
4
5
8
EOF

METHOD 3 - Save to file and redirect:
echo "..." > test_input.txt
python3 bfs-traversal.py < test_input.txt

METHOD 4 - Copy-paste manually:
Just copy the numbers (without quotes) and paste them
one at a time when prompted
"""

# Quick Test Commands (copy these directly to terminal)

QUICK_TEST_1 = """
cd /home/geralt/Desktop/Repositories/College/AI-Lab/practical-1
python3 bfs-traversal.py << 'EOF'
1
5
n
1
2
3
4
5
2
4
5
6
1
8
EOF
"""

QUICK_TEST_2 = """
cd /home/geralt/Desktop/Repositories/College/AI-Lab/practical-1
python3 bfs-traversal.py << 'EOF'
1
7
y
2
10
5
6
1
8
EOF
"""

QUICK_TEST_3 = """
cd /home/geralt/Desktop/Repositories/College/AI-Lab/practical-1
python3 bfs-traversal.py << 'EOF'
3
10
3
20
3
30
4
10
20
4
20
30
5
6
10
8
EOF
"""

if __name__ == "__main__":
    print("📝 BFS Traversal Test Cases")
    print("\nAvailable tests:")
    print("1. TEST_1_BASIC - Manual nodes 1-5 with some edges")
    print("2. TEST_2_RANDOM - 10 random nodes, 12 random edges")
    print("3. TEST_3_MIXED - Manual nodes, automatic edges")
    print("4. TEST_4_EDGE_CASES - Tests duplicate prevention")
    print("5. TEST_5_DISCONNECTED - Creates disconnected components")
    print("6. TEST_6_COMPLETE - Complete graph (all connected)")
    print("7. TEST_7_LINEAR - Linear chain graph")
    print("8. TEST_8_STAR - Star topology graph")
    print("9. TEST_9_CLEAR - Tests clear and rebuild")
    print("10. TEST_10_MAX_EDGES - Tests maximum edge limit")
    print("\nSee comments in file for usage instructions!")
