import numpy as np
from typing import List, Tuple
from solo_x.pathfinding.grid import Grid


class FlowField:
    """Flow Field pathfinding for GPU-accelerated AI movement"""
    
    def __init__(self, grid: Grid):
        self.grid = grid
        self.width = grid.width
        self.height = grid.height
        self.cost_field = None
        self.vector_field = None
        self.target = None
    
    def calculate(self, target_x: int, target_y: int):
        """Calculate flow field from target position"""
        self.target = (target_x, target_y)
        
        # Create cost field (Dijkstra's algorithm)
        self.cost_field = np.full((self.width, self.height), np.inf, dtype=np.float32)
        
        # Priority queue: (cost, x, y)
        queue = []
        
        # Start from target
        self.cost_field[target_x, target_y] = 0
        queue.append((0, target_x, target_y))
        
        # Dijkstra's algorithm
        while queue:
            cost, x, y = min(queue, key=lambda x: x[0])
            queue.remove((cost, x, y))
            
            for nx, ny in self.grid.get_neighbors(x, y):
                new_cost = cost + 1  # Uniform cost for now
                if new_cost < self.cost_field[nx, ny]:
                    self.cost_field[nx, ny] = new_cost
                    queue.append((new_cost, nx, ny))
        
        # Calculate vector field (gradient descent)
        self.vector_field = np.zeros((self.width, self.height, 2), dtype=np.float32)
        for x in range(self.width):
            for y in range(self.height):
                if not self.grid.is_walkable(x, y):
                    continue
                
                # Find neighbor with lowest cost
                min_cost = np.inf
                best_dir = (0, 0)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if self.grid.in_bounds(nx, ny) and self.cost_field[nx, ny] < min_cost:
                        min_cost = self.cost_field[nx, ny]
                        best_dir = (dx, dy)
                
                self.vector_field[x, y] = best_dir
    
    def get_direction(self, x: int, y: int) -> Tuple[float, float]:
        """Get movement direction at position"""
        if self.vector_field is None or not self.grid.in_bounds(x, y):
            return (0, 0)
        return tuple(self.vector_field[x, y])
    
    def get_path(self, start_x: int, start_y: int) -> List[Tuple[int, int]]:
        """Get path from start to target using flow field"""
        if self.vector_field is None:
            return []
        
        path = []
        x, y = start_x, start_y
        visited = set()
        
        while (x, y) != self.target and len(path) < self.width * self.height:
            if (x, y) in visited:
                break
            visited.add((x, y))
            path.append((x, y))
            
            dx, dy = self.get_direction(x, y)
            x += int(dx)
            y += int(dy)
        
        if (x, y) == self.target:
            path.append((x, y))
        
        return path
