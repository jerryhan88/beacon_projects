import wx

MARGIN = 10

########################################################################
class RandomPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, color):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, _):
        print self.GetSize()

class RandomPanel1(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, color):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, _):
        print self.GetSize()

        nb = wx.Notebook(self, style=wx.NB_BOTTOM)

        # create the page windows as children of the notebook
        page1 = PageOne(nb)
        page2 = PageTwo(nb)
        page3 = PageThree(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Page 1")
        nb.AddPage(page2, "Page 2")
        nb.AddPage(page3, "Page 3")

        sizer1 = wx.BoxSizer()
        sizer1.Add(nb, 1, wx.EXPAND)
        self.SetSizer(sizer1)
        self.Refresh()

########################################################################
class MainPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, color):
        """Constructor"""
        wx.Panel.__init__(self, parent, size=parent.GetSize())
        self.SetBackgroundColour(color)

        panelOne = RandomPanel(self, "green")
        panelTwo = RandomPanel(self, "red")

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(panelOne, 2, wx.EXPAND|wx.ALL, MARGIN)
        sizer.Add(panelTwo, 1, wx.EXPAND|wx.ALL, MARGIN)
        self.SetSizer(sizer)

class textPanel(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        base_panel = wx.Panel(self)
        base_panel.SetBackgroundColour('blue')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(base_panel, 1, wx.EXPAND | wx.ALL, MARGIN)
        # self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetSizer(sizer)

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



########################################################################
class MainFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, title="AdaptivePowerLevel", pos=(50, 50), size=(1200, 900)):
        no_resize = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER |
                                                wx.RESIZE_BOX |
                                                wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, title, pos, size, no_resize)




        self.mainPanel = RandomPanel1(self, "blue")


        sizer = wx.BoxSizer(wx.VERTICAL)

        self.controlPanel = RandomPanel(self, "green")
        sizer.Add(self.mainPanel, 9, wx.EXPAND | wx.ALL, MARGIN)
        sizer.Add(self.controlPanel, 1, wx.EXPAND|wx.ALL, MARGIN)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetSizer(sizer)
        print 'after2'
        self.Show()


    def OnSize(self, event):
        size = self.GetSize()
        print size
        print
        # size2 = self.panel1.GetSize()
        # print size, size2
        event.Skip()




# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()