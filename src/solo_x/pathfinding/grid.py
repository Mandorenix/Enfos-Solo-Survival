import numpy as np
from typing import List, Tuple, Optional


class Grid:
    """2D grid for pathfinding and spatial queries"""
    
    def __init__(self, width: int = 128, height: int = 128):
        self.width = width
        self.height = height
        self.cells = np.zeros((width, height), dtype=np.uint8)
        
        # Cell types:
        # 0 = walkable (ground, grass, etc.)
        # 1 = obstacle (walls, trees, etc.)
    
    def is_walkable(self, x: int, y: int) -> bool:
        """Check if cell is walkable"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[x, y] == 0
        return False
    
    def set_obstacle(self, x: int, y: int):
        """Set cell as obstacle"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[x, y] = 1
    
    def clear_obstacle(self, x: int, y: int):
        """Clear obstacle from cell"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[x, y] = 0
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get walkable neighbor coordinates"""
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.is_walkable(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
    
    def in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are within grid bounds"""
        return 0 <= x < self.width and 0 <= y < self.height
