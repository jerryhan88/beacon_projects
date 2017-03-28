import __init__
'''

'''
#
from visualization import MARGIN, ADJUSTMENT
from visualization import PURPLE
from visualization import DEFAULT_BOLD_FONT, BIG_FONT, SMALL_FONT
from visualization import RADIUS
from visualization import checkBoxNames, checkBoxValues, dateTimeInfo
from visualization import grid_adjustment
from _class import Zone, Beacon, Landmark
from _configuration import levelNames
#
import matplotlib.pyplot as plt
import wx
import wx.lib.buttons
from matplotlib import pyplot
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from wx import stc
from xlrd import open_workbook
#
import sys
from bisect import bisect


# logger setting
LOG_TO_CONSOLE = False  # for debugging purpose
LOGGING_LEVEL = 1
_log_out = sys.stdout


loggers = {}

class tempPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(PURPLE)
        t = wx.StaticText(self, -1, "This is a temp panel", (20, 20))


class MainPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size)
        # self.SetBackgroundColour(WHITE)
        #
        nb = wx.Notebook(self, size=self.GetSize(), style=wx.NB_BOTTOM)
        self.pages = []
        for pageName in levelNames:
            page = PagePanel(nb, self.GetSize(), pageName)
            nb.AddPage(page, pageName)
            self.pages.append(page)
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        self.SetSizer(sizer)


class ControlPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size, style=wx.SUNKEN_BORDER)
        # self.SetBackgroundColour(PURPLE)
        baseSizer = wx.BoxSizer(wx.VERTICAL)
        #
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        #
        self.tcs = {}
        for p in ['From', 'Current', 'To']:
            bs = wx.BoxSizer(wx.HORIZONTAL)
            bs.Add(wx.StaticText(self, -1, p), 1, wx.ALL)
            tc = wx.TextCtrl(self)
            tc.SetValue(dateTimeInfo[p])
            tc.Bind(wx.EVT_KEY_DOWN, self.OnEnterPressed)
            self.tcs[p] = tc
            bs.Add(tc, 1, wx.ALL)
            topSizer.Add(bs, 1, wx.ALL, MARGIN)


        baseSizer.Add(topSizer, 1)

        belowSizer = wx.BoxSizer(wx.HORIZONTAL)
        checkBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        for cb_name in checkBoxNames:
            cb = wx.CheckBox(self, -1, cb_name)
            cb.SetFont(BIG_FONT)
            checkBoxSizer.Add(cb, 1, wx.ALL, MARGIN)
            if checkBoxValues[cb_name]:
                cb.SetValue(True)
            self.Bind(wx.EVT_CHECKBOX, self.handleCheckBox, cb)
        belowSizer.Add(checkBoxSizer, 1, wx.ALL)
        #
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        loadBtn = wx.lib.buttons.GenButton(self, label='Load')
        saveBtn = wx.lib.buttons.GenButton(self, label='Save')
        runBtn = wx.lib.buttons.GenButton(self, label='Run')
        self.Bind(wx.EVT_BUTTON, self.probLoad, loadBtn)
        self.Bind(wx.EVT_BUTTON, self.probSave, saveBtn)
        self.Bind(wx.EVT_BUTTON, self.runHeruistic, runBtn)
        for btn in [saveBtn, loadBtn, runBtn]:
            btn.SetFont(DEFAULT_BOLD_FONT)
            btnSizer.Add(btn, 1, wx.ALL, MARGIN)
        belowSizer.Add(btnSizer, 1, wx.ALL)
        baseSizer.Add(belowSizer, 2)
        #
        self.SetSizer(baseSizer)
        baseSizer.Fit(self)

    def handleCheckBox(self, e):
        ce = e.GetEventObject()
        l = ce.GetLabelText()
        print l
        if checkBoxValues[l]:
            checkBoxValues[l] = False
        else:
            checkBoxValues[l] = True
        for p in self.Parent.mainPanel.pages:
            p.background_update()
    def OnEnterPressed(self, e):
        keycode = e.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER or keycode == wx.WXK_TAB:
            print 'Enter!!'
            for p in ['From', 'Current', 'To']:
                print self.tcs[p].GetValue()
                dateTimeInfo[p] = self.tcs[p].GetValue()
                # TODO
                # Refresh!!
        e.Skip()


    def probLoad(self):
        print 'problem loading'

    def probSave(self):
        print 'problem saving'

    def runHeruistic(self):
        print 'run Heuristic'


