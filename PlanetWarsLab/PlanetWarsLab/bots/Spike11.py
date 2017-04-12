from random import choice
from entities import Entity, Fleet
class Spike11(object):
    def update(self, gameinfo):
        
        if gameinfo.my_fleets:
            for src in gameinfo.my_fleets.items():
                for k in src:
                    if type(k) is Fleet:
                        print("fleets attack here")
                        result = k.in_range(gameinfo.not_my_planets)
                        if result.count > 0:       
                            for dest in result:
                                if int(k.num_ships) > int(dest.num_ships):
                                    gameinfo.fleet_order(k,dest, int(k.num_ships))
            return
            

        
                             
        if gameinfo.my_planets and gameinfo.not_my_planets:
            dest = min(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            src = max(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            if src.num_ships >  50 and Entity.distance_to(src,dest) > 0 and dest.num_ships < 35:
                gameinfo.planet_order(src, dest, int(src.num_ships *0.30))

            else:
                dest = max(gameinfo.not_my_planets.values(), key = lambda p: p.growth_rate)
                src = max(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            
                if src.num_ships > 30:
                    gameinfo.planet_order(src, dest, int(src.num_ships *0.75))