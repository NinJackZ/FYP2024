import pygame, sys, os, cv2
from random import *
from menu import Menu
from button import Button
from maze import *
from goal import Goal
from images import Images
from config import grid, rows, cols, RES

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
icon = pygame.image.load(resource_path("assets/icon.jpg"))
bg = pygame.image.load(resource_path("assets/bg.jpg"))
game_bg = pygame.image.load(resource_path("assets/game_bg.jpg"))
player_sprite = pygame.image.load(resource_path('assets/player.png')).convert_alpha()
goal_image_path = resource_path("assets/destination.png")

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(icon)
pygame.display.set_caption("QuickMaze")
bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))
game_bg = pygame.transform.scale(game_bg,(WIDTH,HEIGHT))

# Create menu/game
menu = Menu(screen)

# Time
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 5

# Define object characteristics
play_button = Button(540, 300, 200, 50, "PLAY", (105, 105, 105), (0, 200, 0))
quit_button = Button(540, 500, 200, 50, "QUIT", (105, 105, 105), (0, 200, 0), sys.exit)
solve_button = Button(540, 400, 200, 50, "SOLVE", (105, 105, 105), (0, 200, 0))
title_image = Images(430, 100, resource_path("assets/title.png"), action=None)

# Display objects on screen
menu.add_button(play_button)
menu.add_button(solve_button)
menu.add_button(quit_button)
menu.add_image(title_image)

# Game constants
player_speed = 5
stage = 1

# Maze generation
maze = generate()
walls_collide_list = sum([cell.get_rects() for cell in maze], [])
goal_list = [Goal(grid, goal_image_path) for i in range(1)]

# Player controls
controls = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
key = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
player_sprite = pygame.transform.scale(player_sprite, (grid - 5 * maze[0].thickness, grid - 5 * maze[0].thickness))
player_rect = player_sprite.get_rect()
player_rect.center = grid // 2, grid // 2
direction = (0, 0)

# Main game loop
main_menu = True
in_game = False 
bg_i = 0

while main_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_menu = False
        if event.type == pygame.USEREVENT and in_game == True:
            time -= 1
        key = pygame.key.get_pressed()

    if not in_game:
        # Background animation
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
                    
                # if solve_button.rect.collidepoint(pos):
                #     IP_part()
    if in_game: 
        FPS = 120
        screen.fill('black')
        surface.blit(game_surface, (0, 0))
        game_surface.blit(game_bg, (0, 0))
        

        def hit_goal():
            global goal_list
            for goal in goal_list:
                if player_rect.collidepoint(goal.rect.center):
                    goal.set_pos()
                    regenerate_maze()
                    return True
            return False

        def regenerate_maze():
            global maze, walls_collide_list
            maze = generate()
            walls_collide_list = sum([cell.get_rects() for cell in maze],[])
            
        def collide(x, y):
            tmp_rect = player_rect.move(x, y)
            return tmp_rect.collidelist(walls_collide_list) != -1

        def game_over():
            global time, stage, record, in_game
            pygame.time.wait(700)
            in_game = False
            time = 60

        def reset_player_position():
            global player_rect
            valid_position = False
            while not valid_position:
                player_rect.center = (
                    randrange(1, cols - 1) * grid + grid // 2,
                    randrange(1, rows - 1) * grid + grid // 2
                )
                valid_position = not player_collides_with_walls()

        def player_collides_with_walls():
            return player_rect.collidelist(walls_collide_list) != -1
                
        # Goal and check player collision
        if hit_goal():
            stage += 1
            time += 10
            reset_player_position()
        if time == 0:
            game_over()

        # Draw player
        game_surface.blit(player_sprite, player_rect)

        # Draw Goal
        [goal.draw(game_surface) for goal in goal_list]

        # Draw maze
        for cell in maze:
            cell.draw(game_surface)    

        # Movement
        key = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
        pressed_keys = pygame.key.get_pressed()
        active_keys = [key for key, key_value in key.items() if pressed_keys[key_value]]
        direction = controls.get(active_keys[0], (0, 0)) if active_keys else (0, 0)
        if not collide(*direction):
            player_rect.move_ip(direction)

        # Stats
        time_color = pygame.Color('white')
        repos = 1135
        if time < 10:
            time_color = pygame.Color('red')
            repos += 10
        surface.blit(text_font.render('TIME', True, pygame.Color('white'), True), (1110, 30))
        surface.blit(font.render(f'{time}', True, time_color), (repos, 100))
        surface.blit(text_font.render('STAGE', True, pygame.Color('white'), True), (1100, 300))
        surface.blit(font.render(f'{stage}', True, pygame.Color('white')), (1150, 370))

        pygame.display.flip()
        clock.tick(FPS)
    else:
        menu.draw()
            
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