class PagePanel(wx.Panel):
    def __init__(self, parent, size, pageName):
        wx.Panel.__init__(self, parent, size=size)
        sx, sy = self.GetSize()
        hsRatio = (2, 1)
        hUnit = (sx - (len(hsRatio) + 1) * MARGIN) / sum(hsRatio)
        lp_sx, lp_sy = hUnit * hsRatio[0], sy - ADJUSTMENT
        vsRatio = (4, 1)
        vUnit = (lp_sy - MARGIN) / sum(vsRatio)
        #
        self.logger = None
        self.log_view = LogView(self, (0, vUnit * vsRatio[0] + MARGIN), (lp_sx + 4, vUnit * vsRatio[1] + 4))
        if not LOG_TO_CONSOLE:
            self.logger = self.log_view
        else:
            self.logger = _log_out
        loggers[pageName] = self.logger
        self.layout_view = LayoutView(self, (0, 0), (lp_sx, vUnit * vsRatio[0]), pageName)
        ChartPanel(self, (hUnit * hsRatio[0] + MARGIN, 0), (hUnit * hsRatio[1] + MARGIN * 2, sy - ADJUSTMENT))


    def background_update(self):
        self.layout_view.RefreshGC()

    def write_log(self, s, lvl=0):
        if self.logger:
            self.logger.write(s)


class LogView(stc.StyledTextCtrl):
    def __init__(self, parent, pos, size):
        stc.StyledTextCtrl.__init__(self, parent, pos=pos, size=size, style=wx.SUNKEN_BORDER)

    def write(self, s):
        self.AddText(s)
        self.ScrollToLine(self.GetLineCount())

from random import random

class LineChart(object):
    def __init__(self, subplot_pos, cName):
        self.axes = plt.subplot(*subplot_pos)
        self.axes.set_facecolor('white')
        self.axes.set_title(cName, fontsize=11)
        plt.plot([1, 2, 3], [random() for _ in xrange(3)], linewidth=1)
        plt.plot([1, 2, 3], [random() for _ in xrange(3)], linewidth=1)


class ChartPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(PURPLE)
        self.sizer = wx.GridSizer(4, 1, 0, 0)
        self.SetSizer(self.sizer)
        # self.sizer.Add(wx.StaticText(self, -1, "This is a chart panel"), 0, wx.EXPAND)

        chart, canvas = self.create_chart('C1')
        self.sizer.Add(canvas, 0, wx.EXPAND)
        chart, canvas = self.create_chart('C2')
        self.sizer.Add(canvas, 0, wx.EXPAND)
        chart, canvas = self.create_chart('C3')
        self.sizer.Add(canvas, 0, wx.EXPAND)
        chart, canvas = self.create_chart('C4')
        self.sizer.Add(canvas, 0, wx.EXPAND)


        #
        # self.sizer.Add(wx.StaticText(self, -1, "This is a chart panel"), 0, wx.EXPAND)
        # self.sizer.Add(wx.StaticText(self, -1, "This is a chart panel"), 0, wx.EXPAND)
        # self.sizer.Add(wx.StaticText(self, -1, "This is a chart panel"), 0, wx.EXPAND)
        self.SendSizeEvent()

    def create_chart(self, cName):
        fig = pyplot.figure()
        fig.set_facecolor('white')
        # create chart following a chart type.
        chart = LineChart((1, 1, 1), cName)
        return chart, FigureCanvasWxAgg(self, wx.ID_ANY, fig)


