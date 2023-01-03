from globals import *
from thing import *
from entity import *
from turtle import *
import pygame
from pygame.locals import *


class Player(Entity):
    '''
    A player is a thing that can react to keyboard events, like move and whatever.
    It has inventory, etc.
    '''
    def __init__(self, world, x, y):
        super().__init__(world, x, y, "@")

    def doKey(self, event):
        Move = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.dx,self.dy = face('E')
            elif event.key == pygame.K_LEFT:
                self.dx,self.dy = face('W')
            elif event.key == pygame.K_DOWN:
                self.dx,self.dy = face('S')
            elif event.key == pygame.K_UP:
                self.dx,self.dy = face('N')
            elif event.key == pygame.K_i:
                say('''You're inventory is
2 potions
3 arrows
''')
                return
            elif event.key == pygame.K_F10:
                say('''THINGS:''')
                for thing in self.world.sprites:
                    say(f"{thing.char} {thing.x:>3},{thing.y:>3}")
                for thing in self.world.things:
                    say(f"{thing.char} {thing.x:>3},{thing.y:>3}")
                return
            move = False
            thing = self.GetThingInFront()
            if not thing:
                move = True
            else:
                # Are we trying to step onto a door?
                if thing.char == "+":
                    # Yes.
                    move = True
                    # Then move another imaginary step and see what room that would be?
                    room = self.GetRoomInFront(2)
                    if not room:
                        self.x += self.dx
                        self.y += self.dy
                        turtle = Turtle(self.x, self.y, self.dx, self.dy)
                        turtle.down("#")
                        turtle.left()
                        turtle.move(5)
                        turtle.right()
                        turtle.move(10)
                        turtle.right()
                        turtle.move(10)
                        turtle.right()
                        turtle.move(10)
                        turtle.right()
                        turtle.move(4)

                        for (x,y,c) in turtle.stamps:
                            self.world.addThing(x,y,c)
                if thing.char == "#":
                    pass # Do nothing. Don't move.

            if move:
                self.x += self.dx
                self.y += self.dy
