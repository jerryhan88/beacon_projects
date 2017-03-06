import wx


MARGIN = 10
WHITE = wx.Colour(255, 255, 255)
ORANGE = wx.Colour(228, 108, 10)
RED = wx.Colour(255, 0, 0)
BLACK = wx.Colour(0, 0, 0)
GRAY = wx.Colour(220, 220, 220)

class zone(object):
    def __init__(self, i, j, unitX, unitY):
        self.i, self.j = i, j
        self.unitX, self.unitY = unitX, unitY
        self.halfUnitX = self.unitX / float(2)
        self.halfUnitY = self.unitY / float(2)
        self.cx, self.cy = self.i * self.unitX + self.halfUnitX, self.j * self.unitY + self.halfUnitY
        self.radius = min(self.halfUnitX, self.halfUnitY) / float(4)
        #
        self.isFeasible, self.hasBeacon = False, False
    def __repr__(self):
        return 'z(%d, %d)' % (self.i, self.j)
    def zoneDraw(self, dc):
        if self.isFeasible:
            dc.SetBrush(wx.Brush(ORANGE))
        else:
            dc.SetBrush(wx.Brush(WHITE))
        dc.DrawRectangle(self.cx - self.halfUnitX, self.cy - self.halfUnitY, self.unitX, self.unitY)
        if self.hasBeacon:
            dc.SetBrush(wx.Brush(BLACK))
            dc.DrawCircle(self.cx, self.cy, self.radius)
        dc.DrawText('%d,%d' % (self.i, self.j), self.cx, self.cy)

MAX_BP = 100

class beacon(object):
    MAX_PL = 3

    def __init__(self, i, j, unitX, unitY):
        self.i, self.j = i, j
        self.remaingBP = MAX_BP
        self.p = 0
        #
        self.unitX, self.unitY = unitX, unitY
        self.halfUnitX = self.unitX / float(2)
        self.halfUnitY = self.unitY / float(2)
        self.cx, self.cy = self.i * self.unitX + self.halfUnitX, self.j * self.unitY + self.halfUnitY

    def __repr__(self):
        return 'b(%d, %d)' % (self.i, self.j)

    def rangeDraw(self, dc):
        if self.p != 0:
            old_pen = dc.GetPen()
            old_brush = dc.GetBrush()
            dc.SetPen(wx.Pen("grey"))
            dc.SetBrush(wx.Brush("grey", wx.TRANSPARENT))
            dc.DrawCircle(self.cx, self.cy, self.p * self.unitX)
            dc.SetBrush(old_brush)
            dc.SetPen(old_pen)

class user(object):
    def __init__(self, uid, trajectory):
        self.uid, self.trajectory = uid, trajectory
    def __repr__(self):
        return 'u%d' % self.uid


