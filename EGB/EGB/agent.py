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
from _operator import pos

AGENT_MODES = {
    KEY._1: 'neighbourhood',
}

class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal':0.5,
        'fast': 0.2
    }

    def __init__(self, world=None, scale=10.0, mass=1.5, mode='neighbourhood'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random start pos
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.accel = Vector2D() # current acceleration due to force
        self.mass = mass


        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-0.5,  0.25),
            Point2D( 0.5,  -0.3),
            Point2D(-0.5, -0.25)
        ]
        
        ### wander details
        self.wander_target = Vector2D(1,0)
        self.wander_dist =5.0 * scale
        self.wander_radius =3.0 * scale
        self.wander_jitter =1.0 * scale
        self.bRadius =scale
            

        # limits?
        self.max_speed = 20.0 * scale
        self.max_force = 500.0
        ## max_force ??
        self.tagged = False

        # debug draw info?
        self.show_info = False
        

    def calculate(self,delta):
        # calculate the current steering force
        mode = self.mode
        if self.tagged is False:
            self.neighbours(self.world.agents, self.world.radius)
        if mode == 'neighbourhood':
            force= self.wander(delta)
            force +=self.alignment(self.world.agents) * self.world.alignmnet
            force +=self.cohesion(self.world.agents) * self.world.cohesion
            force +=self.separation(self.world.agents) * self.world.seperation
        else:
            force = Vector2D()
        self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        # calculate and set self.force to be applied
        ## force = self.calculate()
        force = self.calculate(delta)  # <-- delta needed for wander
        ## limit force? <-- for wander
        # determin the new accelteration
        self.accel = force / self.mass  # not needed if mass = 1.0
        # new velocity
        self.vel += self.accel * delta
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)
        
    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        # draw the path if it exists and the mode is follow
        if self.mode == 'follow_path':
            ## ...
            self.path.render()
            pass

        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                        self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)


        
        if self.mode == 'neighbourhood':
            if self.tagged == True:
                self.color = 'BLUE'
            if self.tagged == False:
                self.color = 'ORANGE'
            pass

        # add some handy debug drawing info lines - force and velocity
        if self.show_info:
            s = 0.5 # <-- scaling factor
            # force
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            # velocity
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            # net (desired) change
            egi.white_pen()
            egi.line_with_arrow(self.pos+self.vel * s, self.pos+ (self.force+self.vel) * s, 5)
            egi.line_with_arrow(self.pos, self.pos+ (self.force+self.vel) * s, 5)

    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)



    def wander(self, delta):
        ''' Random wandering using a projected jitter circle. '''
        wt = self.wander_target
        # this behaviour is dependent on the update rate, so this line must
        # be included when using time independent framerate.
        #jitter_tts = self.wander_jitter * delta  this time slice
        jitter_tts  = self.wander_jitter * delta
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
    

    def neighbours(self,bots,radius):
        for bot in bots:
            # untag all first
            bot.tagged = False
            # get the vector between us
            to = self.pos - bot.pos
            # take into account the bounding radius
            gap = radius + bot.bRadius
            if to.length_sq() < gap**2:
                bot.tagged = True
    
    def separation(self,group):
        steering_force = Vector2D()
        for agent in group:
            if self != agent and self.tagged:
                toBot =self.pos - agent.pos         
                steering_force += Vector2D.normalise(toBot) / toBot.length()             
        return steering_force
    
    def alignment(self,group):
        avgHeading = Vector2D()
        avgCount = 0
        
        for agent in group:
            if self != agent and agent.tagged:
                avgHeading += agent.pos
                avgCount += 1
                
        if avgCount > 0:
            avgHeading /= float(avgCount)
            avgHeading -= self.heading
        return avgHeading
    
    def cohesion(self, group):
        centerMass = Vector2D()
        steeringForce = Vector2D()
        avgCount = 0
        
        for agent in group:
            if self != agent and self.tagged:
                centerMass += agent.pos
                avgCount += 1
                
        if avgCount > 0:
            centerMass /= float(avgCount)
            steeringForce = self.seek(centerMass)
        return steeringForce
        