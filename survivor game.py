from typing import Any
import pygame,math,random
import database

#initialising pygame
pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
screen_height = screen.get_height()
screen_width = screen.get_width()
print(screen_height,screen_width)
 
#general variable setup
general_font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",40)
level_font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",100)
global press_timer
press_timer = -1
kills = 0
currency = 0
game_timer = 0

#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #graphics
        self.right90 = [pygame.image.load("pictures for survivor game/dude graphics/dude stand 90.png").convert_alpha(),pygame.image.load("pictures for survivor game/dude graphics/dude run 1 90.png").convert_alpha(),pygame.image.load("pictures for survivor game/dude graphics/dude run 2 90.png").convert_alpha()]
        self.left90 = [pygame.transform.flip(self.right90[0],True,False),pygame.transform.flip(self.right90[1],True,False),pygame.transform.flip(self.right90[2],True,False)]
        self.right45 = [pygame.image.load("pictures for survivor game/dude graphics/dude stand 45.png").convert_alpha(),pygame.image.load("pictures for survivor game/dude graphics/dude run 1 45.png").convert_alpha(),pygame.image.load("pictures for survivor game/dude graphics/dude run 2 45.png").convert_alpha()]
        self.left45 = [pygame.transform.flip(self.right45[0],True,False),pygame.transform.flip(self.right45[1],True,False),pygame.transform.flip(self.right45[2],True,False)]
        self.right135 = [pygame.image.load("pictures for survivor game/dude graphics/dude stand 135.png").convert_alpha(),pygame.image.load("pictures for survivor game/dude graphics/dude run 1 135.png").convert_alpha(),pygame.image.load("pictures for survivor game/dude graphics/dude run 2 135.png").convert_alpha()]
        self.left135 = [pygame.transform.flip(self.right135[0],True,False),pygame.transform.flip(self.right135[1],True,False),pygame.transform.flip(self.right135[2],True,False)]
        self.right0 = [pygame.image.load("pictures for survivor game/dude graphics/dude stand 0.png").convert_alpha(),pygame.image.load("pictures for survivor game/dude graphics/dude run 1 0.png").convert_alpha(),pygame.image.load("pictures for survivor game/dude graphics/dude run 2 0.png").convert_alpha()]
        self.left0 = [pygame.transform.flip(self.right0[0],True,False),pygame.transform.flip(self.right0[1],True,False),pygame.transform.flip(self.right0[2],True,False)]
        self.right180 = [pygame.image.load("pictures for survivor game/dude graphics/dude stand 180.png").convert_alpha(),pygame.image.load("pictures for survivor game/dude graphics/dude run 1 180.png").convert_alpha(),pygame.image.load("pictures for survivor game/dude graphics/dude run 2 180.png").convert_alpha()]
        self.left180 = [pygame.transform.flip(self.right180[0],True,False),pygame.transform.flip(self.right180[1],True,False),pygame.transform.flip(self.right180[2],True,False)]
        self.stand = self.right90[0]
        self.image = self.right90[0]
        self.running_animation = [self.right90[1],self.right90[2]]
        self.image = pygame.transform.scale(self.image,(70,91))
        self.rect = self.image.get_rect(center = (screen_width/2,screen_height/2))
        self.rect = pygame.rect.Rect(self.rect.left+7,self.rect.top+7,56,77)
        self.heart_full = pygame.image.load("pictures for survivor game/heart red.png").convert_alpha()
        self.heart_empty = pygame.image.load("pictures for survivor game/heart black.png").convert_alpha()
        self.heart_full = pygame.transform.scale(self.heart_full,(80,80))
        self.heart_empty = pygame.transform.scale(self.heart_empty,(80,80))
        self.level_bar = pygame.image.load("pictures for survivor game/backgrounds/level up bar.png").convert_alpha()
        self.level_bar = pygame.transform.scale(self.level_bar,(screen_width,screen_height))
        self.level_bar_full = pygame.image.load("pictures for survivor game/backgrounds/level up bar full.png").convert_alpha()
        self.level_bar_full = pygame.transform.scale(self.level_bar_full,(653,13))
        self.ammo_icon = pygame.image.load("pictures for survivor game/buttons and icons/ammo icon.png").convert_alpha()
        self.ammo_icon = pygame.transform.scale(self.ammo_icon,(80,80))
        self.ammo_icon_rect = self.ammo_icon.get_rect(topleft = (100,screen_height - 80))
        self.ammo_num_rect = pygame.rect.Rect(self.ammo_icon_rect.left+8,self.ammo_icon_rect.top+12,60,60)
        self.reload1_icon = pygame.image.load("pictures for survivor game/buttons and icons/reload icon.png").convert_alpha()
        self.reload2_icon = pygame.transform.rotate(self.reload1_icon,180)
        self.reload1_icon = pygame.transform.scale(self.reload1_icon,(40,40))
        self.reload2_icon = pygame.transform.scale(self.reload2_icon,(40,40))
        self.reload_icons = [self.reload1_icon,self.reload2_icon]
        self.reload_icon_rect = self.reload1_icon.get_rect(centerx = self.ammo_icon_rect.centerx - 10,centery = self.ammo_icon_rect.centery)
        self.power_up_font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",30)
        self.nuke_icon = pygame.image.load("pictures for survivor game/buttons and icons/nuke icon.png").convert_alpha()
        self.nuke_icon = pygame.transform.scale(self.nuke_icon,(80,50))
        self.nuke_icon_rect = self.nuke_icon.get_rect(bottomright = (screen_width,screen_height))
        self.explosion1 = pygame.image.load("pictures for survivor game/explosion animation/explosion 1.png").convert_alpha()
        self.explosion2 = pygame.image.load("pictures for survivor game/explosion animation/explosion 2.png").convert_alpha()
        self.explosion3 = pygame.image.load("pictures for survivor game/explosion animation/explosion 3.png").convert_alpha()
        self.explosion4 = pygame.image.load("pictures for survivor game/explosion animation/explosion 4.png").convert_alpha()
        self.explosion_animation = [self.explosion1,self.explosion2,self.explosion3,self.explosion4,self.explosion3]
        for n in range(len(self.explosion_animation)):
            self.explosion_animation[n] = pygame.transform.scale(self.explosion_animation[n],(1000,1000))
        self.nuke_num = 0
        self.explosion_animation_index = -1
        #other attributes
        self.xp = 0
        self.level_up_num = 1
        self.playerlevel = 0
        self.bullet_cooldown = 30
        self.damage_timer = 10
        self.running_index = 0
        self.speed = 3
        self.cooldown_counter = 0
        self.health_num = 5
        self.max_health = 5
        self.invincible = False
        self.invincible_counter = 10
        self.can_shoot = False
        self.max_ammo = 5
        self.ammo = 5
        self.reload_timer = 100
        self.reload = 0
        self.reload_index = 0
        self.lazer_time = 10000
        self.weapon_damage = 1

    def power_ups(self):
        global press_timer
        self.explosion_rect = pygame.rect.Rect(self.rect.centerx - 400, self.rect.centery - 400,1000,1000)
        self.nuke_message = pygame.font.Font.render(self.power_up_font,f"{self.nuke_num}",False,"Green")
        if self.nuke_num > 0:
            screen.blit(self.nuke_icon,self.nuke_icon_rect)
            screen.blit(self.nuke_message,(self.nuke_icon_rect.x + 40,self.nuke_icon_rect.y + 7))
        if key[pygame.K_m] and self.nuke_num > 0 and press_timer == -1:
            self.explosion_animation_index = 0
            press_timer = 0
            self.nuke_num -= 1
        if self.explosion_animation_index >= 0:
            screen.blit(self.explosion_animation[int(self.explosion_animation_index)],self.explosion_rect)
            self.explosion_animation_index += 0.1
            if self.explosion_animation_index >= len(self.explosion_animation):
                self.explosion_animation_index = -1
        if press_timer >= 0:
            press_timer += 1
        if press_timer >= 20:
            press_timer = -1

    def reset(self):
        self.image = self.right90[0]
        self.image = pygame.transform.scale(self.image,(70,91))
        self.rect = self.image.get_rect(center = (screen_width/2,screen_height/2))
        self.health_num = self.max_health
        self.invincible = False
        self.can_shoot = False
        self.explosion_animation_index = -1
        self.ammo = 5
        self.xp = 0
        self.level_up_num = 1
        self.playerlevel = 0
            
    def movement(self):
        self.key = pygame.key.get_pressed()
        #Moves the character using WASD
        if self.key[pygame.K_d]:
            self.rect.x += self.speed
        if self.key[pygame.K_a]:
            self.rect.x -= self.speed
        if self.key[pygame.K_w]:
            self.rect.y -= self.speed
        if self.key[pygame.K_s]:
            self.rect.y += self.speed
        #Moves the enemies/collectables/background when character walks away
        if self.rect.centerx < 580:
            self.rect.centerx = 580
            level_background_rect.x += self.speed
            if self.rect.left > level_background_rect.left:
                for enemy in enemy_group:
                    enemy.rect.x += self.speed
                for collectable in collectables_group:
                    collectable.rect.x += self.speed
        if self.rect.centerx > screen_width - 580:
            self.rect.centerx = screen_width - 580
            level_background_rect.x -= self.speed
            if self.rect.right < level_background_rect.right:
                for enemy in enemy_group:
                    enemy.rect.x -= self.speed
                for collectable in collectables_group:
                    collectable.rect.x -= self.speed
        if self.rect.centery < 300:
            self.rect.centery = 300
            level_background_rect.y += self.speed
            if self.rect.top > level_background_rect.top:
                for enemy in enemy_group:
                    enemy.rect.y += self.speed
                for collectable in collectables_group:
                    collectable.rect.y += self.speed
        if self.rect.centery > screen_height - 300:
            self.rect.centery = screen_height - 300
            level_background_rect.y -= self.speed
            if self.rect.bottom < level_background_rect.bottom:
                for enemy in enemy_group:
                    enemy.rect.y -= self.speed
                for collectable in collectables_group:
                    collectable.rect.y -= self.speed
        #Moves background to appear infinite
        if level_background_rect.top > 0:
            level_background_rect.bottom = screen_height
        if level_background_rect.bottom < screen_height:
            level_background_rect.top = 0
        if level_background_rect.left > 0:
            level_background_rect.right = screen_width
        if level_background_rect.right < screen_width:
            level_background_rect.left = 0

    def aim(self):
        x_dist = mouse[0] - self.rect.centerx
        y_dist = -(mouse[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist,x_dist))
        if (self.angle >= 0 and self.angle <= 22.5) or (self.angle <= 0 and self.angle >= -22.5):
            self.stand = self.right90[0]
            self.running_animation = [self.right90[1],self.right90[2]]
        if self.angle > 22.5 and self.angle <= 57.5:
            self.stand = self.right45[0]
            self.running_animation = [self.right45[1],self.right45[2]]
        if self.angle < -22.5 and self.angle >= -57.5:
            self.stand = self.right135[0]
            self.running_animation = [self.right135[1],self.right135[2]]
        if (self.angle >= 157.5 and self.angle <= 180) or (self.angle <= -157.5 and self.angle >= -180):
            self.stand = self.left90[0]
            self.running_animation = [self.left90[1],self.left90[2]]
        if self.angle < 157.5 and self.angle >= 112.5:
            self.stand = self.left45[0]
            self.running_animation = [self.left45[1],self.left45[2]]
        if self.angle < -112.5 and self.angle >= -157.5:
            self.stand = self.left135[0]
            self.running_animation = [self.left135[1],self.left135[2]]
        if self.angle > 57.5 and self.angle <= 90:
            self.stand = self.right0[0]
            self.running_animation = [self.right0[1],self.right0[2]]
        if self.angle > 90 and self.angle <= 112.5:
            self.stand = self.left0[0]
            self.running_animation = [self.left0[1],self.left0[2]]
        if self.angle < -57.5 and self.angle >= -90:
            self.stand = self.right180[0]
            self.running_animation = [self.right180[1],self.right180[2]]
        if self.angle < -90 and self.angle >= -112.5:
            self.stand = self.left180[0]
            self.running_animation = [self.left180[1],self.left180[2]]
        if game_timer >= 0.5:
            self.can_shoot = True

    def animations(self):
        image = self.stand
        if self.key[pygame.K_d] or self.key[pygame.K_a] or self.key[pygame.K_w] or self.key[pygame.K_s]:
            image = self.running_animation[int(self.running_index)]
            self.running_index += 0.07
            if self.running_index >= len(self.running_animation):
                self.running_index = 0
        
        self.image = image
        self.image = pygame.transform.scale(self.image,(70,91))

    def cooldown(self):
        if self.cooldown_counter >= self.bullet_cooldown:
            self.cooldown_counter = 0
        if self.cooldown_counter > 0:
            self.cooldown_counter += 1  

    def create_bullet(self):
        global pressed
        self.cooldown()
        if self.cooldown_counter == 0 and self.can_shoot and self.ammo > 0:
            if (self.key[pygame.K_SPACE] or pressed[0]):
                bullets_group.add(Bullets(self.rect.x + 62,self.rect.centery,"Bullets",self.angle))
                self.ammo -=1
            self.cooldown_counter = 1
        if self.can_shoot  and self.lazer_time > 0:
            if self.key[pygame.K_n]:
                bullets_group.add(Bullets(self.rect.x + 62,self.rect.centery,"Lazer",self.angle))
                self.lazer_time -= 1
            
        screen.blit(self.ammo_icon,self.ammo_icon_rect)
        self.ammo_num = pygame.font.Font.render(general_font,f"{self.ammo}",False,"#765301")
        if self.ammo > 0:
            screen.blit(self.ammo_num,self.ammo_num_rect)
        else:
            self.reload += 1
            if self.reload > self.reload_timer:
                self.ammo = self.max_ammo
                self.reload = 0
            self.reload_index += 0.03
            if self.reload_index > 2:
                self.reload_index = 0
            screen.blit(self.reload_icons[int(self.reload_index)],self.reload_icon_rect)

    def health(self):
        general_font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",40)
        if pygame.sprite.spritecollide(self,enemy_group,False) and self.invincible == False:
            self.health_num -= enemy_list[enemy_type].damage
            self.invincible = True
        if self.health_num <= 0:
            state_stack.append(game_over_screen)
        if game_timer <= 0.1:
            self.health_num = self.max_health
        if self.invincible:
            self.invincible_counter -= 0.05
        if self.invincible_counter < 0 and self.invincible:
            self.invincible_counter = 10
            self.invincible = False
        if self.health_num >= 10:
            general_font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",20)
        self.health_message = pygame.font.Font.render(general_font,f"{self.health_num}",False,"#8B0000")
        screen.blit(self.heart_empty,(0,screen_height-80))
        screen.blit(self.heart_full,(0,screen_height - (80*(self.health_num/self.max_health))),(0,80 - (80*(self.health_num/self.max_health)),80,80*(self.health_num/self.max_health)))
        screen.blit(self.health_message,(28,screen_height-68))

    def collectables(self):
        global currency
        for collectable in collectables_group:
            if pygame.Rect.colliderect(self.rect,collectable.rect):
                if collectable.type == "Health":
                    if self.health_num < self.max_health:
                        self.health_num += 1
                if collectable.type == "Nuke":
                    self.nuke_num += 1
                if collectable.type == "Coin":
                    currency += 1
                if collectable.type == "Scrap":
                    self.xp += 1
                collectable.kill()

    def player_level(self):
        global press_timer , level_num, current_level, level_up_animation, game_screen
        level_font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",30)
        self.level_number = pygame.font.Font.render(level_font,f"{self.playerlevel}",True,"#027148")
        screen.blit(self.level_bar,(0,0))
        screen.blit(self.level_bar_full,(307,674),(0,0,653*(self.xp/self.level_up_num),13))
        screen.blit(self.level_number,(243,660))
        if self.xp >= self.level_up_num:
            self.xp = 0
            self.level_up_num *= 1.2
            self.playerlevel += 1
            level_up_animation = True
            pygame.image.save(screen,"Screen.png")
            state_stack.append(level_up_screen)
        if self.playerlevel == wave_num:
            press_timer = -1
            database.complete_level(current_level)
            state_stack.pop()
        
    def update(self):
        self.aim()
        self.player_level()
        self.movement()
        self.animations()
        self.create_bullet()
        self.collectables()
        self.health()
        self.power_ups()

