from globals import *
from thing import *
from turtle import *
import pygame
from pygame.locals import *


class Entity(Thing):
    '''
    An entity is a thing that can move, have state (HP, AC), and hold things (inventory).
    '''
    def __init__(self, world, x, y, char):
        super().__init__(world, x, y, char)
        self.inventory = {}

    def addItem(self, name):
        '''Add a named-item to the inventory. If it already exists, then increment its count.'''
        n = 0
        if name in self.inventory:
            n = self.inventory[name]
        self.inventory[name] += 1
