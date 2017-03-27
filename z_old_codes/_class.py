'''
'''
#

class zone(object):
    def __init__(self, i, j, width, height):
        self.i, self.j = i, j
        self.width, self.height = width, height
        halfWidth = self.width / float(2)
        halfHeight = self.height / float(2)
        self.centerCoords = (self.i * self.width + halfWidth, self.j * self.height + halfHeight)
        self.leftUpperCoords = (self.i * self.width, self.j * self.height)
        self.leftLowerCoords = (self.i * self.width, (self.j + 1) * self.height)
        self.rightLowerCoords = ((self.i + 1) * self.width, (self.j + 1) * self.height)
        self.rightUpperCoords = ((self.i + 1) * self.width, self.j * self.height)

    def __repr__(self):
        return 'z(%d, %d)' % (self.i, self.j)


class beacon(object):
    def __init__(self, bid, locatedZone, initBatteryCapacity):
        self.bid = bid
        self.locatedZone = locatedZone
        self.remainingBC = initBatteryCapacity

    def __repr__(self):
        return 'b%d(%d, %d)' % (self.bid, self.locatedZone.i, self.locatedZone.j)



class user(object):
    def __init__(self, uid, trajectory):
        self.uid, self.trajectory = uid, trajectory
    def __repr__(self):
        return 'u%d' % self.uid


