import sys
import math
import numpy

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# Global variables

ATTACK_MONSTER_SPELL_HEALTH = 14
DEFENSE_MONSTER_SPELL_HEALTH = 10
SHIELD_DISTANCE = 5000
RUSH_LENGTH = 2

# Configure

base_y = ""
base_x = ""
enemy_base_y = ""
enemy_base_x = ""
ROUND = 0
ATTACK_SHIELD = 0
entities = []
enemy_base_position = ""
base_position = ""
solution = []
monster = ""
enemy = ""

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
ENEMY_BASE_DISTANCE = "ENEMY_BASE_DISTANCE"
NO_THREAT = 0
IS_THREAT = 1
FRIEND = 2
BASE_DISTANCE_VALUE = 5000

## ENTITY

MONSTER = 0
HERO = 1
ENEMY = 2

def walk_towards_enemy( hero, rate = 0.5 ):
    target = rate * (numpy.array((enemy_base_x,enemy_base_y)) - numpy.array((base_x,base_y)))

    distance_target = distance((hero[X],hero[Y]),target)

    if distance_target > 0:
        return ["MOVE %s %s"%(target[0],target[1])]
    return []

def distance( A, B):

    return float(numpy.linalg.norm(numpy.array(A) - numpy.array(B)))

def object_distance( A, B):

    return distance ((A[X],A[Y]),(B[X],B[Y]))

def get_entities(input):
    global enemy_base_position
    print("Get entities", file=sys.stderr)
    entities = {MONSTER: [], HERO: [], ENEMY: []}
    entity_count = int(input())
    for i in range(entity_count):
        id, type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in
                                                                                             input().split()]
        base_distance = distance(base_position, (x, y))
        enemy_base_distance = distance(enemy_base_position, (x, y))

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
            BASE_DISTANCE: base_distance,
            ENEMY_BASE_DISTANCE: enemy_base_distance
        })



    return entities

def choose_monster(monsters):
    if not monsters:
        return {}
    threat = sorted(monsters, key = lambda x: x[BASE_DISTANCE])

    return threat[0] if threat else {}

def choose_close_monster(monsters,hero):
    if not monsters:
        return {}
    threat = sorted(monsters, key = lambda x: object_distance(x,hero))

    return threat[0] if threat else {}


def sort_monster(monsters,hero, max_distance = -1):
    if not monsters:
        return {}
    if max_distance < 0:
        return sorted(monsters, key=lambda x: object_distance(x, hero))
    else:
        return sorted([monster for monster in monsters if object_distance(monster,hero) <= max_distance], key = lambda x: object_distance(x,hero))


def get_threat_monsters(entities):
    monsters  = entities[MONSTER]
    return [m for m in monsters if m[THREAT] == IS_THREAT]


def get_monsters(entities):
    return entities[MONSTER]

def get_enemies(ent):
    return ent[ENEMY]

def get_options(entity):
    return get_points_on_circumference(entity[X],entity[Y])

VIEW_DISTANCE = 2200

WIND_RANGE = 1280

def potential_monster_to_target(entities, hero):
    hero_position = (hero[X],hero[Y])
    monsters = get_threat_monsters(entities)

    close_monsters = filter(lambda a: distance(hero_position, (a[X], a[Y])) <= 800*2, monsters )

    return close_monsters



def compute_value(option,solution, defense_area):
    cost = 0
    base_distance = distance(option, base_position)
    for hero in solution:

        hero_distance = distance(hero, option)

        cost = cost + max(0,2.0 * float(VIEW_DISTANCE) - hero_distance)
    base_penalty = -100000 if base_distance > BASE_DISTANCE_VALUE * (1 + defense_area) else 1
    return - base_penalty * base_distance + cost

def in_range_control(hero,monster):
    return object_distance(hero, monster) <=2200

def in_range_wind(hero,monster):
    return object_distance(hero, monster) <=1280

def get_points_on_circumference(x, y, number_of_points=32, r=800):
    angle = 2 * math.pi / number_of_points
    return filter(lambda a: a[0] >= 0 and a[1] >= 0 and a[0] <= 17630 and a[1] <= 9000,
                  [(int(x + r * math.cos(angle * i)), int(y + r * math.sin(angle * i))) for i in range(number_of_points)])


