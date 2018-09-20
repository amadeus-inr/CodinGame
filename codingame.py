import sys
import math
import numpy

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.



# CONSTANTS

## KEYS
ID = "ID"
X = "X"
Y = "Y"
SHIELD = "SHIELD"
IS_CONTROLLED = "IS_CONTROLLED"
HEALTH = "HEALTH"
VX = "VX"
VY = "VY"
NEAR_BASE = "NEAR_BASE"
THREAT = "THREAT"
BASE_DISTANCE = "BASE_DISTANCE"
NO_THREAT = 0
IS_THREAT = 1
FRIEND = 2

## ENTITY

MONSTER = 0
HERO = 1
ENEMY = 2


def distance( A, B):

    return numpy.linalg.norm(numpy.array(A) - numpy.array(B))


def get_entities():
    entities = {MONSTER: [], HERO: [], ENEMY: []}
    entity_count = int(input())
    for i in range(entity_count):
        id, type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in
                                                                                             input().split()]
        base_distance = distance(base_position, (x, y))

        entities[type].append({
            ID: id,
            X: x,
            Y: y,
            SHIELD: shield_life,
            IS_CONTROLLED: is_controlled,
            HEALTH: health,
            VX: vx,
            VY: vy,
            NEAR_BASE: near_base,
            THREAT: threat_for,
            BASE_DISTANCE: base_distance
        })



    return entities


def choose_monster(monsters):
    if not monsters:
        return {}
    threat = sorted(monsters, key = lambda x: x[BASE_DISTANCE], reverse=True)

    return threat[0] if threat else {}

def get_monsters(entities):
    monsters  = entities[MONSTER]
    return [m for m in monsters if m[THREAT] == IS_THREAT]

def get_options(entity):
    return get_points_on_circumference(entity[X],entity[Y])

VIEW_DISTANCE = 2200


def potential_monster_to_target(entities, hero_position):
    monsters = get_monsters(entities)
    return filter(lambda a: a[1] <= 800*2, {monster: distance(hero_position, (monster[X], monster[Y])) for monster in monsters})


def compute_value(option,solution, base_penalty = 0):
    cost = 0
    for hero in solution:
        hero_distance = distance(hero, option)

        cost = cost + max(0,2 * VIEW_DISTANCE - hero_distance)

    return - base_penalty * distance(option,base_position) + cost

def get_points_on_circumference(x, y, number_of_points=3, r=800):
    angle = 2 * math.pi / number_of_points
    return filter(lambda a: a[0] >= 0 and a[1] >= 0,
                  [(int(x + r * math.cos(angle * i)), int(y + r * math.sin(angle * i))) for i in range(number_of_points)])

if __name__=="__main__":
    base_x, base_y = [int(i) for i in input().split()]
    base_position = (base_x, base_y)
    heroes_per_player = int(input())
    # game loop
    while True:
        for i in range(2):
            health, mana = [int(j) for j in input().split()]

        entities = get_entities()
        enemy = {}
        monsters = get_monsters(entities)
        for monster in monsters:
            print("I see: %s %s" % (monster[ID], str(monster[BASE_DISTANCE])), file=sys.stderr)
        enemy = choose_monster(monsters)
        solution = []
        for i in range(heroes_per_player):

            print("Hero %s chooses an action" % entities[HERO][i][ID], file=sys.stderr)
            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr)


            # Get options
            options = get_options(entities[HERO][i])

            # Compute value

            ## Minimizing cost

            options = sorted(options,key = lambda o:compute_value(o,solution))

            for option in options:

                print("Evaluating option %s %s" % (str(option),compute_value(option,solution)), file=sys.stderr)



            option = options[0]

            print("Choosing option %s " % (str(option)), file=sys.stderr)

            # Update solution

            solution.append(option)

            if option:
                print("Move to option %s %s" % option, file=sys.stderr)
                print("MOVE %s %s" % option)
            else:
                print("WAIT")
