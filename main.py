import sys
import pygame
from pygame.locals import *

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

# https://www.pygame.org/docs/ref/key.html#pygame.key.set_repeat
pygame.key.set_repeat(delay=50, interval=100)
font = pygame.font.Font('freesansbold.ttf', 32)


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.w = 32
        self.h = 32
        self.x = x
        self.y = y
        self.char = "@"
        self.surface = pygame.Surface((self.w, self.h))
        # self.surface.fill((255,0,0))

    def blit(self):
        px = self.x * self.w
        py = self.y * self.h
        self.rect = self.surface.get_rect(center=(px, py))
        text = font.render(sprite.char, True, white, black)
        screen.blit(text, self.rect)

    def doKey(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.x += 1
            elif event.key == pygame.K_LEFT:
                self.x -= 1
            if event.key == pygame.K_DOWN:
                self.y += 1
            elif event.key == pygame.K_UP:
                self.y -= 1

class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y)


player = Player(3, 6)
player1 = Player(6, 3)

sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(player1)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        player.doKey(event)

    screen.fill(black)

    for sprite in sprites:
        sprite.blit()

    pygame.display.update()
    FramePerSec.tick(FPS)
