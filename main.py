import pygame, pyautogui

pygame.init()

WIDTH, HEIGHT = pyautogui.size()
SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT  = HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

def draw_text(text, font, text_col, x, y):
     img = font.render(text, True, text_col)
     screen.blit(img, (x,y))

run = True
while run:
    
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                run = False

    pygame.display.update()


pygame.quit()