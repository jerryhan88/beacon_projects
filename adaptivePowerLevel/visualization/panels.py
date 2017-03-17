import __init__
'''
'''
from adaptivePowerLevel.visualization import MARGIN, ADJUSTMENT
from adaptivePowerLevel.visualization import PURPLE, WHITE
from adaptivePowerLevel.visualization import levelNames
from adaptivePowerLevel.visualization import DEFAULT_BOLD_FONT
#
import wx


class MainPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size)
        self.SetBackgroundColour(WHITE)
        #
        nb = wx.Notebook(self, size=self.GetSize(), style=wx.NB_BOTTOM)
        for pageName in levelNames:
            page = PagePanel(nb, self.GetSize(), pageName)
            nb.AddPage(page, pageName)
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        self.SetSizer(sizer)


class ControlPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(PURPLE)
        t = wx.StaticText(self, -1, "This is a control panel", (20, 20))

        btnExtendedSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        saveBtn = wx.lib.buttons.GenButton(self, label="Save")
        loadBtn = wx.lib.buttons.GenButton(self, label="Load")
        solBtn = wx.lib.buttons.GenButton(self, label="Solve")
        self.Bind(wx.EVT_BUTTON, self.probSave, saveBtn)
        self.Bind(wx.EVT_BUTTON, self.probLoad, loadBtn)
        self.Bind(wx.EVT_BUTTON, self.probSolve, solBtn)
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
        LayoutPanel(self, (0, 0), (lp_sx, vUnit * vsRatio[0]))
        LogPanel(self, (0, vUnit * vsRatio[0] + MARGIN), (lp_sx, vUnit * vsRatio[1]))
        ChartPanel(self, (hUnit * hsRatio[0] + MARGIN, 0), (hUnit * hsRatio[1] + MARGIN * 2, sy - ADJUSTMENT))


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
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, -1, pos=pos, size=size, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        (self.fixed_x, self.fixed_y), self.isLeftDown = (0, 0), False
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
        self.RefreshGC(False)

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
        gc.DrawLines([(0, 0), (10,10)])
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
        wx.Frame.__init__(self, parent, -1, "DragAndDrop", size=(640,480), pos=(100, 100))
        LayoutPanel(self)


if __name__ == '__main__':
    app = wx.App(False)
    frame = TestFrame(None)
    frame.Show(True)
    app.MainLoop()