from random import choice
class AttackMaxPlanetOnly(object):
    def update(self, gameinfo):
        if gameinfo.my_fleets:
            return
        if gameinfo.my_planets:
            dest = min(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            src = choice(list(gameinfo.my_planets.values()))
            if src.num_ships < 30:
                gameinfo.planet_order(src, dest, int(src.num_ships *0.50))
        if gameinfo.my_planets and gameinfo.not_my_planets:
            dest = max(gameinfo.not_my_planets.values(), key = lambda p: p.num_ships)
            src = choice(list(gameinfo.my_planets.values()))
            
            if src.num_ships > 10:
                gameinfo.planet_order(src, dest, int(src.num_ships *0.75))