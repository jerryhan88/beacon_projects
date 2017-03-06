import __init__
'''

'''
from _class import zone, user
#
from math import sqrt
from random import random
from bisect import bisect
#
DISTANCE = 20
lenX, lenY = 100, 50
numCols, numRows = 10, 5
colUnit, rowUnit = lenX / float(numCols), lenY / float(numRows)
xPoints, yPoints = [i * colUnit for i in range(numCols)], [j * rowUnit for j in range(numRows)]
TIME_INTERVAL = 60
K = 4
TIME_UNIT = TIME_INTERVAL / float(K)


def run():
    users = {uid: user(uid, genRandomTrajectory(lenX, lenY)) for uid in range(10)}
    zones = {}
    for i in range(numCols):
        for j in range(numRows):
            z = zone(i,j, colUnit, rowUnit)
            z.timeSlots = [set() for _ in range(K)]
            zones[i,j] = z

    for u in users.itervalues():
        for l in u.trajectory:
            t, x, y = l
            ts = int(t / TIME_UNIT)
            i, j = bisect(xPoints, x) - 1, bisect(yPoints, y) - 1
            zones[i, j].timeSlots[ts].add(u)
    for z in zones.itervalues():
        print z, z.timeSlots



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