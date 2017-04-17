'''

'''



class Beacon(object):
    def __init__(self, bid, l):
        self.bid, self.l = bid, l
        #
        self.pos = None
        #
        self.rb, self.a, self.b = None, None, None
        #
        self.pbz = {}

    def __repr__(self):
        return 'bid %s (%d, %d)' % (self.bid, self.l.z.coords[0], self.l.z.coords[1])

    def init4viz(self, pos, radius, cUnit, beaconColor, tr_pen, tr_brush):
        self.radius, self.beaconColor = radius, beaconColor
        self.tr_pen, self.tr_brush = tr_pen, tr_brush

        self.pos = pos
        self.cUnit = cUnit
        self.curPowerLevel = 0
        self.cur_transmitRange = 0

    def init4heuristic(self, battery_capacity, alpha, beta):
        self.rb, self.a, self.b = battery_capacity, alpha, beta

    def calc_transmitRange(self):
        self.cur_transmitRange = self.curPowerLevel * self.cUnit

    def draw(self, gc):
        # gc.SetPen(wx.Pen(wx.Colour(100, 100, 100), 0.9))
        gc.SetBrush(self.beaconColor)
        gc.DrawEllipse(self.pos[0] - self.radius, self.pos[1] - self.radius, self.radius * 2, self.radius * 2)
        if self.cur_transmitRange != 0:
            gc.SetPen(self.tr_pen)
            gc.SetBrush(self.tr_brush)
            gc.DrawEllipse(self.pos[0] - self.cur_transmitRange,
                           self.pos[1] - self.cur_transmitRange,
                           self.cur_transmitRange * 2, self.cur_transmitRange * 2)



class Landmark(object):
    def __init__(self, lid, z):
        self.lid, self.z = lid, z

    def __repr__(self):
        return 'lid %s (%d, %d)' % (self.lid, self.z.coords[0], self.z.coords[1])

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

    def init4viz(self, girdXPos, gridYPos, cUnit, feasibleColor):
        self.cUnit, self.feasibleColor = cUnit, feasibleColor
        halfUnit = self.cUnit / float(2)
        self.centerCoords = (girdXPos + self.i * self.cUnit + halfUnit,
                             gridYPos + self.j * self.cUnit + halfUnit)
        self.leftUpperCoords = (girdXPos + self.i * self.cUnit,
                                gridYPos + self.j * self.cUnit)
        self.leftLowerCoords = (girdXPos + self.i * self.cUnit,
                                gridYPos + (self.j + 1) * self.cUnit)
        self.rightLowerCoords = (girdXPos + (self.i + 1) * self.cUnit,
                                 gridYPos + (self.j + 1) * self.cUnit)
        self.rightUpperCoords = (girdXPos + (self.i + 1) * self.cUnit,
                                 gridYPos + self.j * self.cUnit)

    def set_landmark(self, l):
        self.landmark = l

    def add_beacon(self, b):
        self.bs += [b]

    def remove_beacon(self):
        return self.bs.pop()

    def draw(self, gc):
        if self.feasible:
            gc.SetBrush(self.feasibleColor)
            gc.DrawRectangle(self.leftUpperCoords[0], self.leftUpperCoords[1], self.cUnit, self.cUnit)
