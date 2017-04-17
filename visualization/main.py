from _configuration import floorNames
#
import wx
#
app = wx.App(False)
#
from tab import TabBase
from control import ControlPanel
#

TIMER_INTERVAL = 500  # milliseconds

class MainFrame(wx.Frame):
    def __init__(self, title="AdaptivePowerLevel", pos=(30, 30), size=(1600, 1100)):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        #
        self.timer = wx.Timer(self)
        self.timer_running = False
        #
        self.InitUI()
        self.Centre()
        self.Maximize()
        #
        self.update_tabs()
        #
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        #
        self.Show(True)

    def InitUI(self):
        basePanel = wx.Panel(self)
        basePanel.SetBackgroundColour('#4f5049')
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.controller = ControlPanel(basePanel)
        self.tabBase = TabBase(basePanel, floorNames)
        vbox.Add(self.tabBase, 8, wx.EXPAND | wx.ALL, 2)
        vbox.Add(self.controller, 1, wx.EXPAND | wx.ALL, 2)
        basePanel.SetSizer(vbox)

    def OnTimer(self, _e):
        self.controller.increase_datetime()
        self.tabBase.solveProblems()


    def startSolvingProblems(self):
        self.timer.Start(TIMER_INTERVAL)
        self.timer_running = True
        #
        self.tabBase.solveProblems()


    def pauseSolvingProblems(self):
        self.timer.Stop()
        self.timer_running = False

    def resumeSolvingProblems(self):
        self.timer.Start(TIMER_INTERVAL)
        self.timer_running = True
        self.tabBase.solveProblems()


    def OnClose(self, _e):
        if self.timer_running:
            self.timer.Stop()
        self.DestroyChildren()
        self.Destroy()


    def OnExit(self, _e):
        self.Close()

    def update_tabs(self):
        self.tabBase.update_date(self.controller.cur_datetime)


if __name__ == '__main__':
    MainFrame()
    app.MainLoop()
