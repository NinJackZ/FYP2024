import pygame, pyautogui, button

pygame.init()

WIDTH, HEIGHT = pyautogui.size()
SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT  = HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

game_paused = False
font = pygame.font.SysFont("arialblack", 40)
TEXT_COL = (255,255,255)

play_img = pygame.image.load("assets/play.png").convert_alpha()
quit_img = pygame.image.load("assets/quit.png").convert_alpha()
bg = pygame.image.load("assets/bg.png").convert_alpha()
play_button = button.Button(SCREEN_WIDTH/SCREEN_HEIGHT + 200, SCREEN_HEIGHT/4 , play_img, 2)
quit_button = button.Button(SCREEN_WIDTH - 200 , 0, quit_img, 1)
 

def draw_text(text, font, text_col, x, y):
     img = font.render(text, True, text_col)
     screen.blit(img, (x,y))

run = True
while run:
    
    screen.fill((129,133,137))

    if game_paused == True:
        if play_button.draw(screen):
                game_paused = False
        if quit_button.draw(screen):
                game_paused = False
                run = False
    else:
         draw_text("Space", font, TEXT_COL, 160, 250)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                     game_paused = True
                if event.type == pygame.QUIT:
                        run = False

    pygame.display.update()


pygame.quit()