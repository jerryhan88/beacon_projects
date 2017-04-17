import wx


class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(250, 150))
        self.InitUI()

    def InitUI(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.sld = wx.Slider(pnl, value=10, minValue=1, maxValue=100,
                             style=wx.SL_HORIZONTAL)

        vbox.Add(self.sld, 1, flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=20)
        self.sld.Bind(wx.EVT_SLIDER, self.OnSliderScroll)
        self.curDateTime = wx.StaticText(pnl, label='Hello', style=wx.ALIGN_CENTER)
        vbox.Add(self.curDateTime, 1, wx.ALIGN_CENTRE_HORIZONTAL)

        pnl.SetSizer(vbox)
        self.Centre()
        self.Show(True)

    def OnSliderScroll(self, e):
        obj = e.GetEventObject()
        val = obj.GetValue()
        font = self.GetFont()
        font.SetPointSize(self.sld.GetValue())
        self.curDateTime.SetFont(font)


ex = wx.App()
Mywin(None, 'Slider demo')
ex.MainLoop()