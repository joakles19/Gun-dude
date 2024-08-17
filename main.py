#Main file to be executed

#Hash table in Hash_table.py
#Database and SQL functions in database.py
#Binary tree and tree traversal in skill_tree.py

import pygame,math,random,subprocess,numpy as np #importing python libraries
import database,data_structures,image_import,analytics_maker #importing my own modules

#initialising pygame
pygame.init()
screen = pygame.display.set_mode((1280,720)) #Screen surface
clock = pygame.time.Clock() #Clock object
screen_height = screen.get_height()
screen_width = screen.get_width()

#general variable setup
general_font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",40)
level_font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",100)
global press_timer
press_timer = -1 #Press timer used for interface buttons
game_timer = 0 #Define the game timer
player_skin = '' #Sets skin to default

#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #load graphics
        #graphic for each angle the player aims
        right90 = [pygame.image.load(f"pictures for survivor game/dude graphics/dude stand 90{player_skin}.png").convert_alpha(),pygame.image.load(f"pictures for survivor game/dude graphics/dude run 1 90{player_skin}.png").convert_alpha(),pygame.image.load(f"pictures for survivor game/dude graphics/dude run 2 90{player_skin}.png").convert_alpha()]
        left90 = [pygame.transform.flip(right90[0],True,False),pygame.transform.flip(right90[1],True,False),pygame.transform.flip(right90[2],True,False)]
        right45 = [pygame.image.load(f"pictures for survivor game/dude graphics/dude stand 45{player_skin}.png").convert_alpha(),pygame.image.load(f"pictures for survivor game/dude graphics/dude run 1 45{player_skin}.png").convert_alpha(),pygame.image.load(f"pictures for survivor game/dude graphics/dude run 2 45{player_skin}.png").convert_alpha()]
        left45 = [pygame.transform.flip(right45[0],True,False),pygame.transform.flip(right45[1],True,False),pygame.transform.flip(right45[2],True,False)]
        right135 = [pygame.image.load(f"pictures for survivor game/dude graphics/dude stand 135{player_skin}.png").convert_alpha(),pygame.image.load(f"pictures for survivor game/dude graphics/dude run 1 135{player_skin}.png").convert_alpha(),pygame.image.load(f"pictures for survivor game/dude graphics/dude run 2 135{player_skin}.png").convert_alpha()]
        left135 = [pygame.transform.flip(right135[0],True,False),pygame.transform.flip(right135[1],True,False),pygame.transform.flip(right135[2],True,False)]
        right0 = [pygame.image.load(f"pictures for survivor game/dude graphics/dude stand 0{player_skin}.png").convert_alpha(),pygame.image.load(f"pictures for survivor game/dude graphics/dude run 1 0{player_skin}.png").convert_alpha(),pygame.image.load(f"pictures for survivor game/dude graphics/dude run 2 0{player_skin}.png").convert_alpha()]
        left0 = [pygame.transform.flip(right0[0],True,False),pygame.transform.flip(right0[1],True,False),pygame.transform.flip(right0[2],True,False)]
        right180 = [pygame.image.load(f"pictures for survivor game/dude graphics/dude stand 180{player_skin}.png").convert_alpha(),pygame.image.load(f"pictures for survivor game/dude graphics/dude run 1 180{player_skin}.png").convert_alpha(),pygame.image.load(f"pictures for survivor game/dude graphics/dude run 2 180{player_skin}.png").convert_alpha()]
        left180 = [pygame.transform.flip(right180[0],True,False),pygame.transform.flip(right180[1],True,False),pygame.transform.flip(right180[2],True,False)]
        self.right = [right0,right45,right90,right135,right180]
        self.left = [left0,left45,left90,left135,left180]
        self.stand = right90[0]
        self.image = self.stand
        self.rect = self.image.get_rect(center = (screen_width/2,screen_height/2))
        self.running_index = 0
        #health graphics
        self.heart_full = image_import.get_image("pictures for survivor game/heart red.png",(80,80))
        self.heart_empty = image_import.get_image("pictures for survivor game/heart black.png",(80,80))
        #level bar graphics
        self.level_bar = image_import.get_image("pictures for survivor game/backgrounds/level up bar.png",(screen_width,screen_height))
        self.level_bar_full = image_import.get_image("pictures for survivor game/backgrounds/level up bar full.png",(653,13))
        #ammo icon graphics
        self.ammo_icon = image_import.get_image("pictures for survivor game/buttons and icons/ammo icon.png",(80,80))
        self.ammo_icon_rect = self.ammo_icon.get_rect(topleft = (100,screen_height - 80))
        self.ammo_num_rect = pygame.rect.Rect(self.ammo_icon_rect.left+8,self.ammo_icon_rect.top+12,60,60)
        self.reload1_icon = image_import.get_image("pictures for survivor game/buttons and icons/reload icon.png",(40,40))
        self.reload2_icon = pygame.transform.rotate(self.reload1_icon,180)
        self.reload_icons = [self.reload1_icon,self.reload2_icon]
        self.reload_icon_rect = self.reload1_icon.get_rect(centerx = self.ammo_icon_rect.centerx - 10,centery = self.ammo_icon_rect.centery)
        self.reload_index = 0 
        #nuke icon graphics
        self.power_up_font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",30)
        self.nuke_icon = image_import.get_image("pictures for survivor game/buttons and icons/nuke icon.png",(100,70))
        self.nuke_icon_rect = self.nuke_icon.get_rect(bottomright = (screen_width,screen_height))
        #lazer icon graphics
        self.lazer_ammo_icon = image_import.get_image("pictures for survivor game/buttons and icons/lazer ammo icon.png",(80,50))
        self.lazer_ammo_icon_rect = self.lazer_ammo_icon.get_rect(right = self.nuke_icon_rect.left - 10,centery = self.nuke_icon_rect.centery - 10)
        #invcincibility icon graphics
        self.invincibility_icon = image_import.get_image("pictures for survivor game/buttons and icons/invincibilty icon.png",(80,80))
        self.invincibility_icon_rect = self.invincibility_icon.get_rect(right = self.lazer_ammo_icon_rect.left -10, centery = self.lazer_ammo_icon_rect.centery)
        #explosion animation graphics
        self.explosion1 = image_import.get_image("pictures for survivor game/explosion animation/explosion 1.png",(1000,1000))
        self.explosion2 = image_import.get_image("pictures for survivor game/explosion animation/explosion 2.png",(1000,1000))
        self.explosion3 = image_import.get_image("pictures for survivor game/explosion animation/explosion 3.png",(1000,1000))
        self.explosion4 = image_import.get_image("pictures for survivor game/explosion animation/explosion 4.png",(1000,1000))
        self.explosion_animation = [self.explosion1,self.explosion2,self.explosion3,self.explosion4,self.explosion3]
        self.explosion_animation_index = -1
        #player position
        self.x = self.rect.centerx
        self.y = self.rect.centery
        #other attributes
        self.bullet_cooldown = 30 #Time between when bullets can be fired
        self.cooldown_counter = 0 #Variable which tracks the bullet cooldown
        self.max_health = 5 #Players starting max health
        self.invincible_counter = 6 #How long player is invincible for
        self.max_ammo = 5 #Starting max ammo
        self.reload_timer = 100 #Starting time for reloading
        self.reload = 0 #Variable which tracks how long reloading takes
        self.weapon_damage = 1 #Starting damage of players gun
        self.coin_multiplier = 1 #Starting coin multiplier

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

    def reset(self):
        #Set up skills from skill tree
        if skill_purchased[3]:#Damage up 1
            self.weapon_damage = 3
            if skill_purchased[1]:#Damage up 2
                self.weapon_damage = 5
                if skill_purchased[0]:#Damage up 3
                    self.weapon_damage = 7
        
        if skill_purchased[2]:#Lazer
            self.can_lazer = True
            self.lazer_time = 10
        else:
            self.can_lazer = False
            self.lazer_time = 0

        if skill_purchased[5]:#Fire rate up 1
            self.bullet_cooldown = 20
            if skill_purchased[4]:#Fire rate upgrade 2
                self.bullet_cooldown = 10

        if skill_purchased[9]:#Coin multiplier 1
            self.coin_multiplier = 2
            if skill_purchased[8]:#Coin multiplier 2
                self.coin_multiplier = 3

        if skill_purchased[11]:#Health up 1
            self.max_health = 8
            if skill_purchased[13]:#Health up 2
                self.max_health = 12
                if skill_purchased[14]:#Health up 3
                    self.max_health = 15

        if skill_purchased[12]:#Passive heal
            self.passive_heal = True
            self.passive_heal_timer = 0
        else:
            self.passive_heal = False

        if skill_purchased[10]:
            self.invincible_skill = True
        else:
            self.invincible_skill = False
        self.invincible_skill_cooldown = 0

        #Reset player attributes
        self.rect = self.image.get_rect(center = (screen_width/2,screen_height/2))
        self.health_num = self.max_health
        self.invincible = False
        self.can_shoot = False
        self.explosion_animation_index = -1
        self.ammo = 5
        self.xp = 0
        self.level_up_num = 2
        self.playerlevel = 0
        self.speed = 3
        self.coins = 0
        self.nuke_num = 0

        #Game analytics
        self.health_track = []
        self.enemy_kills = []
        self.collectable_pickups = [0,0,0,0]
        for enemy in enemies:
            self.enemy_kills.append(0)
        self.hits_track = 0
        self.kills_track = 0
        self.track_timer = 0
        self.shots_fired = 0
        self.collectables_picked = 0

    def movement(self):
        global level_backgroundy,level_backgroundx
        self.key = pygame.key.get_pressed()
        #Moves the character using WASD
        if self.key[pygame.K_d]:
            self.x += self.speed
        if self.key[pygame.K_a]:
            self.x -= self.speed
        if self.key[pygame.K_w]:
            self.y -= self.speed
        if self.key[pygame.K_s]:
            self.y += self.speed
        #Moves the enemies/collectables/background when character walks away
        if self.x < 500:
            self.x = 500
            level_backgroundx += self.speed
            if self.rect.left > level_background_rect.left:
                for enemy in enemy_group:
                    enemy.x += 3
                for collectable in collectables_group:
                    collectable.x += 3
        if self.x > screen_width - 580:
            self.x = screen_width - 580
            level_backgroundx -= self.speed
            if self.rect.right < level_background_rect.right:
                for enemy in enemy_group:
                    enemy.x -= 3
                for collectable in collectables_group:
                    collectable.x -= 3
        if self.y < 200:
            self.y = 200
            level_backgroundy += self.speed
            if self.rect.top > level_background_rect.top:
                for enemy in enemy_group:
                    enemy.y += 3
                for collectable in collectables_group:
                    collectable.y += 3
        if self.y > screen_height - 300:
            self.y = screen_height - 300
            level_backgroundy -= self.speed
            if self.rect.bottom < level_background_rect.bottom:
                for enemy in enemy_group:
                    enemy.y -= 3
                for collectable in collectables_group:
                    collectable.y -= 3
        #Moves background to appear infinite
        if level_background_rect.top > 0:
            level_backgroundy = -screen_height
        if level_background_rect.bottom < screen_height:
            level_backgroundy = 0
        if level_background_rect.left > 0:
            level_backgroundx = -screen_width
        if level_background_rect.right < screen_width:
            level_backgroundx = 0

        self.rect.x = math.floor(self.x)
        self.rect.y = math.floor(self.y)

    def aim_graphics(self):
        self.x_dist = mouse[0] - self.rect.centerx
        self.y_dist = -(mouse[1] - self.rect.centery)
        self.image_angle = math.degrees(math.atan2(self.x_dist,self.y_dist))
        image_index = abs(math.ceil(self.image_angle/36))
        if self.image_angle > 0:
            self.running_animation = [self.right[image_index-1][1],self.right[image_index-1][2]]
            self.stand = self.right[image_index-1][0]
        else:
            self.running_animation = [self.left[image_index][1],self.left[image_index][2]]
            self.stand = self.left[image_index][0]

    def hitbox(self):
        if self.image_angle > 0:
            self.hitbox_rect = pygame.Rect(self.rect.x,self.rect.y,self.image.get_width()/2,self.image.get_height())
        else:
            self.hitbox_rect = pygame.Rect(self.rect.x+self.image.get_width()/2,self.rect.y,self.image.get_width()/2,self.image.get_height())

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
        if game_timer >= 0.5:
            self.can_shoot = True
        self.cooldown()
        bullet_angle = math.degrees(math.atan2(self.y_dist,self.x_dist))
        if self.cooldown_counter == 0 and self.can_shoot and self.ammo > 0:
            if (self.key[pygame.K_SPACE] or pressed[0]):
                bullets_group.add(Bullets(self.rect.centerx,self.rect.centery,"Bullets",bullet_angle))
                self.shots_fired += 1
                self.ammo -=1
            self.cooldown_counter = 1
        if self.can_shoot  and self.lazer_time > 1 and self.can_lazer:
            if self.key[pygame.K_n]:
                bullets_group.add(Bullets(self.rect.centerx,self.rect.centery,"Lazer",bullet_angle))
                self.lazer_time -= 1

        if self.lazer_time > 0 and self.lazer_time < 10 and self.can_lazer:
            self.lazer_time += 0.02
        lazer_num = pygame.font.Font.render(general_font,f"{int(self.lazer_time)}",False,"#000045")
        lazer_num_rect = lazer_num.get_rect(center = self.lazer_ammo_icon_rect.center)
        if self.can_lazer:
            screen.blit(self.lazer_ammo_icon,(self.lazer_ammo_icon_rect))
            screen.blit(lazer_num,lazer_num_rect)

        screen.blit(self.ammo_icon,self.ammo_icon_rect)
        ammo_num = pygame.font.Font.render(general_font,f"{self.ammo}",False,"#765301")
        if self.ammo > 0:
            screen.blit(ammo_num,self.ammo_num_rect)
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
        for enemy in enemy_group:    
            if pygame.Rect.colliderect(self.hitbox_rect,enemy.rect) and self.invincible == False:
                self.health_num -= enemy.damage
                self.invincible = True
                self.hits_track += 1
        if self.health_num <= 0:
            state_stack.append(game_over_screen)
            self.create_analytics()
        if game_timer <= 0.1:
            self.health_num = self.max_health
        if self.invincible:
            self.invincible_counter -= 0.05
        if self.invincible_counter < 0 and self.invincible:
            self.invincible_counter = 6
            self.invincible = False

        if self.invincible_skill and self.invincible_skill_cooldown < 1:
            screen.blit(self.invincibility_icon,self.invincibility_icon_rect)
            if key[pygame.K_b]:
                self.invincible = True
                self.invincible_skill_cooldown = 800
            
        if self.invincible_skill_cooldown >= 1:
            self.invincible_skill_cooldown -= 1

        if self.passive_heal:
            self.passive_heal_timer += 1
            if self.passive_heal_timer > 1000:
                if self.health_num < self.max_health:
                    self.health_num += 1
                self.passive_heal_timer = 0

        if self.health_num >= 10:
            general_font = pygame.font.Font("pictures for survivor game/PixeloidMono-d94EV.ttf",20)
        self.health_message = pygame.font.Font.render(general_font,f"{self.health_num}",False,"#8B0000")
        screen.blit(self.heart_empty,(0,screen_height-80))
        screen.blit(self.heart_full,(0,screen_height - (80*(self.health_num/self.max_health))),(0,80 - (80*(self.health_num/self.max_health)),80,80*(self.health_num/self.max_health)))
        screen.blit(self.health_message,(28,screen_height-68))

    def collectables(self):
        for collectable in collectables_group:
            if pygame.Rect.colliderect(self.hitbox_rect,collectable.rect):
                self.collectables_picked += 1
                if collectable.type == "Health":
                    if self.health_num < self.max_health:
                        self.health_num += 1
                    self.collectable_pickups[0] += 1
                if collectable.type == "Nuke":
                    self.nuke_num += 1
                    self.collectable_pickups[1] += 1
                if collectable.type == "Coin":
                    self.coins += 1 * self.coin_multiplier
                    self.collectable_pickups[2] += 1
                if collectable.type == "Scrap":
                    self.xp += 1
                    self.collectable_pickups[3] += 1
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
            database.complete_level(current_level,current_user)
            database.add_currency(self.coins)
            self.create_analytics()
            state_stack.append(level_completion_screen)

    def track_health(self):
        self.track_timer += 0.05
        if self.track_timer >= 1:
            self.health_track.append(self.health_num)
            self.track_timer = 0

    def create_analytics(self):
        analytics_maker.create_plot(np.linspace(0,game_timer,len(self.health_track)),self.health_track,'Player health','Duration/s','Health','Healthgraph.png')
        analytics_maker.bar_chart(['Hits taken','Kills','Shots fired','Things collected'],[self.hits_track,self.kills_track,self.shots_fired,self.collectables_picked],'General stats','','','General stats.png')
        enemy_types = []
        for enemy in enemies:
            enemy_types.append(enemy[0])
        analytics_maker.bar_chart(enemy_types,self.enemy_kills,'Enemy kills','','Kills','Enemy kills.png')
        analytics_maker.bar_chart(['Health','Nuke','Coin','Scrap'],self.collectable_pickups,'Collectables picked up','','','Collectable graphs.png')

    def update(self):
        self.aim_graphics()
        self.player_level()
        self.movement()
        self.animations()
        self.create_bullet()
        self.collectables()
        self.health()
        self.power_ups()
        self.hitbox()
        self.track_health()

