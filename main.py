import pygame, sys
from menu import Menu
from button import Button
from maze import *
from images import Images

def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
FPS = 60
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()
text_font = pygame.font.SysFont('Calibri', 50)
font = pygame.font.SysFont('Calibri', 50)

# Assets
icon = pygame.image.load("assets/icon.jpg")
bg = pygame.image.load("assets/bg.jpg")
game_bg = pygame.image.load("assets/game_bg.jpg")
player_sprite = pygame.image.load('assets/quit.png').convert_alpha()

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(icon)
pygame.display.set_caption("QuickMaze")
bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))
game_bg = pygame.transform.scale(game_bg,(WIDTH,HEIGHT))

# Create menu/game
menu = Menu(screen)
maze = generate()

# Collisions
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

# Time
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 60

# Define object characteristics
play_button = Button(540, 300, 200, 50, "PLAY", (105, 105, 105), (0, 200, 0))
quit_button = Button(540, 500, 200, 50, "QUIT", (105, 105, 105), (0, 200, 0), sys.exit)
solve_button = Button(540, 400, 200, 50, "SOLVE", (105, 105, 105), (0, 200, 0))
ingame_quit_button = Button(540, 400, 200, 50, "QUIT", (105, 105, 105), (0, 200, 0), sys.exit)
title_image = Images(430, 100, "assets/title.png", action=None)

# Player
speed = 5
controls = {'a': (-speed, 0), 'd': (speed, 0), 'w': (0, -speed), 's': (0, speed)}
key = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}

player_sprite = pygame.transform.scale(player_sprite, (GRID - 2 * maze[0].thickness, GRID - 2 * maze[0].thickness))
player_rect = player_sprite.get_rect()
player_rect.center = GRID // 2, GRID // 2
direction = (0, 0)

# Display objects on screen
menu.add_button(play_button)
menu.add_button(solve_button)
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
        if event.type == pygame.USEREVENT:
            time -= 1

        key = pygame.key.get_pressed()

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
        FPS = 120
        screen.fill('black')
        surface.blit(game_surface, (0, 0))
        game_surface.blit(game_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                time -= 1

        # Draw player
        game_surface.blit(player_sprite, player_rect)

        # Draw maze
        for cell in maze:
            cell.draw(game_surface)

        # Movement
        key = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
        pressed_keys = pygame.key.get_pressed()
        active_keys = [key for key, key_value in key.items() if pressed_keys[key_value]]
        direction = controls.get(active_keys[0], (0, 0)) if active_keys else (0, 0)
        if not is_collide(*direction):
            player_rect.move_ip(direction)

        # Stats
        surface.blit(text_font.render('TIME', True, pygame.Color('white'), True), (1085, 30))
        surface.blit(font.render(f'{time}', True, pygame.Color('white')), (1110, 105))
        surface.blit(text_font.render('STAGE', True, pygame.Color('white'), True), (1075, 300))

        pygame.display.flip()
        clock.tick(FPS)
        
    else:
        menu.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()