import pygame
from explode import Explosion

#Create Bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

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

    #SPRITE GROUPS: BULLET GRP is at index 0, ALIEN GRP is at index 1, EXPLOSION GRP is at index 2
    #SOUND EFFECTS: EXPLOSION FX is index 0, EXPLOSION FX 2 is at index 1, LASER FX is at index 2

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, self.sprite_groups[1], True): #Check wheather space ship bullets hit an alien in the alien group object
            self.kill()
            self.sound_effects[0].play() #Play explosion_fx sound effect
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            self.sprite_groups[2].add(explosion) #Add explosion to explosion group