player = Player()

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
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def movement(self):
        self.dx = math.cos(self.rangle) * self.speed
        self.dy = -(math.sin(self.rangle)) * self.speed
        if self.type == "Bullets":
            self.image = pygame.image.load("pictures for survivor game/Bullet.png").convert_alpha()
        if self.type == "Lazer":
            self.image = pygame.image.load("pictures for survivor game/Lazer bullet.png").convert_alpha()
        if self.type == "Fireball":
            self.image = pygame.image.load("pictures for survivor game/Fireball.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image,self.dangle)
        self.x += self.dx
        self.y += self.dy
        self.rect.centerx = math.floor(self.x)
        self.rect.centery = math.floor(self.y)

    def update(self):
        self.movement()
        if self.rect.x >= screen.get_width() + 50:
            self.kill()
        if self.rect.x <= -50:
            self.kill()

class Enemy_bullets(Bullets):
    def __init__(self, posx, posy, type, angle,damage,speed):
        super().__init__(posx, posy, type, angle)
        self.damage = damage
        self.speed = speed

bullets_group = pygame.sprite.Group()

#enemies
class Enemies(pygame.sprite.Sprite):
    def __init__(self,posx,posy,info):
        super().__init__()
        self.enemy_info = info
        self.animation = graphics_dict.get(f"{info[0]}")
        self.image = self.animation[0]
        self.rect = self.image.get_rect(center = (posx,posy))
        self.max_health = info[1]
        self.health = self.max_health
        self.bar = pygame.surface.Surface(((self.health/5)*self.image.get_width(),10)).convert_alpha()
        self.bar_rect = self.bar.get_rect(top = self.rect.bottom)
        self.speed = info[3]
        self.run_index = 0
        self.damage = info[2]
        self.x = posx
        self.y = posy

    def item_drop(self):
        self.kill()
        for player in player_group:
            player.kills_track += 1
            player.enemy_kills[enemies.index(self.enemy_info)] += 1

        if skill_purchased[6]:
            more_nukes = True
        else:
            more_nukes = False

        will_drop = random.randint(0,3)
        if will_drop <= 2:
            if more_nukes:
                decider = random.randint(1,105)
            else:
                decider = random.randint(1,100)
            if decider >= 8 and decider <= 40:
                collectables_group.add(Collectables(self.rect.centerx,self.rect.centery,"Coin"))
            if decider > 0 and decider < 8:
                collectables_group.add(Collectables(self.rect.centerx,self.rect.centery,"Health"))
            if decider > 40 and decider < 100:
                collectables_group.add(Collectables(self.rect.centerx,self.rect.centery,"Scrap"))
            if decider >= 100:
                collectables_group.add(Collectables(self.rect.centerx,self.rect.centery,"Nuke"))

    def collide(self):
        if pygame.sprite.spritecollide(self,bullets_group,True):
            for player in player_group:
                self.health -= player.weapon_damage
                if self.health <= 0:
                    self.item_drop()
        for player in player_group:
            if self.rect.colliderect(player.explosion_rect) and player.explosion_animation_index >= 3:
                self.health -= 15

    def movement(self):
        for player in player_group:
            destination = player.rect
        if self.rect.x >= destination.x:
            self.x -= self.speed
        if self.rect.x < destination.x:
            self.x += self.speed
        if self.rect.y >= destination.y:
            self.y -= self.speed
        if self.rect.y < destination.y:
            self.y += self.speed
        
        self.rect.x = math.floor(self.x)
        self.rect.y = math.floor(self.y)


        if self.rect.centerx > screen_width * 2 or self.rect.centerx < (screen_width * 2) * -1:
            self.kill()
        if self.rect.centery > screen_height * 2 or self.rect.centery < (screen_height * 2) * -1:
            self.kill()
    
    def animate(self):
        self.run_index += 0.05
        if self.run_index >= len(self.animation):
            self.run_index = 0
        self.image = self.animation[int(self.run_index)]

    def healthbar(self):
        self.bar = pygame.draw.rect(screen,"Red",(self.rect.left,self.rect.bottom,(self.health/self.max_health)*self.image.get_width(),10))

    def update(self):
        self.collide()
        self.movement()
        self.healthbar()
        self.animate()

class Boss(Enemies):
    def __init__(self, posx, posy, info):
        super().__init__(posx, posy, info)
        self.shoot_cooldown = 0

    def boss_health_bar(self):
        healthbar = image_import.get_image("pictures for survivor game/boss healthbar.png",(960,64))
        healthbar_full = image_import.get_image("pictures for survivor game/boss healthbar full.png",(960,64))
        screen.blit(healthbar,(170,30))
        screen.blit(healthbar_full,(170,30),pygame.rect.Rect(0,0,(self.health/self.max_health)*960,64))

    def shoot(self):
        for player in player_group:
            endx,endy = player.rect.x,player.rect.y
        x_dist = endx-self.rect.centerx
        y_dist = -(endy-self.rect.centery)
        angle = math.degrees(math.atan2(y_dist,x_dist))

        self.shoot_cooldown += 1
        if self.shoot_cooldown >= 50:
            enemy_group.add(Enemy_bullets(self.rect.centerx,self.rect.centery,"Fireball",angle,self.damage/2,10))
            self.shoot_cooldown = 0

    def update(self):
        self.collide()
        self.movement()
        self.boss_health_bar()
        self.animate()
        self.shoot()

enemy_index = 0
def spawn(frequency):
    global enemy_index, boss_spawn
    if enemy_index >= 0:
        enemy_index += 1
    if enemy_index >= frequency:
        enemy_index = 0
        spawn_side = random.randint(0,3)
        enemy_type = random.randint(0,len(enemies)-1)
        enemy_info = enemies[enemy_type]
        #Chooses which side of the screen the enemies spawn on
        if enemy_info[4] == 0:
            if spawn_side == 0:
                enemy_group.add(Enemies(random.randint(-200,-100),random.randint(0,screen_height),enemy_info))
            if spawn_side == 1:
                enemy_group.add(Enemies(random.randint(screen_width + 100,screen_width + 200),random.randint(0,screen_height),enemy_info))
            if spawn_side == 2:
                enemy_group.add(Enemies(random.randint(0,screen_width),random.randint(-200,-100),enemy_info))
            if spawn_side == 3:
                enemy_group.add(Enemies(random.randint(0,screen_width),random.randint(screen_height + 100,screen_height + 200),enemy_info))

        if enemy_info[4] == 1 and boss_spawn:
            enemy_group.add(Boss(300,-100,enemy_info))
            boss_spawn = False
enemy_group = pygame.sprite.Group()

#collectables
class Collectables(pygame.sprite.Sprite):
    def __init__(self,posx,posy,type):
        super().__init__()
        self.x = posx
        self.y = posy
        self.type = type
        if self.type == "Scrap":
            x = random.randint(0,3)
            self.image = graphics_dict.get(self.type)[x]
        else:
            self.image = graphics_dict.get(self.type)
        self.rect = self.image.get_rect(center = (self.x,self.y))
    def update(self):
        self.rect.x = math.floor(self.x)
        self.rect.y = math.floor(self.y)
collectables_group = pygame.sprite.Group()

#Adding all of the object graphics to the hash table
graphics_dict = data_structures.HashTable() #creating hash table
#collectable graphics
graphics_dict.add("Health",image_import.get_image("pictures for survivor game/collectables/heart collectable.png",(30,30)))
graphics_dict.add("Nuke",image_import.get_image("pictures for survivor game/collectables/nuke collectable.png",(40,16)))
graphics_dict.add("Coin",image_import.get_image("pictures for survivor game/collectables/coin collectable.png",(20,20)))
graphics_dict.add("Scrap",pygame.image.load("pictures for survivor game/collectables/scrap 1.png").convert_alpha())
graphics_dict.add("Scrap",pygame.image.load("pictures for survivor game/collectables/scrap 2.png").convert_alpha())
graphics_dict.add("Scrap",pygame.image.load("pictures for survivor game/collectables/scrap 3.png").convert_alpha())
graphics_dict.add("Scrap",pygame.image.load("pictures for survivor game/collectables/scrap 4.png").convert_alpha())
#enemy graphics
graphics_dict.add("Fly",image_import.get_image("pictures for survivor game/enemy graphics/fly 1.png",(50,40)))
graphics_dict.add("Fly",image_import.get_image("pictures for survivor game/enemy graphics/fly 2.png",(50,40)))
graphics_dict.add("Trash",image_import.get_image("pictures for survivor game/enemy graphics/trash monster 1.png",(100,100)))
graphics_dict.add("Trash",image_import.get_image("pictures for survivor game/enemy graphics/trash monster 2.png",(100,100)))
graphics_dict.add("Alien",image_import.get_image("pictures for survivor game/enemy graphics/alien 1.png",(60,100)))
graphics_dict.add("Alien",image_import.get_image("pictures for survivor game/enemy graphics/alien 2.png",(60,100)))
graphics_dict.add("Zombie",image_import.get_image("pictures for survivor game/enemy graphics/zombie 1.png",(90,90)))
graphics_dict.add("Zombie",image_import.get_image("pictures for survivor game/enemy graphics/zombie 2.png",(90,90)))
graphics_dict.add("UFO",image_import.get_image("pictures for survivor game/enemy graphics/ufo 1.png",(50,50)))
graphics_dict.add("UFO",image_import.get_image("pictures for survivor game/enemy graphics/ufo 2.png",(50,50)))
graphics_dict.add("Ninja",image_import.get_image("pictures for survivor game/enemy graphics/ninja 1.png",(80,100)))
graphics_dict.add("Ninja",image_import.get_image("pictures for survivor game/enemy graphics/ninja 2.png",(80,100)))
graphics_dict.add("Thug",image_import.get_image("pictures for survivor game/enemy graphics/thug 1.png",(60,100)))
graphics_dict.add("Thug",image_import.get_image("pictures for survivor game/enemy graphics/thug 2.png",(60,100)))
graphics_dict.add("Thug",image_import.get_image("pictures for survivor game/enemy graphics/thug 3.png",(60,100)))
graphics_dict.add("Thug",image_import.get_image("pictures for survivor game/enemy graphics/thug 4.png",(60,100)))
#boss graphics
graphics_dict.add("Alien boss",image_import.get_image("pictures for survivor game/enemy graphics/alien boss 1.png",(400,400)))
graphics_dict.add("Alien boss",image_import.get_image("pictures for survivor game/enemy graphics/alien boss 2.png",(400,400)))
graphics_dict.add("Robot boss",image_import.get_image("pictures for survivor game/enemy graphics/robot boss 1.png",(236,208)))
graphics_dict.add("Robot boss",image_import.get_image("pictures for survivor game/enemy graphics/robot boss 2.png",(236,208)))
graphics_dict.add("Evil dude",image_import.get_image("pictures for survivor game/enemy graphics/evil dude 1.png",(90,76)))
graphics_dict.add("Evil dude",image_import.get_image("pictures for survivor game/enemy graphics/evil dude 2.png",(90,76)))
graphics_dict.add("Evil dude",image_import.get_image("pictures for survivor game/enemy graphics/evil dude 3.png",(90,76)))
graphics_dict.add("Evil dude",image_import.get_image("pictures for survivor game/enemy graphics/evil dude 4.png",(90,76)))
graphics_dict.add("Evil dude",image_import.get_image("pictures for survivor game/enemy graphics/evil dude 5.png",(90,76)))
graphics_dict.add("Evil dude",image_import.get_image("pictures for survivor game/enemy graphics/evil dude 6.png",(90,76)))

#menu screen
player_menu_index = 0
menu_cloud = image_import.get_image("pictures for survivor game/backgrounds/menu backgrounds/menu clouds.png",(7200,screen_height))
menu_cloud_rect = menu_cloud.get_rect(topleft = (0,0))
menu_ground = image_import.get_image("pictures for survivor game/backgrounds/menu backgrounds/menu ground.png",(7200,screen_height))
menu_ground_rect = menu_ground.get_rect(topleft = (0,0))
menu_sky = image_import.get_image("pictures for survivor game/backgrounds/menu backgrounds/menu sky.png",(7200,screen_height))
menu_sky_rect = menu_sky.get_rect(topleft = (0,0))
menu_rects = [menu_cloud_rect,menu_sky_rect,menu_ground_rect]
title = image_import.get_image("pictures for survivor game/gun dude title.png",(465,225))
start_button_1 = image_import.get_image("pictures for survivor game/buttons and icons/start button 1.png",(620,200))
start_button_2 = image_import.get_image("pictures for survivor game/buttons and icons/start button 2.png",(620,200))
start_button_rect = start_button_1.get_rect(topleft = (575,300))
exit_button_1 = image_import.get_image("pictures for survivor game/buttons and icons/exit button 1.png",(50,50))
exit_button_2 = image_import.get_image("pictures for survivor game/buttons and icons/exit button 2.png",(50,50))
exit_button_rect = exit_button_1.get_rect(topright = (screen_width,0))
shop_button_1 = image_import.get_image("pictures for survivor game/buttons and icons/shop button 2.png",(500,180))
shop_button_2 = image_import.get_image("pictures for survivor game/buttons and icons/shop button 1.png",(500,180))
shop_button_rect = shop_button_1.get_rect(centerx = start_button_rect.centerx, centery = start_button_rect.centery + 200)
save_button1 = image_import.get_image("pictures for survivor game/buttons and icons/save button 1.png",(100,100))
save_button2 = image_import.get_image("pictures for survivor game/buttons and icons/save button 2.png",(100,100))
save_button_border = image_import.get_image("pictures for survivor game/buttons and icons/save button bordered.png",(100,100))
save_button_rect = save_button1.get_rect(center = (570,600))
i_button1 = image_import.get_image("pictures for survivor game/buttons and icons/i button 1.png",(50,50))
i_button2 = image_import.get_image("pictures for survivor game/buttons and icons/i button 2.png",(50,50))
i_button_rect = i_button1.get_rect(topleft = (0,50))
def menu():
    global player_menu_index, press_timer, menu_rects, menu_cloud_rect, menu_ground_rect, menu_sky_rect, mouse, pressed
    player_menu_1 = image_import.get_image(f"pictures for survivor game/dude graphics/dude run 1 90{player_skin}.png",(500,650))
    player_menu_2 = image_import.get_image(f"pictures for survivor game/dude graphics/dude run 2 90{player_skin}.png",(500,650))
    player_menu = [player_menu_1,player_menu_2]
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

    #Display the current user
    user = pygame.font.Font.render(general_font,f"{current_user}",True,'Red')
    screen.blit(user,(0,0))
    
    #menu button collisions
    #start button
    screen.blit(start_button_1,start_button_rect)
    if start_button_rect.collidepoint(mouse) and current_user != "Select/create a user to play":
        screen.blit(start_button_2,start_button_rect)
        if pressed[0] == True:
            state_stack.append(pre_game_screen)
            press_timer = 0
    #shop button
    screen.blit(shop_button_1,shop_button_rect)
    if shop_button_rect.collidepoint(mouse) and current_user != "Select/create a user to play":
        screen.blit(shop_button_2,shop_button_rect)
        if pressed[0] == True:
            subprocess.run(["Python","game_shop.py"])
    #save button
    if current_user != "Select/create a user to play":
        screen.blit(save_button1,save_button_rect)
    else:
        screen.blit(save_button_border,save_button_rect)
    if save_button_rect.collidepoint(mouse):
        screen.blit(save_button2,save_button_rect)
        if pressed[0] == True:
            subprocess.run(["Python","login_screen.py"])
    #Information button
    screen.blit(i_button1,i_button_rect)
    if i_button_rect.collidepoint(mouse):
        screen.blit(i_button2,i_button_rect)
        if pressed[0] and press_timer == -1:
            press_timer = 0
            state_stack.append(information_screen)
    #exit button
    screen.blit(exit_button_2,exit_button_rect)
    if exit_button_rect.collidepoint(mouse):
        screen.blit(exit_button_1,exit_button_rect)
        if pressed[0] == True and press_timer == -1:
            pygame.quit()
            exit() #exit the game

information_background = image_import.get_image("pictures for survivor game/backgrounds/information screen.png",(1280,720))
menu_button1 = image_import.get_image("pictures for survivor game/buttons and icons/menu button 1.png",(320,150))
menu_button2 = image_import.get_image("pictures for survivor game/buttons and icons/menu button 2.png",(320,150))
menu_button_rect = menu_button1.get_rect(topleft = (0,0))
def information_screen():
    global press_timer
    screen.blit(information_background,(0,0))
    screen.blit(menu_button1,menu_button_rect)
    if menu_button_rect.collidepoint(mouse):
        screen.blit(menu_button2,menu_button_rect)
        if pressed[0] and press_timer == -1:
            press_timer = 0
            state_stack.pop()

#game over screen
def game_over_screen():
    global level_message
    player_dead = image_import.get_image(f"pictures for survivor game/dude graphics/dude death{player_skin}.png",(518,238))
    player_dead_rect = player_dead.get_rect(centerx = screen_width/2,centery = 500)
    respawn_button1 = image_import.get_image("pictures for survivor game/buttons and icons/respawn button 1.png",(200,200))
    respawn_button2 = image_import.get_image("pictures for survivor game/buttons and icons/respawn button 2.png",(200,200))
    menu_button1 = image_import.get_image("pictures for survivor game/buttons and icons/menu button 1.png",(320,150))
    menu_button2 = image_import.get_image("pictures for survivor game/buttons and icons/menu button 2.png",(320,150))
    stats_screen_button1 = image_import.get_image("pictures for survivor game/buttons and icons/stats button 1.png",(100,70))
    stats_screen_button2 = image_import.get_image("pictures for survivor game/buttons and icons/stats button 2.png",(100,70))
    stats_screen_button_rect = stats_screen_button1.get_rect(topleft = (10,10))
    respawn_button_rect = respawn_button1.get_rect(centery = player_dead_rect.centery, centerx = 1100)
    menu_button_rect = menu_button1.get_rect(centery = player_dead_rect.centery,centerx = 190)
    screen.blit(level_background,level_background_rect)
    screen.blit(player_dead,player_dead_rect)
    death_message = pygame.font.Font.render(level_font,f"You died",False,"Red")
    screen.blit(death_message,(player_dead_rect.left - 10,50))
    screen.blit(level_message,(player_dead_rect.left + 30,200))
    screen.blit(respawn_button2,respawn_button_rect)
    screen.blit(stats_screen_button1,stats_screen_button_rect)
    #game over button collisions
    if respawn_button_rect.collidepoint(mouse):
        screen.blit(respawn_button1,respawn_button_rect)
        if pressed[0] == True:
            game_reset()
    #Menu button collisions
    screen.blit(menu_button2,menu_button_rect)
    if menu_button_rect.collidepoint(mouse):
        screen.blit(menu_button1,menu_button_rect)
        if pressed[0] == True:
            for n in range(0,2):
                state_stack.pop()
    #Game stats screen collisions
    if stats_screen_button_rect.collidepoint(mouse):
        screen.blit(stats_screen_button2,stats_screen_button_rect)
        if pressed[0] == True:
            state_stack.append(level_stats_screen)
    #Reset group for next game
    enemy_group.empty()
    bullets_group.empty()
    collectables_group.empty()

#level completion screen
def level_completion_screen():
    player = image_import.get_image(f"pictures for survivor game/dude graphics/dude stand 90{player_skin}.png",(250,325))
    player_rect = player.get_rect(centerx = screen_width/2,centery = 500)
    respawn_button1 = image_import.get_image("pictures for survivor game/buttons and icons/respawn button 1.png",(200,200))
    respawn_button2 = image_import.get_image("pictures for survivor game/buttons and icons/respawn button 2.png",(200,200))
    menu_button1 = image_import.get_image("pictures for survivor game/buttons and icons/menu button 1.png",(320,150))
    menu_button2 = image_import.get_image("pictures for survivor game/buttons and icons/menu button 2.png",(320,150))
    stats_screen_button1 = image_import.get_image("pictures for survivor game/buttons and icons/stats button 1.png",(100,70))
    stats_screen_button2 = image_import.get_image("pictures for survivor game/buttons and icons/stats button 2.png",(100,70))
    stats_screen_button_rect = stats_screen_button1.get_rect(topleft = (10,10))
    respawn_button_rect = respawn_button1.get_rect(centery = player_rect.centery, centerx = 1100)
    menu_button_rect = menu_button1.get_rect(centery = player_rect.centery,centerx = 190)
    screen.blit(level_background,level_background_rect)
    screen.blit(player,player_rect)
    completed_message = pygame.font.Font.render(level_font,f"Level completed",False,"Yellow")
    screen.blit(completed_message,(player_rect.left - 400,100))
    screen.blit(respawn_button2,respawn_button_rect)
    screen.blit(stats_screen_button1,stats_screen_button_rect)
    #button collisions
    if respawn_button_rect.collidepoint(mouse):
        screen.blit(respawn_button1,respawn_button_rect)
        if pressed[0] == True:
            game_reset()
    #Menu button collisions
    screen.blit(menu_button2,menu_button_rect)
    if menu_button_rect.collidepoint(mouse):
        screen.blit(menu_button1,menu_button_rect)
        if pressed[0] == True:
            for n in range(0,2):
                state_stack.pop()
    #Game stats screen collisions
    if stats_screen_button_rect.collidepoint(mouse):
        screen.blit(stats_screen_button2,stats_screen_button_rect)
        if pressed[0] == True:
            state_stack.append(level_stats_screen)

#Post level statistics
def level_stats_screen():
    graph1 = image_import.get_image('Game analytics/Collectable graphs.png',(500,300))
    graph2 = image_import.get_image('Game analytics/Enemy kills.png',(500,300))
    graph3 = image_import.get_image('Game analytics/General stats.png',(500,300))
    graph4 = image_import.get_image('Game analytics/Healthgraph.png',(500,300))
    back_button1 = image_import.get_image('pictures for survivor game/buttons and icons/back button 2.png',(50,50))
    back_button2 = image_import.get_image('pictures for survivor game/buttons and icons/back button 1.png',(50,50))
    back_button_rect = back_button1.get_rect(center = (screen_width/2,screen_height/2))
    screen.blit(graph1,(93,20))
    screen.blit(graph2,(686,20))
    screen.blit(graph3,(93,380))
    screen.blit(graph4,(686,380))
    screen.blit(back_button1,back_button_rect)

    if back_button_rect.collidepoint(mouse):
        screen.blit(back_button2,back_button_rect)
        if pressed[0] == True:
            state_stack.pop()


#pause game
def pause_button(state):
    global pause_button_rect, press_timer
    pause_button1 = image_import.get_image("pictures for survivor game/buttons and icons/pause button 1.png",(100,100))
    pause_button2 = image_import.get_image("pictures for survivor game/buttons and icons/pause button 2.png",(100,100))
    pause_button_rect = pause_button1.get_rect(topright = (screen_width,0))
    screen.blit(pause_button1,pause_button_rect)
    if pause_button_rect.collidepoint(mouse):
        screen.blit(pause_button2,pause_button_rect)
        if pressed[0] == True:
            press_timer = 0
            if state == "Game": state_stack.pop()
            if state == "Pause": state_stack.append(pause_screen)

def pause_screen():
    global press_timer
    menu_button1 = image_import.get_image("pictures for survivor game/buttons and icons/menu button 1.png",(320,150))
    menu_button2 = image_import.get_image("pictures for survivor game/buttons and icons/menu button 2.png",(320,150))
    menu_button_rect = menu_button1.get_rect(centerx = screen_width/2,centery = 300)
    screen.blit(pygame.font.Font.render(level_font,"Paused",False,level_colour),(445,60))
    screen.blit(menu_button2,menu_button_rect)
    if menu_button_rect.collidepoint(mouse):
        screen.blit(menu_button1,menu_button_rect)
        if pressed[0] == True:
            for n in range(0,3):
                state_stack.pop()
    play_button1 = image_import.get_image("pictures for survivor game/buttons and icons/respawn button 2.png",(300,300))
    play_button2 = image_import.get_image("pictures for survivor game/buttons and icons/respawn button 1.png",(300,300))
    play_button_rect = play_button1.get_rect(centerx = screen_width/2,centery = 550)
    screen.blit(play_button1,play_button_rect)
    if play_button_rect.collidepoint(mouse):
        screen.blit(play_button2,play_button_rect)
        if pressed[0] == True:
            game_reset()

    if press_timer == -1:
        pause_button("Game")

#level_up screen
level_up_background = image_import.get_image("pictures for survivor game/backgrounds/level up background.png",(screen_width,813))
level_up_background_rect = level_up_background.get_rect(topleft = (0,627))
level_up_animation = False
level_up_exit = False
upgrade_template = image_import.get_image("pictures for survivor game/backgrounds/level up background.png",(280,560))
fire_rate_upgrade = image_import.get_image("pictures for survivor game/buttons and icons/Power ups/Fire rate upgrade.png",(280,560))
speed_upgrade = image_import.get_image("pictures for survivor game/buttons and icons/Power ups/Speed upgrade.png",(280,560))
damage_upgrade = image_import.get_image("pictures for survivor game/buttons and icons/Power ups/Damage upgrade.png",(280,560))
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
                    player.weapon_damage += 0.3
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
#pre game screen
def pre_game_screen():
    global current_level, level_message, press_timer, enemies
    level_setup()
    screen.blit(level_background,(0,0))
    arrow_button1 = image_import.get_image("pictures for survivor game/buttons and icons/arrow button 1.png",(80,80))
    arrow_button2 = image_import.get_image("pictures for survivor game/buttons and icons/arrow button 2.png",(80,80))
    arrow_button_rect = arrow_button1.get_rect(bottomright = (screen_width,screen_height)) 
    left_arrow_button1 = pygame.transform.flip(arrow_button1,True,False)
    left_arrow_button2 = pygame.transform.flip(arrow_button2,True,False)
    left_arrow_button_rect = left_arrow_button1.get_rect(bottomleft = (0,screen_height))
    level_message = pygame.font.Font.render(level_font,f"Level {current_level}",False,level_colour)
    level_message_rect = pygame.rect.Rect(420,80,480,100)
    play_button1 = image_import.get_image("pictures for survivor game/buttons and icons/Play button 1.png",(400,400))
    play_button2 = image_import.get_image("pictures for survivor game/buttons and icons/Play button 2.png",(400,400))
    play_button_rect = pygame.rect.Rect(440,250,400,400)
    locked_icon = image_import.get_image("pictures for survivor game/buttons and icons/locked icon.png",(400,400))
    menu_button_1 = image_import.get_image("pictures for survivor game/buttons and icons/menu button 2.png",(220,100))
    menu_button_2 = image_import.get_image("pictures for survivor game/buttons and icons/menu button 1.png",(220,100))
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

    level_list = database.is_complete(current_user)
    if level_list[current_level-1][0] == 1:
        screen.blit(play_button1,play_button_rect)
        if play_button_rect.collidepoint(mouse) and press_timer == -1:
            screen.blit(play_button2,play_button_rect)
            if pressed[0] == True:
                game_reset()
    else:
        screen.blit(locked_icon,play_button_rect)

    #Pre loads enemy information
    enemies = database.get_enemies(current_level)

#levels
current_level = 1
def level_setup():
    global level_background, enemy_frequency, level_colour, wave_num, level_background_rect, level_backgroundx, level_backgroundy
    #level 1
    if current_level == 1:
        enemy_frequency = 200
        level_background = pygame.image.load("pictures for survivor game/backgrounds/level 1 background.png").convert_alpha()
        level_colour = "Brown"
        wave_num = 1
    #level 2
    if current_level == 2:
        level_background = pygame.image.load("pictures for survivor game/backgrounds/level 1 background.png").convert_alpha()
        level_colour = "#44230D"
        wave_num = 1
        enemy_frequency = 50
    #level 3
    if current_level == 3:
        level_background = pygame.image.load("pictures for survivor game/backgrounds/Level 3 background.png").convert_alpha()
        level_colour = "#0f9100"
        wave_num = 20
        enemy_frequency = 60
    #level 4
    if current_level == 4:
        level_background = pygame.image.load("pictures for survivor game/backgrounds/Level 3 background.png").convert_alpha()
        level_colour = "#78050b"
        wave_num = 20
        enemy_frequency = 60
    #level 5
    if current_level == 5:
        level_background = pygame.image.load("pictures for survivor game/backgrounds/Level 5 background.png").convert_alpha()
        level_colour = "#8f5703"
        wave_num = 30
        enemy_frequency = 70
    #level 6
    if current_level == 6:
        level_background = pygame.image.load("pictures for survivor game/backgrounds/Level 5 background.png").convert_alpha()
        level_colour = "#636630"
        wave_num = 30
        enemy_frequency = 70
    #level 7
    if current_level == 7:
        level_background = pygame.image.load("pictures for survivor game/backgrounds/Level 7 background.png").convert_alpha()
        level_colour = "#080f8c"
        wave_num = 30
        enemy_frequency = 80
    #level 8
    if current_level == 8:
        level_background = pygame.image.load("pictures for survivor game/backgrounds/Level 7 background.png").convert_alpha()
        level_colour = "#76088c"
        wave_num = 30
        enemy_frequency = 80
    #level 9
    if current_level == 9:
        level_background = pygame.image.load("pictures for survivor game/backgrounds/Level 9 background.png").convert_alpha()
        level_colour = "Pink"
        wave_num = 30
        enemy_frequency = 90
    #level 10
    if current_level == 10:
        level_background = pygame.image.load("pictures for survivor game/backgrounds/Level 9 background.png").convert_alpha()
        level_colour = "Pink"
        wave_num = 30
        enemy_frequency = 100
    
    level_background = pygame.transform.scale(level_background,(screen_width*3,screen_height*3))
    level_background_rect = level_background.get_rect(center = (screen_width/2,screen_height/2))
    level_backgroundx = level_background_rect.x
    level_backgroundy = level_background_rect.y

#main game
def main_game():
    global current_level, press_timer, game_timer
    crosshair = image_import.get_image("pictures for survivor game/Crosshair.png",(30,30))
    level_background_rect.x = math.floor(level_backgroundx)
    level_background_rect.y = math.floor(level_backgroundy)
    screen.blit(level_background,level_background_rect)
    bullets_group.draw(screen)
    bullets_group.update()
    collectables_group.draw(screen)
    collectables_group.update()
    enemy_group.draw(screen)
    enemy_group.update()
    for player in player_group:
        if player.invincible:
            if math.ceil(player.invincible_counter) % 2 == 0:
                player_group.draw(screen)
        if player.invincible == False:
            player_group.draw(screen)
    player_group.update()
    spawn(enemy_frequency)
    screen.blit(crosshair,(mouse[0]-15,mouse[1]-15))


    if press_timer == -1:
        pause_button("Pause")
    game_timer += 0.016

#reset game
def game_reset():
    global  game_timer, power_up_list, player_group, boss_spawn
    state_stack.append(main_game)
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Player())
    for player in player_group:
        player.reset()
    bullets_group.empty()
    enemy_group.empty()
    collectables_group.empty()
    game_timer = 0
    power_up_list = [fire_rate_upgrade,speed_upgrade,damage_upgrade]
    boss_spawn = True
    


skill_purchased = [False,False,False,False,False,False,False,None,False,False,False,False,False,False,False,]
def update_skills():
    for skill in user_skills:
        skill_purchased[int(skill[0])-1] = True

#define stack which holds the game state
state_stack = [menu]

#main game loop
while True:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

    #constantly update user information
    current_user = database.get_user()
    try:
        user_skills = database.get_skills()
        player_skin = database.get_selected_skin()
        update_skills()
    except:
        pass

    #constantly update keyboard/mouse variables
    key = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    #run press timer algorithm
    if press_timer >= 0:
        press_timer += 1
        if press_timer >= 20:
            press_timer = -1

    #run the current state
    current_state = len(state_stack) - 1
    state_stack[current_state]()

    #update everything on screen
    pygame.display.update()
    clock.tick(60)