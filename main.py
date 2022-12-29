import functools
import math
import random
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

rooms = []



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
    char = "#"
    walls = []
    for x in range(left, left + room_width):
        wall = Thing(x, top, char)
        world.add(wall)
        walls.append(wall)

        wall = Thing(x, top + room_height - 1, char)
        world.add(wall)
        walls.append(wall)
    for y in range(top + 1, top + room_height - 1):
        wall = Thing(left, y, char)
        world.add(wall)
        walls.append(wall)

        wall = Thing(left + room_width - 1, y, char)
        world.add(wall)
        walls.append(wall)

    # Add 1 to 4 doors
    doors = random.randint(1,4)
    while doors > 0:
        i = random.randint(0, len(walls)-1)
        wall = walls[i]
        if wall.char == "+": continue
        if wall.x == left: continue
        if wall.x == left + room_height: continue
        if wall.y == top: continue
        if wall.y == top + room_height: continue
        wall.char = "+"
        doors -= 1




# ================================================================================
def whatsAt(x, y):
    for thing in world:
        if thing.x == x and thing.y == y:
            return thing
    return None



# ================================================================================
def GetRoom(x, y):
    for room in rooms:
        if room.contains(x, y):
            return room
    return None



# ================================================================================
class Room:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def contains(self, x, y):
        return x >= self.left and x <= self.left + self.width and y >= self.top and y <= self.top + self.height




# ================================================================================
class Thing(pygame.sprite.Sprite):
    '''
    A thing is an ASCII character that has a position in the world.
    A position is (x,y) where x and y are integers (positive or negative with no bounds)
    It can be a player or a wall or potion or monster, etc.
    It has a position in the world.
    '''
    def __init__(self, x, y, char, color=white):
        super().__init__()
        self.w = SQUARE
        self.h = SQUARE
        self.x = x # Grid X
        self.y = y # Grid Y
        self.char = char
        self.surface = pygame.Surface((self.w, self.h))
        self.seen = False # Has this thing been seen before? Fog of war.

    def blit(self):
        # Calc the relative grid position with respect to the player
        rx = self.x - player.x
        ry = self.y - player.y

        # Calculate absolute position relative to the window where (0,0) is upper-left corner
        ax = rx * SQUARE + int(WIDTH/2)
        ay = ry * SQUARE + int(HEIGHT/2)

        inside = ax >= 0 and ax <= WIDTH and ay >= 0 and ay <= WIDTH
        if inside:
            self.rect = self.surface.get_rect(center=(ax, ay))
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
        The rule is that we can see that if it is in the same room as us
        or we have seen it before and it hasn't moved.
        '''
        assert(isinstance(that, Thing))
        return True

def say(s):
    print(s)
    sys.stdout.flush()


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
            elif event.key == pygame.K_i:
                say('''You're inventory is
2 potions
3 arrows
''')
            move = False
            thing = whatsAt(self.x + dx, self.y + dy)
            if not thing:
                Move = True
            else:
                if thing.char == "+":
                    # Take one imaginary step and see if you are in a room?
                    room = GetRoom(self.x + dx + dx, self.y + dy + dy)

            if Move:
                self.x += dx
                self.y += dy




# ================================================================================
player = Player(0, 0)

sprites = pygame.sprite.Group()
sprites.add(player)

world = pygame.sprite.Group()

# Draw a room around the player
room_width = 15
room_height = 7
top = player.y - int(room_height/2)
left = player.x - int(room_width/2)
makeRoomRectangle(left, top, room_width, room_height)
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
