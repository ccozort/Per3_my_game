# This file was created by: Chris Cozort

import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random
from utils import *


# Modified from Chat GPT - create snake game and make snake a pygame sprite
class Snake(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.segments = [[WIDTH // 2, HEIGHT // 2]]
        self.direction = (0, 0)
        self.grow = False
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.direction = (-TILESIZE, 0)
        elif keys[pg.K_a]:
            self.direction = (TILESIZE, 0)
        elif keys[pg.K_s]:
            self.direction = (0, -TILESIZE)
        elif keys[pg.K_d]:
            self.direction = (0, TILESIZE)


    def draw(self):
        for segment in self.segments:
            pg.draw.rect(self.game.screen, BLACK, [segment[0], segment[1], TILESIZE, TILESIZE])

    def check_collision(self):
        head = self.segments[0]
        # Check boundaries
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        # Check self-collision
        if head in self.segments[1:]:
            return True
        return False

    def grow_snake(self):
        self.grow = True

    def update(self):
        self.get_keys()
        if self.direction != (0, 0):
            head_x, head_y = self.segments[0]
            delta_x, delta_y = self.direction
            new_head = [head_x + delta_x, head_y + delta_y]
            self.segments.insert(0, new_head)
            if not self.grow:
                self.segments.pop()
            self.grow = False
        self.draw()


# Modified from Chat GPT - create snake game and make snake a pygame sprite

class Food(Sprite):
    def __init__(self):
        super().__init__()
        self.x = round(random.randrange(0, WIDTH - TILESIZE) / 10.0) * 10.0
        self.y = round(random.randrange(0, HEIGHT - TILESIZE) / 10.0) * 10.0

    def draw(self):
        pg.draw.rect(self.game.screen, GREEN, [self.x, self.y, TILESIZE, TILESIZE])

    def relocate(self):
        self.x = round(random.randrange(0, WIDTH - TILESIZE) / 10.0) * 10.0
        self.y = round(random.randrange(0, HEIGHT - TILESIZE) / 10.0) * 10.0

class Player(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        # self.rect.x = x
        # self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 25
        self.vx, self.vy = 0, 0
        self.coins = 0
        self.health = 100
        self.dir = (0,0)
        self.cd = Cooldown()
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vy -= self.speed
        if keys[pg.K_a]:
            self.vx -= self.speed
        if keys[pg.K_s]:
            self.vy += self.speed
        if keys[pg.K_d]:
            self.vx += self.speed
        if keys[pg.K_LSHIFT]:
            self.get_dir()
            print(self.dir)
            self.dash()
    def get_dir(self):
        if abs(self.vx) > abs(self.vy):
            if self.vx > 0:
                self.dir = (1,0)
            elif self.vx < 0:
                self.dir = (-1,0)         
        elif abs(self.vy) > abs(self.vx):
            if self.vy > 0:
                self.dir = (0,1)
            elif self.vy < 0:
                self.dir = (0,-1)            
    def dash(self):
        self.cd.event_time = floor(pg.time.get_ticks()/1000)
        if self.cd.delta > .001:
            print('dashing')
            self.vx += self.dir[0]*500
            self.vy += self.dir[1]*500
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - TILESIZE
                    # self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - TILESIZE
                    # self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                print("i hit a powerup...")
                self.speed =+ 5
            if str(hits[0].__class__.__name__) == "Coin":
                print("i hit a coin...")
                self.coins += 1
    def update(self):
        self.cd.ticking()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        # reverse order to fix collision issues
        
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)

        self.rect.x = self.x
        self.collide_with_walls('x')
        
        self.rect.y = self.y
        self.collide_with_walls('y')


class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 10
        self.category = random.choice([0,1])
    def update(self):
     
        # moving towards the side of the screen
        self.rect.x += self.speed
        
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        # when it hits the side of the screen, it will move down
        if hits:
            # print("off the screen...")
            self.speed *= -1
            self.rect.y += 32
        if self.rect.right > WIDTH or self.rect.left < 0:
            # print("off the screen...")
            self.speed *= -1
            self.rect.y += 32
        # elif self.rect.colliderect(self.game.player):
        #     self.speed *= -1
        # elif self.rect.colliderect(self):
        #     self.speed *= -1

   
        # then it will move towards the other side of the screen
        # if it gets to the bottom, then it move to the top of the screen
        # (display logic in the terminal)

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


