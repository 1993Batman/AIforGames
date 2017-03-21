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
from hunter import Hunter
from hidingspots import HidingSpots

AGENT_MODES = {
    KEY._1: 'seek',
    KEY._6: 'hide'
}


class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal':0.5,
        'fast': 0.2
        ### ADD 'normal' and 'fast' speeds here
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='seek'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        self.tagged = False
        # where am i and where am i going? random
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.acceleration = Vector2D()  # current steering force
        self.mass = mass
        # limits?
        self.max_speed = 1000.0
        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]
        
        ### wander details
        self.wander_target = Vector2D(1,0)
        self.wander_dist =1.0 * scale
        self.wander_radius =1.0 * scale
        self.wander_jitter =10.0 * scale
        self.bRadius =scale
        self.BestHidingSpot = None
            

        # limits?
        self.max_speed = 20.0 * scale
        self.max_force = 500.0
        ## max_force ??



    def calculate(self, delta):
        # reset the steering force
        mode = self.mode
        if mode == 'seek':
            force = self.seek(self.world.target)
            self.BestHidingSpot = None
        elif mode == 'hide':
            force = self.Hide(self.world.hunter,self.world.spots, delta)
        else:
            force = Vector2D()
        self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        force = self.calculate(delta)
        # new velocity
        self.vel += force * delta
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.lengthSq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)

    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        if self.BestHidingSpot is not None:
            egi.white_pen()
            egi.cross(Vector2D(self.BestHidingSpot.x,self.BestHidingSpot.y), 5)

        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                        self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)


    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos, speed, pursuit_speed):
        ''' move away from hunter position '''
## add panic distance (second)
## add flee calculations (first)
        decel_rate = self.DECELERATION_SPEEDS[speed]
        flee_target = self.pos - hunter_pos
        dist = flee_target.length()
        if dist > 15:
            if AGENT_MODES is 'flee':
                speed = dist / decel_rate
                speed = min(speed, self.max_speed)
                desired_vel = flee_target * (speed / dist)
                return (desired_vel - self.vel)
            else:
                pursuit_speed = dist / decel_rate
                pursuit_speed = min(pursuit_speed, self.max_speed)
                desired_vel = flee_target * (pursuit_speed / dist)
                return (desired_vel - self.vel)
        return Vector2D()

    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def wander(self, delta):
        ''' Random wandering using a projected jitter circle. '''
        wt = self.wander_target
        # this behaviour is dependent on the update rate, so this line must
        # be included when using time independent framerate.
        jitter_tts = self.wander_jitter * delta # this time slice
        # first, add a small random vector to the target's position
        wt += Vector2D(uniform(-1,1) * jitter_tts, uniform(-1,1) * jitter_tts)
        # re-project this new vector back on to a unit circle
        wt.normalise()
        # increase the length of the vector to the same as the radius
        # of the wander circle
        wt *= self.wander_radius
        # move the target into a position WanderDist in front of the agent
        target = wt + Vector2D(self.wander_dist, 0)
        # project the target into world space
        wld_target = self.world.transform_point(target, self.pos, self.heading, self.side)
        # and steer towards it
        return self.seek(wld_target) 

    def pursuit(self, pursuer, delta):
        pursuer = self.world.hunter[0]
                # flee from the estimated future position
        toPursuer = pursuer.pos - self.pos
        if (toPursuer.length() - pursuer.radius)< -50:
            # proportional to distance, inversely proportional to sum of velocities
            lookAheadTime = toPursuer.length() / (self.max_speed
            + pursuer.speed())
            # go in the opposite predicted position
        
            return self.flee(pursuer.pos, 'fast',(pursuer.vel * lookAheadTime))        

        return self.wander(delta)
    
    def GetHidingPosition(self, hunter, obj):
        # set the distance between the object and the hiding point
        DistFromBoundary = 30.0 # system setting
        DistAway = obj.radius + DistFromBoundary
        # get the normal vector from the hunter to the hiding point
        ToObj = Vector2D.get_normalised(obj.pos - hunter.pos)
        # scale size past the object to the hiding location
        return (ToObj*DistAway)+obj.pos 
        
    def Hide(self,hunter,objs, delta):
        DistToClosest = 1000000
        
        self.BestHidingSpot = None
        for hun in hunter:
        # check for possible hiding spots
            for obj in objs:
                HidingSpot = self.GetHidingPosition(hun,obj)
                HidingDist = Vector2D.distanceSq(HidingSpot,self.pos)
                if HidingDist < DistToClosest and (Vector2D.length(hun.pos - obj.pos) - hun.radius) > 0:
                    DistToClosest = HidingDist
                    self.BestHidingSpot = HidingSpot
        # if we have a best hiding spot, use it

        if self.BestHidingSpot is not None:
            return self.arrive(self.BestHidingSpot, 'fast') # speed = fast?
        # default - run away!
        return self.pursuit(hunter, delta) 


   