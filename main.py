import functools
import math
import sys
import pygame
from pygame.locals import *

# sign(x) returns:
#   -1 if x < 0
#    0 if x = 0
#    1 if x > 0
sign = functools.partial(math.copysign, 1)

pygame.init()

WIDTH = 800
HEIGHT = 640
ACC = 0.5
FRIC = -0.12
FPS = 60
white = (255, 255, 255)
black = (0, 0, 0)

FramePerSec = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rogue-like Game")




# ================================================================================
# KEYBOARD REPEAT:
# https://www.pygame.org/docs/ref/key.html#pygame.key.set_repeat
# pygame.key.set_repeat(50, 50)




# ================================================================================
# A SQUARE is the size of a square on game board.
# Fonts typically come in 16x16 or 32x32

# SQUARE = 32
# font = pygame.font.Font('freesansbold.ttf', SQUARE)

SQUARE = 16
font = pygame.font.Font('arial.ttf', SQUARE)


window = (0, 0, 0, 0)
def calcWindow():
    '''
    Calculate the relative left, top, right, and bottom of the window
    relative to the player so that we can quickly determine if a sprite
    might be visible on the screen or not.
    '''
    left = player.x
    top = player.x
    right = player.x
    bottom = player.x
    window = (left, top, right, bottom)



# ================================================================================
def makeRoomRectangle(left, top, width, height):
    for x in range(left, left + wall_width):
        wall = Thing(x, top, "#")
        world.add(wall)
        wall = Thing(x, top + wall_height - 1, "#")
        world.add(wall)
    for y in range(top + 1, top + wall_height - 1):
        wall = Thing(left, y, "#")
        world.add(wall)
        wall = Thing(left + wall_width - 1, y, "#")
        world.add(wall)

def whatsAt(x, y):
    for thing in world:
        if thing.x == x and thing.y == y:
            return thing
    return None



# ================================================================================
class Thing(pygame.sprite.Sprite):
    '''
    A thing is an ASCII character that has a position in the world.
    It can be a player or a wall or potion or monster, etc.
    It has a position in the world.
    '''
    def __init__(self, x, y, char, color=white):
        super().__init__()
        self.w = SQUARE
        self.h = SQUARE
        self.x = x
        self.y = y
        self.char = char
        self.surface = pygame.Surface((self.w, self.h))
        self.seen = False # Has this thing been seen before? Fog of war.

    def blit(self):
        px = self.x * self.w
        py = self.y * self.h
        self.rect = self.surface.get_rect(center=(px, py))
        text = font.render(sprite.char, True, white, black)
        screen.blit(text, self.rect)

    def update(self):
        if self.seen or self.canSee(player):
            self.blit()

    def insideWindow(self):
        '''Return true only if the sprite is in the window.'''
        return self.x >= window[0] and self.x <= window[2] and self.y >= window[1] and self.y <= window[3]

    def canSee(self, that):
        '''
        Can this thing see that thing? Nothing in between?
        @that is the Thing that might be able to see this.
        '''
        assert(isinstance(that, Thing))
        this = self
        if this.x == that.x and this.y == that.y:
            return True

        if this.x == that.x:
            dx = 0
            dy = sign(that.y - this.y)
        elif this.y == that.y:
            dx = sign(that.x - this.x)
            dy = 0
        else:
            dx = (that.x - this.x) / (that.y - this.y)
            dy = 1 / dx

        x = this.x
        y = this.y

        i = 0
        while abs(x - that.x) > 1 or abs(y - that.y):
            # Round down
            nx = int(round(x + dx, 0))
            ny = int(round(y + dy, 0))

            # If there is something there, try looking around it.
            if whatsAt(nx, ny):
                # Round up.
                nx = int(round(x + dx + 0.5, 0))
                ny = int(round(y + dy + 0.5, 0))

                # If there is something there, then we are blocked and cannot see that.
                if whatsAt(nx, ny):
                    return False
            x += dx
            y += dy
            i += 1
            if i > 1000:
                return False

        # We can see it!
        return True




class Player(Thing):
    '''
    A player is a thing that can react to keyboard events, like move and whatever.
    It has inventory, etc.
    '''
    def __init__(self, x, y):
        super().__init__(x, y, "@")
        self.inventory = {}
        self.seen = True # We can see ourself

    def addItem(self, name):
        '''Add a named-item to the inventory. If it already exists, then increment its count.'''
        n = 0
        if name in self.inventory:
            n = self.inventory[name]
        self.inventory[name] += 1

    def doKey(self, event):
        if event.type == pygame.KEYDOWN:
            dx = 0
            dy = 0
            if event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_LEFT:
                dx = -1
            if event.key == pygame.K_DOWN:
                dy = 1
            elif event.key == pygame.K_UP:
                dy = -1
            thing = whatsAt(self.x + dx, self.y + dy)
            if not thing:
                self.x += dx
                self.y += dy




# ================================================================================
player = Player(20, 20)

sprites = pygame.sprite.Group()
sprites.add(player)

world = pygame.sprite.Group()

# Draw a room around the player
wall_width = 5
wall_height = 5
top = player.y - int(wall_height/2)
left = player.x - int(wall_width/2)
makeRoomRectangle(left, top, wall_width, wall_height)
calcWindow()


# ================================================================================
# GAME EVENT LOOP:
while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        player.doKey(event)

    screen.fill(black)

    for sprite in sprites:
        sprite.update()
    for sprite in world:
        sprite.update()

    pygame.display.update()
    FramePerSec.tick(FPS)
