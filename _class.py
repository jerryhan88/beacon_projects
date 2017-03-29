'''

'''


class Beacon(object):
    def __init__(self, bid, l):
        self.bid, self.l = bid, l

    def __repr__(self):
        return 'bid %s (%d, %d)' % (self.bid, self.l.z.coords[0], self.l.z.coords[1])

    def init4viz(self, pos):
        self.pos = pos

    def draw(self, gc, radius, color):
        gc.SetBrush(color)
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
        gc.DrawText('%s' % self.lid[-3:], self.pos[0] + 1, self.pos[1] + 1)
        gc.DrawEllipse(self.pos[0], self.pos[1], radius, radius)


class Zone(object):
    def __init__(self, coords):
        self.coords = coords
        self.i, self.j = coords
        self.zid = 'z(%d, %d)' % (self.i, self.j)
        #
        self.bs = []
        self.feasible = False

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

    def add_beacon(self, b):
        self.bs += [b]

    def remove_beacon(self):
        return self.bs.pop()

    def draw(self, gc, color):
        gc.SetBrush(color)
        gc.DrawRectangle(self.leftUpperCoords[0], self.leftUpperCoords[1], self.width, self.height)


