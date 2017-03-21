import __init__

'''
'''
from adaptivePowerLevel.visualization import MARGIN, ADJUSTMENT
from adaptivePowerLevel.visualization import PURPLE, WHITE
from adaptivePowerLevel.visualization import levelNames
#
import wx
import wx.lib.buttons

DEFAULT_FONT = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
SMALL_FONT = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
BIG_FONT = wx.Font(18, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
DEFAULT_BOLD_FONT = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD)
checkBoxNames = ['Section', 'Room', 'Landmark', 'Landmark2', 'Grid']
checkBoxValues = {cb_name: False for cb_name in checkBoxNames}

# checkBoxValues['Landmark'] = True
# checkBoxValues['Landmark2'] = True
checkBoxValues['Grid'] = True


class tempPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(PURPLE)
        t = wx.StaticText(self, -1, "This is a temp panel", (20, 20))


class MainPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size)
        self.SetBackgroundColour(WHITE)
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
        baseSizer = wx.BoxSizer(wx.HORIZONTAL)
        #
        checkBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        for cb_name in checkBoxNames:
            cb = wx.CheckBox(self, -1, cb_name)
            cb.SetFont(BIG_FONT)
            checkBoxSizer.Add(cb, 1, wx.ALL, MARGIN)
            if checkBoxValues[cb_name]:
                cb.SetValue(True)
            self.Bind(wx.EVT_CHECKBOX, self.handleCheckBox, cb)
        baseSizer.Add(checkBoxSizer, 1, wx.ALL)

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
        baseSizer.Add(btnSizer, 1, wx.ALL)
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
        self.layoutPanel = LayoutPanel(self, (0, 0), (lp_sx, vUnit * vsRatio[0]), pageName)
        LogPanel(self, (0, vUnit * vsRatio[0] + MARGIN), (lp_sx, vUnit * vsRatio[1]))
        ChartPanel(self, (hUnit * hsRatio[0] + MARGIN, 0), (hUnit * hsRatio[1] + MARGIN * 2, sy - ADJUSTMENT))

    def background_update(self):
        self.layoutPanel.RefreshGC()


class LogPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(PURPLE)
        t = wx.StaticText(self, -1, "This is a log panel", (20, 20))


class ChartPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(PURPLE)
        t = wx.StaticText(self, -1, "This is a chart panel", (20, 20))


class LayoutPanel(wx.Panel):
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

        gc.DrawLines([(0, 0), (10, 10)])
        gc.DrawRectangle(10, 10, 10, 10)

    def OnLeftDown(self, e):
        self.isLeftDown, self.fixed_x, self.fixed_y = True, e.GetX(), e.GetY()
        self.SetFocus()
        self.CaptureMouse()

    def OnMotion(self, e):
        if self.isLeftDown:
            cur_x, cur_y = e.GetX(), e.GetY()
            print cur_x, cur_y
            self.RefreshGC()

    def OnLeftUp(self, _):
        if self.isLeftDown:
            self.isLeftDown = False
            self.ReleaseMouse()


class TestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "DragAndDrop", size=(640, 480), pos=(100, 100))
        LayoutPanel(self)


from xlrd import open_workbook

grid_adjustment = {}
grid_adjustment['Lv1'] = (161, 206, 23, 17)
grid_adjustment['Lv2'] = (50, 50, 19, 13)
grid_adjustment['Lv3'] = (50, 51, 21, 18)
grid_adjustment['Lv4'] = (81, 80, 23, 24)
grid_adjustment['Lv5'] = (81, 80, 24, 26)

RADIUS = 2


class Grid(object):
    def __init__(self, floor):
        self.xPos, self.yPos, self.wUnit, self.hUnit = grid_adjustment[floor]

        book = open_workbook('../z_data/Landmark.xlsx')
        sh = book.sheet_by_name('%s' % (floor))
        self.nRows, self.nCols = (sh.nrows - 1), (sh.ncols - 1)
        # About landmarks
        self.landmarks = {}
        for i in xrange(sh.nrows):
            for j in xrange(sh.ncols):
                if i < 1 or j < 1:
                    continue
                if sh.cell(i, j).value:
                    lid = int(sh.cell(i, j).value)
                    coords = i - 1, j - 1
                    self.landmarks[lid] = Landmark(lid,
                                                    coords,
                                  (self.xPos + coords[1] * self.wUnit + self.wUnit * 0.5 - RADIUS / float(2),
                                   self.yPos + coords[0] * self.hUnit + self.hUnit * 0.5 - RADIUS / float(2)))
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
            print entity, building, lv, lm
            if floor_format == lv:
                matched_lm = self.landmarks[int(lm)]
                self.beacons[int(locationID)] = Beacon(int(locationID), matched_lm.coords, matched_lm.pos)
        print self.beacons


    def draw(self, gc):
        # gc.DrawRectangle(self.xPos, self.yPox, self.nCols * self.wUnit, self.nRows * self.hUnit)

        for i in xrange(self.nRows + 1):
            gc.DrawLines([(self.xPos, self.yPos + i * self.hUnit),
                          (self.xPos + self.nCols * self.wUnit, self.yPos + i * self.hUnit)])

        for j in xrange(self.nCols + 1):
            gc.DrawLines([(self.xPos + j * self.wUnit, self.yPos),
                          (self.xPos + j * self.wUnit, self.yPos + self.nRows * self.hUnit)])

        for l in self.landmarks.itervalues():
            l.draw(gc)
        for b in self.beacons.itervalues():
            b.draw(gc)

class Beacon(object):
    def __init__(self, bid, coords=None, pos=None):
        self.bid, self.coords, self.pos = bid, coords, pos

    def __repr__(self):
        return 'bid %d (%d, %d)' % (self.bid, self.coords[0], self.coords[1])

    def draw(self, gc):
        # if checkBoxValues['Landmark2']:
        #     gc.SetFont(SMALL_FONT)
        #     gc.DrawText('%d' % self.lid, self.pos[0] + 1, self.pos[1] + 1)
        gc.DrawEllipse(self.pos[0] - RADIUS, self.pos[1] - RADIUS, RADIUS * 2, RADIUS * 2)

class Landmark(object):
    def __init__(self, lid, coords=None, pos=None):
        self.lid, self.coords, self.pos = lid, coords, pos

    def __repr__(self):
        return 'lid %d (%d, %d)' % (self.lid, self.coords[0], self.coords[1])

    def draw(self, gc):
        if checkBoxValues['Landmark2']:
            gc.SetFont(SMALL_FONT)
            gc.DrawText('%d' % self.lid, self.pos[0] + 1, self.pos[1] + 1)
            gc.DrawEllipse(self.pos[0], self.pos[1], RADIUS, RADIUS)


if __name__ == '__main__':
    app = wx.App(False)
    frame = TestFrame(None)
    frame.Show(True)
    app.MainLoop()