class LayoutView(wx.Panel):
    def __init__(self, parent, pos, size, pageName):
        wx.Panel.__init__(self, parent, -1, pos=pos, size=size, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        (self.fixed_x, self.fixed_y), self.isLeftDown = (0, 0), False
        self.grid = Grid(pageName)
        # event binding
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        # prepare stock objects.
        self.default_pen = self.create_pen(wx.BLACK, 1)
        self.default_font = self.create_font(8, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        # initialize a buffer
        w, h = self.GetSize()
        w, h = max(100, w), max(100, h)
        self.mem_buffer = wx.EmptyBitmap(w, h, 32)
        # initialize a background
        self.init_background(pageName)
        self.RefreshGC(False)

    def init_background(self, pageName):
        self.bg_bmps, self.scale = {}, None
        for i, img_name in enumerate(['Base', 'Landmark', 'Room', 'Section']):
            img_path = '../z_src/%s_%s.png' % (pageName, img_name)
            img = wx.Image(img_path)
            assert img, 'Fail to load image "%s"' % img_path
            if i == 0:
                # set scale
                pWidth, pHeight = self.GetSize()
                iWidth, iHeight = img.GetWidth(), img.GetHeight()
                wScale = pWidth / float(iWidth)
                hSacle = pHeight / float(iHeight)
                self.scale = min(wScale, hSacle)
                assert self.scale, 'Fail to set scale'
            bmp = wx.BitmapFromImage(img.AdjustChannels(1.0, 1.0, 1.0, 1.0))
            w, h = bmp.GetWidth() * self.scale, bmp.GetHeight() * self.scale
            self.bg_bmps[img_name] = (bmp, w, h)

    def create_pen(self, color, width):
        return wx.Pen(color, width)

    def create_font(self, size, family, style, weight):
        return wx.Font(size, family, style, weight)

    def OnPaint(self, _):
        wx.BufferedPaintDC(self, self.mem_buffer)

    def RefreshGC(self, update=True):
        mdc = wx.MemoryDC(self.mem_buffer)
        mdc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        mdc.Clear()
        gc = wx.GraphicsContext.Create(mdc)
        gc.SetPen(self.default_pen)
        gc.SetFont(self.default_font, wx.BLACK)
        self.OnDraw(gc)
        #
        self.Refresh(False)

    def OnDraw(self, gc):
        # draw background image
        base_bmp, w, h = self.bg_bmps['Base']
        gc.DrawBitmap(base_bmp, 0, 0, w, h)
        for cb_name in checkBoxNames:
            if cb_name == 'Grid' or cb_name == 'Landmark2':
                continue
            if checkBoxValues[cb_name]:
                bmp, w, h = self.bg_bmps[cb_name]
                gc.DrawBitmap(bmp, 0, 0, w, h)
        if checkBoxValues['Grid']:
            self.grid.draw(gc)

    def OnLeftDown(self, e):
        self.grid.pick_beacon(e.GetX(), e.GetY())
        self.isLeftDown = True
        self.SetFocus()
        self.CaptureMouse()

    def OnMotion(self, e):
        if self.isLeftDown:
            cur_x, cur_y = e.GetX(), e.GetY()
            self.grid.update_pickedBeaconPos(e.GetX(), e.GetY())
            self.RefreshGC()

    def OnLeftUp(self, e):
        if self.isLeftDown:
            self.isLeftDown = False
            self.grid.drop_beacon(e.GetX(), e.GetY())
            self.ReleaseMouse()
            self.RefreshGC()


class Grid(object):
    def __init__(self, floor):
        self.logger = loggers[floor]
        self.xPos, self.yPos, self.wUnit, self.hUnit = grid_adjustment[floor]
        #
        book = open_workbook('../z_data/Landmark.xlsx')
        sh = book.sheet_by_name('%s' % (floor))
        self.xPoints = [self.xPos + i * self.wUnit for i in range(sh.ncols)]
        self.yPoints = [self.yPos + j * self.hUnit for j in range(sh.nrows)]
        self.nRows, self.nCols = (sh.nrows - 1), (sh.ncols - 1)
        # About zones and landmarks
        self.zones, self.landmarks = {}, {}

        # Load pickle files such as zones, landmarks, Uzk, Zf!!
        # And visualize Zf!!
        # Also load beacons's position
        #    Before doing it, preprocess data!!


        for i in xrange(sh.nrows):
            for j in xrange(sh.ncols):
                if i < 1 or j < 1:
                    continue
                coords = j - 1, i - 1
                z = Zone(coords)
                z.init4viz(self.xPos, self.yPos, self.wUnit, self.hUnit)
                self.zones[coords] = z
                if sh.cell(i, j).value:
                    lid = int(sh.cell(i, j).value)
                    l = Landmark(lid, z)
                    l.init4viz((self.xPos + coords[0] * self.wUnit + self.wUnit * 0.5 - RADIUS / float(2),
                                self.yPos + coords[1] * self.hUnit + self.hUnit * 0.5 - RADIUS / float(2)))
                    self.landmarks[lid] = l
                    z.set_landmark(l)
        # About beacons
        floor_format = '0' + floor[len('Lv'):] + '0'
        self.beacons = {}
        book = open_workbook('../z_data/BeaconLocation.xlsx')
        sh = book.sheet_by_name('BriefRepresentation')
        for i in range(1, sh.nrows):
            locationID, landmarkID = map(str, map(int, [sh.cell(i, 0).value, sh.cell(i, 1).value]))
            entity = landmarkID[:1]
            building = landmarkID[1:3]
            lv = landmarkID[3:6]
            lm = landmarkID[6:]
            if floor_format == lv:
                matched_lm = self.landmarks[int(lm)]
                b = Beacon(int(locationID), matched_lm.z.coords, matched_lm.pos)
                self.beacons[int(locationID)] = b
                z = self.zones[matched_lm.z.coords]
                z.set_beacon(b)
        self.picked_beacon = None

    def write_log(self, s):
        self.logger.write(s)

    def pick_beacon(self, x, y):
        if x < self.xPoints[0] or x > self.xPoints[-1]:
            self.write_log('outside of grid\n')
            return None
        if y < self.yPoints[0] or y > self.yPoints[-1]:
            self.write_log('outside of grid\n')
            return None
        #
        i, j = bisect(self.xPoints, x) - 1, bisect(self.yPoints, y) - 1
        z = self.zones[i, j]
        if z.beacon:
            self.picked_beacon = z.beacon
            self.write_log('picked beacon %s\n' % z.beacon)
            z.remove_beacon()
        else:
            self.write_log('no beacon in the zone\n')

    def update_pickedBeaconPos(self, x, y):
        if not self.picked_beacon:
            self.write_log('there is no picked beacon\n')
            return None
        self.picked_beacon.pos = (x, y)

    def drop_beacon(self, x, y):
        if not self.picked_beacon:
            # self.write_log('there is no picked beacon\n')
            return None
        if x < self.xPoints[0] or x > self.xPoints[-1]:
            self.write_log('outside of grid\n')
            self.return_original_location()
            return None
        if y < self.yPoints[0] or y > self.yPoints[-1]:
            self.write_log('outside of grid\n')
            self.return_original_location()
            return None
        i, j = bisect(self.xPoints, x) - 1, bisect(self.yPoints, y) - 1
        z = self.zones[i, j]
        if z.beacon:
            self.write_log('there is another beacon\n')
            self.return_original_location()
            return None
        else:
            self.write_log('relocate the beacon to zone %s\n' % z)
            self.picked_beacon.coords = z.coords
            self.picked_beacon.pos = z.centerCoords
            z.beacon = self.picked_beacon
            self.picked_beacon = None

    def return_original_location(self):
        self.write_log('return beacon to the original location\n')
        ori_z = self.zones[self.picked_beacon.coords]
        self.picked_beacon.pos = ori_z.centerCoords
        ori_z.set_beacon(self.picked_beacon)
        self.picked_beacon = None

    def draw(self, gc):
        # gc.DrawRectangle(self.xPos, self.yPox, self.nCols * self.wUnit, self.nRows * self.hUnit)

        for i in xrange(self.nRows + 1):
            gc.DrawLines([(self.xPos, self.yPos + i * self.hUnit),
                          (self.xPos + self.nCols * self.wUnit, self.yPos + i * self.hUnit)])

        for j in xrange(self.nCols + 1):
            gc.DrawLines([(self.xPos + j * self.wUnit, self.yPos),
                          (self.xPos + j * self.wUnit, self.yPos + self.nRows * self.hUnit)])





        if checkBoxValues['Landmark2']:
            for l in self.landmarks.itervalues():
                l.draw(gc, SMALL_FONT, RADIUS)
        for b in self.beacons.itervalues():
            b.draw(gc, RADIUS)


class TestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "DragAndDrop", size=(640, 480), pos=(100, 100))
        LayoutView(self)



if __name__ == '__main__':
    app = wx.App(False)
    frame = TestFrame(None)
    frame.Show(True)
    app.MainLoop()