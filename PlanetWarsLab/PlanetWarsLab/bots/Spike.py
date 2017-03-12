from random import choice
from entities import Entity

class Spike(object):
    def update(self, gameinfo):
        entity = Entity
        if gameinfo.my_fleets:
            return
        
        if gameinfo.my_planets:
            dest = min(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            src = max(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            if src.num_ships >  50 and entity.distance_to(src,dest) > 0 and dest.num_ships < 50:
                gameinfo.planet_order(src, dest, int(src.num_ships *0.50))
                
        if gameinfo.my_planets and gameinfo.not_my_planets:
            dest = min(gameinfo.not_my_planets.values(), key = lambda p: p.num_ships)
            src = choice(list(gameinfo.my_planets.values()))
            
            if src.num_ships > 30:
                gameinfo.planet_order(src, dest, int(src.num_ships *0.75))