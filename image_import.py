import pygame
pygame.init()

#function to make importing images across files more efficient
def get_image(image,size):
    new_image = pygame.image.load(image).convert_alpha()
    new_image = pygame.transform.scale(new_image,size)
    return new_image