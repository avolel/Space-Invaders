import pygame
from bullet import Bullets
from explode import Explosion

#Create Space Ship
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health, red, green, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()
        self.health_start = health
        self.health_remaining = health
        self.red = red
        self.green = green
        self.screen = screen

    def get_SpriteGrps(self):
        return [self.bullet_grp, self.alien_grp, self.explosion_grp]

    def set_SpriteGrps(self, sprites_grps = []):
        self.bullet_grp = sprites_grps[0]
        self.alien_grp = sprites_grps[1]
        self.explosion_grp = sprites_grps[2]

    def get_SoundEffects(self):
        return [self.explosion_fx, self.explosion_fx2, self.laser_fx]

    def set_SoundEffects(self, soundeffects = []):
        self.explosion_fx = soundeffects[0]
        self.explosion_fx2 = soundeffects[1]
        self.laser_fx = soundeffects[2]

    sprite_groups = property(get_SpriteGrps, set_SpriteGrps)
    sound_effects = property(get_SoundEffects, set_SoundEffects)
    
    def update(self):
        #Set movement speed
        speed = 8
        gameOver = 0
        #Set bullet cooldown variable
        cooldown = 300 #in milliseconds

        #Get key presses
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < 600:
            self.rect.x += speed
        
        #Record Current Time
        time_now = pygame.time.get_ticks()

        #SPRITE GROUPS: BULLET GRP is at index 0, ALIEN GRP is at index 1, EXPLOSION GRP is at index 2
        #SOUND EFFECTS: EXPLOSION FX is index 0, EXPLOSION FX 2 is at index 1, LASER FX is at index 2

        #Spaceship firing it's Guns
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            self.sound_effects[2].play() #Play laser_fx sound effect
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet.sprite_groups = self.sprite_groups
            bullet.sound_effects = self.sound_effects
            self.bullet_grp.add(bullet)
            self.last_shot = time_now
        
        #Update Mask
        self.mask = pygame.mask.from_surface(self.image)
    
        #Draw Health Bar
        pygame.draw.rect(self.screen,self.red, (self.rect.x,(self.rect.bottom + 10),self.rect.width, 15))
        
        #Health Remaining is greater than 0
        if self.health_remaining > 0:
            pygame.draw.rect(self.screen,self.green, (self.rect.x,(self.rect.bottom + 10),int(self.rect.width * (self.health_remaining /  self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            self.sprite_groups[2].add(explosion) #Add Explosion to explosion group
            self.kill()
            gameOver = -1
        return gameOver