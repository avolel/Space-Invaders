import pygame
from explode import Explosion

#Create Alien Bullets
class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_height, spaceship):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.screen_height = screen_height
        self.spacehip = spaceship

    def get_SpriteGrps(self):
        return [self.bullet_grp, self.alien_grp, self.explosion_grp, self.spaceship_grp]

    def set_SpriteGrps(self, sprites_grps = []):        
        self.bullet_grp = sprites_grps[0]
        self.alien_grp = sprites_grps[1]
        self.explosion_grp = sprites_grps[2]
        self.spaceship_grp = sprites_grps[3]

    def get_SoundEffects(self):
        return [self.explosion_fx, self.explosion_fx2, self.laser_fx]

    def set_SoundEffects(self, soundeffects = []):
        self.explosion_fx = soundeffects[0]
        self.explosion_fx2 = soundeffects[1]
        self.laser_fx = soundeffects[2]

    sprite_groups = property(get_SpriteGrps, set_SpriteGrps)
    sound_effects = property(get_SoundEffects, set_SoundEffects)

    #SPRITE GROUPS: BULLET GRP is at index 0, ALIEN GRP is at index 1, EXPLOSION GRP is at index 2, SPACESHIP GRP is at index 3
    #SOUND EFFECTS: EXPLOSION FX is index 0, EXPLOSION FX 2 is at index 1, LASER FX is at index 2

    def update(self):
        self.rect.y += 2
        if self.rect.top > self.screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, self.sprite_groups[3], False, pygame.sprite.collide_mask): #Check if Alien Bullets hit Space ship
            self.kill()
            self.sound_effects[1].play() #Play explosion_fx2 when spaceship is destroyed
            #Reduce Spaceship Health
            self.spacehip.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            self.sprite_groups[2].add(explosion) #Add explosion to explosion group

