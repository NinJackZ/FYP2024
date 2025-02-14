import pygame
from random import randrange

class Goal:
    def __init__(self, GRID, image_path):
        self.img = pygame.image.load(image_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (GRID - 10, GRID - 10))
        self.rect = self.img.get_rect()
        self.GRID = GRID
        self.set_pos()
        

    def set_pos(self):
        self.rect.topleft = randrange(1080 // self.GRID) * self.GRID + 5, randrange(520 // self.GRID) * self.GRID + 5
        self.pos = self.rect.topleft


    def draw(self, game_surface):
        game_surface.blit(self.img, self.rect.topleft)

