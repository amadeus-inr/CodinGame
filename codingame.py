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

def object_distance( A, B):

    return distance ((A[X],A[Y]),(B[X],B[Y]))

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
    threat = sorted(monsters, key = lambda x: x[BASE_DISTANCE])

    return threat[0] if threat else {}

def get_monsters(entities):
    monsters  = entities[MONSTER]
    return [m for m in monsters if m[THREAT] == IS_THREAT]

def get_options(entity):
    return get_points_on_circumference(entity[X],entity[Y])

VIEW_DISTANCE = 2200


def potential_monster_to_target(entities, hero):
    hero_position = (hero[X],hero[Y])
    monsters = get_monsters(entities)

    close_monsters = filter(lambda a: distance(hero_position, (a[X], a[Y])) <= 800*2, monsters )

    return close_monsters

BASE_DISTANCE = 5000

def compute_value(option,solution, base_penalty = 1):
    cost = 0
    base_distance = distance(option, base_position)
    for hero in solution:

        hero_distance = distance(hero, option)

        cost = cost + max(0,2 * VIEW_DISTANCE - hero_distance)
    base_penalty = -100000 if base_distance > BASE_DISTANCE else 1
    return - base_penalty * base_distance + cost

def in_range_control(hero,monster):
    return object_distance(hero, monster) <=2200

def in_range_wind(hero,monster):
    return object_distance(hero, monster) <=1280

def get_points_on_circumference(x, y, number_of_points=32, r=800):
    angle = 2 * math.pi / number_of_points
    return filter(lambda a: a[0] >= 0 and a[1] >= 0 and a[0] <= 17630 and a[1] <= 9000,
                  [(int(x + r * math.cos(angle * i)), int(y + r * math.sin(angle * i))) for i in range(number_of_points)])

if __name__=="__main__":
    base_x, base_y = [int(i) for i in input().split()]
    base_position = (base_x, base_y)
    if base_x == 0:
        enemy_base_x = 17630
        enemy_base_y = 9000
    else:
        enemy_base_x = 0
        enemy_base_y = 0


    heroes_per_player = int(input())
    # game loop
    while True:
        our_mana = 0
        for i in range(2):
            health, mana = [int(j) for j in input().split()]
            if i == 0:
                our_mana = mana

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

           # for option in options:

            #    print("Evaluating option %s %s" % (str(option),compute_value(option,solution)), file=sys.stderr)



            option = options[0]

            #print("Choosing option %s " % (str(option)), file=sys.stderr)

            # Update solution

            monster = choose_monster(get_monsters(entities))

            if monster:
                attack = "MOVE %s %s" % (monster[X], monster[Y])
                if our_mana >= 10 and monster[HEALTH] > 10:
                    if monster[BASE_DISTANCE] <= 5000 and in_range_wind(entities[HERO][i],monster):
                        attack = "SPELL WIND %s %s"%(enemy_base_x,enemy_base_y)
                        our_mana = our_mana - 10
                    elif in_range_control(entities[HERO][i],monster):
                        attack = "SPELL CONTROL %s %s %s" % (monster[ID],enemy_base_x, enemy_base_y)
                        our_mana = our_mana - 10
                print("Attack monster %s" % str(monster), file=sys.stderr)
                solution.append((monster[X],monster[Y]))
                print("%s"% attack)

            elif option:
                print("Move to option %s %s" % option, file=sys.stderr)
                solution.append(option)
                print("MOVE %s %s" % option)
            else:
                print("WAIT")
