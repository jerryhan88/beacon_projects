import wx,os

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, (-1, -1), wx.Size(500, 500))
        self.panel1 = wx.Panel(self, -1,style= wx.SIMPLE_BORDER)
        panel2 = wx.Panel(self, -1,style= wx.SIMPLE_BORDER)
        panel3 = wx.Panel(self, -1,style= wx.SIMPLE_BORDER)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.panel1, 1,flag = wx.EXPAND|wx.ALL,border = 3 )
        box.Add(panel2, 1,flag = wx.EXPAND|wx.ALL,border = 3 )
        box.Add(panel3, 1,flag = wx.EXPAND |wx.ALL,border = 3)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetSizer(box)

    def OnSize(self, event):
        size = self.GetSize()
        size2 = self.panel1.GetSize()
        print size,size2
        event.Skip()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'wxboxsizer.py')
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()