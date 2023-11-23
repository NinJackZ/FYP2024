import pygame, random
from random import choice

# Constants
RES = WIDTH, HEIGHT = 1080, 520
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE

class Game:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4

    def get_rects(self):
        rects = []
        x, y = self.x * TILE, self.y * TILE
        wall_params = [
            ('top', (x, y), (TILE, self.thickness)),
            ('bottom', (x, y + TILE), (TILE, self.thickness)),
            ('left', (x, y), (self.thickness, TILE)),
            ('right', (x + TILE, y), (self.thickness, TILE))
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
        x, y = self.x * TILE + 10, self.y * TILE + 10
        wall_draw_params = [
            ('top', (x, y), (x + TILE, y)),
            ('bottom', (x + TILE, y + TILE), (x, y + TILE)),
            ('left', (x, y + TILE), (x, y)),
            ('right', (x + TILE, y), (x + TILE, y + TILE))
        ]

        for wall, start, end in wall_draw_params:
            if self.walls[wall]:
                pygame.draw.line(sc, pygame.Color('white'), start, end, self.thickness)

def generate_maze():
    grid_cells = [Game(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    stack = []

    while True:
        current_cell.visited = True
        next_cell = current_cell.check_next(grid_cells)

        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
        else:
            break

    return grid_cells

def remove_walls(current, next):
    dx, dy = current.x - next.x, current.y - next.y

    if dx == 1:
        current.walls['left'] = next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = next.walls['left'] = False

    if dy == 1:
        current.walls['top'] = next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = next.walls['top'] = False