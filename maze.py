import pygame, random
from random import choice
from config import *

# Depth-first search algorithm used to generate random mazes
class Generate_Maze:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4

    def get_rects(self):
        rects = []
        x, y = self.x * grid, self.y * grid
        wall_params = [
            ('top', (x, y), (grid, self.thickness)),
            ('bottom', (x, y + grid), (grid, self.thickness)),
            ('left', (x, y), (self.thickness, grid)),
            ('right', (x + grid, y), (self.thickness, grid))
        ]

        for wall, pos, size in wall_params:
            if self.walls[wall]:
                rects.append(pygame.Rect(pos, size))

        return rects

    def is_valid_index(self, x, y):
        return 0 <= x < cols and 0 <= y < rows

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        return self.grid_cells[find_index(x, y)] if self.is_valid_index(x, y) else False
    
    def find_index(self, x, y):
        return x + y * cols

    def check_next(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = [
            self.check_cell(self.x, self.y - 1),
            self.check_cell(self.x + 1, self.y),
            self.check_cell(self.x, self.y + 1),
            self.check_cell(self.x - 1, self.y)
        ]

        valid_neighbors = [neighbor for neighbor in neighbors if neighbor and not neighbor.visited]
        
        return choice(valid_neighbors) if valid_neighbors else False
    
    def draw(self, sc):
        x, y = self.x * grid, self.y * grid
        wall_draw_params = [
            ('top', (x, y), (x + grid, y)),
            ('bottom', (x + grid, y + grid), (x, y + grid)),
            ('left', (x, y + grid), (x, y)),
            ('right', (x + grid, y), (x + grid, y + grid))
        ]

        for wall, start, end in wall_draw_params:
            if self.walls[wall]:
                pygame.draw.line(sc, pygame.Color('white'), start, end, self.thickness)
    
    def neighbors(self, maze):
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]):
                neighbors.append(maze[new_x][new_y])
        return neighbors
    

def generate():
    grid_cells = [Generate_Maze(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    stack = []

    while True:
        current_cell.visited = True
        next_cell = current_cell.check_next(grid_cells)

        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
        else:
            break

    return grid_cells

def remove(current, next):
    dx, dy = current.x - next.x, current.y - next.y

    if dx == 1:
        current.walls['left'] = next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = next.walls['left'] = False

    if dy == 1:
        current.walls['top'] = next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = next.walls['top'] = False