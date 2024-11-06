# This file was created by: Chris Cozort (PER 3)

# IMPORT ALL NECESSARY MODULES AND LIBRARIES
import pygame as pg
from settings import *
# from sprites_sidescroller import *
from sprites import *
from tilemap import *
from os import path
import sys
from random import randint
'''
GOALS: Eat all the enemies
RULES: You have to get a powerup to eat enemies
FEEDBACK: If you collide with an enemy before eating a powerup you die
FREEDOM: Move around inside the game space

What sentence does your game make? 

When the player collides with an enemy the enemy bounces off

'''

'''
Sources:


'''



# created a game class to instantiate later
# it will have all the necessary parts to run the game
# the game class is created to organize the elements needed to create a gam
class Game:
    # The game init method initializes all the necessary components for the game, including video and sound
    # this includes the game clock which allows us to set the framerate
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Chris' Game")
        self.clock = pg.time.Clock()
        self.running = True
        self.create_pillars = True
    # create player block, creates the all_sprites group so that we can batch update and render, defines properties that can be seen in the game system
    #
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images' )
        self.map = Map(path.join(self.game_folder, 'level1.txt'))
        self.player_img = pg.image.load(path.join(self.img_folder, "bell.png"))
        self.ladder_img = pg.image.load(path.join(self.img_folder, "ladder.png"))
        self.ladder_img = pg.image.load(path.join(self.img_folder, "ladder.png"))
    def new(self):
        self.load_data()
        print(self.map.data)
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_pillars = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_ladders = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()
        # self.player = Player(self, 1, 1)
        # instantiated a mob
        # self.mob = Mob(self, 100,100)
        # makes new mobs and walls using a for loop a
        # for i in range(randint(10,20)):
        #     m = Mob(self, i*randint(0, 200), i*randint(0, 200))
        #     Wall(self, i*TILESIZE, i*TILESIZE)
        

        # takes map.data and parses it using enumerate so that we can assign x and y values to 
        # object instances.
        # p = Pillar(self, 1, 5, 1, 4)
        for row, tiles in enumerate(self.map.data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'U':
                    Powerup(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                # if tile == 'L':
                #     Ladder(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
    
    # using self.running as a boolean to continue running the game
    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        # input
    def quit(self):
        pg.quit()
        sys.exit()
    # Looks for any events, and this specifically looks for closing the game with 'x'
    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

        # pg.quit()
        # process
    # def pillargenerator(self):
    #     Pillar(self, 1, 1)
    def update(self):
        self.all_sprites.update()
        if self.player.health <= 0:
            self.running = False

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(pg.time.get_ticks()), 24, WHITE, WIDTH/30, HEIGHT/30)
        self.draw_text(self.screen, "Coins collected: " + str(self.player.coins), 24, BLACK, WIDTH/2, HEIGHT/24)
        pg.display.flip()
    def show_death_screen(self):
        self.screen.fill(RED)
        self.draw_text(self.screen, "Wasted!", 42, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False



# checks file name and creates a game object
if __name__ == "__main__":
    g = Game()
    # create all game elements with the new method (not function)
    g.new()
    # run the game...
    g.run()
    g.show_death_screen()

        