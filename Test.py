import pygame, pyautogui

pygame.init()

width, height = pyautogui.size()

SCREEN_WIDTH = width
SCREEN_HEIGHT  = height

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = pygame.Rect((300,150,50,50))

run = True
while run:

    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255,155,150), player)

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1,0)
    elif key[pygame.K_d] == True:
        player.move_ip(1,0)
    elif key[pygame.K_w] == True:
        player.move_ip(0,-1)
    elif key[pygame.K_s] == True:
        player.move_ip(0,1)
    elif key[pygame.K_ESCAPE] == True:
        pygame.quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()