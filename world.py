import random
import pygame
import sys
from tools import *
from pygame.locals import *
from thing import Thing
from player import Player
from globals import *

class World():
    def __init__(self):
        pygame.init()
        self.player = Player(self, 0, 0)

        # Fixtures: things that don't move, like walls.
        self.things = pygame.sprite.Group()

        # Actors: things that move
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.player)

        # ================================================================================
        # A SQUARE is the size of a square on game board.
        # Fonts typically come in 16x16 or 32x32
        # SQUARE = 32
        # font = pygame.font.Font('freesansbold.ttf', SQUARE)

        self.font = pygame.font.Font('arial.ttf', SQUARE)

        self.FramePerSec = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rogue-like Game")

        self.window = (0, 0, 0, 0)
        self.rooms = []

        # ================================================================================
        # KEYBOARD REPEAT:
        # https://www.pygame.org/docs/ref/key.html#pygame.key.set_repeat
        # You can play with the keyboard repeat by uncommenting the following line:
        # pygame.key.set_repeat(50, 50)


    def Run(self):
        # ================================================================================
        # GAME EVENT LOOP:
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                self.player.doKey(event)

            self.screen.fill(black)

            for thing in self.sprites:
                thing.update()
            for thing in self.things:
                thing.update()

            pygame.display.update()
            self.FramePerSec.tick(FPS)



    def calcWindow(self):
        '''
        Calculate the relative left, top, right, and bottom of the window
        relative to the player so that we can quickly determine if a sprite
        might be visible on the screen or not.
        '''
        left = self.player.x
        top = self.player.x
        right = self.player.x
        bottom = self.player.x
        self.window = (left, top, right, bottom)

    def addThing(self, x, y, char):
        thing = Thing(self, x, y, char)
        self.things.add(thing)
        return thing

    def makeRoomRectangle(self, left, top, width, height):
        char = "#"
        walls = []
        for x in range(left, left + width):
            wall = Thing(self, x, top, char)
            self.things.add(wall)
            walls.append(wall)

            wall = Thing(self, x, top + height - 1, char)
            self.things.add(wall)
            walls.append(wall)
        for y in range(top + 1, top + height - 1):
            wall = Thing(self, left, y, char)
            self.things.add(wall)
            walls.append(wall)

            wall = Thing(self, left + width - 1, y, char)
            self.things.add(wall)
            walls.append(wall)

        # Add 1 to 4 doors
        doors = random.randint(1,4)
        while doors > 0:
            i = random.randint(0, len(walls)-1)
            wall = walls[i]
            if wall.char == "+": continue
            if wall.x == left: continue
            if wall.x == left + height: continue
            if wall.y == top: continue
            if wall.y == top + height: continue
            wall.char = "+"
            doors -= 1

    def whatsAt(self, x, y):
        for thing in self.things:
            if thing.x == x and thing.y == y:
                return thing
        for thing in self.sprites:
            if thing.x == x and thing.y == y:
                return thing
        return None


    def GetRoom(self, x, y):
        for room in self.rooms:
            if room.contains(x, y):
                return room
        return None
