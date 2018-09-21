import codingame

print({} == codingame.choose_monster([]))

monster1 = {"id": 1, codingame.THREAT: codingame.IS_THREAT, codingame.BASE_DISTANCE: 1}
monster2 = {"id": 2, codingame.THREAT: codingame.IS_THREAT, codingame.BASE_DISTANCE: 2}

print(1 == codingame.choose_monster([monster1,monster2])["id"])



# ARRANGE
monster1 = {"id": 1, codingame.THREAT: codingame.FRIEND, codingame.BASE_DISTANCE: 1}
monster2 = {"id": 2, codingame.THREAT: codingame.IS_THREAT, codingame.BASE_DISTANCE: 2}
# ASSERT
print(2 == codingame.choose_monster([monster1,monster2])["id"])


print(min([{"A":1,"B":2},{"A":1,"B":1}],key=lambda a: a["A"]))

enemy_base_x = 2
enemy_base_y = 2
base_x = 0
base_y = 0
print(['MOVE 1.0 1.0']==codingame.walk_towards_enemy({"X":0,"Y":0},enemy_base_x,enemy_base_y,base_x,base_y))