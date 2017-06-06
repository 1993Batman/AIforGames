from random import choice
from entities import Entity
class Spike11(object):
    def __init__(self):
        self.orders_list = []  # as allocated by the game
   
    def update(self, gameinfo):
        if gameinfo.my_fleets:
            src = gameinfo.my_fleets.values()
            dest = gameinfo.not_my_planets.values()
            for f in src:
                for p in dest:
                    if Entity.distance_to(f,p) < f.vision_range() and int(f.num_ships) > int(p.num_ships) and int(f.dest.num_ships) > int(p.num_ships):
                        gameinfo.fleet_order(f,p,f.num_ships)
                        break
            return
           
                             
        if gameinfo.my_planets and gameinfo.not_my_planets:
            dest = min(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            src = max(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            if src.num_ships >  50 and Entity.distance_to(src,dest) > 0 and dest.num_ships < 35:
                gameinfo.planet_order(src, dest, int(src.num_ships *0.30))

            else:
                dest = max(gameinfo.not_my_planets.values(), key = lambda p: p.growth_rate)
                src = max(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
                if len(self.orders_list) > 0:
                    count = 0
                    for i in self.orders_list:
                        if dest.id is self.orders_list[len(self.orders_list)-1].id and dest.id is not src.id:
                            count +=1
                        if count is 2:
                            if len(gameinfo.neutral_planets) > 0:
                                dest = max(gameinfo.neutral_planets.values(), key = lambda p: p.growth_rate)
                            else:
                                dest = min(gameinfo.not_my_planets.values(), key = lambda p: p.num_ships)
                            self.orders_list.clear()
                            break
                        if i is 2:
                            break
                if src.num_ships > 30:
                    gameinfo.planet_order(src, dest, int(src.num_ships *0.75))
                    self.orders_list.append(dest)
                