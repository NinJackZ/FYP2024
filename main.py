import pygame, sys
from menu import Menu
from button import Button
from game import Game
from images import Images

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
GREY = (105, 105, 105)
icon = pygame.image.load("assets/icon.jpg")

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(icon)
pygame.display.set_caption("QuickMaze")
bg = pygame.image.load("assets/bg.jpg")
bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))

# Create menu
menu = Menu(screen)

# Define object characteristics
play_button = Button(540, 300, 200, 50, "Play", GREY, (0, 200, 0))
quit_button = Button(540, 400, 200, 50, "Quit", GREY, (0, 200, 0), sys.exit)
title_image = Images(430, 100, "assets/title.png", action=None)

# Display objects on screen
menu.add_button(play_button)
menu.add_button(quit_button)
menu.add_image(title_image)
game = Game(screen, 10, 10)

# Main game loop
running = True
in_game = False 
bg_i = 0

while running:
    screen.fill((0,0,0))
    screen.blit(bg,(bg_i,0))
    screen.blit(bg,(WIDTH+bg_i,0))
    if (bg_i==-WIDTH):
        screen.blit(bg,(WIDTH+bg_i,0))
        bg_i=0
    bg_i-=1
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

    pygame.display.update()

pygame.quit()