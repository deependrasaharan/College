"""
N-Queens Problem - Heuristic Approaches
AI Lab Practical 3

Implements multiple heuristic approaches:
1. Min-Conflicts Heuristic (Local Search)
2. Backtracking with MRV (Most Constrained Variable) Heuristic
3. Backtracking with LCV (Least Constraining Value) Heuristic
4. Classical Backtracking (for comparison)

Author: [Your Name]
Date: November 4, 2025
"""

import random
import time
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for saving plots to files
import matplotlib.pyplot as plt
from collections import defaultdict


class NQueensSolver:
    """N-Queens solver with multiple heuristic approaches."""
    
    def __init__(self, n):
        self.n = n
        self.solutions_count = 0
        self.nodes_explored = 0
        
    def is_safe(self, board, row, col):
        """Check if placing queen at (row, col) is safe."""
        # Check all other rows (both before and after, since MRV fills out of order)
        for i in range(self.n):
            if i == row:
                continue
            if board[i] == -1:  # Skip unfilled rows
                continue
            
            # Check column conflict
            if board[i] == col:
                return False
            
            # Check diagonal conflict
            if abs(board[i] - col) == abs(i - row):
                return False
        
        return True
    
    def count_conflicts(self, board, row, col):
        """Count number of conflicts if queen is placed at (row, col)."""
        conflicts = 0
        
        # Check column conflicts
        for i in range(self.n):
            if i != row and board[i] == col:
                conflicts += 1
        
        # Check diagonal conflicts
        for i in range(self.n):
            if i != row and board[i] != -1:
                if abs(board[i] - col) == abs(i - row):
                    conflicts += 1
        
        return conflicts
    
    def get_min_conflict_position(self, board, row):
        """Find position with minimum conflicts in given row (LCV heuristic)."""
        min_conflicts = float('inf')
        best_positions = []
        
        for col in range(self.n):
            conflicts = self.count_conflicts(board, row, col)
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_positions = [col]
            elif conflicts == min_conflicts:
                best_positions.append(col)
        
        return random.choice(best_positions), min_conflicts
    
    def get_most_constrained_row(self, board, rows_left):
        """
        MRV (Minimum Remaining Values) Heuristic.
        Choose row with fewest valid placements.
        """
        min_options = float('inf')
        best_row = None
        
        for row in rows_left:
            valid_positions = sum(1 for col in range(self.n) 
                                 if self.is_safe(board, row, col))
            if valid_positions < min_options:
                min_options = valid_positions
                best_row = row
        
        return best_row
    
    # ========== 1. MIN-CONFLICTS HEURISTIC ==========
    def solve_min_conflicts(self, max_iterations=1000, visualize=False):
        """
        Min-Conflicts Heuristic Algorithm with Random Restarts.
        Local search approach - starts with random configuration,
        iteratively moves queens to reduce conflicts.
        Uses random restarts to escape local minima.
        """
        print(f"\n{'='*60}")
        print(f"MIN-CONFLICTS HEURISTIC (N={self.n})")
        print(f"{'='*60}")
        
        start_time = time.perf_counter()
        total_iterations = 0
        restart_interval = min(100, max_iterations // 10)  # Restart every 100 iterations or 10% of max
        
        for restart in range(max_iterations // restart_interval + 1):
            # Initialize with random positions (one queen per row)
            board = [random.randint(0, self.n-1) for _ in range(self.n)]
            
            if visualize and restart == 0:
                print(f"Initial configuration: {board}")
                print(f"Initial conflicts: {self.total_conflicts(board)}")
            
            for iteration in range(restart_interval):
                total_iterations += 1
                if total_iterations > max_iterations:
                    break
                
                # Calculate conflicts for each queen
                conflicts = [(i, self.count_conflicts(board, i, board[i])) 
                            for i in range(self.n)]
                
                # Check if solution found
                total = sum(c for _, c in conflicts)
                if total == 0:
                    end_time = time.perf_counter()
                    if visualize:
                        print(f"\n✓ Solution found in {total_iterations} iterations (restart #{restart})!")
                        print(f"Final configuration: {board}")
                        self.print_board(board)
                    else:
                        print(f"\n✓ Solution found in {total_iterations} iterations (restart #{restart})")
                    print(f"Time: {end_time - start_time:.6f} seconds")
                    print(f"Iterations: {total_iterations}")
                    return board, total_iterations, end_time - start_time
                
                # Random walk with 5% probability to escape local minima
                if random.random() < 0.05:
                    # Make a random move
                    random_row = random.randint(0, self.n-1)
                    random_col = random.randint(0, self.n-1)
                    board[random_row] = random_col
                else:
                    # Select queen with most conflicts
                    conflicts.sort(key=lambda x: x[1], reverse=True)
                    most_conflicted_row = conflicts[0][0]
                    
                    # Move queen to position with minimum conflicts
                    best_col, min_conf = self.get_min_conflict_position(board, most_conflicted_row)
                    board[most_conflicted_row] = best_col
                
                if visualize and iteration % 100 == 0:
                    print(f"Iteration {total_iterations}: conflicts = {total}")
            
            if total_iterations >= max_iterations:
                break
            
            if visualize:
                print(f"Restart #{restart + 1} (after {total_iterations} iterations)")
        
        end_time = time.perf_counter()
        print(f"\n✗ No solution found in {total_iterations} iterations")
        print(f"Time: {end_time - start_time:.6f} seconds")
        return None, total_iterations, end_time - start_time
    
    def total_conflicts(self, board):
        """Calculate total conflicts in current board configuration."""
        total = 0
        for i in range(self.n):
            total += self.count_conflicts(board, i, board[i])
        return total // 2  # Each conflict counted twice
    
    # ========== 2. BACKTRACKING WITH MRV HEURISTIC ==========
    def solve_backtracking_mrv(self, visualize=False):
        """
        Backtracking with MRV (Most Constrained Variable) Heuristic.
        Chooses row with fewest valid placements first - fail-fast strategy.
        """
        print(f"\n{'='*60}")
        print(f"BACKTRACKING WITH MRV HEURISTIC (N={self.n})")
        print(f"{'='*60}")
        
        board = [-1] * self.n
        rows_left = set(range(self.n))
        self.nodes_explored = 0
        
        start_time = time.perf_counter()
        result = self._backtrack_mrv(board, rows_left, 0)
        end_time = time.perf_counter()
        
        if result:
            if visualize:
                print(f"\n✓ Solution found!")
                print(f"Configuration: {board}")
                self.print_board(board)
            print(f"Time: {end_time - start_time:.6f} seconds")
            print(f"Nodes explored: {self.nodes_explored}")
            return board, self.nodes_explored, end_time - start_time
        else:
            print(f"\n✗ No solution found")
            return None, self.nodes_explored, end_time - start_time
    
    def _backtrack_mrv(self, board, rows_left, depth):
        """Recursive backtracking with MRV heuristic."""
        self.nodes_explored += 1
        
        if depth == self.n:
            return True
        
        # MRV Heuristic: Choose row with minimum remaining values
        if not rows_left:
            return False
            
        row = self.get_most_constrained_row(board, rows_left)
        
        if row is None:
            return False
        
        rows_left_copy = rows_left.copy()
        rows_left_copy.remove(row)
        
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row] = col
                
                if self._backtrack_mrv(board, rows_left_copy, depth + 1):
                    return True
                
                board[row] = -1  # Backtrack
        
        return False
    
    # ========== 3. BACKTRACKING WITH LCV HEURISTIC ==========
    def solve_backtracking_lcv(self, visualize=False):
        """
        Backtracking with LCV (Least Constraining Value) Heuristic.
        Chooses position that leaves maximum options for remaining queens.
        """
        print(f"\n{'='*60}")
        print(f"BACKTRACKING WITH LCV HEURISTIC (N={self.n})")
        print(f"{'='*60}")
        
        board = [-1] * self.n
        self.nodes_explored = 0
        
        start_time = time.perf_counter()
        result = self._backtrack_lcv(board, 0)
        end_time = time.perf_counter()
        
        if result:
            if visualize:
                print(f"\n✓ Solution found!")
                print(f"Configuration: {board}")
                self.print_board(board)
            print(f"Time: {end_time - start_time:.6f} seconds")
            print(f"Nodes explored: {self.nodes_explored}")
            return board, self.nodes_explored, end_time - start_time
        else:
            print(f"\n✗ No solution found")
            return None, self.nodes_explored, end_time - start_time
    
    def _backtrack_lcv(self, board, row):
        """Recursive backtracking with LCV heuristic."""
        self.nodes_explored += 1
        
        if row == self.n:
            return True
        
        # Get valid positions with their constraining values
        positions = []
        for col in range(self.n):
            if self.is_safe(board, row, col):
                # Count how many future positions this choice eliminates
                constraining_value = self.count_future_constraints(board, row, col)
                positions.append((col, constraining_value))
        
        # LCV: Sort by least constraining first
        positions.sort(key=lambda x: x[1])
        
        for col, _ in positions:
            board[row] = col
            
            if self._backtrack_lcv(board, row + 1):
                return True
            
            board[row] = -1  # Backtrack
        
        return False
    
    def count_future_constraints(self, board, row, col):
        """Count how many future positions this placement constrains."""
        constraints = 0
        for future_row in range(row + 1, self.n):
            for future_col in range(self.n):
                # Check if this position would be attacked
                if future_col == col:
                    constraints += 1
                elif abs(future_col - col) == abs(future_row - row):
                    constraints += 1
        return constraints
    
    # ========== 4. CLASSICAL BACKTRACKING ==========
    def solve_classical_backtracking(self, visualize=False):
        """Classical backtracking without heuristics (for comparison)."""
        print(f"\n{'='*60}")
        print(f"CLASSICAL BACKTRACKING (N={self.n})")
        print(f"{'='*60}")
        
        board = [-1] * self.n
        self.nodes_explored = 0
        
        start_time = time.perf_counter()
        result = self._backtrack_classical(board, 0)
        end_time = time.perf_counter()
        
        if result:
            if visualize:
                print(f"\n✓ Solution found!")
                print(f"Configuration: {board}")
                self.print_board(board)
            print(f"Time: {end_time - start_time:.6f} seconds")
            print(f"Nodes explored: {self.nodes_explored}")
            return board, self.nodes_explored, end_time - start_time
        else:
            print(f"\n✗ No solution found")
            return None, self.nodes_explored, end_time - start_time
    
    def _backtrack_classical(self, board, row):
        """Classical recursive backtracking."""
        self.nodes_explored += 1
        
        if row == self.n:
            return True
        
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row] = col
                
                if self._backtrack_classical(board, row + 1):
                    return True
                
                board[row] = -1  # Backtrack
        
        return False
    
    # ========== UTILITY FUNCTIONS ==========
    def print_board(self, board):
        """Print board in visual format."""
        print("\nChessboard:")
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                if board[row] == col:
                    line += "Q "
                else:
                    line += ". "
            print(line)
        print()
    
    def verify_solution(self, board):
        """Verify if the solution is valid."""
        for i in range(self.n):
            for j in range(i + 1, self.n):
                # Check column
                if board[i] == board[j]:
                    return False
                # Check diagonal
                if abs(board[i] - board[j]) == abs(i - j):
                    return False
        return True


