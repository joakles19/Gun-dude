import pygame,database,image_import, data_structures
from math import log10, floor
pygame.init()
screen = pygame.display.set_mode((1280,720))

currency = database.get_currency() #Fetches currency from database
coin_rect = pygame.rect.Rect(1120,60,90,70)

#Shop

#Main shop menu
menu_button1 = image_import.get_image("pictures for survivor game/buttons and icons/shop menu button 2.png",(220,100))
menu_button2 = image_import.get_image("pictures for survivor game/buttons and icons/shop menu button 1.png",(220,100))
menu_button_rect = menu_button1.get_rect(center = (1110,400))
char_button1 = image_import.get_image("pictures for survivor game/buttons and icons/char button 1.png",(420,540))
char_button2 = image_import.get_image("pictures for survivor game/buttons and icons/char button 2.png",(420,540))
char_button_rect = char_button1.get_rect(topleft = (70,150))
skill_tree_button1 = image_import.get_image("pictures for survivor game/buttons and icons/skill tree button 2.png",(420,540))
skill_tree_button2 = image_import.get_image("pictures for survivor game/buttons and icons/skill tree button 1.png",(420,540))
skill_tree_button_rect = skill_tree_button1.get_rect(topleft = (550,150))
back_button1 = image_import.get_image("pictures for survivor game/buttons and icons/back button 1.png",(90,90))
back_button2 = image_import.get_image("pictures for survivor game/buttons and icons/back button 2.png",(90,90))
back_button_rect = back_button1.get_rect(center = (1000,100))

#sounds
purchase_sound = pygame.mixer.Sound("Game music/purchasing.mp3")
beep_sound = pygame.mixer.Sound("Game music/skill selection.mp3")

def shop_main():
    global mouse_pos, pressed, can_press,press_cooldown
    #Menu button
    screen.blit(menu_button1,menu_button_rect)
    if menu_button_rect.collidepoint(mouse_pos):
        screen.blit(menu_button2,menu_button_rect)
        if pressed[0]:
            pygame.quit()
            exit()
    #Character customistion button
    screen.blit(char_button1,char_button_rect)
    if char_button_rect.collidepoint(mouse_pos):
        screen.blit(char_button2,char_button_rect)
        if pressed[0] and can_press:
            shop_state_stack.append(customisation_menu)
            can_press = False
            press_cooldown = 0
    #Skill tree button
    screen.blit(skill_tree_button1,skill_tree_button_rect)
    if skill_tree_button_rect.collidepoint(mouse_pos):
        screen.blit(skill_tree_button2,skill_tree_button_rect)
        if pressed[0]:
            shop_state_stack.append(skill_tree_menu)
            can_press = False
            press_cooldown = 0


#Skill tree menu
skill_tree_base = image_import.get_image("pictures for survivor game/backgrounds/Skill tree base.png",(770,410))
skill_tree_rect = skill_tree_base.get_rect(center = (480,420))
red_dot = image_import.get_image("pictures for survivor game/buttons and icons/available skill button.png",(70,70))
green_dot = image_import.get_image("pictures for survivor game/buttons and icons/purchased skill button.png",(70,70))
blue_outline = image_import.get_image("pictures for survivor game/buttons and icons/selected skill outline.png",(70,70))
base_description = image_import.get_image("pictures for survivor game/buttons and icons/Base description.png",(330,456))

class skills:
    def __init__(self,rect,description,value,price):
        self.node_rect = rect
        self.skill_description = description
        self.purchased = False
        self.value = value
        self.price = price

    def display(self):
        global current_tree, currency
        if self.purchased:
            screen.blit(green_dot,self.node_rect)
        else:
            screen.blit(red_dot,self.node_rect)

        if self.price < currency:
            can_buy = True
        else:
            can_buy = False
        if self.node_rect.collidepoint(mouse_pos):
            screen.blit(self.skill_description,(900,200))
            screen.blit(blue_outline,self.node_rect)
            if pressed[0] and self.purchased == False and can_buy:
                pygame.mixer.Sound.play(beep_sound)
                add_to_tree(self)
                self.purchase()
                currency -= self.price
                database.add_currency(-self.price)
                database.purchase_skill(self.value)
        
    def purchase(self):
        self.purchased = True

def add_to_tree(skill):
    node1,node2 = upgrade_tree.find_next_nodes(skill.value)
    if node1 is not None and node2 is not None:
        current_tree.insert(node1.node_value,node1.node_content)
        current_tree.insert(node2.node_value,node2.node_content)

