import random
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
ENEMY_BASE_DISTANCE = "ENEMY_BASE_DISTANCE"
NO_THREAT = 0
IS_THREAT = 1
FRIEND = 2

## ENTITY

MONSTER = 0
HERO = 1
ENEMY = 2

def walk_towards_enemy( hero, enemy_base_x,enemy_base_y,base_x,base_y,rate = 0.5 ):
    target = rate * (numpy.array((enemy_base_x,enemy_base_y)) - numpy.array((base_x,base_y)))

    distance_target = distance((hero[X],hero[Y]),target)

    if distance_target > 0:
        return ["MOVE %s %s"%(target[0],target[1])]
    return []

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

BASE_DISTANCE = 5000

def compute_value(option,solution, defense_area, _):
    cost = 0
    base_distance = distance(option, base_position)
    for hero in solution:

        hero_distance = distance(hero, option)

        cost = cost + max(0,2 * VIEW_DISTANCE - hero_distance)
    base_penalty = -100000 if base_distance > BASE_DISTANCE * (1 + defense_area) else 1
    return - base_penalty * base_distance + cost


def compute_value_base(option,solution, inner_defense_area, outer_defense_area):
    # inner_defense_area < outer_defense_area
    prox_cost = proximity_cost(option, solution)

    base_distance = distance(option, base_position)
    within_internal_wall_cost = max(0, (BASE_DISTANCE * (1 + inner_defense_area) - base_distance)*21)
    above_external_wall_cost = max(0, (base_distance - BASE_DISTANCE * (1 + outer_defense_area))*42)

    return within_internal_wall_cost + above_external_wall_cost + prox_cost

def proximity_cost(option, solution):
    cost = 0
    for hero in solution:
        hero_distance = distance(hero, option)
        cost = cost + max(0, 2 * VIEW_DISTANCE - hero_distance)
    return cost

def compute_value_enemy_base(option,solution, inner_defense_area, outer_defense_area):
    # inner_defense_area < outer_defense_area
    prox_cost = proximity_cost(option, solution)

    enemy_base_distance = distance(option, enemy_base_position)
    within_internal_wall_cost = max(0, enemy_base_distance - (BASE_DISTANCE * (1 + outer_defense_area))*42)
    above_external_wall_cost = max(0, (BASE_DISTANCE * (1 + inner_defense_area) - enemy_base_distance)*21)

    return within_internal_wall_cost + above_external_wall_cost + prox_cost

def in_range_control(hero,monster):
    return object_distance(hero, monster) <=2200

def in_range_wind(hero,monster):
    return object_distance(hero, monster) <=1280

def get_points_on_circumference(x, y, number_of_points=32, r=800):
    angle = 2 * math.pi / number_of_points
    return filter(lambda a: a[0] >= 0 and a[1] >= 0 and a[0] <= 17630 and a[1] <= 9000,
                  [(int(x + r * math.cos(angle * i)), int(y + r * math.sin(angle * i))) for i in range(number_of_points)])

ATTACK_SHIELD = 0
def rush(hero):
    global ATTACK_SHIELD

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
    if not flag:
        print("Rush!!!!", file=sys.stderr)
        ATTACK_SHIELD = ATTACK_SHIELD - 1
        print("MOVE %s %s"%(enemy_base_x,enemy_base_y))


def get_unprotected_enemy_rush_for_wind(hero):

    enemies = sort_monster(get_enemies(entities), hero, max_distance=VIEW_DISTANCE)
    return [enemy for enemy in enemies if in_range_wind(hero, enemy) and enemy[SHIELD] == 0]


def get_unprotected_monster_rush_for_wind(hero):

    monsters = sort_monster(get_monsters(entities), hero, max_distance=VIEW_DISTANCE)
    return [monster for monster in monsters if in_range_wind(hero, monster) and monster[SHIELD] == 0]


def can_monster_reach_before_being_killed(monster, distace_to_base, numer_of_defenders = 2):
    return monster[HEALTH] > int((distace_to_base - 300)*2*numer_of_defenders/400)


