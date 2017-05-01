from graphics import egi
from math import sqrt
class Entity(object): 
    def __init__(self,boxes,path):
        self.boxes = boxes
        self.path = path
        self.src = self.boxes[path[0]]._vc
        self.dest = self.boxes[path[1]]._vc
        self.total_trip_length= 0
        self.progress = 0
        self.turns_remaining = 0
        self.calculate_trip()
        self.end = False

    def calculate_trip(self):
        self.total_trip_length = self.distance_to(self.dest)
        self.turns_remaining = self.total_trip_length - self.progress
        return self.turns_remaining

    def update_next_dest(self):
        self.src = self.dest
        for i in range(0 ,len(self.path)):
            print(i)
            if self.distance_to(self.boxes[self.path[len(self.path)-1]]._vc) < 0.5:
                self.end = True
                print(self.end)
                break

            if self.dest is self.boxes[self.path[i]]._vc:
                self.dest = self.boxes[self.path[i + 1]]._vc
                break


    def distance_to(self, other):
        dx = self.src.x - other.x
        dy = self.src.y - other.y
        return sqrt(dx * dx + dy * dy)

    def update(self):
        self.turns_remaining -= 1
        src = self.src
        dest = self.dest
        scale = 1 - (float(self.turns_remaining) / float(self.total_trip_length))
        src.x = src.x + (dest.x - src.x) * scale
        src.y = src.y + (dest.y - src.y) * scale
        self.progress = self.total_trip_length - self.turns_remaining
        print(src)
        print(self.dest)
        print(self.distance_to(self.dest))
        if self.distance_to(self.dest) < 0.5:
            self.update_next_dest()
            print("i got here")