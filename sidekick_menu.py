#API call on line 15
#Json parsing on line 47

import pygame, database, image_import, requests
import random
pygame.init()

screen = pygame.display.set_mode((1280,720))
cooldown_timer = 0

font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",23)
denied_font  = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",50)
code_font = pygame.font.Font(None,140)

headers = {"Accept": "application/json","Content-Type": "application/json"}
response = requests.request("GET","https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15",headers=headers) #API call to recieve game information
games_json = response.json() #Stores information into json format

#Menu graphics
background = image_import.get_image("pictures for survivor game/backgrounds/menu backgrounds/deals background.png",(1280,720))
logo = image_import.get_image("pictures for survivor game/Shop logo.png",(350,350))
menu_button1 = image_import.get_image("pictures for survivor game/buttons and icons/shop menu button 2.png",(220,100))
menu_button2 = image_import.get_image("pictures for survivor game/buttons and icons/shop menu button 1.png",(220,100))
menu_button_rect = menu_button1.get_rect(topleft = (20,20))
price_button1 = image_import.get_image("pictures for survivor game/buttons and icons/price button 1.png",(150,100))
price_button2 = image_import.get_image("pictures for survivor game/buttons and icons/price button 2.png",(150,100))
price_button_rect = price_button1.get_rect(topleft = (30,550))
rating_button1 = image_import.get_image("pictures for survivor game/buttons and icons/rating button 1.png",(150,100))
rating_button2 = image_import.get_image("pictures for survivor game/buttons and icons/rating button 2.png",(150,100))
rating_button_rect = price_button1.get_rect(topleft = (200,550))
right_button1,right_button2 = image_import.get_image("pictures for survivor game/buttons and icons/arrow button 1.png",(70,70)),image_import.get_image("pictures for survivor game/buttons and icons/arrow button 2.png",(70,70))
left_button1, left_button2 = pygame.transform.rotate(right_button1,180),pygame.transform.rotate(right_button2,180)
right_button_rect = right_button1.get_rect(center = (1200,70))
left_button_rect = left_button1.get_rect(center = (400,70))
discount_button1 = image_import.get_image("pictures for survivor game/buttons and icons/discount button 1.png",(300,50))
discount_button2 = image_import.get_image("pictures for survivor game/buttons and icons/discount button 2.png",(300,50))
discount_button_rect = discount_button1.get_rect(center = (190,500))

#Indexes and timers for interface
info_num = 0
press_index = 0
can_press = True

class game_info:
    def __init__(self,info,index):
        self.index = index
        #Parsing of json file to display specific information
        self.display_name = pygame.font.Font.render(font,info["title"],False,"#fc6aa2")
        self.deal_message = "From £"+info["normalPrice"]+" down to £"+info["salePrice"]
        self.rating_message = "Metacritic:"+info["metacriticScore"]+ " Steam:"+info["steamRatingPercent"]
        self.display_info = pygame.font.Font.render(font,self.deal_message,False,"#ffb0ce")
        self.rect1 = self.display_name.get_rect(topleft = (390,self.index*54+130))
        self.rect2 = self.display_info.get_rect(topleft = self.rect1.bottomleft)
    def display(self,info_num):
        screen.blit(self.display_name,self.rect1)
        if info_num == 0:
            self.display_info = pygame.font.Font.render(font,self.deal_message,False,"#ffb0ce")
        if info_num == 1:
            self.display_info = pygame.font.Font.render(font,self.rating_message,False,"#ffb0ce")
        screen.blit(self.display_info,self.rect2)

