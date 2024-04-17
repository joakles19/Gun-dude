import pygame
pygame.init()

#function to make importing images across files more efficient
def get_image(image,size):
    new_image = pygame.image.load(image).convert_alpha()
    new_image = pygame.transform.scale(new_image,size)
    return new_image

#Parent class for animations
class animation:
    def __init__(self,animation_list,animation_speed,size):
        self.animation = []
        for image in animation_list:
            self.animation.append(get_image(image,size))
        self.speed = animation_speed
        self.index = 0

    def play(self):
        if self.index >= len(self.animation):
            self.index = 0

        image = self.animation[self.index]
        self.index += self.speed

        return image

#Child classes for animations
class player_animation(animation):
    def __init__(self, animation_list, animation_speed,standing_image,size):
        super().__init__(animation_list, animation_speed,size)
        self.image = standing_image

class enemy_animation(animation):
    def __init__(self, animation_list, animation_speed,size):
        super().__init__(animation_list, animation_speed,size)