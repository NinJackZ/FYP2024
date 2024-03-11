import pygame
from button import Button

class Endscreen:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.images =[]

    def add_button(self, button):
        self.buttons.append(button)

    def add_image(self,image):
        self.images.append(image)

    def check_button_clicks(self, pos):
        for button in self.buttons:
            if button.is_hovered(pos):
                if button.action:
                    button.action()

    def draw(self):
        for button in self.buttons:
            if button.is_hovered(pygame.mouse.get_pos()):
                button.draw(self.screen, (105, 255, 255))
            else:
                button.draw(self.screen)

        for image in self.images:
            image.draw(self.screen)