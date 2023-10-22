import pygame
from button import Button

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

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