player = Player()
player_group = pygame.sprite.GroupSingle()
player_group.add(Player())

#bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self,posx,posy,type,angle):
        super().__init__()
        self.image = pygame.surface.Surface((12,5),pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect(center = (posx,posy))
        self.speed = 30
        self.type = type
        self.dangle= angle
        self.rangle = math.radians(angle)

    def movement(self):
        self.dx = math.cos(self.rangle) * self.speed
        self.dy = -(math.sin(self.rangle)) * self.speed
        if self.type == "Bullets":
            self.image = pygame.image.load("pictures for survivor game/Bullet.png").convert_alpha()
            self.image = pygame.transform.rotate(self.image,self.dangle)
            self.rect.x += self.dx
            self.rect.y += self.dy
        if self.type == "Lazer":
            self.image = pygame.image.load("pictures for survivor game/Lazer bullet.png").convert_alpha()
            self.image = pygame.transform.rotate(self.image,self.dangle)
            self.rect.x += self.dx
            self.rect.y += self.dy

    def update(self):
        self.movement()
        if self.rect.x >= screen.get_width() + 50:
            self.kill()
        if self.rect.x <= -50:
            self.kill()
bullets_group = pygame.sprite.Group()

#enemies
class enemy_attributes():
    def __init__(self,health,speed,animation,animation_speed,size,damage,attack_frame):
        self.health = health
        self.speed = speed
        self.animation = animation
        self.animation_speed = animation_speed
        self.size = size
        self.damage = damage
        self.attack_frame = attack_frame

class Enemies(pygame.sprite.Sprite,enemy_attributes):
    def __init__(self,posx,posy):
        super().__init__()
        self.image = enemy_list[enemy_type].animation[0]
        self.image = pygame.transform.scale(self.image,enemy_list[enemy_type].size)
        self.rect = pygame.rect.Rect(posx + self.image.get_width()*0.1,posy + self.image.get_height()*0.05,self.image.get_width()*0.8,self.image.get_height() - self.image.get_height()*0.1)
        self.health = enemy_list[enemy_type].health
        self.max_health = enemy_list[enemy_type].health
        self.bar = pygame.surface.Surface(((self.health/5)*self.image.get_width(),10)).convert_alpha()
        self.bar.fill("Red")
        self.bar_rect = self.bar.get_rect(top = self.rect.bottom)
        self.speed = enemy_list[enemy_type].speed
        self.run_index = 0
        self.run = enemy_list[enemy_type].animation
        self.size = enemy_list[enemy_type].size

    def item_drop(self):
        global kills
        self.kill()
        kills += 1
        will_drop = random.randint(0,2)
        if will_drop <= 1:
            decider = random.randint(1,100)
            if decider >= 8 and decider <= 35:
                collectables_group.add(Collectables(self.rect.centerx,self.rect.centery,"Coin"))
            if decider == 1:
                collectables_group.add(Collectables(self.rect.centerx,self.rect.centery,"Nuke"))
            if decider > 1 and decider < 8:
                collectables_group.add(Collectables(self.rect.centerx,self.rect.centery,"Health"))
            if decider > 35:
                collectables_group.add(Collectables(self.rect.centerx,self.rect.centery,"Scrap"))

    def collide(self):
        if pygame.sprite.spritecollide(self,bullets_group,True):
            for player in player_group:
                self.health -= player.weapon_damage
                if self.health <= 0:
                    self.item_drop()
        for player in player_group:
            if self.rect.colliderect(player.explosion_rect) and player.explosion_animation_index >= 3:
                self.item_drop()

    def movement(self):
        for player in player_group:
            destination = player.rect
        if self.rect.x > destination.x:
            self.rect.x -= self.speed
        elif self.rect.x < destination.x:
            self.rect.x += self.speed
        if self.rect.y > destination.y:
            self.rect.y -= self.speed
        elif self.rect.y < destination.y:
            self.rect.y += self.speed

        if self.rect.centerx > screen_width * 2 or self.rect.centerx < (screen_width * 2) * -1:
            self.kill()
        if self.rect.centery > screen_height * 2 or self.rect.centery < (screen_height * 2) * -1:
            self.kill()
    
    def animation(self):
        self.run_index += enemy_list[enemy_type].animation_speed
        if self.run_index >= len(self.run):
            self.run_index = 0
        self.image = self.run[int(self.run_index)]
        self.image = pygame.transform.scale(self.image,self.size)

    def healthbar(self):
        self.bar = pygame.draw.rect(screen,"Red",(self.rect.left,self.rect.bottom,(self.health/self.max_health)*self.image.get_width(),10))
        pygame.draw

    def update(self):
        self.collide()
        self.movement()
        self.healthbar()
        self.animation()
enemy_index = -1
def spawn(frequency):
    global enemy_index, enemy_type
    if enemy_index >= -1:
        enemy_index += 1
    if enemy_index >= frequency:
        enemy_index = -1
    if enemy_index == 0:
        spawn_side = random.randint(0,3)    
        enemy_type = random.randint(0,len(enemy_list)-1)
        #Chooses which side of the screen the enemies spawn on
        if spawn_side == 0:
            enemy_group.add(Enemies(random.randint(-200,-100),random.randint(0,screen_height)))
        if spawn_side == 1:
            enemy_group.add(Enemies(random.randint(screen_width + 100,screen_width + 200),random.randint(0,screen_height)))
        if spawn_side == 2:
            enemy_group.add(Enemies(random.randint(0,screen_width),random.randint(-200,-100)))
        if spawn_side == 3:
            enemy_group.add(Enemies(random.randint(0,screen_width),random.randint(screen_height + 100,screen_height + 200)))
enemy_group = pygame.sprite.Group()

enemy_list = []

fly_enemy = enemy_attributes(2,
                             1,
                             [pygame.image.load("pictures for survivor game/enemy graphics/fly 1.png").convert_alpha(),pygame.image.load("pictures for survivor game/enemy graphics/fly 2.png").convert_alpha(),pygame.image.load("pictures for survivor game/enemy graphics/fly 3.png").convert_alpha(),pygame.image.load("pictures for survivor game/enemy graphics/fly 2.png").convert_alpha()],
                             0.1,
                             (50,35),
                             1,
                             False)
trash_enemy = enemy_attributes(5,
                               0.6,
                               [pygame.image.load("pictures for survivor game/enemy graphics/trash monster 1.png").convert_alpha(),pygame.image.load("pictures for survivor game/enemy graphics/trash monster 2.png").convert_alpha()],
                               0.01,
                               (100,100),
                               2,
                               False)
alien_enemy = enemy_attributes(10,
                               0.8,
                               [pygame.image.load("pictures for survivor game/enemy graphics/alien 1.png"),pygame.image.load("pictures for survivor game/enemy graphics/alien 2.png")],
                               0.06,
                               (65,120),
                               3,
                               False)

#collectables
class Collectables(pygame.sprite.Sprite):
    def __init__(self,posx,posy,type):
        super().__init__()
        self.x = posx
        self.y = posy
        self.heart_collectable = pygame.image.load("pictures for survivor game/collectables/heart collectable.png").convert_alpha()
        self.heart_collectable = pygame.transform.scale(self.heart_collectable,(30,30))
        self.nuke_collectable = pygame.image.load("pictures for survivor game/collectables/nuke collectable.png").convert_alpha()
        self.nuke_collectable = pygame.transform.scale(self.nuke_collectable,(40,16))
        self.coin_collectable = pygame.image.load("pictures for survivor game/collectables/coin collectable.png").convert_alpha()
        self.coin_collectable = pygame.transform.scale(self.coin_collectable,(20,20))
        self.scrap1 = pygame.image.load("pictures for survivor game/collectables/scrap 1.png").convert_alpha()
        self.scrap2 = pygame.image.load("pictures for survivor game/collectables/scrap 2.png").convert_alpha()
        self.scrap3 = pygame.image.load("pictures for survivor game/collectables/scrap 3.png").convert_alpha()
        self.scrap4 = pygame.image.load("pictures for survivor game/collectables/scrap 4.png").convert_alpha()
        self.type = type
        if type == "Health":
            self.image = self.heart_collectable
        if type == "Nuke":
            self.image = self.nuke_collectable
        if type == "Coin":
            self.image = self.coin_collectable
        if type == "Scrap":
            self.scrap_image = random.randint(0,3)
            if self.scrap_image == 0:
                self.image = self.scrap1
            if self.scrap_image == 1:
                self.image = self.scrap2
            if self.scrap_image == 2:
                self.image = self.scrap3
            if self.scrap_image == 3:
                self.image = self.scrap4

        self.rect = self.image.get_rect(center = (self.x,self.y))
collectables_group = pygame.sprite.Group()
        
#menu screen
player_menu_1 = pygame.image.load("pictures for survivor game/dude graphics/dude run 1 90.png").convert_alpha()
player_menu_2 = pygame.image.load("pictures for survivor game/dude graphics/dude run 2 90.png").convert_alpha()
player_menu_1 = pygame.transform.scale(player_menu_1,(500,650))
player_menu_2 = pygame.transform.scale(player_menu_2,(500,650))
player_menu = [player_menu_1,player_menu_2]
player_menu_index = 0
menu_cloud = pygame.image.load("pictures for survivor game/backgrounds/menu backgrounds/menu clouds.png").convert_alpha()
menu_cloud = pygame.transform.scale(menu_cloud,(7200,screen_height))
menu_cloud_rect = menu_cloud.get_rect(topleft = (0,0))
menu_ground = pygame.image.load("pictures for survivor game/backgrounds/menu backgrounds/menu ground.png").convert_alpha()
menu_ground = pygame.transform.scale(menu_ground,(7200,screen_height))
menu_ground_rect = menu_ground.get_rect(topleft = (0,0))
menu_sky = pygame.image.load("pictures for survivor game/backgrounds/menu backgrounds/menu sky.png").convert_alpha()
menu_sky = pygame.transform.scale(menu_sky,(7200,screen_height))
menu_sky_rect = menu_sky.get_rect(topleft = (0,0))
menu_rects = [menu_cloud_rect,menu_sky_rect,menu_ground_rect]
title = pygame.image.load("pictures for survivor game/gun dude title.png").convert_alpha()
title = pygame.transform.scale(title,(465,225))
start_button_1 = pygame.image.load("pictures for survivor game/buttons and icons/start button 1.png").convert_alpha()
start_button_2 = pygame.image.load("pictures for survivor game/buttons and icons/start button 2.png").convert_alpha()
start_button_1 = pygame.transform.scale(start_button_1,(620,200))
start_button_2 = pygame.transform.scale(start_button_2,(620,200))
start_button_rect1 = start_button_1.get_rect(topleft = (575,400))
start_button_rect2 = start_button_2.get_rect(topleft = (575,400))
exit_button_1 = pygame.image.load("pictures for survivor game/buttons and icons/exit button 1.png")
exit_button_1 = pygame.transform.scale(exit_button_1,(50,50))
exit_button_2 = pygame.image.load("pictures for survivor game/buttons and icons/exit button 2.png")
exit_button_2 = pygame.transform.scale(exit_button_2,(50,50))
exit_button_rect = exit_button_1.get_rect(topright = (screen_width,0))

def menu():
    global player_menu_index, press_timer, menu_rects, menu_cloud_rect, menu_ground_rect, menu_sky_rect
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    #menu background animations
    menu_cloud_rect.x -= 4
    menu_ground_rect.x -= 6
    menu_sky_rect.x -= 1
    screen.blit(menu_sky,menu_sky_rect)
    screen.blit(menu_cloud,menu_cloud_rect)
    screen.blit(menu_ground,menu_ground_rect)
    for n in menu_rects:
        if n.right <= screen_width:
            n.left = 0
    player_menu_index += 0.07
    if player_menu_index >= len(player_menu):
        player_menu_index = 0
    screen.blit(player_menu[int(player_menu_index)],(20,50))
    screen.blit(title,(650,50))
    screen.blit(start_button_1,start_button_rect1)
    #menu button collisions
    if start_button_rect1.collidepoint(mouse):
        screen.blit(start_button_2,start_button_rect2)
        if mouse_pressed[0] == True:
            state_stack.append(pre_game_screen)
            press_timer = 0
    screen.blit(exit_button_2,exit_button_rect)
    if exit_button_rect.collidepoint(mouse):
        screen.blit(exit_button_1,exit_button_rect)
        if mouse_pressed[0] == True:
            pygame.quit()
            exit()

#game over screen
def game_over_screen():
    global level_message
    player_dead = pygame.image.load("pictures for survivor game/dude graphics/dude death.png").convert_alpha()
    player_dead = pygame.transform.scale(player_dead,(518,238))
    player_dead_rect = player_dead.get_rect(centerx = screen_width/2,centery = 500)
    respawn_button1 = pygame.image.load("pictures for survivor game/buttons and icons/respawn button 1.png").convert_alpha()
    respawn_button1 = pygame.transform.scale(respawn_button1,(200,200))
    respawn_button2 = pygame.image.load("pictures for survivor game/buttons and icons/respawn button 2.png").convert_alpha()
    respawn_button2 = pygame.transform.scale(respawn_button2,(200,200))
    menu_button1 = pygame.image.load("pictures for survivor game/buttons and icons/menu button 1.png").convert_alpha()
    menu_button1 = pygame.transform.scale(menu_button1,(320,150))
    menu_button2 = pygame.image.load("pictures for survivor game/buttons and icons/menu button 2.png").convert_alpha()
    menu_button2 = pygame.transform.scale(menu_button2,(320,150))
    respawn_button_rect = respawn_button1.get_rect(centery = player_dead_rect.centery, centerx = 1100)
    menu_button_rect = menu_button1.get_rect(centery = player_dead_rect.centery,centerx = 190)
    screen.blit(level_background,level_background_rect)
    screen.blit(player_dead,player_dead_rect)
    death_message = pygame.font.Font.render(level_font,f"You died",False,"Red")
    screen.blit(death_message,(player_dead_rect.left - 10,50))
    screen.blit(level_message,(player_dead_rect.left + 30,200))
    screen.blit(respawn_button2,respawn_button_rect)
    #game over button collisions
    if respawn_button_rect.collidepoint(mouse):
        screen.blit(respawn_button1,respawn_button_rect)
        if pressed[0] == True:
            game_reset()
    screen.blit(menu_button2,menu_button_rect)
    if menu_button_rect.collidepoint(mouse):
        screen.blit(menu_button1,menu_button_rect)
        if pressed[0] == True:
            for n in range(0,2):
                state_stack.pop()
    enemy_group.empty()
    bullets_group.empty()
    collectables_group.empty()

#pause game
def pause_button(state):
    global pause_button_rect, press_timer
    pause_button1 = pygame.image.load("pictures for survivor game/buttons and icons/pause button 1.png").convert_alpha()
    pause_button2 = pygame.image.load("pictures for survivor game/buttons and icons/pause button 2.png").convert_alpha()
    pause_button1 = pygame.transform.scale(pause_button1,(100,100))
    pause_button2 = pygame.transform.scale(pause_button2,(100,100))
    pause_button_rect = pause_button1.get_rect(topright = (screen_width,0))
    screen.blit(pause_button1,pause_button_rect)
    if pause_button_rect.collidepoint(mouse):
        screen.blit(pause_button2,pause_button_rect)
        if pressed[0] == True:
            press_timer = 0
            if state == "Game": state_stack.pop()
            if state == "Pause": state_stack.append(pause_screen)

def pause_screen():
    global press_timer, kills
    menu_button1 = pygame.image.load("pictures for survivor game/buttons and icons/menu button 1.png").convert_alpha()
    menu_button1 = pygame.transform.scale(menu_button1,(320,150))
    menu_button2 = pygame.image.load("pictures for survivor game/buttons and icons/menu button 2.png").convert_alpha()
    menu_button2 = pygame.transform.scale(menu_button2,(320,150))
    menu_button_rect = menu_button1.get_rect(centerx = screen_width/2,centery = 300)
    screen.blit(pygame.font.Font.render(level_font,"Paused",False,level_colour),(445,60))
    screen.blit(menu_button2,menu_button_rect)
    if menu_button_rect.collidepoint(mouse):
        screen.blit(menu_button1,menu_button_rect)
        if pressed[0] == True:
            for n in range(0,3):
                state_stack.pop()
    play_button1 = pygame.image.load("pictures for survivor game/buttons and icons/respawn button 2.png").convert_alpha()
    play_button2 = pygame.image.load("pictures for survivor game/buttons and icons/respawn button 1.png").convert_alpha()
    play_button1 = pygame.transform.scale(play_button1,(300,300))
    play_button2 = pygame.transform.scale(play_button2,(300,300))
    play_button_rect = play_button1.get_rect(centerx = screen_width/2,centery = 550)
    screen.blit(play_button1,play_button_rect)
    if play_button_rect.collidepoint(mouse):
        screen.blit(play_button2,play_button_rect)
        if pressed[0] == True:
            game_reset()
    if press_timer >= 0:
        press_timer += 1
    if press_timer >= 20:
        press_timer = -1
    if press_timer == -1:
        pause_button("Game")

#level_up screen
level_up_background = pygame.image.load("pictures for survivor game/backgrounds/level up background.png").convert_alpha()
level_up_background = pygame.transform.scale(level_up_background,(screen_width,813))
level_up_background_rect = level_up_background.get_rect(topleft = (0,627))
level_up_animation = False
level_up_exit = False
upgrade_template = pygame.image.load("pictures for survivor game/buttons and icons/Power ups/Template.png")
upgrade_template = pygame.transform.scale(upgrade_template,(280,560))
fire_rate_upgrade = pygame.image.load("pictures for survivor game/buttons and icons/Power ups/Fire rate upgrade.png")
fire_rate_upgrade = pygame.transform.scale(fire_rate_upgrade,(280,560))
speed_upgrade = pygame.image.load("pictures for survivor game/buttons and icons/Power ups/Speed upgrade.png")
speed_upgrade = pygame.transform.scale(speed_upgrade,(280,560))
damage_upgrade = pygame.image.load("pictures for survivor game/buttons and icons/Power ups/Damage upgrade.png")
damage_upgrade = pygame.transform.scale(damage_upgrade,(280,560))
upgrade_rect1 = fire_rate_upgrade.get_rect(topleft = (152,110))
upgrade_rect2 = fire_rate_upgrade.get_rect(topleft = (500,110))
upgrade_rect3 = fire_rate_upgrade.get_rect(topleft = (846,110))
class level_ups(pygame.sprite.Sprite):
    def __init__(self,rect):
        super().__init__()
        image = random.randint(0,len(power_up_list)-1)
        self.image = power_up_list[image]
        if rect == 0:
            self.rect = upgrade_rect1
        if rect == 1:
            self.rect = upgrade_rect2
        if rect == 2:
            self.rect = upgrade_rect3
        self.selected = False
    def powerup_choice(self):
        global pressed
        for player in player_group:
            if self.rect.collidepoint(mouse) and pressed[0] and self.selected == False:
                self.selected = True
                if self.image == fire_rate_upgrade:
                    player.bullet_cooldown *= 0.85
                if self.image == damage_upgrade:
                    player.weapon_damage += 0.5
                if self.image == speed_upgrade:
                    player.speed += 0.2

    def update(self):
        self.powerup_choice()

level_up_group = pygame.sprite.Group()
def level_up_screen():
    global  level_up_animation, level_up_exit, game_screen
    game_screen = pygame.image.load("Screen.png").convert_alpha()
    screen.blit(game_screen,(0,0))
    screen.blit(level_up_background,level_up_background_rect)
    if level_up_background_rect.top > -93 and level_up_animation:
        level_up_background_rect.top -= 40
        if level_up_background_rect.top <= -93:
            level_up_background_rect.top = -93
            level_up_animation = False
            level_up_exit = False
            for n in range(0,3):
                level_up_group.add(level_ups(n))
    if level_up_animation == False and level_up_exit == False:
        level_up_group.draw(screen)
        level_up_group.update()
    if upgrade_rect1.collidepoint(mouse) or upgrade_rect2.collidepoint(mouse) or upgrade_rect3.collidepoint(mouse):
        if pressed[0]:
            level_up_exit = True

    if level_up_animation == False and level_up_exit:
        if level_up_background_rect.top < 627:
            level_up_background_rect.top += 40
        else:
            state_stack.pop()

#game reset
def game_reset():
    global kills, game_timer, power_up_list
    state_stack.append(main_game)
    for player in player_group:
        player.reset()
    bullets_group.empty()
    enemy_group.empty()
    collectables_group.empty()
    kills = 0
    game_timer = 0
    power_up_list = [fire_rate_upgrade,speed_upgrade,damage_upgrade]

#pre game screen
def pre_game_screen():
    global current_level, level_message, press_timer, kills
    level_setup()
    screen.blit(level_background,(0,0))
    arrow_button1 = pygame.image.load("pictures for survivor game/buttons and icons/arrow button 1.png").convert_alpha()
    arrow_button1 = pygame.transform.scale(arrow_button1,(80,80))
    arrow_button2 = pygame.image.load("pictures for survivor game/buttons and icons/arrow button 2.png").convert_alpha()    
    arrow_button2 = pygame.transform.scale(arrow_button2,(80,80))  
    arrow_button_rect = arrow_button1.get_rect(bottomright = (screen_width,screen_height)) 
    left_arrow_button1 = pygame.transform.flip(arrow_button1,True,False)
    left_arrow_button2 = pygame.transform.flip(arrow_button2,True,False)
    left_arrow_button_rect = left_arrow_button1.get_rect(bottomleft = (0,screen_height))
    level_message = pygame.font.Font.render(level_font,f"Level {current_level}",False,level_colour)
    level_message_rect = pygame.rect.Rect(420,80,480,100)
    play_button1 = pygame.image.load("pictures for survivor game/buttons and icons/Play button 1.png").convert_alpha()
    play_button2 = pygame.image.load("pictures for survivor game/buttons and icons/Play button 2.png").convert_alpha()
    play_button1 = pygame.transform.scale(play_button1,(400,400))
    play_button2 = pygame.transform.scale(play_button2,(400,400))
    play_button_rect = pygame.rect.Rect(440,250,400,400)
    locked_icon = pygame.image.load("pictures for survivor game/buttons and icons/locked icon.png").convert_alpha()
    locked_icon = pygame.transform.scale(locked_icon,(400,400))
    menu_button_1 = pygame.image.load("pictures for survivor game/buttons and icons/menu button 2.png").convert_alpha()
    menu_button_2 = pygame.image.load("pictures for survivor game/buttons and icons/menu button 1.png").convert_alpha()
    menu_button_1 = pygame.transform.scale(menu_button_1,(220,100))
    menu_button_2 = pygame.transform.scale(menu_button_2,(220,100))
    menu_button_rect = menu_button_1.get_rect(topleft = (0,0))
    screen.blit(level_message,level_message_rect)
    screen.blit(menu_button_1,menu_button_rect)
    if menu_button_rect.collidepoint(mouse):
        screen.blit(menu_button_2,menu_button_rect)
        if pressed[0] == True and press_timer == -1:
            press_timer = 0
            state_stack.pop()
    if current_level < 10:
        screen.blit(arrow_button1,arrow_button_rect)
        if arrow_button_rect.collidepoint(mouse):
            screen.blit(arrow_button2,arrow_button_rect)
            if pressed[0] == True and press_timer == -1:
                press_timer = 0
                current_level += 1
    if current_level > 1:
        screen.blit(left_arrow_button1,left_arrow_button_rect)
        if left_arrow_button_rect.collidepoint(mouse):
            screen.blit(left_arrow_button2,left_arrow_button_rect)
            if pressed[0] == True and press_timer == -1:
                press_timer = 0
                current_level -= 1
    if press_timer >= 0:
        press_timer += 1
    if press_timer >= 10:
        press_timer = -1
    level_list = database.is_complete()
    if level_list[current_level-1][0] == 1:
        screen.blit(play_button1,play_button_rect)
        if play_button_rect.collidepoint(mouse) and press_timer == -1:
            screen.blit(play_button2,play_button_rect)
            if pressed[0] == True:
                game_reset()
    else:
        screen.blit(locked_icon,play_button_rect)

#levels
current_level = 1
def level_setup():
    global level_background, enemy_health, enemy_speed, enemy_animation, enemy_size, enemy_frequency, level_colour, wave_num, enemy_damage, level_background_rect, enemy_animation_speed, enemy_list
    #level 1
    if current_level == 1:
        enemy_list = [fly_enemy,trash_enemy]
        enemy_frequency = random.randint(25,200)
        level_background = pygame.image.load("pictures for survivor game/backgrounds/level 1 background.png").convert_alpha()
        level_colour = "Brown"
        wave_num = 1
    #level 2
    if current_level == 2:
        level_background = pygame.image.load("pictures for survivor game/backgrounds/level 1 background.png").convert_alpha()
        level_colour = "#44230D"
        wave_num = 10
        enemy_health = 2
        enemy_speed = 1
        enemy_animation = [pygame.image.load("pictures for survivor game/enemy graphics/fly 1.png").convert_alpha(),pygame.image.load("pictures for survivor game/enemy graphics/fly 2.png").convert_alpha(),pygame.image.load("pictures for survivor game/enemy graphics/fly 3.png").convert_alpha(),pygame.image.load("pictures for survivor game/enemy graphics/fly 2.png").convert_alpha()]
        enemy_animation_speed = 0.2
        enemy_size = (50,35)
        enemy_frequency = random.randint(1,100)
        enemy_damage = 1
    #level 3
    if current_level == 3:
        level_background = pygame.surface.Surface((1280,720))
        level_background.fill("Blue")
        level_colour = "Pink"
        wave_num = 30
        enemy_list = [alien_enemy]
        enemy_frequency = 100
    
    level_background = pygame.transform.scale(level_background,(screen_width*3,screen_height*3))
    level_background_rect = level_background.get_rect(center = (screen_width/2,screen_height/2))

#main game
def main_game():
    global level_num, current_level, press_timer, game_timer, kills
    crosshair = pygame.image.load("pictures for survivor game/Crosshair.png").convert_alpha()
    crosshair = pygame.transform.scale(crosshair,(30,30))
    screen.blit(level_background,level_background_rect)
    bullets_group.draw(screen)
    bullets_group.update()
    collectables_group.draw(screen)
    collectables_group.update()
    enemy_group.draw(screen)
    enemy_group.update()
    for player in player_group:
        if player.invincible:
            if (player.invincible_counter >= 2 and player.invincible_counter <= 5) or (player.invincible_counter >= 6 and player.invincible_counter <= 9):
                player_group.draw(screen)
        if player.invincible == False:
            player_group.draw(screen)
    player_group.update()
    spawn(enemy_frequency)
    screen.blit(crosshair,(mouse[0]-15,mouse[1]-15))
           
    if press_timer >= 0:
        press_timer += 1
    if press_timer >= 20:
        press_timer = -1
    if press_timer == -1:
        pause_button("Pause")
    game_timer += 0.016

state_stack = [menu]

#game loop
while True:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
    current_state = len(state_stack) - 1
    state_stack[current_state]()
    key = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
    pygame.display.update()
    clock.tick(60)