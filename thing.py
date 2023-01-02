import pygame
from globals import *
from pygame.locals import *

class Thing(pygame.sprite.Sprite):
    '''
    A thing is an ASCII character that has a position in the world
    and is pointing in one of the five directions: (0,1), (1,0), (0,-1), (-1,0), (0,0)
    where (0,0) means that it cannot move; e.g. a wall.
    A position is (x,y) where x and y are integers (positive or negative with no bounds)
    It can be a player or a wall or potion or monster, etc.
    '''
    def __init__(self, world, x, y, char, color=white):
        super().__init__()
        self.world = world
        self.x = x # Grid X
        self.y = y # Grid Y
        self.char = char
        self.color = color
        self.seen = False
        self.w = SQUARE
        self.h = SQUARE
        self.dx = 0
        self.dy = 0
        self.char = char
        self.surface = pygame.Surface((self.w, self.h))
        self.seen = False # Has this thing been seen before? Fog of war.

    def setColor(self, color):
        self.color = color

    def GetThingInFront(self, steps=1):
        '''
        Given the direction we are facing, take n steps and return what is there, if anything.
        '''
        thing = self.world.whatsAt(self.x + self.dx*steps, self.y + self.dy*steps)

    def GetRoomInFront(self, steps=1):
        '''
        Given the direction we are facing, take n steps and look to see what room we are in.
        Return None if no room exists at that point.
        '''
        thing = self.world.GetRoom(self.x + self.dx*steps, self.y + self.dy*steps)

    def blit(self):
        # Calc the relative grid position with respect to the player
        rx = self.x - self.world.player.x
        ry = self.y - self.world.player.y

        # Calculate absolute position relative to the window where (0,0) is upper-left corner
        ax = rx * SQUARE + int(WIDTH/2)
        ay = ry * SQUARE + int(HEIGHT/2)

        inside = ax >= 0 and ax <= WIDTH and ay >= 0 and ay <= WIDTH
        if inside:
            self.rect = self.surface.get_rect(center=(ax, ay))
            text = self.world.font.render(self.char, True, white, black)
            self.world.screen.blit(text, self.rect)

    def update(self):
        if self.seen or self.canSee(self.world.player):
            self.blit()

    def insideWindow(self, window):
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