def rush(hero):
    global ATTACK_SHIELD, entities, our_mana

    monsters = sort_monster(get_monsters(entities), hero, max_distance=VIEW_DISTANCE)
    flag = False
    for monster in monsters:
        if our_mana >= 20 and monster[HEALTH] > ATTACK_MONSTER_SPELL_HEALTH and monster[SHIELD] == 0:
            if monster[ENEMY_BASE_DISTANCE] <= SHIELD_DISTANCE:
                if in_range_control(entities[HERO][int(hero[ID])-1], monster):
                    print("SPELL SHIELD %s" % monster[ID])
                    our_mana = our_mana - 10
                    ATTACK_SHIELD = RUSH_LENGTH
                    flag = True
    if not flag:
        print("Rush!!!!", file=sys.stderr)
        ATTACK_SHIELD = ATTACK_SHIELD - 1
        print("MOVE %s %s"%(enemy_base_x,enemy_base_y))



def attack(defense_area,hero, entities):
        global monster, our_mana, ROUND, ATTACK_SHIELD, base_position

        if not ATTACK_SHIELD == 0:
            rush(hero)
        else:
            print("Hero %s chooses an action" % hero, file=sys.stderr)
            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr)
            # Get options
            options = get_options(hero)
            # Compute value
            ## Minimizing cost
            options = sorted(options, key=lambda o: compute_value(o, solution, defense_area))
            # for option in options:
            #    print("Evaluating option %s %s" % (str(option),compute_value(option,solution)), file=sys.stderr)
            option = options[0]
            i = int(hero[ID]) - 1
            # print("Choosing option %s " % (str(option)), file=sys.stderr)
            # Update solution
            monsters = sort_monster(get_monsters(entities), hero, max_distance=VIEW_DISTANCE)
            flag = False
            for monster in monsters:
                attack = "WAIT"
                if our_mana >= 20 and monster[HEALTH] > ATTACK_MONSTER_SPELL_HEALTH and monster[SHIELD] == 0:
                    if monster[ENEMY_BASE_DISTANCE] <= SHIELD_DISTANCE:
                        if in_range_control(entities[HERO][i], monster):
                            attack = "SPELL SHIELD %s" % monster[ID]
                            our_mana = our_mana - 10
                            ATTACK_SHIELD = RUSH_LENGTH
                            flag = True
                    elif monster[ENEMY_BASE_DISTANCE] <= 6000:
                        if in_range_wind(entities[HERO][i], monster):
                            attack = "SPELL WIND %s %s" % (enemy_base_x, enemy_base_y)
                            our_mana = our_mana - 10
                            flag = True
                    else:
                        if monster[THREAT] != FRIEND and in_range_control(entities[HERO][i], monster):
                            attack = "SPELL CONTROL %s %s %s" % (monster[ID], enemy_base_x, enemy_base_y)
                            our_mana = our_mana - 10
                            flag = True
                if not flag:
                    if monster[THREAT] != FRIEND and distance((monster[X], monster[Y]),enemy_base_position) < 11000:
                        attack = "MOVE %s %s" % (monster[X], monster[Y])
                        flag = True

                if flag:
                    print("Attack monster %s" % str(monster), file=sys.stderr)
                    solution.append((monster[X], monster[Y]))
                    print("%s" % attack)
                    break

            if option and not flag:
                print("Move to option %s %s" % option, file=sys.stderr)
                solution.append(option)
                print("MOVE %s %s" % option)
            elif not flag:
                print("WAIT")

DEFENSE = [1,2]
PUSH = [1]
ATTACK  = [0]

