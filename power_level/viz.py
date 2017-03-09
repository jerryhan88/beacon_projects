import __init__
#
'''
'''
#
from power_level import prob_dpath, default_pn, default_pn_fpath
from _class import zone, beacon
import _heuristic
#
from file_handling_functions import save_pklFile, load_pklFile, get_fnOnly, check_file_exist
#
import wx
import wx.lib.buttons
from bisect import bisect

app = wx.App(False)
MARGIN = 10
WHITE = wx.Colour(255, 255, 255)
ORANGE = wx.Colour(228, 108, 10)
RED = wx.Colour(255, 0, 0)
BLACK = wx.Colour(0, 0, 0)
GRAY = wx.Colour(220, 220, 220)
DEFAULT_FONT = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
DEFAULT_BOLD_FONT = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD)
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
        self.controlPanel = self.initControls((MARGIN + px, MARGIN + py + MARGIN + sy),
                            (horizonUnit * horizonRatio[0], verticalUnit * verticalRatio[1] - 2 * MARGIN))
        #
        sx, sy = self.gridPanel.GetSize()
        chartPanel = self.initChart((MARGIN + px + MARGIN + sx, MARGIN + py),
                                    (horizonUnit * horizonRatio[1], verticalUnit * sum(verticalRatio) - MARGIN))
        chartPanel.SetBackgroundColour(RED)
        #
        if not check_file_exist(default_pn_fpath):
            self.zones = {}
            for i in range(numCols):
                for j in range(numRows):
                    self.zones[i, j] = zone(i, j, colUnit, rowUnit)
            self.beacons = {}
        else:
            self.zones = load_pklFile(default_pn_fpath)
            self.beacons = {}
            for (i, j), z in self.zones.iteritems():
                if z.hasBeacon:
                    self.beacons[i, j] = beacon(i, j, z.unitX, z.unitY)
            self.gridPanel.Refresh()
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

    def OnQuit(self, _):
        self.Destroy()

    def initControls(self, _pos, _size):
        controlPanel = wx.Panel(self.basePanel, -1, pos=_pos, size=_size)
        # controlPanel.SetBackgroundColour(purple)
        #
        btnExtendedSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        saveBtn = wx.lib.buttons.GenButton(controlPanel, label="Save")
        loadBtn = wx.lib.buttons.GenButton(controlPanel, label="Load")
        solBtn = wx.lib.buttons.GenButton(controlPanel, label="Solve")
        controlPanel.Bind(wx.EVT_BUTTON, self.probSave, saveBtn)
        controlPanel.Bind(wx.EVT_BUTTON, self.probLoad, loadBtn)
        controlPanel.Bind(wx.EVT_BUTTON, self.probSolve, solBtn)
        for btn in [saveBtn, loadBtn, solBtn]:
            btn.SetFont(DEFAULT_BOLD_FONT)
            btnSizer.Add(btn, 1, wx.ALL, MARGIN)
        # btnExtendedSizer.Add(wx.StaticText(controlPanel, -1, ''), 0.1, wx.ALL)
        btnExtendedSizer.Add(btnSizer, 2, wx.ALL)
        btnExtendedSizer.Add(wx.StaticText(controlPanel, -1, ''), 0.1, wx.ALL)
        #
        pnSizer = wx.BoxSizer(wx.VERTICAL)
        pnStatic = wx.StaticText(controlPanel, -1, 'Problem name')
        pnSizer.Add(pnStatic, 1, wx.ALL, MARGIN / 2)
        pnStatic.SetFont(DEFAULT_FONT)
        self.problemName = wx.TextCtrl(controlPanel, -1, default_pn)
        self.problemName.SetFont(DEFAULT_FONT)
        pnSizer.Add(self.problemName, 1, wx.ALL, MARGIN / 2)
        #
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(btnExtendedSizer, 2.5, wx.ALL, MARGIN)
        topSizer.Add(pnSizer, 1, wx.ALL, MARGIN)
        #
        controlPanel.SetSizer(topSizer)
        topSizer.Fit(controlPanel)
        return controlPanel

    def probSave(self, _):
        wildcard = "Pickle file (*.pkl)|*.pkl"
        openFileDialog = wx.FileDialog(self, "Choose a file", prob_dpath, self.problemName.GetValue(), wildcard, wx.SAVE | wx.OVERWRITE_PROMPT)
        if openFileDialog.ShowModal() == wx.ID_OK:
            save_pklFile(openFileDialog.GetPath(), self.zones)
        openFileDialog.Destroy()

    def probLoad(self, _):
        wildcard = "Pickle file (*.pkl)|*.pkl"
        openFileDialog = wx.FileDialog(None, "Choose a file", prob_dpath, "", wildcard, wx.OPEN)
        if openFileDialog.ShowModal() == wx.ID_OK:
            fpath = openFileDialog.GetPath()
            self.zones = load_pklFile(fpath)
            openFileDialog.Destroy()
            self.problemName.SetValue(get_fnOnly(fpath)[:-len('.pkl')])
            self.controlPanel.Refresh()
            self.gridPanel.Refresh()

    def probSolve(self, _):
        print '-----------------------------------'
        print 'run'
        self.beacons = {}
        for (i, j), z in self.zones.iteritems():
            if z.hasBeacon:
                self.beacons[i, j] = beacon(i, j, z.unitX, z.unitY)
        _heuristic.run(self.beacons, self.zones)
        self.gridPanel.Refresh()

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
        if not self.zones[i, j].isFeasible:
            self.zones[i, j].isFeasible = True
        else:
            self.zones[i, j].isFeasible = False
        self.gridPanel.Refresh()

    def OnRightClick(self, e):
        x, y = e.GetX(), e.GetY()
        i, j = bisect(self.xPoints, x) - 1, bisect(self.yPoints, y) - 1
        if not self.zones[i, j].hasBeacon:
            self.zones[i, j].hasBeacon = True
        else:
            self.zones[i, j].hasBeacon = False
        self.gridPanel.Refresh()

    def Draw(self, dc):
        dc.Clear()
        for z in self.zones.itervalues():
            z.zoneDraw(dc)
        for b in self.beacons.itervalues():
            b.rangeDraw(dc)

    def OnPaint(self, e):
        dc = wx.BufferedPaintDC(self.gridPanel)
        self.Draw(dc)



if __name__ == '__main__':
    numCols, numRows = 10, 10
    # numRows, numCols = 12, 12
    mv = beaconViewer('Viewer', numRows, numCols, pos=(200, 200), size=(1200, 600))
    mv.Show(True)
    app.MainLoop()
