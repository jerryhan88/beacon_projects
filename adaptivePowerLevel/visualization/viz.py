import __init__
'''

'''
from adaptivePowerLevel.visualization import MARGIN
from adaptivePowerLevel.visualization import BLUE
from panels import MainPanel, ControlPanel
#
import wx
#
app = wx.App(False)


class MainFrame(wx.Frame):
    def __init__(self, title="AdaptivePowerLevel", pos=(30, 30), size=(1500, 1000)):
        no_resize = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |
                                                wx.RESIZE_BOX |
                                                wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, title, pos, size, no_resize)
        basePanel = wx.Panel(self, -1, pos=(0, 0), size=size)
        basePanel.SetBackgroundColour(BLUE)
        sx, sy = basePanel.GetSize()
        vsRatio = (11, 1)
        vUnit = (sy - (len(vsRatio) + 1) * MARGIN) / sum(vsRatio)
        #
        MainPanel(basePanel, (MARGIN, MARGIN), (sx - 2 * MARGIN, vUnit * vsRatio[0]))

        ControlPanel(basePanel, (MARGIN, MARGIN + vUnit * vsRatio[0] + MARGIN),
                    (sx - 2 * MARGIN, vUnit * vsRatio[1] - MARGIN))
        #
        self.Show(True)


if __name__ == '__main__':
    MainFrame()
    app.MainLoop()
