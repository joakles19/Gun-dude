import pygame, database, image_import
pygame.init()
screen = pygame.display.set_mode((1280,720))

font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",50)

class username:
    def __init__(self):
        self.list = []
        self.can_type = True
        self.type_marker_timer = 0

    def backspace(self):
        if len(self.list) > 0:
            self.list.pop()    
    
    def space(self):
        self.list.append(" ")
    
    def add(self,input):
        if self.can_type:
            if (input >= 97 and input <= 122) or (input >= 48 and input <= 58):
                self.type(input)
            if input == 32:
                self.space()
        if input == 8:
            self.backspace()

    def type(self,input):
        alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        numbers = ["0","1","2","3","4","5","6","7","8","9"]
        typekey = ""
        if input >= 97 and input <= 122:
            input -= 97
            typekey = alphabet[input]
        if input >= 48 and input <= 58:
            input -= 48
            typekey = numbers[input]

        self.list.append(typekey)

    def display(self,rect):
        username = ""
        for letter in self.list:
            username += letter

        display_name = pygame.font.Font.render(font,username,False,"White")
        display_name_rect = display_name.get_rect(center = rect.center)
        if display_name_rect.width > rect.width - 150:
            self.can_type = False
        else:
            self.can_type = True
        screen.blit(display_name,display_name_rect)
        
        type_marker = pygame.font.Font.render(font,"|",False,"Grey")
        self.type_marker_timer += 0.01
        if self.type_marker_timer >= 5:
            screen.blit(type_marker,(display_name_rect.topright))
        if self.type_marker_timer >= 10:
            self.type_marker_timer = 0
Username = username()

text_box = image_import.get_image("pictures for survivor game/backgrounds/Text box.png",(1100,150))
text_box_rect = text_box.get_rect(center = (screen.get_width()/2,screen.get_height()/2))
background = image_import.get_image("pictures for survivor game/backgrounds/login screen background.png",(1280,720))
save_button1 = image_import.get_image("pictures for survivor game/buttons and icons/save 1.png",(400,200))
save_button2 = image_import.get_image("pictures for survivor game/buttons and icons/save 2.png",(400,200))
save_button_rect = save_button1.get_rect(center = (640,550))


def main_screen():
    screen.blit(background,(0,0))
    screen.blit(text_box,text_box_rect)
    screen.blit(save_button1,save_button_rect)
    Username.display(text_box_rect)

    if save_button_rect.collidepoint(mouse) and Username.list != []:
        screen.blit(save_button2,save_button_rect)


while True:
    mouse = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    main_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            Username.add(event.key)

    pygame.display.update()