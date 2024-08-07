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
def shop_main():
    global mouse_pos, pressed
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
    #Skill tree button
    screen.blit(skill_tree_button1,skill_tree_button_rect)
    if skill_tree_button_rect.collidepoint(mouse_pos):
        screen.blit(skill_tree_button2,skill_tree_button_rect)
        if pressed[0]:
            shop_state_stack.append(skill_tree_menu)


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

skilltree_back_rect = back_button1.get_rect(center = (1000,100))

def skill_tree_menu():
    #display skill tree
    screen.blit(skill_tree_base,skill_tree_rect)
    screen.blit(base_description,(900,200))
    display_tree = current_tree.return_tree()
    for skill in display_tree:
        if skill is not None:
            skill.display()

    #back button
    screen.blit(back_button1,skilltree_back_rect)
    if skilltree_back_rect.collidepoint(mouse_pos):
        screen.blit(back_button2,skilltree_back_rect)
        if pressed[0]:
            shop_state_stack.pop()


shop_state_stack = [shop_main]

shop_background = image_import.get_image("pictures for survivor game/backgrounds/menu backgrounds/shop menu background.png",(screen.get_width(),screen.get_height()))
while True:
    key = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
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
    