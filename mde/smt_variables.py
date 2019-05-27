from z3helper import *

# sends
moveForward = Bool('moveForward')
moveForwardReal = Int('moveForwardReal')
moveRight = Bool('moveRight')
moveRightReal = Int('moveRightReal')
spin = Bool('spin')
spinReal = Int('spinReal')
stop = Bool('stop')
setSuction = Bool('setSuction')
setSuctionReal = Int('setSuctionReal')
getSuction = Bool('getSuction')
GPS = Bool('GPS')
ballGPS = Bool('ballGPS')
getCompass = Bool('getCompass')

# utility
rewardReal = Int('reward')