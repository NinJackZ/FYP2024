import pygame, sys, pyautogui
from menu import Menu
from button import Button
from game import Game

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = pyautogui.size()
WHITE = (255, 255, 255)
GREY = (105, 105, 105)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Menu")

# Create menu
menu = Menu(screen)

# Create buttons and add them to the menu
play_button = Button(300, 250, 200, 50, "Play", GREY, (0, 200, 0))
quit_button = Button(300, 350, 200, 50, "Quit", GREY, (0, 200, 0), sys.exit)

menu.add_button(play_button)
menu.add_button(quit_button)

game = Game(screen, 10, 10)

# Main game loop
running = True
in_game = False 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

    if not in_game:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                menu.check_button_clicks(pos)
                if play_button.rect.collidepoint(pos):
                    in_game = True

    screen.fill(WHITE)

    if in_game:
        # Handle player movement based on keys
        if keys[pygame.K_w]:
            game.move_player(0, -1)  # Move up
        if keys[pygame.K_a]:
            game.move_player(-1, 0)  # Move left
        if keys[pygame.K_s]:
            game.move_player(0, 1)   # Move down
        if keys[pygame.K_d]:
            game.move_player(1, 0)   # Move right
        game.draw()
    else:
        menu.draw()

    pygame.display.flip()

pygame.quit()