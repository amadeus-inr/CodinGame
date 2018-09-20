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