def compare_algorithms():
    """Compare all heuristic approaches."""
    print("="*70)
    print("N-QUEENS HEURISTIC APPROACHES - COMPARATIVE ANALYSIS")
    print("="*70)
    
    n_values = [4, 6, 8, 10, 12]
    
    results = {
        'Min-Conflicts': {'times': [], 'metrics': []},
        'Backtracking + MRV': {'times': [], 'metrics': []},
        'Backtracking + LCV': {'times': [], 'metrics': []},
        'Classical Backtracking': {'times': [], 'metrics': []}
    }
    
    for n in n_values:
        print(f"\n{'#'*70}")
        print(f"Testing N = {n}")
        print(f"{'#'*70}")
        
        solver = NQueensSolver(n)
        
        # 1. Min-Conflicts
        solution, iterations, time_taken = solver.solve_min_conflicts(max_iterations=5000)
        results['Min-Conflicts']['times'].append(time_taken)
        results['Min-Conflicts']['metrics'].append(iterations)
        
        # 2. Backtracking with MRV
        solver = NQueensSolver(n)
        solution, nodes, time_taken = solver.solve_backtracking_mrv()
        results['Backtracking + MRV']['times'].append(time_taken)
        results['Backtracking + MRV']['metrics'].append(nodes)
        
        # 3. Backtracking with LCV
        solver = NQueensSolver(n)
        solution, nodes, time_taken = solver.solve_backtracking_lcv()
        results['Backtracking + LCV']['times'].append(time_taken)
        results['Backtracking + LCV']['metrics'].append(nodes)
        
        # 4. Classical Backtracking
        solver = NQueensSolver(n)
        solution, nodes, time_taken = solver.solve_classical_backtracking()
        results['Classical Backtracking']['times'].append(time_taken)
        results['Classical Backtracking']['metrics'].append(nodes)
    
    # Plotting results
    plot_comparison(n_values, results)


