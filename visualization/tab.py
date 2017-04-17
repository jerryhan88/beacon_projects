from logger import LogView, choose_logger
from scene import LayoutView
from chart import ChartView

import wx

class TabBase(wx.Panel):
    def __init__(self, parent, floorNames):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.WHITE)
        #
        nb = wx.Notebook(self, size=self.GetSize(), style=wx.NB_BOTTOM)
        self.tabs = []
        for floorName in floorNames:
            tab = Floor(nb, self.GetSize(), floorName)
            nb.AddPage(tab, floorName)
            self.tabs.append(tab)
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def update_date(self, cur_datetime):
        for t in self.tabs:
            t.update_date(cur_datetime)

    def solveProblems(self):
        for t in self.tabs:
            t.iterativeSolving()




P = 60  # The maximum power level
K = 4  # The number of time slots
alpha, beta = 1, 1
INIT_BATTERY_CAPA = P * 9 * 10  # Maximum power level * hours in a day * days in a month (except weekends)
N = 10  # The number of candidate solutions
MIN_POWER_LEVEL = 1


class Floor(wx.Panel):
    def __init__(self, parent, size, floorName):
        wx.Panel.__init__(self, parent, size=size)
        self.InitUI(floorName)
        #
        self.cur_datetime = None

    def InitUI(self, floorName):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.layout_view = LayoutView(self, floorName)
        hbox.Add(self.layout_view, 15, wx.EXPAND | wx.ALL, 1)
        self.layout_view.grid.initProblem(INIT_BATTERY_CAPA, alpha, beta, P, MIN_POWER_LEVEL)
        #
        self.chart_view = ChartView(self, self.layout_view.grid.measures_APL,
                                    (self.layout_view.grid.measures_F10,
                                     self.layout_view.grid.measures_F20,
                                     self.layout_view.grid.measures_F30))
        hbox.Add(self.chart_view, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(hbox)

    def update_date(self, cur_datetime):
        self.cur_datetime = cur_datetime
        self.layout_view.update_date(cur_datetime)

    def iterativeSolving(self):
        self.layout_view.grid.iterativeSolving(self.cur_datetime)
        self.chart_view.refresh_charts()