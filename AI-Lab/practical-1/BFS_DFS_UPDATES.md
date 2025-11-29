# BFS-DFS GUI Program - Updates Summary

## File: `bfs-dfs-gui.py`

### Changes Made:
1. **Renamed** from `bfs-traversal-gui.py` to `bfs-dfs-gui.py`
2. **Added DFS Algorithm** to Graph class
3. **Updated GUI** to support both BFS and DFS traversal

---

## New Features:

### 1. DFS Algorithm Implementation
Added `dfs_traversal()` method to the `Graph` class:
- Uses **Stack** data structure (LIFO - Last In First Out)
- Implements iterative DFS using a list as stack
- Explores depth-first before exploring breadth
- Time Complexity: O(V + E)
- Space Complexity: O(V)

```python
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
            
            # Add unvisited neighbors to stack
            for neighbor in sorted(self.adjacency_list[current], reverse=True):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return traversal_order
```

### 2. GUI Updates

#### New DFS Button
- Added "🌲 Run DFS" button in Traversal Section
- Background color: Pink (#E91E63)
- Positioned below "Run BFS" button

#### New DFS Label
- Shows DFS traversal result below BFS label
- Font: Arial 12, bold
- Color: Dark red
- Format: "DFS Traversal: node1 → node2 → node3..."

#### Updated Color Scheme for DFS Animation
- **Purple**: Currently processing node
- **Lavender**: Nodes added to stack (to be explored)
- Different from BFS colors (green/lightgreen) for clear distinction

#### Updated Help Text
Added DFS information:
```
• BFS: Level-order (Queue)
• DFS: Depth-first (Stack)
```

### 3. Animation System

#### `run_dfs()` Method
- Interactive DFS visualization with step-by-step animation
- 500ms delay between steps for clear viewing
- Color-coded states:
  - Lavender: Node added to stack
  - Purple: Node being visited/processed
- Shows real-time progress in DFS label
- Completion popup with full traversal path

### 4. Updated Window Title
Changed from:
```
"Graph Builder & BFS Traversal - Interactive GUI"
```
To:
```
"Graph Builder & BFS/DFS Traversal - Interactive GUI"
```

### 5. Reset Colors Enhancement
The `reset_colors()` method now:
- Resets both BFS and DFS labels
- Clears both `bfs_result` and `dfs_result` lists
- Returns all nodes to default blue color

---

## Algorithm Comparison

### BFS (Breadth-First Search)
- **Data Structure**: Queue (FIFO)
- **Strategy**: Explore level-by-level
- **Use Cases**: Shortest path, level-order traversal
- **Color Scheme**: Green (visited), Light Green (in queue)
- **AI Application**: Optimal pathfinding in unweighted graphs

### DFS (Depth-First Search)
- **Data Structure**: Stack (LIFO)
- **Strategy**: Explore depth-first
- **Use Cases**: Topological sort, cycle detection, pathfinding
- **Color Scheme**: Purple (visited), Lavender (in stack)
- **AI Application**: Game tree exploration, constraint satisfaction

---

## Testing Checklist

✅ Program launches without errors
✅ All original BFS functionality preserved
✅ DFS button appears and is clickable
✅ DFS animation works with proper color coding
✅ Both algorithms can be run on same graph
✅ Reset colors works for both algorithms
✅ Clear graph resets both BFS and DFS labels
✅ Node/edge operations work correctly
✅ Auto-generation features functional
✅ Manual operations functional
✅ Delete operations work properly

---

## File Structure
```
College/AI-Lab/practical-1/
├── bfs-traversal-gui.py      (original - BFS only)
├── bfs-dfs-gui.py             (new - BFS + DFS)
├── bfs-traversal.py           (CLI version)
├── PRACTICAL_REPORT.txt       (lab report)
└── BFS_DFS_UPDATES.md         (this file)
```

---

## How to Use

1. **Launch Program**:
   ```bash
   python3 bfs-dfs-gui.py
   ```

2. **Create Graph**:
   - Use automatic or manual node/edge generation
   - Click canvas to add nodes interactively
   - Click two nodes to connect them

3. **Run BFS**:
   - Click "🔍 Run BFS" button
   - Enter start node
   - Watch green animation (level-order)

4. **Run DFS**:
   - Click "🌲 Run DFS" button
   - Enter start node
   - Watch purple animation (depth-first)

5. **Compare Results**:
   - Both traversal results shown simultaneously
   - BFS label shows breadth-first path
   - DFS label shows depth-first path

---

## Code Quality
- ✅ No syntax errors
- ✅ Follows existing code style
- ✅ Proper docstrings for all methods
- ✅ Consistent variable naming
- ✅ Error handling preserved
- ✅ All features tested and working

---

## Dependencies
- Python 3.x (standard library only)
- tkinter (built-in GUI framework)
- collections.deque (for BFS queue)
- math, random (standard utilities)

**No external packages required!**
