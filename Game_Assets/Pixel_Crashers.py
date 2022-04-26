#Pixel Crashers by Nick Czernik, Freshman


import pygame
import random
import time
import os

WIDTH = 1000
HEIGHT = 600
DISP = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("-|Pixel Crashers|-")
special = 1
speed = 5
laser_speed = 10
CRASHW = 125
CRASHH = 170
randy = 55
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
PURPLE = (191, 64, 191)
HITREG = pygame.USEREVENT + 1
playerdamage = pygame.USEREVENT + 2
SPECHIT = pygame.USEREVENT + 3
#Images
BACKGROUND = pygame.image.load(os.path.join('images', 'backg.jpg'))
CRASHER = pygame.image.load(os.path.join('images', 'crasher.png'))
ENEMY1 = pygame.image.load(os.path.join('images', 'owly.png'))

#Image Transforming
BGSCALE = pygame.transform.scale(BACKGROUND, (1000, 600))
CRASHSCALE = pygame.transform.scale(CRASHER, (CRASHW, CRASHH))
OWLSCALE = pygame.transform.scale(ENEMY1, (CRASHW, CRASHH))
OWLFLIP = pygame.transform.flip(OWLSCALE, True, False)
def draw(crsh, owlr, claser, bproj, special_attack, damage, life, bdamage, bosslife):
    DISP.blit(BGSCALE,(0,0))
    DISP.blit(CRASHSCALE,(crsh.x, crsh.y))
    DISP.blit(OWLFLIP,(owlr.x, owlr.y))
    pygame.draw.rect(DISP, RED, damage)
    pygame.draw.rect(DISP, GREEN, life)
    pygame.draw.rect(DISP, BLACK, bdamage)
    pygame.draw.rect(DISP, PURPLE, bosslife)
    for projectile in bproj:
        pygame.draw.rect(DISP, WHITE, projectile)
    for laser in claser:
        pygame.draw.rect(DISP, RED, laser)
    for speciallaser in special_attack:
        pygame.draw.rect(DISP, PURPLE, speciallaser)
    pygame.display.update()

def crash_moveset(keys, crsh):
    if keys[pygame.K_a] and crsh.x + 15 > 0:
        crsh.x -= speed
    if keys[pygame.K_d] and crsh.x < 400:
        crsh.x += speed
    if keys[pygame.K_w] and crsh.y + 15 > 0:
        crsh.y -= speed
    if keys[pygame.K_s] and crsh.y + speed + CRASHH < HEIGHT:
        crsh.y += speed

               


def makelasers(claser, bproj, special_attack, crsh, owlr):
    for projectile in bproj:
        projectile.x -= laser_speed
        if crsh.colliderect(projectile):
            bproj.remove(projectile)
            pygame.event.post(pygame.event.Event(playerdamage))
        elif projectile.x < 0:
            bproj.remove(projectile)
    for laser in claser:
        laser.x += laser_speed
        if owlr.colliderect(laser):
            claser.remove(laser)
            pygame.event.post(pygame.event.Event(HITREG))
        elif laser.x > WIDTH:
            claser.remove(laser)
    for speciallaser in special_attack:
        speciallaser.x += laser_speed
        if owlr.colliderect(speciallaser):
            special_attack.remove(speciallaser)
            pygame.event.post(pygame.event.Event(SPECHIT))
        elif speciallaser.x > WIDTH:
            special_attack.remove(speciallaser)
def enemyupdate(claser, bproj, special_attack, keys, owlr):
    if keys[pygame.K_SPACE] and owlr.y + speed + CRASHH < HEIGHT:
        
        owlr.y += speed * 2
    if keys[pygame.K_w] and owlr.y + speed + CRASHH < HEIGHT:
        
        owlr.y += speed/2
    if keys[pygame.K_s] and owlr.y + 15 > 0:
        
        owlr.y -= speed
    for laser in claser:
        if laser.x > 500 and owlr.y + 15 > 0:
            owlr.y -= speed
   
    for projectile in bproj:
        if projectile.x < 500 and owlr.y + speed + CRASHH < HEIGHT:
            owlr.y += speed/2
        if projectile.x < 100 and owlr.y + 15 > 0:
            owlr.y -= speed/2
    for speciallaser in special_attack:
        if speciallaser.x > 500 and owlr.y + 15 > 0:
            owlr.y -= speed * 2
def main():
    BOSSHEALTH = 200
    PLAYERHEALTH = 100
    claser = []
    bproj = []
    special_attack = []
    clock = pygame.time.Clock()
    crsh = pygame.Rect(100, 300, CRASHW, CRASHH)
    owlr = pygame.Rect(800,300, CRASHW, CRASHH)
    
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            damage = pygame.Rect(125,550, 100, 5)
            life = pygame.Rect(125,550, PLAYERHEALTH, 5)
            bdamage = pygame.Rect(725,550, 200, 5)
            bosslife = pygame.Rect(725,550, BOSSHEALTH, 5)
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    laser = pygame.Rect(crsh.x + CRASHW, crsh.y + CRASHH - 105, 25, 10)
                    claser.append(laser)

                if randy >= 50:
                    projectile = pygame.Rect(owlr.x, owlr.y + CRASHH - 105, 25, 10)
                    bproj.append(projectile)
                    
                if event.key == pygame.K_b and len(special_attack) < special:
                    speciallaser = pygame.Rect(crsh.x + CRASHW, crsh.y + CRASHH - 105, 50, 20)
                    special_attack.append(speciallaser)
                 
                    
            if event.type == HITREG:
                
                BOSSHEALTH -= 2
            if event.type == playerdamage:

                PLAYERHEALTH -= 2
            if event.type == SPECHIT:

                BOSSHEALTH -= 8

                
        if BOSSHEALTH <= 0:
            print("YOU WON!!")
            run = False
        if PLAYERHEALTH <= 0:
            print("You lost...")
            run = False
       
            
        keys = pygame.key.get_pressed()
        crash_moveset(keys, crsh)
        enemyupdate(claser, bproj, special_attack,  keys, owlr)
        makelasers(claser, bproj, special_attack, crsh, owlr)
        draw(crsh, owlr, claser, bproj, special_attack, damage, life, bdamage, bosslife)
        
    pygame.quit()

if __name__ == "__main__":
    main()
