# This file was created by: Chris Cozort (PER 3)

# IMPORT ALL NECESSARY MODULES AND LIBRARIES
import pygame as pg
from settings import *
from sprites import *
from random import randint


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
    # create player block, creates the all_sprites group so that we can batch update and render, defines properties that can be seen in the game system
    # 
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self, 1, 1)
        # instantiated a mob
        self.mob = Mob(self, 100,100)
        # makes new mobs and walls using a for loop
        for i in range(randint(10,20)):
            m = Mob(self, i*randint(0, 200), i*randint(0, 200))
            Wall(self, i*TILESIZE, i*TILESIZE)
    # using self.running as a boolean to continue running the game
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        # input
    # Looks for any events, and this specifically looks for closing the game with 'x'
    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

        # pg.quit()
        # process
    def update(self):
        self.all_sprites.update()
        # output
        print(self.player.rect.colliderect(self.mob))
        pass
    # 
    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

# checks file name and creates a game object
if __name__ == "__main__":
    g = Game()
    # create all game elements with the new method (not function)
    g.new()
    # run the game...
    g.run()

        