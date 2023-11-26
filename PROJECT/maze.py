import pygame, random
from random import choice

# Constants
RES = WIDTH, HEIGHT = 1080, 520
GRID = 100   
cols, rows = WIDTH // GRID, HEIGHT // GRID

class Generate_Maze:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4

    def get_rects(self):
        rects = []
        x, y = self.x * GRID, self.y * GRID
        wall_params = [
            ('top', (x, y), (GRID, self.thickness)),
            ('bottom', (x, y + GRID), (GRID, self.thickness)),
            ('left', (x, y), (self.thickness, GRID)),
            ('right', (x + GRID, y), (self.thickness, GRID))
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
        x, y = self.x * GRID, self.y * GRID
        wall_draw_params = [
            ('top', (x, y), (x + GRID, y)),
            ('bottom', (x + GRID, y + GRID), (x, y + GRID)),
            ('left', (x, y + GRID), (x, y)),
            ('right', (x + GRID, y), (x + GRID, y + GRID))
        ]

        for wall, start, end in wall_draw_params:
            if self.walls[wall]:
                pygame.draw.line(sc, pygame.Color('white'), start, end, self.thickness)

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