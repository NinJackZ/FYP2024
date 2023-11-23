import pygame, sys
from menu import Menu
from button import Button
from game import *
from images import Images

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
GREY = (105, 105, 105)
FPS = 60
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()
icon = pygame.image.load("assets/icon.jpg")
bg = pygame.image.load("assets/bg.jpg")
game_bg = pygame.image.load("assets/game_bg.jpg")

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(icon)
pygame.display.set_caption("QuickMaze")
bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))
game_bg = pygame.transform.scale(game_bg,(WIDTH,HEIGHT))

# Create menu/game
menu = Menu(screen)
maze = generate_maze()

# collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

# timer, score, record
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 60
score = 0

# Define object characteristics
play_button = Button(540, 300, 200, 50, "PLAY", GREY, (0, 200, 0))
quit_button = Button(540, 400, 200, 50, "QUIT", GREY, (0, 200, 0), sys.exit)
title_image = Images(430, 100, "assets/title.png", action=None)

# Display objects on screen
menu.add_button(play_button)
menu.add_button(quit_button)
menu.add_image(title_image)

# Main game loop
running = True
in_game = False 
bg_i = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()

    if not in_game:
        screen.fill((0,0,0))
        screen.blit(bg,(bg_i,0))
        screen.blit(bg,(WIDTH+bg_i,0))
        if (bg_i==-WIDTH):
            screen.blit(bg,(WIDTH+bg_i,0))
            bg_i=0
        bg_i-=1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                menu.check_button_clicks(pos)
                if play_button.rect.collidepoint(pos):
                    in_game = True


    if in_game: 
        screen.fill('black')
        surface.blit(game_surface, (0, 0))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                time -= 1

        # draw maze
        for cell in maze:
            cell.draw(game_surface)
        pygame.display.flip()
        clock.tick(FPS)
        
    else:
        menu.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()