import pygame,database,image_import, skill_tree
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

#Rectangles so skill tree nodes are interactive
STrect1 = pygame.rect.Rect(95,215,70,70)
STrect2 = pygame.rect.Rect(95,315,70,70)
STrect3 = pygame.rect.Rect(95,455,70,70)
STrect4 = pygame.rect.Rect(95,555,70,70)
STrect6 = pygame.rect.Rect(215,265,70,70)
STrect7 = pygame.rect.Rect(215,505,70,70)
STrect8 = pygame.rect.Rect(675,265,70,70)
STrect9 = pygame.rect.Rect(795,215,70,70)
STrect10 = pygame.rect.Rect(795,315,70,70)
STrect11 = pygame.rect.Rect(795,455,70,70)
STrect12 = pygame.rect.Rect(795,555,70,70)
STrect13 = pygame.rect.Rect(575,385,70,70)
STrect14 = pygame.rect.Rect(675,505,70,70)

class skills:
    def __init__(self,rect,description):
        self.node_rect = rect
        self.skill_description = description
    def description_display(self):
        if self.node_rect.collidepoint(mouse_pos):
            screen.blit(self.skill_description,(900,200))
            screen.blit(blue_outline,self.node_rect)

damage_up1 = skills(pygame.rect.Rect(315,385,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Damage up description.png",(330,456)))
damage_up2 = skills(pygame.rect.Rect(215,265,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Damage up description 2.png",(330,456)))
damage_up3 = skills(pygame.rect.Rect(95,215,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Damage up description 3.png",(330,456)))
health_up1 = skills(pygame.rect.Rect(575,385,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Health up description.png",(330,456)))
lazer = skills(pygame.rect.Rect(95,315,70,70),image_import.get_image("pictures for survivor game/buttons and icons/skill descriptions/Lazer description.png",(330,456)))
skills_list = [damage_up1,health_up1,damage_up2,damage_up3,lazer]

#setting up tree
upgrade_tree = skill_tree.Tree(None)
upgrade_tree.root.left = skill_tree.Node(damage_up1)
upgrade_tree.root.right =  skill_tree.Node(health_up1)

#Skill descriptions
base_description = image_import.get_image("pictures for survivor game/buttons and icons/Base description.png",(330,456))

game_skill_tree = skill_tree.Tree("Base")
game_skill_tree.root.left = "Fill"
def skill_tree_menu():
    screen.blit(skill_tree_base,skill_tree_rect)
    screen.blit(base_description,(900,200))
    for skill in skills_list:
        skill.description_display()

    

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
    