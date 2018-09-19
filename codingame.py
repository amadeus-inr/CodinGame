import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())

# game loop
while True:
    for i in range(2):
        health, mana = [int(j) for j in input().split()]
    entity_count = int(input())
    for i in range(entity_count):
        id, type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
    for i in range(heroes_per_player):

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)

        print("WAIT")
