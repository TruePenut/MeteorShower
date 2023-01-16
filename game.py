import pygame, sys
from math import *
import random

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720

fps = 60

clock = pygame.time.Clock()

def det(num):
    return trunc(round(num*dt))

class Object:
    def __init__(self, surf, rect):

            self.surf = surf
            self.rect = rect

    def blit(self):
        display_surface.blit(self.surf,self.rect)    


class Player(Object):
    def __init__(self, surf, rect, upin, downin, leftin, rightin, surf_r, surf_l):
        Object.__init__(self, surf, rect)
        self.upin = upin
        self.downin = downin
        self.leftin = leftin
        self.rightin = rightin
        self.verticalshipspeed = 0
        self.horizontalshipspeed = 0
        self.surfr = surf_r
        self.surfl = surf_l

    def move(self, acc, deacc):
    
        keys = pygame.key.get_pressed()
        if keys[self.upin]:
            self.verticalshipspeed -= acc
        if keys[self.downin]:
            self.verticalshipspeed += acc
        if keys[self.leftin]:
            self.horizontalshipspeed -= acc
        if keys[self.rightin]:
            self.horizontalshipspeed += acc
        if keys[pygame.K_r]:
            self.rect.center = 640, 360
        
        #Adds a speed limit and stops the code from doign extra complex math
        if -3 < self.verticalshipspeed < 3 :
            self.verticalshipspeed = 0
        if -3 < self.horizontalshipspeed < 3:
            self.horizontalshipspeed = 0
        self.verticalshipspeed /= deacc
        self.horizontalshipspeed /= deacc

        #Moves the ship
        self.rect.centery += det(self.verticalshipspeed)
        self.rect.centerx += det(self.horizontalshipspeed)

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 720:
            self.rect.bottom = 720
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1280:
            self.rect.right = 1280

    def blit(self):
        if self.horizontalshipspeed >= 200:
            display_surface.blit(self.surfr,self.rect)   
            print(self.horizontalshipspeed) 
        elif self.horizontalshipspeed <= -200:
            display_surface.blit(self.surfl,self.rect)
            print(self.horizontalshipspeed)
        else:
            display_surface.blit(self.surf,self.rect)        


class Bullet(Object):
    def __init__(self, surf, rect, speed, parent_rect, sh_in, cl_list, reload_time):
        Object.__init__(self, surf, rect)
        self.surf = surf
        self.rect = rect
        self.speed = speed
        self.parent = parent_rect
        self.sh_in = sh_in
        self.cl_list = cl_list
        self.reload_t = reload_time
        self.reload = False
        self.t = 0
        self.x = 0

    def timer(self):
        if self.reload == False:           
            current_time = int(pygame.time.get_ticks())
            if current_time - self.t > self.reload_t:
                self.reload = True

    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[self.sh_in]:
            if self.reload == True:
                if self.x == 0:
                    bullet_rect = bullet_surf.get_rect(bottomleft = self.parent.midtop)
                    self.x =1
                else:
                    bullet_rect = bullet_surf.get_rect(bottomright = self.parent.midtop)
                    self.x =0
                self.cl_list.append(bullet_rect)
                self.reload = False
                self.t = int(pygame.time.get_ticks())
                


display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
font = pygame.font.Font("../assets/graphics/REDENSEK.TTF",50)
pygame.display.set_caption("Astral Violaters")


ship_surf = pygame.image.load("../assets/graphics/ship.png").convert_alpha()
ship_surf = pygame.transform.scale(ship_surf, (ship_surf.get_width()*5, ship_surf.get_height()*5))
ship_rect = ship_surf.get_rect(center = (640, 360))

ship_surf_r = pygame.image.load("../assets/graphics/ship_r.png").convert_alpha()
ship_surf_r = pygame.transform.scale(ship_surf_r, (ship_surf_r.get_width()*5, ship_surf_r.get_height()*5))

ship_surf_l = pygame.image.load("../assets/graphics/ship_l.png").convert_alpha()
ship_surf_l = pygame.transform.scale(ship_surf_l, (ship_surf_l.get_width()*5, ship_surf_l.get_height()*5))

bullet_surf = pygame.image.load("../assets/graphics/bullet.png").convert_alpha()
bullet_surf = pygame.transform.scale(bullet_surf, (bullet_surf.get_width()*5, bullet_surf.get_height()*5))
bullet_rect = 0

asteriod_surf = pygame.image.load("../assets/graphics/asteriod-medium1.png").convert_alpha()
asteriod_surf = pygame.transform.scale(asteriod_surf, (asteriod_surf.get_width()*5, asteriod_surf.get_height()*5))

text_surf = font.render("Fick Dich", False, (225,255,255))
text_surf2 = font.render("Fick Dich", False, (225,255,255))

asteroid_timer = pygame.event.custom_type()
pygame.time.set_timer(asteroid_timer,random.randint(1000, 2000))

laser_list = []

asteroid_list = []

Ship1 = Player(ship_surf, ship_rect, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, ship_surf_r, ship_surf_l)
PBullet = Bullet(bullet_surf, bullet_rect, 12, ship_rect, pygame.K_SPACE, laser_list, 60)

while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:      
            pygame.quit()
            sys.exit()
        if event.type == asteroid_timer:
            asteroid_rect = asteriod_surf.get_rect(midbottom = (random.randint(100, 1000),0))
            asteroid_list.append(asteroid_rect)
            

    dt = clock.tick(60) /1000

    text_surf = font.render(f"{det(Ship1.verticalshipspeed)}", False, (225,255,255))
    text_surf2 = font.render(f"{det(Ship1.horizontalshipspeed)}", False, (225,255,255))
    display_surface.fill((15,15,35))
    display_surface.blit(text_surf,(200,200))
    display_surface.blit(text_surf2,(200,100))


    PBullet.shoot()
    PBullet.timer()

    Ship1.blit()
    Ship1.move(100, 1.2)

    print(len(asteroid_list))
    

    for rect in laser_list:
        rect.y -= det(100*PBullet.speed)
        display_surface.blit(bullet_surf, rect)
        if rect.bottom < 0:
            laser_list.remove(rect)


    for rect in asteroid_list:
        rect.y += det(150)
        if rect.top > 720:
            asteroid_list.remove(rect)
        display_surface.blit(asteriod_surf, rect)

    pygame.display.update()