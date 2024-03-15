import pygame
pygame.init()
screen = pygame.display.set_mode((1280,720))

font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",100)

#Shop
shop_background = pygame.image.load("pictures for survivor game/backgrounds/level 1 background.png")

def shop_menu():
    pass

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            pygame.quit()
            exit()
    pygame.display.update()