def get_monsters_that_can_reach_base(hero, number_of_defenders = 2):
    return [monster for monster in get_unprotected_monster_rush_for_wind(hero) if
            can_monster_reach_before_being_killed(monster, distance(base_position, (monster[X], monster[Y])),
                                                  number_of_defenders)]


def get_defensive_wind_direction(hero):
    return ( 2*hero[X] - base_x, 2*hero[Y] - base_y)


def get_options_sorted(hero, value_calc, inner_defense_area, outer_defense_area):
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    # Get options
    options = get_options(hero)
    # Compute value
    ## Minimizing cost
    options_with_values = [(option, value_calc(option, solution, inner_defense_area, outer_defense_area)) for option in options]
    return sorted(options_with_values, key=lambda o: o[1])


def get_option(hero, value_calc, inner_defense_area, outer_defense_area):
    option_with_values = get_options_sorted(hero, value_calc, inner_defense_area, outer_defense_area)
    # for option in options:
    #    print("Evaluating option %s %s" % (str(option),compute_value(option,solution)), file=sys.stderr)
    _, best_score = option_with_values[0]
    # print("Choosing option %s " % (str(option)), file=sys.stderr)
    best_options = [option[0] for option in option_with_values if option[1] < (best_score + 1)]
    return random.choice(best_options)


def can_attack(monster):
    return our_mana >= 20 and monster[HEALTH] > ATTACK_MONSTER_SPELL_HEALTH and monster[SHIELD] == 0


def in_enemies_base(entity):
    return entity[ENEMY_BASE_DISTANCE] <= SHIELD_DISTANCE


def is_not_friend_monster(monster):
    return monster[THREAT] != FRIEND


def shield(entity):
    return "SPELL SHIELD %s" % entity[ID]


def wind():
    return "SPELL WIND %s %s" % (enemy_base_x, enemy_base_y)


def control(entity):
    return "SPELL CONTROL %s %s %s" % (entity[ID], enemy_base_x, enemy_base_y)


def move(entity):
    return "MOVE %s %s" % (entity[X], entity[Y])


def get_attack_spell(monster):
    if in_enemies_base(monster):
        if in_range_control(entities[HERO][i], monster):
            ATTACK_SHIELD = RUSH_LENGTH
            return shield(monster)
    elif monster[ENEMY_BASE_DISTANCE] <= 6000:
        if in_range_wind(entities[HERO][i], monster):
            return wind()
    elif is_not_friend_monster(monster) and in_range_control(entities[HERO][i], monster):
        return control(monster)
    return None


def wait():
    print("WAIT")


def is_monster_moving_towards_enemy_base(monster):
    enemy_base_x, _ = enemy_base_position
    if enemy_base_x == 0:
        return monster[VX] < 0 and monster[VY] < 0
    else:
        return monster[VX] > 0 and monster[VY] > 0


def get_monsters_for_enemy_be_controlled(hero, max_distance, distance_to_enemy_base, check_monster_direction = False):

    monsters = list()
    for monster in get_monsters(entities):
        # if monster[THREAT] == FRIEND and object_distance(monster,hero) <= max_distance and (not check_monster_direction or is_monster_moving_towards_enemy_base(monster)):
        if monster[THREAT] == FRIEND and object_distance(monster, hero) <= max_distance and distance((monster[X], monster[Y]), enemy_base_position) < distance_to_enemy_base:
            monsters.append(monster)
    return monsters


ASSIST_MONSTER_RUSH = 5
ATTACK_ENEMY_CONTROL_RUSH_MANA = 100
IN_ASSIST_RUSH_MODE = False
STOP_ASSIST_RUSH_MODE_MANA = 9
DISTANCE_TO_ENEMY_BASE = 1500


