import pygame
from random import randrange

class Goal:
    def __init__(self, GRID, cols, rows):
        self.img = pygame.image.load('assets/destination.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (GRID - 10, GRID - 10))
        self.rect = self.img.get_rect()
        self.GRID = GRID
        self.set_pos(cols, rows)

    def set_pos(self, cols, rows):
        self.rect.topleft = randrange(cols) * self.GRID + 5, randrange(rows) * self.GRID + 5


    def draw(self, game_surface):
        game_surface.blit(self.img, self.rect)