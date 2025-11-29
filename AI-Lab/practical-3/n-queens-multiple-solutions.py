"""
N-Queens Problem - Multiple Solutions Finder with Comparison
AI Lab Practical 3

Finds multiple distinct solutions within a time limit using:
1. Heuristic approach (Min-Conflicts with Random Restarts)
2. Systematic Backtracking (finds all solutions)

Compares efficiency and visualizes results.

Author: [Your Name]
Date: November 4, 2025
"""

import time
import random
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from collections import defaultdict


class NQueensMultipleSolver:
    """Solver for finding multiple distinct N-Queens solutions."""
    
    def __init__(self, n):
        self.n = n
        self.solutions_found = set()  # Store solutions as tuples for uniqueness
        
    def is_valid_solution(self, board):
        """
        Fast validation of a complete solution.
        Checks all constraints: no two queens attack each other.
        Time Complexity: O(N)
        """
        if len(board) != self.n or -1 in board:
            return False
        
        # Quick check: all positions must be unique (one queen per column)
        if len(set(board)) != self.n:
            return False
        
        # Check diagonal conflicts only (columns already checked above)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                # Check if queens at rows i and j attack each other diagonally
                if abs(board[i] - board[j]) == abs(i - j):
                    return False
        
        return True
    
    def is_safe(self, board, row, col):
        """
        Check if placing queen at (row, col) is safe.
        Only checks already placed queens.
        Time Complexity: O(N)
        """
        for i in range(self.n):
            if board[i] == -1:  # Skip unfilled rows
                continue
            if i == row:  # Skip current row
                continue
            
            # Check column conflict
            if board[i] == col:
                return False
            
            # Check diagonal conflict
            if abs(board[i] - col) == abs(i - row):
                return False
        
        return True
    
    def add_solution(self, board):
        """
        Add solution if it's distinct.
        Returns True if added, False if duplicate.
        IMPORTANT: Makes a copy of the board to avoid reference issues.
        """
        solution_tuple = tuple(board[:])  # Create a copy with board[:]
        if solution_tuple not in self.solutions_found:
            self.solutions_found.add(solution_tuple)
            return True
        return False
    
    # ========== HEURISTIC APPROACH: MIN-CONFLICTS WITH RANDOM RESTARTS ==========
    
    def count_conflicts(self, board, row, col):
        """Count conflicts if queen placed at (row, col)."""
        conflicts = 0
        for i in range(self.n):
            if i == row:
                continue
            
            # Column conflict
            if board[i] == col:
                conflicts += 1
            
            # Diagonal conflict
            if abs(board[i] - col) == abs(i - row):
                conflicts += 1
        
        return conflicts
    
    def solve_heuristic(self, time_limit):
        """
        Find multiple solutions using Min-Conflicts with random restarts.
        Runs for specified time limit.
        
        Returns: (solutions_list, iterations, time_elapsed)
        """
        print(f"\n{'='*70}")
        print(f"HEURISTIC APPROACH: Min-Conflicts (N={self.n})")
        print(f"Time Limit: {time_limit} seconds")
        print(f"{'='*70}")
        
        start_time = time.perf_counter()
        iterations = 0
        restarts = 0
        max_iterations_per_restart = 1000
        
        while time.perf_counter() - start_time < time_limit:
            # Random restart: new random configuration
            board = [random.randint(0, self.n - 1) for _ in range(self.n)]
            restarts += 1
            
            # Try to improve this configuration
            for _ in range(max_iterations_per_restart):
                iterations += 1
                
                # Check time limit
                if time.perf_counter() - start_time >= time_limit:
                    break
                
                # Calculate conflicts
                total_conflicts = 0
                for i in range(self.n):
                    total_conflicts += self.count_conflicts(board, i, board[i])
                total_conflicts //= 2  # Each conflict counted twice
                
                # If solution found, validate and store it
                if total_conflicts == 0:
                    if self.is_valid_solution(board):
                        if self.add_solution(board):
                            print(f"  Solution #{len(self.solutions_found)} found at iteration {iterations}")
                    break  # Start new random restart
                
                # Random walk (5% chance) to escape local minima
                if random.random() < 0.05:
                    random_row = random.randint(0, self.n - 1)
                    board[random_row] = random.randint(0, self.n - 1)
                else:
                    # Find queen with most conflicts
                    max_conflicts = -1
                    conflicted_row = 0
                    for i in range(self.n):
                        conf = self.count_conflicts(board, i, board[i])
                        if conf > max_conflicts:
                            max_conflicts = conf
                            conflicted_row = i
                    
                    # Move to position with minimum conflicts
                    min_conf = float('inf')
                    best_cols = []
                    for col in range(self.n):
                        conf = self.count_conflicts(board, conflicted_row, col)
                        if conf < min_conf:
                            min_conf = conf
                            best_cols = [col]
                        elif conf == min_conf:
                            best_cols.append(col)
                    
                    board[conflicted_row] = random.choice(best_cols)
        
        elapsed = time.perf_counter() - start_time
        
        print(f"\nHeuristic Results:")
        print(f"  Solutions found: {len(self.solutions_found)}")
        print(f"  Total iterations: {iterations}")
        print(f"  Random restarts: {restarts}")
        print(f"  Time elapsed: {elapsed:.3f} seconds")
        print(f"  Solutions/second: {len(self.solutions_found)/elapsed:.2f}")
        
        return list(self.solutions_found), iterations, elapsed
    
    # ========== SYSTEMATIC BACKTRACKING APPROACH ==========
    
    def solve_backtracking(self, time_limit):
        """
        Find multiple solutions using systematic backtracking.
        Explores solution space systematically.
        
        Returns: (solutions_list, nodes_explored, time_elapsed)
        """
        print(f"\n{'='*70}")
        print(f"BACKTRACKING APPROACH: Systematic Search (N={self.n})")
        print(f"Time Limit: {time_limit} seconds")
        print(f"{'='*70}")
        
        # Clear previous solutions
        self.solutions_found = set()
        
        board = [-1] * self.n
        self.nodes_explored = 0
        self.start_time = time.perf_counter()
        self.time_limit = time_limit
        self.time_exceeded = False
        
        # Start backtracking from row 0
        self._backtrack(board, 0)
        
        elapsed = time.perf_counter() - self.start_time
        
        print(f"\nBacktracking Results:")
        print(f"  Solutions found: {len(self.solutions_found)}")
        print(f"  Nodes explored: {self.nodes_explored}")
        print(f"  Time elapsed: {elapsed:.3f} seconds")
        if elapsed > 0:
            print(f"  Solutions/second: {len(self.solutions_found)/elapsed:.2f}")
        if self.time_exceeded:
            print(f"  Note: Time limit reached, search terminated early")
        
        return list(self.solutions_found), self.nodes_explored, elapsed
    
    def _backtrack(self, board, row):
        """Recursive backtracking to find all solutions."""
        self.nodes_explored += 1
        
        # Check time limit every 1000 nodes
        if self.nodes_explored % 1000 == 0:
            if time.perf_counter() - self.start_time >= self.time_limit:
                self.time_exceeded = True
                return
        
        if self.time_exceeded:
            return
        
        # Base case: all queens placed
        if row == self.n:
            if self.is_valid_solution(board):
                if self.add_solution(board):
                    print(f"  Solution #{len(self.solutions_found)} found at node {self.nodes_explored}")
            return
        
        # Try placing queen in each column of current row
        for col in range(self.n):
            if self.is_safe(board, row, col):
                board[row] = col
                self._backtrack(board, row + 1)
                board[row] = -1  # Backtrack
                
                if self.time_exceeded:
                    return
    
    # ========== SOLUTION VERIFICATION AND DISPLAY ==========
    
    def verify_all_solutions(self):
        """Verify all found solutions are valid and distinct."""
        print(f"\n{'='*70}")
        print(f"VERIFICATION")
        print(f"{'='*70}")
        
        all_valid = True
        for i, sol in enumerate(self.solutions_found, 1):
            if not self.is_valid_solution(list(sol)):
                print(f"  ✗ Solution {i} is INVALID: {sol}")
                all_valid = False
        
        if all_valid:
            print(f"  ✓ All {len(self.solutions_found)} solutions are VALID")
        
        # Check distinctness
        if len(self.solutions_found) == len(set(self.solutions_found)):
            print(f"  ✓ All solutions are DISTINCT")
        else:
            print(f"  ✗ Duplicate solutions found!")
        
        return all_valid
    
    def print_solution(self, board):
        """Print a single solution as chessboard."""
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                if board[row] == col:
                    line += "Q "
                else:
                    line += ". "
            print(line)
    
    def display_solutions(self, max_display=5):
        """Display first few solutions."""
        print(f"\n{'='*70}")
        print(f"SAMPLE SOLUTIONS (showing first {max_display})")
        print(f"{'='*70}")
        
        for i, sol in enumerate(list(self.solutions_found)[:max_display], 1):
            print(f"\nSolution {i}: {list(sol)}")
            self.print_solution(list(sol))
    
    def display_all_solutions_raw(self):
        """Display ALL solutions in their raw stored form."""
        print(f"\n{'='*70}")
        print(f"ALL SOLUTIONS IN STORED FORM (Total: {len(self.solutions_found)})")
        print(f"{'='*70}")
        
        for i, sol in enumerate(sorted(self.solutions_found), 1):
            print(f"Solution {i}: {list(sol)}")


