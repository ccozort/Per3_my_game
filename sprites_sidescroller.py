# This file was created by: Chris Cozort

import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random
from utils import *

# test comment for GIT

vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 2
        self.jumping = False
        self.jump_power = 15
        self.coins = 0
        self.health = 10
        self.projectile_cd = Cooldown()
        self.powerup_cd = Cooldown()
        self.can_collect_powerup = True
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.collide_with_stuff(self.game.all_ladders, False):
            self.vel.y -= self.speed
        if keys[pg.K_a]:
            self.vel.x -= self.speed
        if keys[pg.K_d]:
            self.vel.x += self.speed
        if keys[pg.K_SPACE]:
            self.jump()
        if pg.mouse.get_pressed()[0]:
            print(pg.mouse.get_pos())
            self.shoot()

    def shoot(self):
        self.projectile_cd.event_time = floor(pg.time.get_ticks()/1000)
        if self.projectile_cd.delta > .001:
            p = Projectile(self.game, self.rect.x, self.rect.y)

    
    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game.jump_snd.play()
            self.jumping = True
            self.vel.y = -self.jump_power
            print("trying to jump")
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                    # self.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.jumping = False
                    # self.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup" and self.can_collect_powerup:
                print("i got a powerup...")
                self.can_collect_powerup = False
                self.powerup_cd.event_time = floor(pg.time.get_ticks()/1000)
                
                    
                    # hits[0].image = pg.transform.scale(hits[0].image, (200, 200))

            if str(hits[0].__class__.__name__) == "Mob":
                print("i hit a mob...")
                old_center = hits[0].rect.center
                hits[0].image = pg.transform.scale(hits[0].image, (64, 64))
                hits[0].rect = hits[0].image.get_rect()
                hits[0].rect.center = old_center
            if str(hits[0].__class__.__name__) == "Coin":
                print("i hit a coin...")
                self.coins += 1
    def update(self):
        self.projectile_cd.ticking()
        self.powerup_cd.ticking()
        if self.powerup_cd.delta > 1:
            print("i can get a powerup again")
            self.can_collect_powerup = True
        if self.can_collect_powerup:
            self.collide_with_stuff(self.game.all_powerups, True)
            
        self.acc = vec(0, GRAVITY)
        self.get_keys()
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc 

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc

        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
        # reverse order to fix collision issues

        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_mobs, False)

class Projectile(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 10
        # self.category = random.choice([0,1])
    def update(self):

        # # moving towards the side of the screen
        self.rect.x += self.speed
        
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        # when it hits the side of the screen, it will move down
        if hits:
            # print("off the screen...")
            self.speed *= -1
            # self.rect.y += 32
        if self.rect.right > WIDTH or self.rect.left < 0:
            # print("off the screen...")
            self.speed *= -1
            # self.rect.y += 32
        # elif self.rect.colliderect(self.game.player):
        #     self.speed *= -1
        # elif self.rect.colliderect(self):
        #     self.speed *= -1

   
        # # then it will move towards the other side of the screen
        # # if it gets to the bottom, then it move to the top of the screen
        # # (display logic in the terminal)

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(BLUE)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        pass
class Pillar(Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        self.groups = game.all_sprites, game.all_pillars
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.rect.w = w * TILESIZE
        self.rect.h = h * TILESIZE


    def update(self):
        pass

class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(PINK)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.width = self.rect.width
    def update(self):
        # self.rect = self.image.get_rect()
        # self.rect.width = self.width
        pass

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Ladder(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_ladders
        Sprite.__init__(self, self.groups)
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.ladder_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # self.image.fill(YELLOW)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE