import pygame, database, image_import, requests
pygame.init()

screen = pygame.display.set_mode((1280,720))
cooldown_timer = 0

font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",23)

headers = {"Accept": "application/json","Content-Type": "application/json"}
response = requests.request("GET","https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15",headers=headers)
games_json = response.json()

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
info_num = 0

class game_info:
    def __init__(self,info,index):
        self.index = index
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
    global info_num
    screen.blit(background,(0,0))
    screen.blit(logo,(20,150))
    screen.blit(menu_button1,menu_button_rect)
    if menu_button_rect.collidepoint(mouse):
        screen.blit(menu_button2,menu_button_rect)
        if pressed[0] and cooldown_timer == 0:
            pygame.quit()
            exit()
    
    display_games = []
    for n in range(0,10):
        display_games.append(game_info(games_json[n],n))

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



while True:
    mouse = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    main_screen()

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