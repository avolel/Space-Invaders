import pygame
import random
from pygame import mixer
from pygame.locals import *
from spaceship import Spaceship
from alien import Aliens
from alienbullets import AlienBullets

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

#Define Frames Per Second (FPS)
clock = pygame.time.Clock()
fps = 60

#Define Colours
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)

#Define Game Variables
rows = 5
columns = 5
alien_cooldown = 1000 #Bullet cooldown in milliseconds
last_alien_shot = pygame.time.get_ticks()
last_count = pygame.time.get_ticks()
countdown = 3
gameOver = 0 #0 means the game is not over, 1 means the player has won, -1 means the player has lost
health = 3

screenWidth = 600
screenHeight = 800

screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption('Space Invaders')

#Define fonts
font30 = pygame.font.SysFont("Constantia", 30)
font40 = pygame.font.SysFont("Constantia", 40)

#Load Sound Effects
explosion_fx = pygame.mixer.Sound("assets/explosion.wav")
explosion_fx.set_volume(0.25)

explosion_fx2 = pygame.mixer.Sound("assets/explosion2.wav")
explosion_fx2.set_volume(0.25)

laser_fx = pygame.mixer.Sound("assets/laser.wav")
laser_fx.set_volume(0.25)

#Load Image
background = pygame.image.load("assets/bg.jpg")

#Create Sprite Groups
spaceship_grp = pygame.sprite.Group()
bullet_grp = pygame.sprite.Group()
alien_grp = pygame.sprite.Group()
alienbullet_grp = pygame.sprite.Group()
explosion_grp = pygame.sprite.Group()

#Create Player
spaceship = Spaceship(int(screenWidth / 2), screenHeight - 100, health, red, green, screen)
spaceship.sprite_groups = [bullet_grp, alien_grp, explosion_grp]
spaceship.sound_effects = [explosion_fx, explosion_fx2, laser_fx]
spaceship_grp.add(spaceship)

def create_aliens():
    for row in range(rows):
        for item in range(columns):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_grp.add(alien)

def draw_bg():
    screen.blit(background,(0,0))

def restart():
    global gameOver, countdown, health, spaceship
    gameOver = 0
    countdown = 3
    health = 3

    if len(spaceship_grp) > 0:
        spaceship_grp.empty()
    if len(bullet_grp) > 0:
        bullet_grp.empty()
    if len(alien_grp) > 0:    
        alien_grp.empty()
    if len(alienbullet_grp) > 0:    
        alienbullet_grp.empty()
    if len(explosion_grp) > 0:    
        explosion_grp.empty()

    spaceship = Spaceship(int(screenWidth / 2), screenHeight - 100, health, red, green, screen)
    spaceship.sprite_groups = [bullet_grp, alien_grp, explosion_grp]
    spaceship.sound_effects = [explosion_fx, explosion_fx2, laser_fx]
    spaceship_grp.add(spaceship)
    create_aliens()

#Create function for creating text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

create_aliens()

run = True
while run:
    clock.tick(fps)
    #Draw Background
    draw_bg()

    if countdown == 0:
        #Create random alien bullets
        #Record current time
        time_now = pygame.time.get_ticks()
        #Aliens Fires Gun at player
        if time_now - last_alien_shot > alien_cooldown and len(alienbullet_grp) < 5 and len(alien_grp) > 0:
            attacking_alien = random.choice(alien_grp.sprites())
            alien_bullet = AlienBullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom, screenHeight, spaceship)
            alien_bullet.sprite_groups = [bullet_grp, alien_grp, explosion_grp, spaceship_grp]
            alien_bullet.sound_effects = spaceship.sound_effects
            alienbullet_grp.add(alien_bullet)
            last_alien_shot = time_now
        
        #Check if all the aliens have been killed
        if len(alien_grp) == 0:
            gameOver = 1
        
        if gameOver == 0:
            #Update space ship
            gameOver = spaceship.update()

            #Update Sprite Groups
            bullet_grp.update()
            alien_grp.update()
            alienbullet_grp.update()
        else:
            if gameOver == -1:
                draw_text("GAME OVER!",font40,white, int(screenWidth / 2 - 100), int(screenHeight / 2 + 50))
                restart()
            if gameOver == 1:
                draw_text("YOU WIN!",font40,white, int(screenWidth / 2 - 100), int(screenHeight / 2 + 50))
                restart()

    
    if countdown > 0:
        draw_text("GET READY!",font40,white, int(screenWidth / 2 - 110), int(screenHeight / 2 + 50))
        draw_text(str(countdown),font40,white, int(screenWidth / 2 - 10), int(screenHeight / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer
    
    #Update Explosion Group
    explosion_grp.update()

    #Draw Sprite Groups
    spaceship_grp.draw(screen)
    bullet_grp.draw(screen)
    alien_grp.draw(screen)
    alienbullet_grp.draw(screen)
    explosion_grp.draw(screen)

    #Event  Handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
pygame.quit()