import __init__
'''

'''
from _class import zone, user, beacon
#
from math import sqrt
from random import random, seed, choice

#
DISTANCE = 20
TIME_INTERVAL = 60


def problem1():
    seed(1)
    # Zones generation
    lenX, lenY = 100, 50
    numCols, numRows = 10, 5
    colUnit, rowUnit = lenX / float(numCols), lenY / float(numRows)
    Z = {}
    for i in range(numCols):
        for j in range(numRows):
            z = zone(i, j, colUnit, rowUnit)
            z.timeSlots = [set() for _ in range(K)]
            Z[i, j] = z
    #
    # Beacons generation
    #
    numBeacons = 5
    B = {}
    initBatteryCapacity = 20
    beaconsPosition = set()
    for bid in range(numBeacons):
        z = choice(Z.values())
        while z in beaconsPosition:
            z = choice(Z.values())
        B[bid] = beacon(bid, initBatteryCapacity, z)
    #
    # Users generation
    #
    numUsers = 10
    U = {uid: user(uid, genRandomTrajectory(lenX, lenY)) for uid in range(numUsers)}
    #
    K, _alpha, _beta, P = 4, 1, 1, 3
    return Z, B, U, K, _alpha, _beta, P


def genRandomTrajectory(lenX, lenY):
    initX, initY = random() * lenX, random() * lenY
    trajectory = [(0, initX, initY)]
    while len(trajectory) < TIME_INTERVAL:
        t0, x0, y0 = trajectory[-1]
        # dx, dy = x0 - random() * lenX, y0 - random() * lenY
        if x0 <= lenX / float(2):
            dx = random() * lenX / float(2)
        else:
            dx = -(random() * lenX / float(2))
        if y0 <= lenY / float(2):
            dy = random() * lenY / float(2)
        else:
            dy = -(random() * lenY / float(2))
        lenV = sqrt(dx**2 + dy**2)
        x1, y1 = x0 + (dx / lenV) * DISTANCE, y0 + (dy / lenV) * DISTANCE
        if x1 < 0:
            x1 = 0
        elif x1 > lenX:
            x1 = lenX
        if y1 < 0:
            y1 = 0
        elif y1 > lenY:
            y1 = lenY
        trajectory += [(t0 + 1, x1, y1)]
    return trajectory


if __name__ == '__main__':
    run()