from bisect import bisect
import wx
import wx.lib.buttons

MARGIN = 10
WHITE = wx.Colour(255, 255, 255)
ORANGE = wx.Colour(228, 108, 10)
RED = wx.Colour(255, 0, 0)
BLACK = wx.Colour(0, 0, 0)
GRAY = wx.Colour(220, 220, 220)
#

purple = wx.Colour(115, 28, 96)
dark_sky = wx.Colour(189, 207, 231)

blue = wx.Colour(0, 0, 255)
sky = wx.Colour(222, 239, 247)
light_orange = wx.Colour(248, 238, 211)
dark_orange = wx.Colour(238, 108, 0)

class beaconViewer(wx.Frame):
    def __init__(self, title, numRows, numCols, pos, size):
        no_resize = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |
                                                wx.RESIZE_BOX |
                                                wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, title, pos, size, no_resize)
        self.basePanel = wx.Panel(self, -1, pos=(0, 0), size=size)
        self.basePanel.SetBackgroundColour(WHITE)
        px, py = self.basePanel.GetPosition()
        sx, sy = self.basePanel.GetSize()
        #
        horizonRatio = (1, 1)
        horizonUnit = (sx - (len(horizonRatio) + 1) * MARGIN) / sum(horizonRatio)
        verticalRatio = (4, 1)
        verticalUnit = (sy - (len(verticalRatio) + 1) * MARGIN) / sum(verticalRatio)
        self.gridPanel = self.initGrid((MARGIN + px, MARGIN + py),
                                       (horizonUnit * horizonRatio[0], verticalUnit * verticalRatio[0]))
        sx, sy = self.gridPanel.GetSize()
        colUnit = sx / float(numCols)
        rowUnit = sy / float(numRows)
        self.xPoints, self.yPoints = [i * colUnit for i in range(numCols)], [j * rowUnit for j in range(numRows)]
        #
        sx, sy = self.gridPanel.GetSize()
        self.initControls((MARGIN + px, MARGIN + py + MARGIN + sy),
                          (horizonUnit * horizonRatio[0], verticalUnit * verticalRatio[1] - 2 * MARGIN))
        #
        sx, sy = self.gridPanel.GetSize()
        chartPanel = self.initChart((MARGIN + px + MARGIN + sx, MARGIN + py),
                                    (horizonUnit * horizonRatio[1], verticalUnit * sum(verticalRatio) - MARGIN))
        chartPanel.SetBackgroundColour(RED)
        #
        self.zones = {}
        for i in range(numCols):
            for j in range(numRows):
                self.zones[i, j] = zone(i, j, colUnit, rowUnit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

    def OnQuit(self, _):
        self.Destroy()

    def initControls(self, _pos, _size):
        controlPanel = wx.Panel(self.basePanel, -1, pos=_pos, size=_size)
        controlPanel.SetBackgroundColour(purple)
        #
        sx, sy = controlPanel.GetSize()
        bSx, bSy = sx / float(3), sy / float(2)
        qx, cy = sx / float(4), sy / float(2)

        solBtn = wx.lib.buttons.GenButton(controlPanel, label="solve", pos=(qx - bSx / 2, cy - bSy / 2), size=(bSx, bSy))
        solBtn.SetFont(wx.Font(bSy / 2, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        solBtn.SetBackgroundColour(GRAY)
        controlPanel.Bind(wx.EVT_BUTTON, self.runHeuristic, solBtn)

    def runHeuristic(self, _):
        print 'run'

    def initGrid(self, _pos, _size):
        gridPanel = wx.Panel(self.basePanel, -1, pos=_pos, size=_size)
        #
        gridPanel.Bind(wx.EVT_PAINT, self.OnPaint)
        gridPanel.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
        gridPanel.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        return gridPanel


    def initChart(self, _pos, _size):
        return wx.Panel(self.basePanel, -1, pos=_pos, size=_size)

    def OnLeftClick(self, e):
        x, y = e.GetX(), e.GetY()
        i, j = bisect(self.xPoints, x) - 1, bisect(self.yPoints, y) - 1
        # print x, y, i, j
        if not self.zones[i, j].isFeasible:
            self.zones[i, j].isFeasible = True
        else:
            self.zones[i, j].isFeasible = False
        self.gridPanel.Refresh()

    def OnRightClick(self, e):
        x, y = e.GetX(), e.GetY()
        i, j = bisect(self.xPoints, x) - 1, bisect(self.yPoints, y) - 1
        # print 'right', x, y, i, j
        if not self.zones[i, j].hasBeacon:
            self.zones[i, j].hasBeacon = True
        else:
            self.zones[i, j].hasBeacon = False
        self.gridPanel.Refresh()


    def Draw(self, dc):
        dc.Clear()
        for z in self.zones.itervalues():
            z.zoneDraw(dc)

    def OnPaint(self, e):
        dc = wx.BufferedPaintDC(self.gridPanel)
        self.Draw(dc)


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

    def zoneDraw(self, dc):
        if self.isFeasible:
            dc.SetBrush(wx.Brush(ORANGE))
        else:
            dc.SetBrush(wx.Brush(WHITE))
        dc.DrawRectangle(self.cx - self.halfUnitX, self.cy - self.halfUnitY, self.unitX, self.unitY)
        if self.hasBeacon:
            dc.SetBrush(wx.Brush(BLACK))
            dc.DrawCircle(self.cx, self.cy, self.radius)



if __name__ == '__main__':
    app = wx.App(False)
    numRows, numCols = 10, 12
    mv = beaconViewer('Viewer', numRows, numCols, pos=(200, 200), size=(1200, 600))
    mv.Show(True)
    app.MainLoop()