def compare_and_visualize(n, time_limit):
    """
    Compare both approaches and visualize results.
    
    Args:
        n: Board size
        time_limit: Time limit in seconds for each approach
    """
    print("\n" + "="*70)
    print(f"N-QUEENS MULTIPLE SOLUTIONS FINDER - COMPARISON")
    print(f"Board Size: N={n}, Time Limit: {time_limit}s per approach")
    print("="*70)
    
    # Run Heuristic Approach
    solver_heuristic = NQueensMultipleSolver(n)
    heuristic_solutions, heuristic_iterations, heuristic_time = solver_heuristic.solve_heuristic(time_limit)
    
    # Run Backtracking Approach
    solver_backtrack = NQueensMultipleSolver(n)
    backtrack_solutions, backtrack_nodes, backtrack_time = solver_backtrack.solve_backtracking(time_limit)
    
    # Verify solutions
    print("\n" + "="*70)
    print("VERIFICATION - HEURISTIC APPROACH")
    print("="*70)
    solver_heuristic.verify_all_solutions()
    
    print("\n" + "="*70)
    print("VERIFICATION - BACKTRACKING APPROACH")
    print("="*70)
    solver_backtrack.verify_all_solutions()
    
    # Display ALL solutions in raw form from each approach
    if len(heuristic_solutions) > 0:
        solver_heuristic.display_all_solutions_raw()
    
    if len(backtrack_solutions) > 0:
        solver_backtrack.display_all_solutions_raw()
    
    # Comparison Summary
    print("\n" + "="*70)
    print("COMPARATIVE ANALYSIS")
    print("="*70)
    print(f"\n{'Metric':<30} {'Heuristic':<20} {'Backtracking':<20}")
    print("-" * 70)
    print(f"{'Solutions Found':<30} {len(heuristic_solutions):<20} {len(backtrack_solutions):<20}")
    print(f"{'Time Elapsed (s)':<30} {heuristic_time:<20.3f} {backtrack_time:<20.3f}")
    print(f"{'Iterations/Nodes':<30} {heuristic_iterations:<20} {backtrack_nodes:<20}")
    
    if heuristic_time > 0:
        heur_rate = len(heuristic_solutions) / heuristic_time
        print(f"{'Solutions/Second':<30} {heur_rate:<20.2f}", end="")
    else:
        print(f"{'Solutions/Second':<30} {'N/A':<20}", end="")
    
    if backtrack_time > 0:
        back_rate = len(backtrack_solutions) / backtrack_time
        print(f"{back_rate:<20.2f}")
    else:
        print(f"{'N/A':<20}")
    
    print(f"{'Efficiency (iters/solution)':<30}", end="")
    if len(heuristic_solutions) > 0:
        print(f"{heuristic_iterations/len(heuristic_solutions):<20.1f}", end="")
    else:
        print(f"{'N/A':<20}", end="")
    
    if len(backtrack_solutions) > 0:
        print(f"{backtrack_nodes/len(backtrack_solutions):<20.1f}")
    else:
        print(f"{'N/A':<20}")
    
    # Create visualization
    create_comparison_plot(n, time_limit, 
                          len(heuristic_solutions), len(backtrack_solutions),
                          heuristic_time, backtrack_time,
                          heuristic_iterations, backtrack_nodes)
    
    # Determine winner
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    
    if len(backtrack_solutions) > len(heuristic_solutions):
        print(f"✓ Backtracking found MORE solutions: {len(backtrack_solutions)} vs {len(heuristic_solutions)}")
        print(f"  Backtracking systematically explores the solution space.")
    elif len(heuristic_solutions) > len(backtrack_solutions):
        print(f"✓ Heuristic found MORE solutions: {len(heuristic_solutions)} vs {len(backtrack_solutions)}")
        print(f"  Random restarts help find diverse solutions quickly.")
    else:
        print(f"✓ Both approaches found EQUAL solutions: {len(heuristic_solutions)}")
    
    if backtrack_time > 0 and heuristic_time > 0:
        if len(backtrack_solutions) / backtrack_time > len(heuristic_solutions) / heuristic_time:
            print(f"✓ Backtracking is MORE EFFICIENT: {len(backtrack_solutions)/backtrack_time:.2f} vs {len(heuristic_solutions)/heuristic_time:.2f} solutions/second")
        else:
            print(f"✓ Heuristic is MORE EFFICIENT: {len(heuristic_solutions)/heuristic_time:.2f} vs {len(backtrack_solutions)/backtrack_time:.2f} solutions/second")