def plot_comparison(n_values, results):
    """Plot comparison graphs."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Time comparison
    colors = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12']
    for i, (algo, data) in enumerate(results.items()):
        ax1.plot(n_values, data['times'], marker='o', label=algo, 
                color=colors[i], linewidth=2, markersize=8)
    
    ax1.set_xlabel('Board Size (N)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('Execution Time Comparison', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Metrics comparison (iterations/nodes)
    for i, (algo, data) in enumerate(results.items()):
        ax2.plot(n_values, data['metrics'], marker='s', label=algo,
                color=colors[i], linewidth=2, markersize=8)
    
    ax2.set_xlabel('Board Size (N)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Iterations/Nodes Explored', fontsize=12, fontweight='bold')
    ax2.set_title('Algorithm Efficiency Comparison', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')
    
    plt.tight_layout()
    
    # Save the plot to file
    output_file = 'n_queens_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    
    print(f"\n{'='*70}")
    print(f"✓ Comparison graphs saved as '{output_file}'")
    print(f"  You can view the graphs by opening this file.")
    print(f"{'='*70}")


def interactive_demo():
    """Interactive demonstration of different heuristics."""
    print("\n" + "="*70)
    print("N-QUEENS HEURISTIC SOLVER - INTERACTIVE DEMO")
    print("="*70)
    
    while True:
        print("\nChoose a heuristic approach:")
        print("1. Min-Conflicts Heuristic (Recommended for large N)")
        print("2. Backtracking with MRV Heuristic")
        print("3. Backtracking with LCV Heuristic")
        print("4. Classical Backtracking (No heuristic)")
        print("5. Compare All Algorithms")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '6':
            print("\nThank you for using N-Queens Solver!")
            break
        
        if choice == '5':
            compare_algorithms()
            continue
        
        try:
            n = int(input("Enter board size N (4-20 recommended): "))
            if n < 4:
                print("N must be at least 4!")
                continue
        except ValueError:
            print("Invalid input!")
            continue
        
        visualize = input("Show board visualization? (y/n): ").lower() == 'y'
        
        solver = NQueensSolver(n)
        
        if choice == '1':
            max_iter = int(input("Max iterations (default 10000): ") or "10000")
            solution, _, _ = solver.solve_min_conflicts(max_iter, visualize)
        elif choice == '2':
            solution, _, _ = solver.solve_backtracking_mrv(visualize)
        elif choice == '3':
            solution, _, _ = solver.solve_backtracking_lcv(visualize)
        elif choice == '4':
            solution, _, _ = solver.solve_classical_backtracking(visualize)
        else:
            print("Invalid choice!")
            continue
        
        if solution and not visualize:
            show = input("\nShow solution? (y/n): ").lower() == 'y'
            if show:
                solver.print_board(solution)
                print(f"Valid solution: {solver.verify_solution(solution)}")


if __name__ == "__main__":
    # You can run either:
    # 1. Interactive demo
    interactive_demo()
    
    # 2. Or direct comparison (uncomment below)
    # compare_algorithms()
    
    # 3. Or test specific algorithm (uncomment below)
    # solver = NQueensSolver(8)
    # solution, _, _ = solver.solve_min_conflicts(visualize=True)