def should_enemy_be_controlled(hero):

    monsters = get_monsters_for_enemy_be_controlled(hero, VIEW_DISTANCE, DISTANCE_TO_ENEMY_BASE)
    return len(monsters) > ASSIST_MONSTER_RUSH and (our_mana > ATTACK_ENEMY_CONTROL_RUSH_MANA or (
                IN_ASSIST_RUSH_MODE and our_mana > STOP_ASSIST_RUSH_MODE_MANA))


def get_monsters_closest_to_enemy_base(distance_to_enemy_base):
    monsters = list()
    for monster in get_monsters(entities):
        # if monster[THREAT] == FRIEND and object_distance(monster,hero) <= max_distance and (not check_monster_direction or is_monster_moving_towards_enemy_base(monster)):
        if monster[THREAT] == FRIEND and distance((monster[X], monster[Y]), enemy_base_position) < distance_to_enemy_base:
            monsters.append(monster)
    return sorted(monsters, key=lambda x: distance((x[X], x[Y]), enemy_base_position))


def should_walk_towards_monster(hero, monster):
    return object_distance(hero, monster) > 800


ASSIST_MONSTER_DISTANCE = 1500


def assist_monster(hero):
    monsters = get_monsters_closest_to_enemy_base(ASSIST_MONSTER_DISTANCE)
    target = None
    for monster in monsters:
        if should_walk_towards_monster(hero, monster):
            target = monster
            break
    if target:
        return move(target)
    return None


def attack(hero, inner, outer):

        global monster, our_mana, ROUND, ATTACK_SHIELD

        def can_move(monster):
            return monster[THREAT] != FRIEND and distance((monster[X], monster[Y]), enemy_base_position) < 11000

        if not ATTACK_SHIELD == 0:
            rush(hero)
        else:
            print("Hero %s chooses an action" % hero, file=sys.stderr)
            # option = get_option(hero, compute_value, inner, outer)
            option = get_option(hero, compute_value_enemy_base, inner, outer)
            # Update solution
            monsters = sort_monster(get_monsters(entities), hero, max_distance=VIEW_DISTANCE)
            has_spell = False

            for monster in monsters:
                action = "WAIT"

                if can_attack(monster):
                    spell = get_attack_spell(monster)
                    if spell:
                        action = spell
                        has_spell = True

                if has_spell:
                    our_mana = our_mana - 10
                elif can_move(monster):
                    action = "MOVE %s %s" % (monster[X], monster[Y])
                    has_spell = True

                if has_spell:
                    print("Attack monster %s" % str(monster), file=sys.stderr)
                    solution.append((monster[X], monster[Y]))
                    print("%s" % action)
                    break

            if option and not has_spell:
                print("Move to option %s %s" % option, file=sys.stderr)
                solution.append(option)
                print("MOVE %s %s" % option)
            elif not has_spell:
                wait()


DEFENSE = [1,2]
PUSH = [1]
ATTACK  = [0]


def filter_and_choose_enemy(hero, defense_area):
    return choose_close_monster(
        filter(lambda x: distance((x[X], x[Y]), (base_x, base_y)) < BASE_DISTANCE * (1 + defense_area),
               get_enemies(entities)), hero)


def get_to_be_shielded():
    return filter(lambda x: entities[HERO][x][SHIELD] < 1,
                  sorted(DEFENSE, key=lambda x: entities[HERO][x][SHIELD], reverse=True))


def can_spell_defensive_wind(id, i):
    return id in PUSH and enemy[SHIELD] < 1 and in_range_wind(entities[HERO][i], enemy)


def get_threat_monster_within_reach(hero):
    return [monster for monster in get_threat_monsters(entities) if monster != hero and object_distance(hero, monster) < 1600]


def get_center(entities):
    return sum(entity[X] for entity in entities) / len(entities), sum(entity[Y] for entity in entities) / len(entities)


def get_closer_to_monster(center, dist, target):
    return target + (center - target) * 799 / dist


