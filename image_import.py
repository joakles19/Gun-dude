import pygame
pygame.init()

#function to make importing images across files more efficient
def get_image(image,size):
    new_image = pygame.image.load(image).convert_alpha()
    new_image = pygame.transform.scale(new_image,size)
    return new_image

#Parent class for animations
class animation:
    def __init__(self,animation_list,animation_speed):
        self.animation = animation_list
        self.speed = animation_speed
        self.index = 0
    
    def play(self):
        if self.index >= len(self.animation):
            self.index = 0

        image = self.animation[self.index]
        self.index += self.speed

        return image
