import codingame


def get_hero(id, type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for):
    return "%s %s %s %s %s %s %s %s %s %s %s"%(id, type, x, y, shield_life,
                                               is_controlled, health, vx, vy, near_base, threat_for)

hero1 = "id type x y shield_life is_controlled health vx vy near_base threat_for"


start_hero1 = get_hero(0 , 1 , 10 , 10 , 0 , 0 , -1 , -1 , -1 , -1, -1)
start_hero2 = get_hero(0 , 1 , 10 , 20 , 0 , 0 , -1 , -1 , -1 , -1, -1)
start_hero3 = get_hero(0 , 1 , 10 , 30 , 0 , 0 , -1 , -1 , -1 , -1, -1)


start_hero1_2 = get_hero(0 , 1 , 675, 454 , 0 , 0 , -1 , -1 , -1 , -1, -1)
start_hero2_2 = get_hero(0 , 1 , 10, 82 , 0 , 0 , -1 , -1 , -1 , -1, -1)
start_hero3_2 = get_hero(0 , 1 , 810, 30 , 0 , 0 , -1 , -1 , -1 , -1, -1)

game = [["0 0", "3", "3 0","3 0", "3", start_hero1, start_hero2, start_hero3]]
round = 0
calls = 0

def input():
    global calls, game, round
    print("------------Round: %s , Call %s---------------" % (round, calls) )

    if calls == len(game[round]):
        raise Exception("Game over")
        print("Game over")
    data = game[round][calls]
    print("data: %s" % data)
    calls += 1
    return data


codingame.run(input)