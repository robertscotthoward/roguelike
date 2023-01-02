from player import Player
from thing import Thing
from world import World
import pygame
from pygame.locals import *
from globals import *




world = World()

# Draw a room around the player
room_width = 15
room_height = 7
top = world.player.y - int(room_height/2)
left = world.player.x - int(room_width/2)
world.makeRoomRectangle(left, top, room_width, room_height)


world.Run()