"""
BFS & DFS Traversal Program with GUI
A comprehensive graph builder with visual interface and BFS/DFS traversal
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import math
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
    
    def remove_node(self, value):
        """Remove a node from the graph."""
        if value in self.nodes:
            self.nodes.remove(value)
            del self.adjacency_list[value]
            # Remove from all adjacency lists
            for node in self.adjacency_list:
                if value in self.adjacency_list[node]:
                    self.adjacency_list[node].remove(value)
            return True
        return False
    
    def remove_edge(self, node1, node2):
        """Remove an edge between two nodes."""
        if self.edge_exists(node1, node2):
            self.adjacency_list[node1].remove(node2)
            self.adjacency_list[node2].remove(node1)
            return True
        return False
    
    def clear(self):
        """Clear the entire graph."""
        self.nodes.clear()
        self.adjacency_list.clear()
    
    def bfs_traversal(self, start_node):
        """Perform BFS traversal starting from the given node."""
        if start_node not in self.nodes:
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
    
    def dfs_traversal(self, start_node):
        """Perform DFS traversal starting from the given node."""
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
                
                # Add unvisited neighbors to stack (in reverse sorted order for consistent traversal)
                for neighbor in sorted(self.adjacency_list[current], reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return traversal_order


class GraphGUI:
    """GUI for Graph Builder and BFS/DFS Traversal."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Builder & BFS/DFS Traversal - Interactive GUI")
        self.root.geometry("1200x800")
        
        # Graph logic
        self.graph = Graph()
        
        # Visual elements
        self.node_positions = {}  # {value: (x, y)}
        self.canvas_nodes = {}  # {value: (oval_id, text_id)}
        self.canvas_edges = []  # [(line_id, text_id, node1, node2)]
        
        # Selection state
        self.selected_nodes_for_edge = []
        self.mode = "normal"  # normal, delete_node, delete_edge
        
        # Traversal state
        self.bfs_result = []
        self.dfs_result = []
        
        # Setup GUI
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI layout."""
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Canvas
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas for graph visualization
        canvas_frame = tk.LabelFrame(left_frame, text="Graph Visualization", font=("Arial", 10, "bold"))
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas.bind("<Button-1>", self.canvas_click)
        
        # Status label
        self.status_label = tk.Label(left_frame, text="Mode: Normal | Click on canvas to add nodes, click nodes to create edges", 
                                     font=("Arial", 11), fg="blue", anchor="w", justify="left")
        self.status_label.pack(fill=tk.X, padx=5, pady=5)
        
        # BFS result label
        self.bfs_label = tk.Label(left_frame, text="BFS Traversal: (not yet performed)", 
                                  font=("Arial", 12, "bold"), fg="darkgreen", anchor="w", justify="left")
        self.bfs_label.pack(fill=tk.X, padx=5, pady=5)
        
        # DFS result label
        self.dfs_label = tk.Label(left_frame, text="DFS Traversal: (not yet performed)", 
                                  font=("Arial", 12, "bold"), fg="darkred", anchor="w", justify="left")
        self.dfs_label.pack(fill=tk.X, padx=5, pady=5)
        
        # Right panel - Controls
        right_frame = tk.Frame(main_frame, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        right_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(right_frame, text="Graph Builder", font=("Arial", 16, "bold"), fg="darkblue")
        title_label.pack(pady=10)
        
        # Automatic Generation Section
        auto_frame = tk.LabelFrame(right_frame, text="Automatic Generation", font=("Arial", 11, "bold"))
        auto_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(auto_frame, text="🔢 Generate Nodes Auto", command=self.generate_nodes_auto, 
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        tk.Button(auto_frame, text="🔗 Generate Edges Auto", command=self.generate_edges_auto, 
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        
        # Manual Operations Section
        manual_frame = tk.LabelFrame(right_frame, text="Manual Operations", font=("Arial", 11, "bold"))
        manual_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(manual_frame, text="➕ Add Node Manually", command=self.add_node_manual, 
                 bg="#8BC34A", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        tk.Button(manual_frame, text="🔗 Add Edge Manually", command=self.add_edge_manual, 
                 bg="#03A9F4", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        
        # Deletion Section
        delete_frame = tk.LabelFrame(right_frame, text="Delete Operations", font=("Arial", 11, "bold"))
        delete_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(delete_frame, text="🗑️ Delete Node", command=self.delete_node_mode, 
                 bg="#FF5722", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        tk.Button(delete_frame, text="✂️ Delete Edge", command=self.delete_edge_mode, 
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        
        # Traversal Section
        traversal_frame = tk.LabelFrame(right_frame, text="Graph Traversal", font=("Arial", 11, "bold"))
        traversal_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(traversal_frame, text="🔍 Run BFS", command=self.run_bfs, 
                 bg="#9C27B0", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        tk.Button(traversal_frame, text="🌲 Run DFS", command=self.run_dfs, 
                 bg="#E91E63", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        tk.Button(traversal_frame, text="🔄 Reset Colors", command=self.reset_colors, 
                 bg="#607D8B", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        
        # Display Section
        display_frame = tk.LabelFrame(right_frame, text="Display & Info", font=("Arial", 11, "bold"))
        display_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(display_frame, text="📊 Show Graph Info", command=self.show_graph_info, 
                 bg="#00BCD4", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        tk.Button(display_frame, text="📋 Show Adjacency List", command=self.show_adjacency_list, 
                 bg="#009688", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        
        # Utility Section
        utility_frame = tk.LabelFrame(right_frame, text="Utilities", font=("Arial", 11, "bold"))
        utility_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(utility_frame, text="🎨 Reorganize Layout", command=self.reorganize_layout, 
                 bg="#795548", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        tk.Button(utility_frame, text="🧹 Clear Graph", command=self.clear_graph, 
                 bg="#F44336", fg="white", font=("Arial", 10, "bold"), cursor="hand2").pack(fill=tk.X, padx=5, pady=3)
        
        # Info text
        info_frame = tk.LabelFrame(right_frame, text="Quick Help", font=("Arial", 11, "bold"))
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        info_text = tk.Text(info_frame, wrap=tk.WORD, font=("Arial", 9), height=10)
        info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        info_text.insert("1.0", 
            "📌 Quick Guide:\n\n"
            "• Click canvas to add nodes\n"
            "• Click 2 nodes to connect them\n"
            "• Use buttons for operations\n"
            "• Generate nodes/edges automatically\n"
            "• Run BFS/DFS to see traversal\n"
            "• Delete nodes/edges as needed\n\n"
            "💡 Tips:\n"
            "• Node values must be unique\n"
            "• No self-loops allowed\n"
            "• No duplicate edges\n"
            "• BFS: Level-order (Queue)\n"
            "• DFS: Depth-first (Stack)"
        )
        info_text.config(state=tk.DISABLED)
    
    def canvas_click(self, event):
        """Handle canvas click events."""
        if self.mode == "delete_node":
            self.delete_node_at(event.x, event.y)
            return
        elif self.mode == "delete_edge":
            self.select_node_for_edge_deletion(event.x, event.y)
            return
        
        # Normal mode
        clicked_node = self.get_node_at(event.x, event.y)
        
        if clicked_node is None:
            # Add new node at click position
            self.add_node_at_position(event.x, event.y)
            self.clear_edge_selection()
        else:
            # Select node for edge creation
            self.handle_node_selection_for_edge(clicked_node)
    
    def get_node_at(self, x, y):
        """Get node value at given canvas position."""
        for value, (nx, ny) in self.node_positions.items():
            if math.hypot(x - nx, y - ny) <= 25:
                return value
        return None
    
    def add_node_at_position(self, x, y):
        """Add a node at specific canvas position."""
        # Get value from user
        value = simpledialog.askinteger("Add Node", "Enter node value (integer):", 
                                       parent=self.root, minvalue=-1000, maxvalue=1000)
        if value is None:
            return
        
        if self.graph.node_exists(value):
            messagebox.showerror("Error", f"Node with value {value} already exists!")
            return
        
        # Add to graph
        self.graph.add_node(value)
        self.node_positions[value] = (x, y)
        
        # Draw on canvas
        self.draw_node(value, x, y)
        self.update_status(f"Added node {value}")
    
    def draw_node(self, value, x, y, color="lightblue"):
        """Draw a node on the canvas."""
        r = 25
        oval = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="black", width=2)
        text = self.canvas.create_text(x, y, text=str(value), font=("Arial", 13, "bold"))
        self.canvas_nodes[value] = (oval, text)
    
    def draw_edge(self, node1, node2):
        """Draw an edge between two nodes."""
        x1, y1 = self.node_positions[node1]
        x2, y2 = self.node_positions[node2]
        
        line = self.canvas.create_line(x1, y1, x2, y2, width=2, fill="black", tags="edge")
        # Move line behind nodes
        self.canvas.tag_lower(line)
        
        # Draw edge label (optional - shows connection)
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        label = self.canvas.create_text(mid_x, mid_y, text="", font=("Arial", 8), fill="red")
        
        self.canvas_edges.append((line, label, node1, node2))
    
    def handle_node_selection_for_edge(self, node):
        """Handle node selection for edge creation."""
        if node in self.selected_nodes_for_edge:
            # Deselect
            self.selected_nodes_for_edge.remove(node)
            self.highlight_node(node, "lightblue")
        else:
            # Select
            self.selected_nodes_for_edge.append(node)
            self.highlight_node(node, "orange")
        
        # If two nodes selected, create edge
        if len(self.selected_nodes_for_edge) == 2:
            node1, node2 = self.selected_nodes_for_edge
            
            if node1 == node2:
                messagebox.showwarning("Invalid Edge", "Cannot create edge from node to itself!")
            elif self.graph.edge_exists(node1, node2):
                messagebox.showwarning("Duplicate Edge", f"Edge between {node1} and {node2} already exists!")
            else:
                self.graph.add_edge(node1, node2)
                self.draw_edge(node1, node2)
                self.update_status(f"Added edge between {node1} and {node2}")
            
            self.clear_edge_selection()
    
    def clear_edge_selection(self):
        """Clear node selection for edge creation."""
        for node in self.selected_nodes_for_edge:
            if node in self.canvas_nodes:
                self.highlight_node(node, "lightblue")
        self.selected_nodes_for_edge.clear()
    
    def highlight_node(self, value, color):
        """Change node color."""
        if value in self.canvas_nodes:
            oval, text = self.canvas_nodes[value]
            self.canvas.itemconfig(oval, fill=color)
    
    def generate_nodes_auto(self):
        """Generate nodes automatically."""
        num_nodes = simpledialog.askinteger("Generate Nodes", 
                                           "How many nodes to generate?",
                                           parent=self.root, minvalue=1, maxvalue=50)
        if num_nodes is None:
            return
        
        # Ask if random or manual values
        use_random = messagebox.askyesno("Node Values", 
                                        "Use random values?\n\nYes = Random values\nNo = Enter manually")
        
        if use_random:
            # Generate random unique values
            available = list(range(1, 1001))
            random.shuffle(available)
            
            added = 0
            for i in range(num_nodes):
                value = available[i]
                if not self.graph.node_exists(value):
                    self.graph.add_node(value)
                    added += 1
            
            # Arrange in circle
            self.arrange_nodes_circle()
            messagebox.showinfo("Success", f"Generated {added} nodes with random values!")
        else:
            # Manual input
            values = []
            for i in range(num_nodes):
                while True:
                    val = simpledialog.askinteger(f"Node {i+1}/{num_nodes}", 
                                                 f"Enter value for node {i+1}:",
                                                 parent=self.root)
                    if val is None:
                        return
                    if self.graph.node_exists(val) or val in values:
                        messagebox.showerror("Error", f"Value {val} already used!")
                    else:
                        values.append(val)
                        self.graph.add_node(val)
                        break
            
            self.arrange_nodes_circle()
            messagebox.showinfo("Success", f"Generated {len(values)} nodes!")
        
        self.update_status(f"Generated {num_nodes} nodes")
    
    def arrange_nodes_circle(self):
        """Arrange all nodes in a circle on canvas."""
        self.canvas.delete("all")
        self.canvas_nodes.clear()
        self.canvas_edges.clear()
        self.node_positions.clear()
        
        nodes = sorted(self.graph.nodes)
        n = len(nodes)
        
        if n == 0:
            return
        
        # Canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 700
        if canvas_height <= 1:
            canvas_height = 600
        
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        radius = min(canvas_width, canvas_height) // 2 - 60
        
        # Arrange in circle
        for i, value in enumerate(nodes):
            angle = 2 * math.pi * i / n - math.pi / 2  # Start from top
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.node_positions[value] = (x, y)
            self.draw_node(value, x, y)
        
        # Redraw all edges
        self.redraw_all_edges()
    
    def redraw_all_edges(self):
        """Redraw all edges based on current node positions."""
        self.canvas_edges.clear()
        drawn = set()
        
        for node1 in self.graph.nodes:
            for node2 in self.graph.adjacency_list[node1]:
                edge_key = tuple(sorted([node1, node2]))
                if edge_key not in drawn:
                    self.draw_edge(node1, node2)
                    drawn.add(edge_key)
    
    def generate_edges_auto(self):
        """Generate edges automatically."""
        if self.graph.get_node_count() < 2:
            messagebox.showerror("Error", "Need at least 2 nodes to create edges!")
            return
        
        n = self.graph.get_node_count()
        max_edges = (n * (n - 1)) // 2
        
        num_edges = simpledialog.askinteger("Generate Edges", 
                                           f"How many edges? (max {max_edges})",
                                           parent=self.root, minvalue=1, maxvalue=max_edges)
        if num_edges is None:
            return
        
        nodes = list(self.graph.nodes)
        added = 0
        attempts = 0
        max_attempts = num_edges * 10
        
        while added < num_edges and attempts < max_attempts:
            node1, node2 = random.sample(nodes, 2)
            if not self.graph.edge_exists(node1, node2):
                self.graph.add_edge(node1, node2)
                self.draw_edge(node1, node2)
                added += 1
            attempts += 1
        
        messagebox.showinfo("Success", f"Generated {added} edges!")
        self.update_status(f"Generated {added} edges")
    
    def add_node_manual(self):
        """Add a node manually at random position."""
        value = simpledialog.askinteger("Add Node", "Enter node value (integer):",
                                       parent=self.root, minvalue=-1000, maxvalue=1000)
        if value is None:
            return
        
        if self.graph.node_exists(value):
            messagebox.showerror("Error", f"Node with value {value} already exists!")
            return
        
        self.graph.add_node(value)
        
        # Add to canvas at random position
        canvas_width = self.canvas.winfo_width() or 700
        canvas_height = self.canvas.winfo_height() or 600
        
        x = random.randint(50, canvas_width - 50)
        y = random.randint(50, canvas_height - 50)
        
        self.node_positions[value] = (x, y)
        self.draw_node(value, x, y)
        
        messagebox.showinfo("Success", f"Node {value} added!")
        self.update_status(f"Added node {value}")
    
    def add_edge_manual(self):
        """Add an edge manually between two nodes."""
        if self.graph.get_node_count() < 2:
            messagebox.showerror("Error", "Need at least 2 nodes to create an edge!")
            return
        
        nodes_list = sorted(self.graph.nodes)
        
        # Get first node
        node1 = simpledialog.askinteger("Add Edge", 
                                       f"Available nodes: {nodes_list}\n\nEnter first node:",
                                       parent=self.root)
        if node1 is None:
            return
        
        if not self.graph.node_exists(node1):
            messagebox.showerror("Error", f"Node {node1} does not exist!")
            return
        
        # Get second node
        node2 = simpledialog.askinteger("Add Edge", 
                                       f"Available nodes: {nodes_list}\n\nEnter second node:",
                                       parent=self.root)
        if node2 is None:
            return
        
        if not self.graph.node_exists(node2):
            messagebox.showerror("Error", f"Node {node2} does not exist!")
            return
        
        if node1 == node2:
            messagebox.showerror("Error", "Cannot create edge from node to itself!")
            return
        
        if self.graph.edge_exists(node1, node2):
            messagebox.showerror("Error", f"Edge between {node1} and {node2} already exists!")
            return
        
        self.graph.add_edge(node1, node2)
        self.draw_edge(node1, node2)
        
        messagebox.showinfo("Success", f"Edge between {node1} and {node2} added!")
        self.update_status(f"Added edge: {node1} <-> {node2}")
    
    def delete_node_mode(self):
        """Enter delete node mode."""
        if self.graph.get_node_count() == 0:
            messagebox.showinfo("Info", "No nodes to delete!")
            return
        
        self.mode = "delete_node"
        self.update_status("DELETE NODE MODE: Click on a node to delete it")
        self.clear_edge_selection()
    
    def delete_node_at(self, x, y):
        """Delete node at given position."""
        node = self.get_node_at(x, y)
        
        if node is None:
            messagebox.showinfo("Info", "No node at that position. Click on a node.")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Delete node {node} and all its edges?"):
            # First, delete all edges connected to this node from canvas
            edges_to_remove = []
            for line, label, n1, n2 in self.canvas_edges:
                if n1 == node or n2 == node:
                    # Delete the edge visuals from canvas
                    self.canvas.delete(line)
                    self.canvas.delete(label)
                    edges_to_remove.append((line, label, n1, n2))
            
            # Remove edges from the list
            for edge in edges_to_remove:
                self.canvas_edges.remove(edge)
            
            # Remove from graph
            self.graph.remove_node(node)
            
            # Remove node visuals from canvas
            if node in self.canvas_nodes:
                oval, text = self.canvas_nodes[node]
                self.canvas.delete(oval)
                self.canvas.delete(text)
                del self.canvas_nodes[node]
            
            # Remove position
            if node in self.node_positions:
                del self.node_positions[node]
            
            self.update_status(f"Deleted node {node}")
        
        # Exit delete mode
        self.mode = "normal"
        self.update_status("Mode: Normal")
    
    def delete_edge_mode(self):
        """Enter delete edge mode."""
        if self.graph.get_node_count() < 2:
            messagebox.showinfo("Info", "Need at least 2 nodes with edges!")
            return
        
        self.mode = "delete_edge"
        self.update_status("DELETE EDGE MODE: Click on 2 connected nodes to delete the edge")
        self.clear_edge_selection()
    
    def select_node_for_edge_deletion(self, x, y):
        """Select nodes to delete edge."""
        node = self.get_node_at(x, y)
        
        if node is None:
            return
        
        if node in self.selected_nodes_for_edge:
            self.selected_nodes_for_edge.remove(node)
            self.highlight_node(node, "lightblue")
        else:
            self.selected_nodes_for_edge.append(node)
            self.highlight_node(node, "orange")
        
        if len(self.selected_nodes_for_edge) == 2:
            node1, node2 = self.selected_nodes_for_edge
            
            if self.graph.edge_exists(node1, node2):
                if messagebox.askyesno("Confirm Delete", f"Delete edge between {node1} and {node2}?"):
                    self.graph.remove_edge(node1, node2)
                    
                    # Remove from canvas
                    self.canvas_edges = [(line, label, n1, n2) for line, label, n1, n2 in self.canvas_edges 
                                        if not (set([n1, n2]) == set([node1, node2]))]
                    
                    # Redraw
                    self.canvas.delete("edge")
                    self.redraw_all_edges()
                    
                    self.update_status(f"Deleted edge: {node1} <-> {node2}")
            else:
                messagebox.showinfo("Info", f"No edge exists between {node1} and {node2}")
            
            self.clear_edge_selection()
            self.mode = "normal"
            self.update_status("Mode: Normal")
    
    def run_bfs(self):
        """Run BFS traversal with visualization."""
        if self.graph.get_node_count() == 0:
            messagebox.showinfo("Info", "Graph is empty! Add some nodes first.")
            return
        
        # Ask for start node
        nodes_list = sorted(self.graph.nodes)
        start = simpledialog.askinteger("BFS Traversal", 
                                       f"Available nodes: {nodes_list}\n\nEnter start node:",
                                       parent=self.root)
        if start is None:
            return
        
        if not self.graph.node_exists(start):
            messagebox.showerror("Error", f"Node {start} does not exist!")
            return
        
        # Reset colors
        self.reset_colors()
        
        # Perform BFS with animation
        self.bfs_result = []
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        def animate_bfs(queue, visited):
            if not queue:
                # BFS complete
                result_str = " → ".join(map(str, self.bfs_result))
                self.bfs_label.config(text=f"BFS Traversal: {result_str}")
                messagebox.showinfo("BFS Complete", f"BFS Traversal: {result_str}")
                return
            
            current = queue.popleft()
            self.bfs_result.append(current)
            
            # Highlight current node
            self.highlight_node(current, "green")
            
            # Update label
            result_str = " → ".join(map(str, self.bfs_result))
            self.bfs_label.config(text=f"BFS Traversal (in progress): {result_str}")
            
            # Visit neighbors
            for neighbor in sorted(self.graph.adjacency_list[current]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    self.highlight_node(neighbor, "lightgreen")
            
            # Continue animation
            self.root.after(500, lambda: animate_bfs(queue, visited))
        
        # Start animation
        self.highlight_node(start, "lightgreen")
        self.root.after(500, lambda: animate_bfs(queue, visited))
    
    def run_dfs(self):
        """Run DFS traversal with visualization."""
        if self.graph.get_node_count() == 0:
            messagebox.showinfo("Info", "Graph is empty! Add some nodes first.")
            return
        
        # Ask for start node
        nodes_list = sorted(self.graph.nodes)
        start = simpledialog.askinteger("DFS Traversal", 
                                       f"Available nodes: {nodes_list}\n\nEnter start node:",
                                       parent=self.root)
        if start is None:
            return
        
        if not self.graph.node_exists(start):
            messagebox.showerror("Error", f"Node {start} does not exist!")
            return
        
        # Reset colors
        self.reset_colors()
        
        # Perform DFS with animation
        self.dfs_result = []
        visited = set()
        stack = [start]
        
        def animate_dfs(stack, visited):
            if not stack:
                # DFS complete
                result_str = " → ".join(map(str, self.dfs_result))
                self.dfs_label.config(text=f"DFS Traversal: {result_str}")
                messagebox.showinfo("DFS Complete", f"DFS Traversal: {result_str}")
                return
            
            current = stack.pop()
            
            # Skip if already visited
            if current in visited:
                self.root.after(100, lambda: animate_dfs(stack, visited))
                return
            
            visited.add(current)
            self.dfs_result.append(current)
            
            # Highlight current node
            self.highlight_node(current, "purple")
            
            # Update label
            result_str = " → ".join(map(str, self.dfs_result))
            self.dfs_label.config(text=f"DFS Traversal (in progress): {result_str}")
            
            # Add unvisited neighbors to stack (in reverse sorted order)
            for neighbor in sorted(self.graph.adjacency_list[current], reverse=True):
                if neighbor not in visited:
                    stack.append(neighbor)
                    self.highlight_node(neighbor, "lavender")
            
            # Continue animation
            self.root.after(500, lambda: animate_dfs(stack, visited))
        
        # Start animation
        self.highlight_node(start, "lavender")
        self.root.after(500, lambda: animate_dfs(stack, visited))
    
    def reset_colors(self):
        """Reset all node and edge colors."""
        for value in self.canvas_nodes:
            self.highlight_node(value, "lightblue")
        
        # Reset edge colors
        for line, label, n1, n2 in self.canvas_edges:
            self.canvas.itemconfig(line, fill="black", width=2)
        
        # Reset labels
        self.bfs_label.config(text="BFS Traversal: (not yet performed)")
        self.dfs_label.config(text="DFS Traversal: (not yet performed)")
        self.bfs_result.clear()
        self.dfs_result.clear()
    
    def show_graph_info(self):
        """Show graph information."""
        n = self.graph.get_node_count()
        edges = sum(len(adj) for adj in self.graph.adjacency_list.values()) // 2
        
        info = f"Graph Information:\n\n"
        info += f"Total Nodes: {n}\n"
        info += f"Total Edges: {edges}\n"
        info += f"Nodes: {sorted(self.graph.nodes)}\n\n"
        
        if n > 0:
            max_edges = (n * (n - 1)) // 2
            info += f"Maximum Possible Edges: {max_edges}\n"
            info += f"Graph Density: {edges}/{max_edges}\n"
        
        messagebox.showinfo("Graph Information", info)
    
    def show_adjacency_list(self):
        """Show adjacency list in a popup."""
        if self.graph.get_node_count() == 0:
            messagebox.showinfo("Adjacency List", "Graph is empty!")
            return
        
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title("Adjacency List")
        popup.geometry("400x500")
        
        tk.Label(popup, text="Adjacency List", font=("Arial", 12, "bold")).pack(pady=10)
        
        text_frame = tk.Frame(popup)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(text_frame, yscrollcommand=scrollbar.set, font=("Courier", 10))
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Build adjacency list text
        for node in sorted(self.graph.nodes):
            neighbors = sorted(self.graph.adjacency_list[node])
            text_widget.insert(tk.END, f"{node:4d} → {neighbors}\n")
        
        text_widget.config(state=tk.DISABLED)
        
        tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
    
    def reorganize_layout(self):
        """Reorganize nodes in circular layout."""
        if self.graph.get_node_count() == 0:
            messagebox.showinfo("Info", "No nodes to reorganize!")
            return
        
        self.arrange_nodes_circle()
        self.update_status("Layout reorganized")
    
    def clear_graph(self):
        """Clear the entire graph."""
        if self.graph.get_node_count() == 0:
            messagebox.showinfo("Info", "Graph is already empty!")
            return
        
        if messagebox.askyesno("Confirm Clear", "Clear entire graph? This cannot be undone!"):
            self.graph.clear()
            self.canvas.delete("all")
            self.canvas_nodes.clear()
            self.canvas_edges.clear()
            self.node_positions.clear()
            self.selected_nodes_for_edge.clear()
            self.bfs_result.clear()
            self.dfs_result.clear()
            self.bfs_label.config(text="BFS Traversal: (not yet performed)")
            self.dfs_label.config(text="DFS Traversal: (not yet performed)")
            self.update_status("Graph cleared")
    
    def update_status(self, message):
        """Update status label."""
        mode_text = f"Mode: {self.mode.replace('_', ' ').title()}"
        self.status_label.config(text=f"{mode_text} | {message}")


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