def create_comparison_plot(n, time_limit, heur_sols, back_sols, heur_time, back_time, heur_iters, back_nodes):
    """Create visualization comparing both approaches."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'N-Queens Multiple Solutions Comparison (N={n}, Time Limit={time_limit}s)', 
                 fontsize=16, fontweight='bold')
    
    # 1. Solutions Found
    ax1 = axes[0, 0]
    approaches = ['Heuristic\n(Min-Conflicts)', 'Backtracking\n(Systematic)']
    solutions = [heur_sols, back_sols]
    colors = ['#3498db', '#e74c3c']
    bars1 = ax1.bar(approaches, solutions, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax1.set_ylabel('Number of Solutions Found', fontsize=11, fontweight='bold')
    ax1.set_title('Solutions Found', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # 2. Time Comparison
    ax2 = axes[0, 1]
    times = [heur_time, back_time]
    bars2 = ax2.bar(approaches, times, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax2.set_ylabel('Time (seconds)', fontsize=11, fontweight='bold')
    ax2.set_title('Execution Time', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    ax2.axhline(y=time_limit, color='red', linestyle='--', linewidth=2, label='Time Limit')
    ax2.legend()
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}s', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 3. Efficiency (Solutions per Second)
    ax3 = axes[1, 0]
    efficiency = [heur_sols/heur_time if heur_time > 0 else 0, 
                  back_sols/back_time if back_time > 0 else 0]
    bars3 = ax3.bar(approaches, efficiency, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax3.set_ylabel('Solutions per Second', fontsize=11, fontweight='bold')
    ax3.set_title('Efficiency Rate', fontsize=12, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # 4. Work Done (Iterations/Nodes)
    ax4 = axes[1, 1]
    work = [heur_iters, back_nodes]
    bars4 = ax4.bar(approaches, work, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax4.set_ylabel('Iterations/Nodes Explored', fontsize=11, fontweight='bold')
    ax4.set_title('Computational Work', fontsize=12, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)
    ax4.set_yscale('log')
    
    for bar in bars4:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    
    # Save plot
    filename = f'n_queens_comparison_n{n}_t{time_limit}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\n✓ Comparison visualization saved as '{filename}'")


def interactive_demo():
    """Interactive demonstration."""
    print("\n" + "="*70)
    print("N-QUEENS MULTIPLE SOLUTIONS FINDER")
    print("="*70)
    
    while True:
        print("\nOptions:")
        print("1. Compare approaches (recommended)")
        print("2. Heuristic approach only")
        print("3. Backtracking approach only")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '4':
            print("\nThank you!")
            break
        
        if choice not in ['1', '2', '3']:
            print("Invalid choice!")
            continue
        
        try:
            n = int(input("Enter board size N (4-12 recommended): "))
            if n < 4:
                print("N must be at least 4!")
                continue
            
            time_limit = float(input("Enter time limit in seconds (5-30 recommended): "))
            if time_limit <= 0:
                print("Time limit must be positive!")
                continue
        except ValueError:
            print("Invalid input!")
            continue
        
        if choice == '1':
            compare_and_visualize(n, time_limit)
        elif choice == '2':
            solver = NQueensMultipleSolver(n)
            solutions, iterations, elapsed = solver.solve_heuristic(time_limit)
            solver.verify_all_solutions()
            if solutions:
                solver.display_all_solutions_raw()
        elif choice == '3':
            solver = NQueensMultipleSolver(n)
            solutions, nodes, elapsed = solver.solve_backtracking(time_limit)
            solver.verify_all_solutions()
            if solutions:
                solver.display_all_solutions_raw()


if __name__ == "__main__":
    interactive_demo()
