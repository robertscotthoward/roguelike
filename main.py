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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((20, 20))
        self.surface.fill((255,0,0))
        self.rect = self.surface.get_rect(center = (100, 220))

player = Player()

sprites = pygame.sprite.Group()
sprites.add(player)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255,255,255))

    for sprite in sprites:
        screen.blit(sprite.surface, sprite.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)