def defend_with_barycenter(monster):
    centroid_x, centroid_y = monster[X], monster[Y]
    monsters_within_reach = get_threat_monster_within_reach(monster)

    if monsters_within_reach:
        centroid_x, centroid_y = get_center(monsters_within_reach)
        dist = distance((monster[X], monster[Y]), (centroid_x, centroid_y))
        if dist >= 800:
            centroid_x = get_closer_to_monster(centroid_x, dist, monster[X])
            centroid_y = get_closer_to_monster(centroid_y, dist, monster[Y])

    return int(centroid_x), int(centroid_y)


def defend(id, inner, outer):

    global monster, our_mana
    print("Hero %s chooses an action" % entities[HERO][i][ID], file=sys.stderr)
    # option = get_option(entities[HERO][i], compute_value, inner, outer)
    option = get_option(entities[HERO][i], compute_value_base, inner, outer)
    # print("Choosing option %s " % (str(option)), file=sys.stderr)
    # Update solution
    enemy = filter_and_choose_enemy(entities[HERO][i], outer)
    monster = choose_monster(get_threat_monsters(entities))
    if enemy:
        print("Preparing a spell on enemy %s shield %s range %s " % (str(enemy),enemy[SHIELD],in_range_wind(entities[HERO][i], enemy)), file=sys.stderr)

    attack  = ""
    if enemy:
        if can_spell_defensive_wind(id, i):
            print("Trying to push %s" % str(enemy), file=sys.stderr)
            attack = wind()
            print("Attack enemy %s" % str(enemy), file=sys.stderr)
            solution.append((enemy[X], enemy[Y]))
            print("%s" % attack)
        if id not in PUSH or enemy[SHIELD] >0:
            print("Trying to shield" , file=sys.stderr)
            to_be_shielded = get_to_be_shielded()

            id = next(to_be_shielded,None)
            if id is not None:
                hero = entities[HERO][id]
                attack = shield(hero)
                print("Shield %s" % str(hero[ID]), file=sys.stderr)
                solution.append((hero[X], hero[Y]))
                print("%s" % attack)

    if attack:
        our_mana = our_mana - 10
        enemy[SHIELD] = 100
    elif monster:
        attack = "MOVE %s %s" % (monster[X], monster[Y])
        if our_mana >= 10 and monster[HEALTH] > DEFENSE_MONSTER_SPELL_HEALTH and monster[SHIELD] == 0:
            if monster[BASE_DISTANCE] <= 5000:
                if in_range_wind(entities[HERO][i], monster):
                    attack = wind()
                    our_mana = our_mana - 10
                    monster[SHIELD] = 100
            else:
                if in_range_control(entities[HERO][i], monster):
                    attack = control(monster)
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


def get_enemy_position(base_x):
    global enemy_base_x, enemy_base_y
    if base_x == 0:
        enemy_base_x = 17630
        enemy_base_y = 9000
    else:
        enemy_base_x = 0
        enemy_base_y = 0
    return (enemy_base_x, enemy_base_y)


def attacker(i):

    return i == 0

ATTACK_MONSTER_SPELL_HEALTH = 14
DEFENSE_MONSTER_SPELL_HEALTH = 10
SHIELD_DISTANCE = 5000
RUSH_LENGTH = 2

if __name__=="__main__":

    base_x, base_y = [int(i) for i in input().split()]
    base_position = (base_x, base_y)
    enemy_base_position = get_enemy_position(base_x)

    heroes_per_player = int(input())
    # game loop
    ROUND = 0
    while True:
        ROUND = ROUND + 1
        our_mana = 0
        for i in range(2):
            health, mana = [int(j) for j in input().split()]
            if i == 0:
                our_mana = mana

        entities = get_entities()
        enemy = {}
        monsters = get_threat_monsters(entities)
        for monster in monsters:
            print("I see: %s %s" % (monster[ID], str(monster[BASE_DISTANCE])), file=sys.stderr)
        enemy = choose_monster(monsters)
        solution = []
        for i in range(heroes_per_player):
            if attacker(i):
                attack(entities[HERO][i], -0.2, 0.5)
            else:
                defend(i, 0, 0.3)
