import pygame
from random import randrange

class Goal:
    def __init__(self, GRID):
        self.img = pygame.image.load('assets/destination.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (GRID - 10, GRID - 10))
        self.rect = self.img.get_rect()
        self.GRID = GRID
        

    def set_pos(self):
        self.rect.topleft = randrange(1080 // self.GRID) * self.GRID + 5, randrange(520 // self.GRID) * self.GRID + 5


    def draw(self, game_surface):
        game_surface.blit(self.img, self.rect)