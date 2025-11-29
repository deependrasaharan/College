"""
BFS Traversal Program with Graph Generation
This program allows users to create a graph by adding nodes and edges
either automatically or manually, and then perform BFS traversal.
"""

import random
from collections import deque


class Graph:
    """Graph class to represent an undirected graph using adjacency list."""
    
    def __init__(self):
        self.adjacency_list = {}  # {node_value: [list of connected nodes]}
        self.nodes = set()  # Set of all node values for quick lookup
    
    def add_node(self, value):
        """Add a node to the graph."""
        if value not in self.nodes:
            self.nodes.add(value)
            self.adjacency_list[value] = []
            return True
        return False
    
    def add_edge(self, node1, node2):
        """Add an undirected edge between two nodes."""
        if node1 in self.nodes and node2 in self.nodes:
            # Add edge in both directions for undirected graph
            if node2 not in self.adjacency_list[node1]:
                self.adjacency_list[node1].append(node2)
                self.adjacency_list[node2].append(node1)
                return True
        return False
    
    def node_exists(self, value):
        """Check if a node with given value exists."""
        return value in self.nodes
    
    def edge_exists(self, node1, node2):
        """Check if an edge exists between two nodes."""
        if node1 in self.nodes and node2 in self.nodes:
            return node2 in self.adjacency_list[node1]
        return False
    
    def get_node_count(self):
        """Return the number of nodes in the graph."""
        return len(self.nodes)
    
    def display_graph(self):
        """Display the graph structure."""
        if not self.nodes:
            print("\n⚠️  Graph is empty!")
            return
        
        print("\n" + "="*50)
        print("📊 GRAPH STRUCTURE")
        print("="*50)
        print(f"Total Nodes: {len(self.nodes)}")
        print(f"Nodes: {sorted(self.nodes)}")
        print("\nAdjacency List:")
        for node in sorted(self.nodes):
            neighbors = sorted(self.adjacency_list[node])
            print(f"  {node} -> {neighbors}")
        print("="*50)
    
    def bfs_traversal(self, start_node):
        """Perform BFS traversal starting from the given node."""
        if start_node not in self.nodes:
            print(f"❌ Node {start_node} does not exist in the graph!")
            return []
        
        visited = set()
        queue = deque([start_node])
        traversal_order = []
        
        visited.add(start_node)
        
        while queue:
            current = queue.popleft()
            traversal_order.append(current)
            
            # Visit all unvisited neighbors
            for neighbor in sorted(self.adjacency_list[current]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return traversal_order


# Utility Functions

def get_integer_input(prompt, min_value=None, max_value=None):
    """Get validated integer input from user."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"❌ Value must be at least {min_value}. Try again.")
                continue
            if max_value is not None and value > max_value:
                print(f"❌ Value must be at most {max_value}. Try again.")
                continue
            return value
        except ValueError:
            print("❌ Invalid input! Please enter a valid integer.")


def get_yes_no_input(prompt):
    """Get yes/no input from user."""
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("❌ Invalid input! Please enter 'y' or 'n'.")


def generate_nodes_automatically(graph):
    """Generate nodes automatically based on user input."""
    num_nodes = get_integer_input("\nHow many nodes to generate? ", min_value=1)
    
    # Ask if user wants random values or manual input
    use_random = get_yes_no_input("Fill with random values? (y/n): ")
    
    added_count = 0
    if use_random:
        # Generate random unique values
        print(f"\n🔄 Generating {num_nodes} nodes with random values...")
        available_values = list(range(1, 1001))  # Pool of values from 1 to 1000
        random.shuffle(available_values)
        
        for i in range(num_nodes):
            value = available_values[i]
            if graph.add_node(value):
                added_count += 1
                print(f"  ✓ Added node with value: {value}")
    else:
        # Manual input for each node
        print(f"\n📝 Enter values for {num_nodes} nodes:")
        for i in range(num_nodes):
            while True:
                value = get_integer_input(f"  Enter value for node {i+1}: ")
                if graph.node_exists(value):
                    print(f"  ❌ Node with value {value} already exists! Choose a different value.")
                else:
                    graph.add_node(value)
                    added_count += 1
                    print(f"  ✓ Node added successfully!")
                    break
    
    print(f"\n✅ Successfully added {added_count} nodes!")


def generate_edges_automatically(graph):
    """Generate edges automatically between existing nodes."""
    node_count = graph.get_node_count()
    
    if node_count < 2:
        print("\n❌ Need at least 2 nodes to create edges!")
        return
    
    max_possible_edges = (node_count * (node_count - 1)) // 2
    print(f"\nMaximum possible edges: {max_possible_edges}")
    
    num_edges = get_integer_input(
        f"How many edges to generate? ",
        min_value=1,
        max_value=max_possible_edges
    )
    
    nodes_list = list(graph.nodes)
    added_count = 0
    attempts = 0
    max_attempts = num_edges * 10  # Prevent infinite loop
    
    print(f"\n🔄 Generating {num_edges} edges...")
    
    while added_count < num_edges and attempts < max_attempts:
        # Pick two random different nodes
        node1, node2 = random.sample(nodes_list, 2)
        
        if not graph.edge_exists(node1, node2):
            graph.add_edge(node1, node2)
            added_count += 1
            print(f"  ✓ Added edge: {node1} <-> {node2}")
        
        attempts += 1
    
    if added_count < num_edges:
        print(f"\n⚠️  Could only create {added_count} edges (may have reached maximum possible edges)")
    else:
        print(f"\n✅ Successfully added {added_count} edges!")


def add_node_manually(graph):
    """Add a single node manually."""
    print("\n📝 Add a new node")
    while True:
        value = get_integer_input("Enter node value: ")
        if graph.node_exists(value):
            print(f"❌ Node with value {value} already exists! Choose a different value.")
        else:
            graph.add_node(value)
            print(f"✅ Node with value {value} added successfully!")
            break


def add_edge_manually(graph):
    """Add a single edge manually."""
    if graph.get_node_count() < 2:
        print("\n❌ Need at least 2 nodes to create an edge!")
        return
    
    print(f"\nAvailable nodes: {sorted(graph.nodes)}")
    
    node1 = get_integer_input("Enter first node value: ")
    if not graph.node_exists(node1):
        print(f"❌ Node {node1} does not exist!")
        return
    
    node2 = get_integer_input("Enter second node value: ")
    if not graph.node_exists(node2):
        print(f"❌ Node {node2} does not exist!")
        return
    
    if node1 == node2:
        print("❌ Cannot create an edge from a node to itself!")
        return
    
    if graph.edge_exists(node1, node2):
        print(f"❌ Edge between {node1} and {node2} already exists!")
        return
    
    graph.add_edge(node1, node2)
    print(f"✅ Edge between {node1} and {node2} added successfully!")


def perform_bfs(graph):
    """Perform BFS traversal on the graph."""
    if graph.get_node_count() == 0:
        print("\n❌ Graph is empty! Add some nodes first.")
        return
    
    print(f"\nAvailable nodes: {sorted(graph.nodes)}")
    start_node = get_integer_input("Enter starting node for BFS: ")
    
    if not graph.node_exists(start_node):
        print(f"❌ Node {start_node} does not exist!")
        return
    
    print(f"\n🔍 Performing BFS traversal starting from node {start_node}...")
    traversal = graph.bfs_traversal(start_node)
    
    print("\n" + "="*50)
    print("🎯 BFS TRAVERSAL RESULT")
    print("="*50)
    print(f"Traversal Order: {' -> '.join(map(str, traversal))}")
    print("="*50)


def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("🌐 GRAPH BUILDER & BFS TRAVERSAL")
    print("="*50)
    print("1. Generate nodes automatically")
    print("2. Generate edges automatically")
    print("3. Add node manually")
    print("4. Add edge manually")
    print("5. Display graph")
    print("6. Perform BFS traversal")
    print("7. Clear graph")
    print("8. Exit")
    print("="*50)


def main():
    """Main function to run the program."""
    graph = Graph()
    
    print("\n" + "🎓 Welcome to Graph Builder & BFS Traversal Program! 🎓".center(50))
    
    while True:
        display_menu()
        choice = get_integer_input("\nEnter your choice (1-8): ", min_value=1, max_value=8)
        
        if choice == 1:
            generate_nodes_automatically(graph)
        elif choice == 2:
            generate_edges_automatically(graph)
        elif choice == 3:
            add_node_manually(graph)
        elif choice == 4:
            add_edge_manually(graph)
        elif choice == 5:
            graph.display_graph()
        elif choice == 6:
            perform_bfs(graph)
        elif choice == 7:
            if get_yes_no_input("\n⚠️  Are you sure you want to clear the graph? (y/n): "):
                graph = Graph()
                print("✅ Graph cleared successfully!")
        elif choice == 8:
            print("\n👋 Thank you for using Graph Builder! Goodbye!\n")
            break


if __name__ == "__main__":
    main()
