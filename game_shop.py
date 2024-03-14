import pygame
pygame.init()
screen = pygame.display.set_mode((1280,720))
#Shop
shop_background = pygame.image.load("pictures for survivor game/backgrounds/level 1 background.png")
def shop():
    screen.blit(shop_background,(0,0))
    