damage_up1 = skills(pygame.rect.Rect(315,385,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Damage up description.png",(330,456)),4,20)
damage_up2 = skills(pygame.rect.Rect(215,265,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Damage up description 2.png",(330,456)),2,40)
damage_up3 = skills(pygame.rect.Rect(95,215,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Damage up description 3.png",(330,456)),1,60)
health_up1 = skills(pygame.rect.Rect(575,385,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Health up description.png",(330,456)),12,15)
health_up2 = skills(pygame.rect.Rect(675,265,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Health up description 2.png",(330,456)),14,30)
health_up3 = skills(pygame.rect.Rect(795,215,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Health up description 3.png",(330,456)),15,45)
lazer = skills(pygame.rect.Rect(95,315,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Lazer description.png",(330,456)),3,60)
fire_rate_up = skills(pygame.rect.Rect(215,505,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Fire rate description.png",(330,456)),6,45)
fire_rate_up2 = skills(pygame.rect.Rect(95,455,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Fire rate up description 2.png",(330,456)),5,55)
more_nukes = skills(pygame.rect.Rect(95,555,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/More nukes description.png",(330,456)),7,60)
coin_multiplier = skills(pygame.rect.Rect(675,505,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Coin multiplier description.png",(330,456)),10,25)
coin_multiplier2 = skills(pygame.rect.Rect(795,555,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Coin multiplier description 2.png",(330,456)),9,70)
invincibility = skills(pygame.rect.Rect(795,455,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Invincibility description.png",(330,456)),11,70)
passive_healing = skills(pygame.rect.Rect(795,315,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Passive healing description.png",(330,456)),13,70)

#setting up trees
#Tree base
upgrade_tree = data_structures.Tree(8,None)
upgrade_tree.insert(4,damage_up1)
upgrade_tree.insert(2,damage_up2)
upgrade_tree.insert(1,damage_up3)
upgrade_tree.insert(3,lazer)
upgrade_tree.insert(6,fire_rate_up)
upgrade_tree.insert(5,fire_rate_up2)
upgrade_tree.insert(7,more_nukes)
upgrade_tree.insert(12,health_up1)
upgrade_tree.insert(10,coin_multiplier)
upgrade_tree.insert(14,health_up2)
upgrade_tree.insert(9,coin_multiplier2)
upgrade_tree.insert(11,invincibility)
upgrade_tree.insert(13,passive_healing)
upgrade_tree.insert(15,health_up3)
skills_list = [damage_up3,damage_up2,lazer,damage_up1,fire_rate_up2,fire_rate_up,more_nukes,None,coin_multiplier2,coin_multiplier,invincibility,health_up1,passive_healing,health_up2,health_up3]

#User's skill tree
current_tree = data_structures.Tree(8,None)
current_tree.insert(4,damage_up1)
current_tree.insert(12,health_up1)
users_skills = database.get_skills()

for skill in users_skills:
    skill_num = int(skill[0])-1
    skills_list[skill_num].purchase()
    add_to_tree(skills_list[skill_num])

def skill_tree_menu():
    #display skill tree
    screen.blit(skill_tree_base,skill_tree_rect)
    screen.blit(base_description,(900,200))
    display_tree = current_tree.return_tree()
    for skill in display_tree:
        if skill is not None:
            skill.display()

    #back button
    screen.blit(back_button1,back_button_rect)
    if back_button_rect.collidepoint(mouse_pos):
        screen.blit(back_button2,back_button_rect)
        if pressed[0]:
            shop_state_stack.pop()


class skin_button:
    def __init__(self,skin,skin_name,price):
        self.base1 = image_import.get_image("pictures for survivor game/buttons and icons/skin button 1.png",(230,290))
        self.base2 = image_import.get_image("pictures for survivor game/buttons and icons/skin button 2.png",(230,290))
        self.price = price
        if price == 5:
            self.locked = image_import.get_image("pictures for survivor game/buttons and icons/lock 5.png",(230,290))
        else:
            self.locked = image_import.get_image("pictures for survivor game/buttons and icons/lock 10.png",(230,290))
        self.skin = image_import.get_image(skin,(192,228))
        self.skin_name = skin_name
        self.num = 1
        if database.is_skin_puchased(skin_name) == 1:
            self.purchased = True
        else:
            self.purchased = False
    
    def display(self):
        global can_press, press_cooldown, currency
        self.rect = self.base1.get_rect(topleft = (250*self.num-100,250))
        self.skin_rect = self.skin.get_rect(center = self.rect.center)
        self.selected_message = image_import.get_image("pictures for survivor game/selected.png",(186,50))
        self.message_rect = self.selected_message.get_rect(bottom = self.rect.top, centerx = self.rect.centerx)

        screen.blit(self.base1,self.rect)
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.base2,self.rect)
            if pressed[0] and can_press:
                if self.purchased:
                    database.select_skin(self.skin_name,True,False)
                if self.purchased == False and currency >= self.price:
                    pygame.mixer.Sound.play(purchase_sound)
                    database.add_currency(-self.price)
                    currency -= self.price
                    database.select_skin(self.skin_name,False,True)
                    self.purchased = True
                can_press = False
                press_cooldown = 0

        screen.blit(self.skin,self.skin_rect)

        if self.purchased == False:
            screen.blit(self.locked,self.rect)
        
        if database.get_selected_skin() == self.skin_name:
            screen.blit(self.selected_message,self.message_rect)

skin_buttons = []
skin_buttons.append(skin_button("pictures for survivor game/dude graphics/dude stand 90.png",'',0))
skin_buttons.append(skin_button("pictures for survivor game/dude graphics/dude stand 90Green.png",'Green',5))
skin_buttons.append(skin_button("pictures for survivor game/dude graphics/dude stand 90Purple.png",'Purple',5))
skin_buttons.append(skin_button("pictures for survivor game/dude graphics/dude stand 90Grey.png",'Grey',5))
skin_buttons.append(skin_button("pictures for survivor game/dude graphics/dude stand 90Orange.png",'Orange',5))
skin_buttons.append(skin_button("pictures for survivor game/dude graphics/dude stand 90Black.png",'Black',10))
skin_buttons.append(skin_button("pictures for survivor game/dude graphics/dude stand 90Naked.png",'Naked',10))
skin_buttons.append(skin_button("pictures for survivor game/dude graphics/dude stand 90Gman.png",'Gman',10))


display_list = []
for n in range(0,4):
    display_list.append(skin_buttons[n])

right_arrow1 = image_import.get_image("pictures for survivor game/buttons and icons/arrow button 1.png",(60,60))
right_arrow2 = image_import.get_image("pictures for survivor game/buttons and icons/arrow button 2.png",(60,60))
left_arrow1 = pygame.transform.rotate(right_arrow1,180)
left_arrow2 = pygame.transform.rotate(right_arrow2,180)
left_arrow_rect = left_arrow1.get_rect(topleft = (70,370))
right_arrow_rect = right_arrow1.get_rect(topleft = (1150,370))

def customisation_menu():
    global can_press,press_cooldown

    for button in display_list:
        button.display()

    for n in range(0,4):
        display_list[n].num = n+1

    if display_list[0] != skin_buttons[0]:
        screen.blit(left_arrow1,left_arrow_rect)
        if left_arrow_rect.collidepoint(mouse_pos):
            screen.blit(left_arrow2,left_arrow_rect)
            if pressed[0] and can_press:
                can_press = False
                press_cooldown = 0
                display_list.pop()
                display_list.insert(0,skin_buttons[skin_buttons.index(display_list[0])-1])

    if display_list[3] != skin_buttons[len(skin_buttons)-1]:
        screen.blit(right_arrow1,right_arrow_rect)
        if right_arrow_rect.collidepoint(mouse_pos):
            screen.blit(right_arrow2,right_arrow_rect)
            if pressed[0] and can_press:
                can_press = False
                press_cooldown = 0
                display_list.append(skin_buttons[skin_buttons.index(display_list[3])+1])
                display_list.pop(0)

    #back button
    screen.blit(back_button1,back_button_rect)
    if back_button_rect.collidepoint(mouse_pos):
        screen.blit(back_button2,back_button_rect)
        if pressed[0]:
            shop_state_stack.pop()

can_press = True
press_cooldown = -1

shop_state_stack = [shop_main]

shop_background = image_import.get_image("pictures for survivor game/backgrounds/menu backgrounds/shop menu background.png",(screen.get_width(),screen.get_height()))
while True:
    key = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    if press_cooldown >= 0:
        press_cooldown += 1
        if press_cooldown >= 60:
            press_cooldown = -1
            can_press = True

    #Rendering permanent shop background graphics
    #Rendering currency in top corner/ resizing it to fit in graphic
    currency_font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",floor(50-(log10(currency+1))*5))
    currency_message = currency_font.render(f"{currency}",False,"Orange")
    currency_rect = currency_message.get_rect(center = coin_rect.center)
    #displaying the graphics to the screen
    screen.blit(shop_background,(0,0))
    screen.blit(currency_message,currency_rect)

    current_state = len(shop_state_stack) - 1
    shop_state_stack[current_state]()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

    pygame.display.update()
    