import pygame

class Images:
    def __init__(self, x, y, image_path, action=None):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)