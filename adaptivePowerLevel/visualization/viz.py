import wx

from dragDropExample import DragPanel
MARGIN = 10
WHITE = wx.Colour(255, 255, 255)
RED = wx.Colour(255, 0, 0)

app = wx.App(False)



class MainFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, title="AdaptivePowerLevel", pos=(50, 50), size=(1200, 900)):
        no_resize = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |
                                                wx.RESIZE_BOX |
                                                wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, title, pos, size, no_resize)

        basePanel = wx.Panel(self, -1, pos=(0, 0), size=size)
        basePanel.SetBackgroundColour(WHITE)
        px, py = basePanel.GetPosition()
        sx, sy = basePanel.GetSize()

        horizonRatio = (1, 1)
        horizonUnit = (sx - (len(horizonRatio) + 1) * MARGIN) / sum(horizonRatio)
        verticalRatio = (4, 1)
        verticalUnit = (sy - (len(verticalRatio) + 1) * MARGIN) / sum(verticalRatio)
        self.gridPanel = self.initGrid(basePanel, (MARGIN + px, MARGIN + py),
                                       (horizonUnit * horizonRatio[0], verticalUnit * verticalRatio[0]))
        self.Show(True)

    def initGrid(self, parent, _pos, _size):
        gridPanel = wx.Panel(parent, -1, pos=_pos, size=_size)
        gridPanel.SetBackgroundColour(RED)
        nb = wx.Notebook(gridPanel, size=_size, style=wx.NB_BOTTOM)

        # create the page windows as children of the notebook
        page1 = PageOne(nb)
        page2 = PageTwo(nb)
        page3 = DragPanel(nb)
        page4 = PageTwo(nb)
        page5 = PageThree(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Page 1")
        nb.AddPage(page2, "Page 2")
        nb.AddPage(page3, "Page 3")
        nb.AddPage(page4, "Page 4")
        nb.AddPage(page5, "Page 5")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        gridPanel.SetSizer(sizer)

        return gridPanel


class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a PageOne object", (20, 20))

class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a PageTwo object", (40, 40))

class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a PageThree object", (60, 60))


if __name__ == '__main__':
    numCols, numRows = 10, 10
    # numRows, numCols = 12, 12
    MainFrame()

    app.MainLoop()