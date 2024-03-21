import pygame,database,image_import
from math import log10, floor
pygame.init()
screen = pygame.display.set_mode((1280,720))

currency = database.get_currency() #Fetches currency from database
coin_rect = pygame.rect.Rect(1120,60,90,70)

#Shop

#Main shop menu
menu_button1 = image_import.get_image("pictures for survivor game/buttons and icons/shop menu button 2.png",(220,100))
menu_button2 = image_import.get_image("pictures for survivor game/buttons and icons/shop menu button 1.png",(220,100))
menu_button_rect = menu_button1.get_rect(bottomright = (screen.get_width()-40,screen.get_height()/2))
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

    screen.blit(char_button1,char_button_rect)
    if char_button_rect.collidepoint(mouse_pos):
        screen.blit(char_button2,char_button_rect)

    screen.blit(skill_tree_button1,skill_tree_button_rect)

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
    shop_main()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

    pygame.display.update()
    