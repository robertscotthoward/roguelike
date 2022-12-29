import sys
import pygame
from pygame.locals import *

pygame.init()

WIDTH = 800
HEIGHT = 640
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rogue-like Game")
font = pygame.font.Font('freesansbold.ttf', 32)

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.w = 20
        self.h = 20
        self.x = x
        self.y = y
        self.char = "@"
        self.surface = pygame.Surface((self.w, self.h))
        #self.surface.fill((255,0,0))

    def blit(self):
        px = self.x * self.w
        py = self.y * self.h
        self.rect = self.surface.get_rect(center = (px, py))
        text = font.render(sprite.char, True, (0,255,0), (0,0,255))
        screen.blit(text, self.rect)


class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y)

player = Player(3,6)
player1 = Player(6,3)

sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(player1)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255,255,255))

    for sprite in sprites:
        sprite.blit()

    pygame.display.update()
    FramePerSec.tick(FPS)