def main_screen():
    global info_num, press_index, can_press, cooldown_timer
    screen.blit(background,(0,0))
    screen.blit(logo,(20,150))
    screen.blit(menu_button1,menu_button_rect)
    if menu_button_rect.collidepoint(mouse):
        screen.blit(menu_button2,menu_button_rect)
        if pressed[0] and cooldown_timer == 0:
            pygame.quit()
            exit()
    
    display_games = []
    
    for n in range(press_index,press_index + 10):
        display_games.append(game_info(games_json[n],n-press_index)) 


    for game in display_games:
        game.display(info_num)

    screen.blit(price_button1,price_button_rect)
    if price_button_rect.collidepoint(mouse):
        screen.blit(price_button2,price_button_rect)
        if pressed[0]:
            info_num = 0
    screen.blit(rating_button1,rating_button_rect)
    if rating_button_rect.collidepoint(mouse):
        screen.blit(rating_button2,rating_button_rect)
        if pressed[0]:
            info_num = 1
    if press_index > 0:
        screen.blit(left_button1,left_button_rect)
        if left_button_rect.collidepoint(mouse):
            screen.blit(left_button2,left_button_rect)
            if pressed[0] and can_press:
                can_press = False
                cooldown_timer = 1
                press_index -= 10

    if press_index < len(games_json)-10: 
        screen.blit(right_button1,right_button_rect)
        if right_button_rect.collidepoint(mouse):
            screen.blit(right_button2,right_button_rect)
            if pressed[0] and can_press:
                can_press = False
                cooldown_timer = 1
                press_index += 10

    screen.blit(discount_button1,discount_button_rect)
    if discount_button_rect.collidepoint(mouse):
        screen.blit(discount_button2,discount_button_rect)
        if pressed[0] and can_press:
            cooldown_timer = 1
            can_press = False
            state_stack.append(discount_screen)

can_access = False
redeemed = False
user = database.get_user()
discount_background = image_import.get_image("pictures for survivor game/backgrounds/menu backgrounds/discount code background.png",(1280,720))
denied_background = image_import.get_image("pictures for survivor game/backgrounds/menu backgrounds/denied background.png",(1280,720))
denied_message1 = "Choose an account to reedeem"
denied_message2 = "Complete level 12 to redeeem"
denied_message3 = "Already redeemed on this account"
if user != 'Select/create a user to play':
    levels = database.is_complete(user)
    if levels[12][0] == 1:
        if database.check_for_redeem(user) == 1:
            can_access = False
            reason = denied_message3
        else:
            can_access = True
    else:
        reason = denied_message2
else:
    can_access = False
    reason = denied_message1

generate_button1 = image_import.get_image("pictures for survivor game/buttons and icons/generate button 1.png",(440,150))
generate_button2 = image_import.get_image("pictures for survivor game/buttons and icons/generate button 2.png",(440,150))
generate_button_rect = generate_button1.get_rect(center = (640,370))
code = ""
logo2 = image_import.get_image("pictures for survivor game/Shop logo.png",(200,200))
back_button1 = image_import.get_image('pictures for survivor game/buttons and icons/back button 1.png',(80,80))
back_button2 = image_import.get_image('pictures for survivor game/buttons and icons/back button 2.png',(80,80))
back_button_rect = back_button1.get_rect(center = (80,80))

def discount_screen():
    global redeemed, code, cooldown_timer, can_press
    screen.blit(discount_background,(0,0))
    if can_access:
        screen.blit(generate_button1,generate_button_rect)
        if generate_button_rect.collidepoint(mouse):
            screen.blit(generate_button2,generate_button_rect)
            if pressed[0] and redeemed == False:
                code = pygame.font.Font.render(code_font,generate_code(),False,"Black")
                redeemed = True
                database.redeem_code(user)
        if redeemed:
            screen.blit(code,(330,500))
        
        screen.blit(logo2,(30,500))
        screen.blit(logo2,(1050,500)) 

    else:
        screen.blit(denied_background,(0,0))
        denied = pygame.font.Font.render(denied_font,reason,False,"White")
        denied_rect = denied.get_rect(center = (640,360))
        screen.blit(denied,denied_rect)

    screen.blit(back_button1,back_button_rect)
    if back_button_rect.collidepoint(mouse):
        screen.blit(back_button2,back_button_rect)
        if pressed[0] and can_press:
            can_press = False
            cooldown_timer = 1
            state_stack.pop()
        
def generate_code():
    character = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
    generated_code = ""
    for n in range(0,10):
        num = random.randint(0,len(character)-1)
        generated_code += character[num]
    
    return generated_code

state_stack = [main_screen]

while True:
    mouse = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    state_stack[len(state_stack)-1]()

    if cooldown_timer > 0:
        cooldown_timer += 1
        if cooldown_timer >= 50:
            cooldown_timer = 0
            can_press = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

    pygame.display.update()