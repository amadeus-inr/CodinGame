import codingame

# TEST1
## ASSERT
print({} == codingame.choose_monster([]))


# TEST2

## ARRANGE
monster1 = {"id": 1, codingame.THREAT: codingame.IS_THREAT, codingame.BASE_DISTANCE: 1}
monster2 = {"id": 2, codingame.THREAT: codingame.IS_THREAT, codingame.BASE_DISTANCE: 2}
## ASSERT
print(1 == codingame.choose_monster([monster1,monster2])["id"])



# TEST3
## ARRANGE
monster1 = {"id": 1, codingame.THREAT: codingame.FRIEND, codingame.BASE_DISTANCE: 1}
monster2 = {"id": 2, codingame.THREAT: codingame.IS_THREAT, codingame.BASE_DISTANCE: 2}
## ASSERT
print(2 == codingame.choose_monster([monster1,monster2])["id"])

## ASSERT
print(min([{"A":1,"B":2},{"A":1,"B":1}],key=lambda a: a["A"]))

#
## ASSERT
print(['MOVE 1.0 1.0']==codingame.walk_towards_enemy({"X":0,"Y":0},2,2,0,0))