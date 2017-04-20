from graphics import egi
from math import sqrt
class Entity(object): 
    def __init__(self,src, dest,world= None):
        self.src = src
        self.world = world
        self.dest = dest
        self.total_trip_length= 0
        self.progress = 0
        self.turns_remaining = 0
        self.agent = egi.cross(src,15)
        egi.set_pen_color(name = 'BLACK')

    def calculate_trip(self):
        self.total_trip_length = self.distance_to(self.dest)
        if self.total_trip_length == 0:
            return 0;
        self.turns_remaining = self.total_trip_length - self.progress
        return self.turns_remaining

    def update_next_dest(self,dest):
        self.src = self.dest
        self.dest = dest

    def distance_to(self, other):
        dx = self.src.x - other.x
        dy = self.src.y - other.y
        return sqrt(dx * dx + dy * dy)

    def update(self):
        ''' Move the fleet (progress) by one game time step.'''
        self.turns_remaining -= 1
        # update position and progress
        src = self.src
        dest = self.dest
        scale = 1 - (float(self.turns_remaining) / float(self.total_trip_length))
        self.x = src.x + (dest.x - src.x) * scale
        self.y = src.y + (dest.y - src.y) * scale
        self.progress = self.total_trip_length - self.turns_remaining

