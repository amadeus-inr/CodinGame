import sys
import math
import numpy

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

base_x, base_y = [int(i) for i in input().split()]
base_position = numpy.array((base_x, base_y))
heroes_per_player = int(input())

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
THREAT = 1
FRIEND = 2

## ENTITY

MONSTER = 0
HERO = 1
ENEMY = 2


def get_entities():
    entities = {MONSTER: [], HERO: [], ENEMY: []}
    entity_count = int(input())
    for i in range(entity_count):
        id, type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in
                                                                                             input().split()]
        base_distance = numpy.linalg.norm(base_position - numpy.array((x, y)))

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

    threat = sorted([m for m in monsters if m[THREAT] == THREAT], lambda x,y: x[BASE_DISTANCE] < y[BASE_DISTANCE])

    return threat[0] if threat else {}

def get_monsters(entities):

    return entities[MONSTER]

if __name__=="__main__":
    # game loop
    while True:
        for i in range(2):
            health, mana = [int(j) for j in input().split()]

        entities = get_entities()
        enemy = {}
        monsters = get_monsters(entities)
        for monster in monsters:
            print("I see: %s %s" % (monster[ID], str(monster[BASE_DISTANCE])), file=sys.stderr)
            enemy = monster
        # enemy = choose_monster(monsters)
        for i in range(heroes_per_player):
            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr)
            if enemy:
                print("Attacking %s %s" % (enemy[ID], str(enemy[BASE_DISTANCE])), file=sys.stderr)
                print("MOVE %s %s" % (enemy[X], enemy[Y]))
            else:
                print("WAIT")
