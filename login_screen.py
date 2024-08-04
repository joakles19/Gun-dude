import pygame, database, image_import, data_structures
pygame.init()
screen = pygame.display.set_mode((1280,720))

font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",50)

class keyboard:
    def __init__(self):
        self.list = []
        self.word = ""
        self.can_type = True
        self.type_marker_timer = 0

    def backspace(self):
        if len(self.list) > 0:
            self.list.pop()    
    
    def add(self,input):
        if self.can_type:
            if (input >= 97 and input <= 122) or (input >= 48 and input <= 58):
                self.type(input)
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
        if display_name_rect.width > rect.width - 180:
            self.can_type = False
        else:
            self.can_type = True
        screen.blit(display_name,display_name_rect)
        
        type_marker = pygame.font.Font.render(font,"|",False,"Grey")
        self.type_marker_timer += 0.01
        if self.type_marker_timer >= 2:
            screen.blit(type_marker,(display_name_rect.topright))
        if self.type_marker_timer >= 4:
            self.type_marker_timer = 0

    def get_word(self):
        for letter in self.list:
            self.word = self.word + letter
        return self.word

Username = keyboard()

text_box = image_import.get_image("pictures for survivor game/backgrounds/Text box.png",(1100,150))
text_box_rect = text_box.get_rect(center = (screen.get_width()/2,screen.get_height()/2))
background1 = image_import.get_image("pictures for survivor game/backgrounds/save background.png",(1280,720))
background2 = image_import.get_image("pictures for survivor game/backgrounds/login screen background.png",(1280,720))
save_button1 = image_import.get_image("pictures for survivor game/buttons and icons/save 1.png",(400,200))
save_button2 = image_import.get_image("pictures for survivor game/buttons and icons/save 2.png",(400,200))
save_button_rect = save_button1.get_rect(center = (640,550))

back_button1 = image_import.get_image('pictures for survivor game/buttons and icons/back button 1.png',(80,80))
back_button2 = image_import.get_image('pictures for survivor game/buttons and icons/back button 2.png',(80,80))
back_button_rect = back_button1.get_rect(center = (100,110))

delete_user_button1 = image_import.get_image("pictures for survivor game/buttons and icons/exit button 2.png",(40,40))
delete_user_button2 = image_import.get_image("pictures for survivor game/buttons and icons/exit button 1.png",(40,40))

class username:
    def __init__(self,name,inuse,index):
        self.name = name
        self.pos_index = index
        self.state = inuse

    def display(self):
        global cooldown_timer, can_press
        display_name1 = pygame.font.Font.render(font,self.name,False,'Black')
        display_name2 = pygame.font.Font.render(font,self.name,False,'White')
        display_name3 = pygame.font.Font.render(font,self.name,False,'Blue')

        rect = display_name1.get_rect(topleft = (170,self.pos_index*65+190))
        delete_rect = delete_user_button1.get_rect(left = rect.right, centery = rect.centery)

        if self.state == 1:
            screen.blit(display_name3,rect)
        else:
            screen.blit(display_name1,rect)
        if rect.collidepoint(mouse) or delete_rect.collidepoint(mouse):
            screen.blit(display_name2,rect)
            screen.blit(delete_user_button1,delete_rect)
            if pressed[0] and can_press and delete_rect.collidepoint(mouse) == False:
                database.choose_user(self.name)
                can_press = False
                cooldown_timer = 1

            if delete_rect.collidepoint(mouse):
                screen.blit(delete_user_button2,delete_rect)
                if pressed[0] and can_press:
                    database.delete_user(self.name)
                    can_press = False
                    cooldown_timer = 1

            

arrow_button1,arrow_button2 = image_import.get_image("pictures for survivor game/buttons and icons/arrow button 1.png",(70,70)),image_import.get_image("pictures for survivor game/buttons and icons/arrow button 2.png",(70,70))
up_button1,up_button2 = pygame.transform.rotate(arrow_button1,90),pygame.transform.rotate(arrow_button2,90)
down_button1,down_button2 = pygame.transform.rotate(arrow_button1,270),pygame.transform.rotate(arrow_button2,270)
up_button_rect = up_button1.get_rect(topleft = (70,180))
down_button_rect = down_button1.get_rect(topleft = (70,540))

add_user_button1 = image_import.get_image("pictures for survivor game/buttons and icons/add user button 1.png",(180,130))
add_user_button2 = image_import.get_image("pictures for survivor game/buttons and icons/add user button 2.png",(180,130))
add_user_button_rect = add_user_button1.get_rect(center = (1010,400))

cooldown_timer = 0
can_press = True
min_name = 0

def main_screen():
    global cooldown_timer, can_press, min_name, Username
    Username = keyboard()
    display_names = []
    for n in range(0,6):
        try:
            display_names.append(username(database_names[n+min_name][0],database_names[n+min_name][1],n))
        except:
            break

    screen.blit(background1,(0,0))
    for name in display_names:
        name.display()
    
    if min_name > 0:
        screen.blit(up_button1,up_button_rect)
        if up_button_rect.collidepoint(mouse):
            screen.blit(up_button2,up_button_rect)
            if pressed[0] and can_press:
                min_name -= 1
                cooldown_timer = 1
                can_press = False

    if min_name + 6 < len(database_names):
        screen.blit(down_button1,down_button_rect)
        if down_button_rect.collidepoint(mouse):
            screen.blit(down_button2,down_button_rect)
            if pressed[0] and can_press:
                min_name += 1
                cooldown_timer = 1
                can_press = False
    
    screen.blit(add_user_button1,add_user_button_rect)
    if add_user_button_rect.collidepoint(mouse):
        screen.blit(add_user_button2,add_user_button_rect)
        if pressed[0] and can_press:
            login_screen_stack.append(new_user_screen)

def new_user_screen():
    global cooldown_timer, can_press, Username, unique_name
    screen.blit(background2,(0,0))
    screen.blit(text_box,text_box_rect)
    screen.blit(save_button1,save_button_rect)
    Username.display(text_box_rect)

    if save_button_rect.collidepoint(mouse) and Username.list != []:
        screen.blit(save_button2,save_button_rect)
        if pressed[0] and can_press:
            entername = Username.get_word()
            for name in database_names:
                if name[0] == entername:
                    entername += 'I'
            database.new_username(entername)
            database.create_tables(entername)
            can_press = False
            cooldown_timer = 1
            login_screen_stack.pop()

login_screen_stack = [main_screen]

while True:
    mouse = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
    database_names = database.return_usernames()
    database_names = data_structures.quick_sort(database_names)

    login_screen_stack[len(login_screen_stack)-1]()

    screen.blit(back_button1,back_button_rect)
    if back_button_rect.collidepoint(mouse):
        screen.blit(back_button2,back_button_rect)
        if pressed[0] and can_press:
            if len(login_screen_stack)>1:
                login_screen_stack.pop()
                cooldown_timer = 1
                can_press = False
            else:
                pygame.quit()
                exit()

    if cooldown_timer > 0:
        cooldown_timer += 1
        if cooldown_timer >= 50:
            cooldown_timer = 0
            can_press = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            Username.add(event.key)

    pygame.display.update()