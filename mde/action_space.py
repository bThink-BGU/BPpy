from mde.smt_variables import *

action_space = {
    0: {'request': moveForward, 'block': Or(Not(moveForward), moveForwardReal != 100)},
    1: {'request': moveForward, 'block': Or(Not(moveForward), moveForwardReal != 90)},
    2: {'request': moveForward, 'block': Or(Not(moveForward), moveForwardReal != 80)},
    3: {'request': moveForward, 'block': Or(Not(moveForward), moveForwardReal != 70)},
    4: {'request': moveForward, 'block': Or(Not(moveForward), moveForwardReal != -100)},
    5: {'request': moveForward, 'block': Or(Not(moveForward), moveForwardReal != -90)},
    6: {'request': moveForward, 'block': Or(Not(moveForward), moveForwardReal != -80)},
    7: {'request': moveForward, 'block': Or(Not(moveForward), moveForwardReal != -70)},
    8: {'request': spin, 'block': Or(Not(spin), spinReal != 100)},
    9: {'request': spin, 'block': Or(Not(spin), spinReal != 90)},
    10: {'request': spin, 'block': Or(Not(spin), spinReal != 80)},
    11: {'request': spin, 'block': Or(Not(spin), spinReal != 70)},
    12: {'request': spin, 'block': Or(Not(spin), spinReal != -100)},
    13: {'request': spin, 'block': Or(Not(spin), spinReal != -90)},
    14: {'request': spin, 'block': Or(Not(spin), spinReal != -80)},
    15: {'request': spin, 'block': Or(Not(spin), spinReal != -70)},
    16: {'request': stop, 'block': Not(stop)},
    17: {'request': setSuction, 'block': Or(Not(setSuction), setSuctionReal != 100)},
    18: {'request': setSuction, 'block': Or(Not(setSuction), setSuctionReal != 0)},
    19: {'request': setSuction, 'block': Or(Not(setSuction), setSuctionReal != -100)},
}