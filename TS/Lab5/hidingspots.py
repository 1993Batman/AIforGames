'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path
from tkinter import Scale


class HidingSpots(object):


    def __init__(self, world=None):
        # keep a reference to the world object
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        # data for drawing this agent
        self.radius = 25

    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        egi.grey_pen()
        egi.circle(self.pos, self.radius)


        
        


   