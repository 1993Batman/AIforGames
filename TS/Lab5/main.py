'''Autonomous Agent Movement: Seek, Arrive and Flee

Created for COS30002 AI for Games, Lab 05
By Clinton Woodward cwoodward@swin.edu.au

'''

from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from agent import Agent, AGENT_MODES  # Agent with seek, arrive, flee and pursuit
from hunter import Hunter, AGENT_MODES  # Agent with seek, arrive, flee and pursuit
from hidingspots import HidingSpots

def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # left
        world.target = Vector2D(x, y)


def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol in AGENT_MODES:
        for agent in world.agents:
            agent.mode = AGENT_MODES[symbol]
        for hunter in world.hunter:
            hunter.mode = AGENT_MODES[symbol]
    elif symbol == KEY.A:
        world.agents.append(Agent(world))
    elif symbol == KEY.U:
        for hunter in world.hunter:
            hunter.radius +=10
    elif symbol == KEY.I:
        for hunter in world.hunter:
            hunter.radius -=10
    elif symbol == KEY.F:
        world.spots.append(HidingSpots(world))



def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy


if __name__ == '__main__':
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()      
    screen = display.get_default_screen()
    screen_width = screen.width
    screen_height = screen.height
    # create a pyglet window and set glOptions
    win = window.Window(width=screen_width, height=screen_height, vsync=True, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = clock.ClockDisplay()
    # register key and mouse event handlers
    win.push_handlers(on_key_press)
    win.push_handlers(on_mouse_press)
    win.push_handlers(on_resize)

    # create a world for agents
    world = World(screen_width,screen_height)
    # add one agent
    world.agents.append(Agent(world))
    world.hunter.append(Hunter(world))
    #world.hunter.append(Hunter(world))
    i = 0
    while i < 5:
        world.spots.append(HidingSpots(world))
        i+=1

    
    # unpause the world ready for movement
    world.paused = False

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default)
        delta = clock.tick()
        world.update(delta)
        world.render()
        fps_display.draw()
        for ag in world.agents:
            if ag.tagged is True:
                world.agents.remove(ag)
                world.agents.append(Agent(world))
            if world.hunter[0].mode is "seek":
                ag.mode = "seek"
            else:
                ag.mode = "hide"
        # swap the double buffer
        win.flip()


