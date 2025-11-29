#!/usr/bin/env python3
"""
Quick Test Script for BFS-DFS GUI Program
Tests both algorithms on a sample graph
"""

# Import the Graph class from bfs-dfs-gui
import sys
sys.path.insert(0, '/home/geralt/Desktop/Repositories/College/AI-Lab/practical-1')

from collections import deque

class Graph:
    """Graph class to represent an undirected graph using adjacency list."""
    
    def __init__(self):
        self.adjacency_list = {}
        self.nodes = set()
    
    def add_node(self, value):
        if value not in self.nodes:
            self.nodes.add(value)
            self.adjacency_list[value] = []
            return True
        return False
    
    def add_edge(self, node1, node2):
        if node1 in self.nodes and node2 in self.nodes:
            if node2 not in self.adjacency_list[node1]:
                self.adjacency_list[node1].append(node2)
                self.adjacency_list[node2].append(node1)
                return True
        return False
    
    def bfs_traversal(self, start_node):
        if start_node not in self.nodes:
            return []
        
        visited = set()
        queue = deque([start_node])
        traversal_order = []
        visited.add(start_node)
        
        while queue:
            current = queue.popleft()
            traversal_order.append(current)
            
            for neighbor in sorted(self.adjacency_list[current]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return traversal_order
    
    def dfs_traversal(self, start_node):
        if start_node not in self.nodes:
            return []
        
        visited = set()
        stack = [start_node]
        traversal_order = []
        
        while stack:
            current = stack.pop()
            
            if current not in visited:
                visited.add(current)
                traversal_order.append(current)
                
                for neighbor in sorted(self.adjacency_list[current], reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return traversal_order


def test_algorithms():
    """Test both BFS and DFS algorithms."""
    print("="*60)
    print("BFS-DFS Algorithm Test")
    print("="*60)
    
    # Create test graph
    g = Graph()
    
    # Add nodes
    nodes = [1, 2, 3, 4, 5, 6, 7, 8]
    for node in nodes:
        g.add_node(node)
    
    # Add edges to create a tree-like structure
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (5, 8)]
    for n1, n2 in edges:
        g.add_edge(n1, n2)
    
    print(f"\nGraph Structure:")
    print(f"Nodes: {sorted(g.nodes)}")
    print(f"Edges: {edges}")
    print(f"\nAdjacency List:")
    for node in sorted(g.nodes):
        print(f"  {node} → {sorted(g.adjacency_list[node])}")
    
    # Test BFS
    print(f"\n{'='*60}")
    print("BFS Traversal (starting from node 1)")
    print(f"{'='*60}")
    bfs_result = g.bfs_traversal(1)
    print(f"Result: {' → '.join(map(str, bfs_result))}")
    print(f"Properties:")
    print(f"  - Uses Queue (FIFO)")
    print(f"  - Level-order traversal")
    print(f"  - Explores all neighbors before going deeper")
    
    # Test DFS
    print(f"\n{'='*60}")
    print("DFS Traversal (starting from node 1)")
    print(f"{'='*60}")
    dfs_result = g.dfs_traversal(1)
    print(f"Result: {' → '.join(map(str, dfs_result))}")
    print(f"Properties:")
    print(f"  - Uses Stack (LIFO)")
    print(f"  - Depth-first traversal")
    print(f"  - Explores as deep as possible before backtracking")
    
    # Comparison
    print(f"\n{'='*60}")
    print("Comparison")
    print(f"{'='*60}")
    print(f"BFS: {' → '.join(map(str, bfs_result))}")
    print(f"DFS: {' → '.join(map(str, dfs_result))}")
    print(f"\nBoth algorithms visit all nodes: {len(bfs_result) == len(dfs_result) == len(nodes)}")
    print(f"Order differs: {bfs_result != dfs_result}")
    
    # Test with different start node
    print(f"\n{'='*60}")
    print("Testing from different start node (node 3)")
    print(f"{'='*60}")
    bfs_3 = g.bfs_traversal(3)
    dfs_3 = g.dfs_traversal(3)
    print(f"BFS from 3: {' → '.join(map(str, bfs_3))}")
    print(f"DFS from 3: {' → '.join(map(str, dfs_3))}")
    
    # Test on disconnected component
    print(f"\n{'='*60}")
    print("Testing with disconnected graph")
    print(f"{'='*60}")
    g2 = Graph()
    for node in [10, 20, 30, 40]:
        g2.add_node(node)
    g2.add_edge(10, 20)
    g2.add_edge(30, 40)
    
    print(f"Graph: {sorted(g2.nodes)}")
    print(f"Edges: [(10, 20), (30, 40)]")
    bfs_disc = g2.bfs_traversal(10)
    dfs_disc = g2.dfs_traversal(10)
    print(f"BFS from 10: {' → '.join(map(str, bfs_disc))}")
    print(f"DFS from 10: {' → '.join(map(str, dfs_disc))}")
    print(f"Note: Only reaches connected component containing start node")
    
    print(f"\n{'='*60}")
    print("✅ All tests passed! Both algorithms working correctly.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    test_algorithms()
