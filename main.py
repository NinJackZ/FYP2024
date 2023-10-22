import pygame, sys, pyautogui
from menu import Menu
from button import Button

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = pyautogui.size()
WHITE = (255, 255, 255)
GREY = (105, 105, 105)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Menu")

# Create a menu
menu = Menu(screen)

# Create buttons and add them to the menu
play_button = Button(300, 250, 200, 50, "Play", GREY, (0, 200, 0))
quit_button = Button(300, 350, 200, 50, "Quit", GREY, (0, 200, 0), sys.exit)

menu.add_button(play_button)
menu.add_button(quit_button)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                menu.check_button_clicks(pos)

    screen.fill(WHITE)
    menu.draw()
    pygame.display.flip()

pygame.quit()