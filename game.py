import pygame, random

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

class Game:
    def __init__(self, screen, maze_width, maze_height):
        self.screen = screen
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.cell_size = screen.get_width() // maze_width, screen.get_height() // maze_height
        self.maze = [[0 for _ in range(maze_width)] for _ in range(maze_height)]
        self.player_x, self.player_y = 1, 1
        self.generate_maze()

    def generate_maze(self):
        stack = [(0, 0)]
        visited = set()

        while stack:
            x, y = stack[-1]
            visited.add((x, y))
            self.maze[y][x] |= 16  # Mark the current cell as visited

            neighbors = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
            random.shuffle(neighbors)
            # Applying Depth-first search algorithm
            for nx, ny in neighbors:
                if (nx, ny) not in visited and 0 <= nx < self.maze_width and 0 <= ny < self.maze_height:
                    stack.append((nx, ny))
                    dx, dy = nx - x, ny - y
                    self.maze[y + dy // 2][x + dx // 2] |= 16
                    self.maze[ny][nx] |= 16
                    break
                else:
                    visited.add((nx, ny))
            else:
                stack.pop()

    def move_player(self, dx, dy):
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        if (
            0 <= new_x < self.maze_width
            and 0 <= new_y < self.maze_height
            and not (self.maze[self.player_y][self.player_x] & (1 << [(1, 0), (-1, 0), (0, 1), (0, -1)].index((dx, dy))))
        ):
            self.player_x = new_x
            self.player_y = new_y

    def draw(self):
        self.screen.fill(WHITE)

        # Draw maze
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                if not (self.maze[y][x] & 1):  # Right wall
                    pygame.draw.line(self.screen, BLACK, (x * self.cell_size[0], y * self.cell_size[1]),
                                     (x * self.cell_size[0], (y + 1) * self.cell_size[1]), 2)
                if not (self.maze[y][x] & 2):  # Left wall
                    pygame.draw.line(self.screen, BLACK, (x * self.cell_size[0], y * self.cell_size[1]),
                                     ((x + 1) * self.cell_size[0], y * self.cell_size[1]), 2)
                if not (self.maze[y][x] & 4):  # Down wall
                    pygame.draw.line(self.screen, BLACK, (x * self.cell_size[0], (y + 1) * self.cell_size[1]),
                                     ((x + 1) * self.cell_size[0], (y + 1) * self.cell_size[1]), 2)
                if not (self.maze[y][x] & 8):  # Up wall
                    pygame.draw.line(self.screen, BLACK, (x * self.cell_size[0], y * self.cell_size[1]),
                                     ((x + 1) * self.cell_size[0], y * self.cell_size[1]), 2)

        pygame.draw.circle(self.screen, (255, 0, 0), (self.player_x * self.cell_size[0], self.player_y * self.cell_size[1]), 10)
        pygame.display.flip()