def defend(defense_area,id, entities):
    global monster, our_mana

    print("Hero %s chooses an action" % entities[HERO][id][ID], file=sys.stderr)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    # Get options
    i = id
    options = get_options(entities[HERO][i])
    # Compute value
    ## Minimizing cost
    options = sorted(options, key=lambda o: compute_value(o, solution,defense_area))
    # for option in options:
    #    print("Evaluating option %s %s" % (str(option),compute_value(option,solution)), file=sys.stderr)
    option = options[0]
    # print("Choosing option %s " % (str(option)), file=sys.stderr)
    # Update solution
    enemy = choose_close_monster(filter(lambda x: distance((x[X], x[Y]),(base_x,base_y)) < BASE_DISTANCE_VALUE * (1 + defense_area) ,get_enemies(entities)),entities[HERO][i])
    monster = choose_monster(get_threat_monsters(entities))
    if enemy:
        print("Preparing a spell on enemy %s shield %s range %s " % (str(enemy),enemy[SHIELD],in_range_wind(entities[HERO][i], enemy)), file=sys.stderr)

    attack  = ""
    if enemy:
        if id in PUSH and enemy[SHIELD] < 1 and in_range_wind(entities[HERO][i], enemy) :
            print("Trying to push %s" % str(enemy), file=sys.stderr)

            our_mana = our_mana - 10
            attack = "SPELL WIND %s %s" % (enemy_base_x, enemy_base_y)
            enemy[SHIELD] = 100
            print("Attack enemy %s" % str(enemy), file=sys.stderr)
            solution.append((enemy[X], enemy[Y]))
            print("%s" % attack)
        if id not in PUSH or enemy[SHIELD] >0:
            print("Trying to shield" , file=sys.stderr)
            to_be_shielded = filter(lambda x: entities[HERO][x][SHIELD] < 1,sorted(DEFENSE,key = lambda x: entities[HERO][x][SHIELD],reverse=True))

            id = next(to_be_shielded,None)
            if not id is None:
                hero = entities[HERO][id]
                attack = "SPELL SHIELD %s" % (hero[ID])
                our_mana = our_mana - 10
                enemy[SHIELD] = 100
                print("Shield %s" % str(hero[ID]), file=sys.stderr)
                solution.append((hero[X], hero[Y]))
                print("%s" % attack)
    if not attack:
        if monster :
            attack = "MOVE %s %s" % (monster[X], monster[Y])
            if our_mana >= 10 and monster[HEALTH] > DEFENSE_MONSTER_SPELL_HEALTH and monster[SHIELD] == 0:
                if monster[BASE_DISTANCE] <= 5000:
                    if in_range_wind(entities[HERO][i], monster):
                        attack = "SPELL WIND %s %s" % (enemy_base_x, enemy_base_y)
                        our_mana = our_mana - 10
                        monster[SHIELD] = 100
                else:
                    if in_range_control(entities[HERO][i], monster):
                        attack = "SPELL CONTROL %s %s %s" % (monster[ID], enemy_base_x, enemy_base_y)
                        our_mana = our_mana - 10
                        monster[SHIELD] = 200
            print("Attack monster %s" % str(monster), file=sys.stderr)
            solution.append((monster[X], monster[Y]))
            print("%s" % attack)

        elif option:
            print("Move to option %s %s" % option, file=sys.stderr)
            solution.append(option)
            print("MOVE %s %s" % option)
        else:
            print("WAIT")



def run( input = input):
    global base_y, base_x, enemy_base_position, enemy_base_y,enemy_base_x, ROUND, our_mana, enemy, solution, base_position
    base_x, base_y = [int(i) for i in input().split()]
    base_position = (base_x, base_y)
    if base_x == 0:
        enemy_base_x = 17630
        enemy_base_y = 9000
    else:
        enemy_base_x = 0
        enemy_base_y = 0
    enemy_base_position = (enemy_base_x, enemy_base_y)

    heroes_per_player = int(input())
    # game loop
    while True:
        ROUND = ROUND + 1
        our_mana = 0
        for i in range(2):
            health, mana = [int(j) for j in input().split()]
            if i == 0:
                our_mana = mana

        entities = get_entities(input)
        enemy = {}
        monsters = get_threat_monsters(entities)
        for monster in monsters:
            print("I see: %s %s" % (monster[ID], str(monster[BASE_DISTANCE])), file=sys.stderr)
        enemy = choose_monster(monsters)
        solution = []
        for i in range(heroes_per_player):
            if i == 0:
                attack(1.9, entities[HERO][i], entities)
            else:
                defend(0.1,i, entities)
    return solution

if __name__=="__main__":
    run()