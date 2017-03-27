'''

'''


class Beacon(object):
    def __init__(self, bid, coords, pos):
        self.bid, self.coords, self.pos = bid, coords, pos

    def __repr__(self):
        return 'bid %d (%d, %d)' % (self.bid, self.coords[0], self.coords[1])

    def draw(self, gc, radius):
        gc.DrawEllipse(self.pos[0] - radius, self.pos[1] - radius, radius * 2, radius * 2)


class Landmark(object):
    def __init__(self, lid, z):
        self.lid, self.z = lid, z

    def __repr__(self):
        return 'lid %s (%d, %d)' % (self.lid, self.z.coords[0], self.z.coords[1])

    def init4viz(self, pos):
        self.pos = pos

    def draw(self, gc, font, radius):
        gc.SetFont(font)
        gc.DrawText('%d' % self.lid, self.pos[0] + 1, self.pos[1] + 1)
        gc.DrawEllipse(self.pos[0], self.pos[1], radius, radius)


class Zone(object):
    def __init__(self, coords):
        self.coords = coords
        self.i, self.j = coords
        self.zid = 'z(%d, %d)' % (self.i, self.j)
        #
        self.landmark, self.beacon = None, None

    def __repr__(self):
        return self.zid

    def init4viz(self, girdXPos, gridYPos, wUnit, hUnit):
        self.width, self.height = wUnit, hUnit
        halfWidth = self.width / float(2)
        halfHeight = self.height / float(2)
        self.centerCoords = (girdXPos + self.i * self.width + halfWidth,
                             gridYPos + self.j * self.height + halfHeight)
        self.leftUpperCoords = (girdXPos + self.i * self.width,
                                gridYPos + self.j * self.height)
        self.leftLowerCoords = (girdXPos + self.i * self.width,
                                gridYPos + (self.j + 1) * self.height)
        self.rightLowerCoords = (girdXPos + (self.i + 1) * self.width,
                                 gridYPos + (self.j + 1) * self.height)
        self.rightUpperCoords = (girdXPos + (self.i + 1) * self.width,
                                 gridYPos + self.j * self.height)

    def set_landmark(self, l):
        self.landmark = l

    def set_beacon(self, b):
        self.beacon = b

    def remove_beacon(self):
        self.beacon = None