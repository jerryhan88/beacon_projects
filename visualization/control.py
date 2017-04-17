import __init__
'''

'''
#
from _configuration import Zf_dpath
from supporting_modules.file_handling_functions import get_all_files
#
from datetime import datetime
import wx
import wx.lib.buttons
from visualization import DEFAULT_FONT, DEFAULT_BOLD_FONT, BIG_FONT, BIG_BOLD_FONT


class ControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.WHITE)
        self.mainFrame = self.Parent.Parent
        self.from_date, self.to_date = None, None
        dates = set()
        hours = set()
        for fn in get_all_files(Zf_dpath, '*.pkl'):
            _, _, _date, H = fn[:-len('.pkl')].split('-')
            year, month, day = map(int, (_date[:-len('mmdd')], _date[len('yyyy'):-len('dd')], _date[len('yyyymm'):]))
            hour = int(H[len('H'):])
            dates.add((year, month, day))
            hours.add(hour)
        self.datetimes = []
        for year, month, day in sorted(list(dates)):
            for hour in hours:
                self.datetimes += [datetime(year, month, day, hour)]
        self.first_datetime, self.last_datetime = self.datetimes[0], self.datetimes[-1]
        self.cur_datetime = self.datetimes[0]
        self.InitUI()

    def InitUI(self):
        baseBox = wx.BoxSizer(wx.VERTICAL)
        #
        # DateTime Controller
        #
        dateTimeControllerBox = wx.BoxSizer(wx.HORIZONTAL)
        self.sld = wx.Slider(self,
                             value=self.datetimes.index(self.cur_datetime),
                             minValue=self.datetimes.index(self.first_datetime),
                             maxValue=self.datetimes.index(self.last_datetime),
                             style=wx.SL_HORIZONTAL)
        st_fdt = wx.StaticText(self,
                      label='%02d/%02d/%d' % (
                      self.first_datetime.day, self.first_datetime.month, self.first_datetime.year),
                      style=wx.ALIGN_CENTER)
        st_fdt.SetFont(DEFAULT_FONT)
        dateTimeControllerBox.Add(st_fdt, 1, wx.EXPAND| wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=10)
        dateTimeControllerBox.Add(self.sld, 10, wx.EXPAND, border=10)
        st_ldt = wx.StaticText(self,
                      label='%02d/%02d/%d' % (
                      self.last_datetime.day, self.last_datetime.month, self.last_datetime.year),
                      style=wx.ALIGN_CENTER)
        st_ldt.SetFont(DEFAULT_FONT)
        dateTimeControllerBox.Add(st_ldt, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, border=10)
        baseBox.Add(dateTimeControllerBox, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP)
        self.st_cur_datetime = wx.StaticText(self,
                                             label='%02d/%02d/%d:H%02d' % (self.cur_datetime.day, self.cur_datetime.month, self.cur_datetime.year, self.cur_datetime.hour),
                                             style=wx.ALIGN_CENTER)
        self.st_cur_datetime.SetFont(BIG_BOLD_FONT)
        baseBox.Add(self.st_cur_datetime, 1, wx.ALIGN_CENTRE_HORIZONTAL)
        #
        # bottomBox = wx.BoxSizer(wx.HORIZONTAL)
        gs = wx.GridSizer(1, 4, 5, 5)
        #
        # File selection for beacon's configuration
        #
        BC_Box = wx.BoxSizer(wx.HORIZONTAL)
        self.beaconConf_fn = wx.StaticText(self, label='Beacon configuration file: default.bcc', style=wx.ALIGN_CENTER)
        self.beaconConf_fn.SetFont(DEFAULT_FONT)
        BC_Box.Add(self.beaconConf_fn, 5, wx.ALIGN_CENTER | wx.TOP, border=5)
        loadBtn = wx.lib.buttons.GenButton(self, label='Load')
        saveBtn = wx.lib.buttons.GenButton(self, label='Save')
        for btn in [saveBtn, loadBtn]:
            btn.SetFont(DEFAULT_BOLD_FONT)
            BC_Box.Add(btn, 1, wx.ALL, border=1)
        #
        # Reset and Heuristic run
        #
        RH_Box = wx.BoxSizer(wx.HORIZONTAL)
        resetBtn = wx.lib.buttons.GenButton(self, label='Reset')
        runBtn = wx.lib.buttons.GenButton(self, label='Run')
        pauseBtn = wx.lib.buttons.GenButton(self, label='Pause')
        resumeBtn = wx.lib.buttons.GenButton(self, label='Resume')
        for btn in [resetBtn, runBtn, pauseBtn, resumeBtn]:
            btn.SetFont(DEFAULT_BOLD_FONT)
            RH_Box.Add(btn, 1, border=1)
        #
        gs.AddMany([BC_Box, (wx.StaticText(self), wx.EXPAND), (wx.StaticText(self), wx.EXPAND), RH_Box])
        baseBox.Add(gs, 1, wx.EXPAND | wx.ALIGN_CENTRE_HORIZONTAL)
        self.SetSizer(baseBox)
        self.Centre()
        #
        self.sld.Bind(wx.EVT_SLIDER, self.OnSliderScroll)
        self.Bind(wx.wx.EVT_KEY_DOWN, self.OnSlidersKeyboard)
        #
        self.Bind(wx.EVT_BUTTON, self.runHeruistic, runBtn)
        self.Bind(wx.EVT_BUTTON, self.pauseHeuristic, pauseBtn)
        self.Bind(wx.EVT_BUTTON, self.resumeHeuristic, resumeBtn)

        # self.Bind(wx.EVT_BUTTON, self.probLoad, loadBtn)
        # self.Bind(wx.EVT_BUTTON, self.probSave, saveBtn)

    def runHeruistic(self, _):
        self.cur_datetime = self.datetimes[0]
        self.sld.SetValue(self.datetimes.index(self.cur_datetime))
        #
        self.mainFrame.update_tabs()
        self.mainFrame.startSolvingProblems()
        print 'run Heuristic'

    def pauseHeuristic(self, _):
        self.mainFrame.pauseSolvingProblems()
        print 'pause Heuristic'

    def resumeHeuristic(self, _):
        self.mainFrame.resumeSolvingProblems()
        print 'resume Heuristic'

    def probLoad(self):
        print 'problem loading'

    def probSave(self):
        print 'problem saving'

    def increase_datetime(self):
        cur_index = self.datetimes.index(self.cur_datetime)
        temp_index = cur_index + 1
        if 0 < temp_index < len(self.datetimes):
            self.cur_datetime = self.datetimes[temp_index]
            self.update_st_cur()
            self.sld.SetValue(self.datetimes.index(self.cur_datetime))


    def OnSliderScroll(self, e):
        obj = e.GetEventObject()
        val = obj.GetValue()
        self.cur_datetime = self.datetimes[val]
        self.update_st_cur()

    def update_st_cur(self):
        self.st_cur_datetime.SetLabel('%02d/%02d/%d:H%02d' % (
        self.cur_datetime.day, self.cur_datetime.month, self.cur_datetime.year, self.cur_datetime.hour))
        self.mainFrame.update_tabs()

    def OnSlidersKeyboard(self, e):
        keycode = e.GetKeyCode()
        if keycode == wx.WXK_RIGHT or keycode == wx.WXK_LEFT:
            cur_index = self.datetimes.index(self.cur_datetime)
            temp_index = cur_index + 1 if keycode == wx.WXK_RIGHT else cur_index - 1
            if 0 < temp_index < len(self.datetimes):
                self.cur_datetime = self.datetimes[temp_index]
            self.update_st_cur()
            self.sld.SetValue(self.datetimes.index(self.cur_datetime))
        e.Skip()




    # def handleCheckBox(self, e):
    #     ce = e.GetEventObject()
    #     l = ce.GetLabelText()
    #     print l
    #     if checkBoxValues[l]:
    #         checkBoxValues[l] = False
    #     else:
    #         checkBoxValues[l] = True
    #     for p in self.Parent.tabBase.tabs:
    #         p.background_update()
    #
    # def OnEnterPressed(self, e):
    #     keycode = e.GetKeyCode()
    #     if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER or keycode == wx.WXK_TAB:
    #         print 'Enter!!'
    #         for p in ['From', 'Current', 'To']:
    #             print self.tcs[p].GetValue()
    #             dateTimeInfo[p] = self.tcs[p].GetValue()
    #             self.Parent.tabBase.notify_curDateChange()
    #     e.Skip()


class tempFrame(wx.Frame):
    def __init__(self, title="AdaptivePowerLevel", pos=(30, 30), size=(1500, 150)):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        #
        self.InitUI()
        self.Centre()
        self.Show(True)

    def InitUI(self):
        basePanel = wx.Panel(self)
        basePanel.SetBackgroundColour('#4f5049')
        vbox = wx.BoxSizer(wx.VERTICAL)
        controller = ControlPanel(basePanel)
        vbox.Add(controller, 1, wx.EXPAND | wx.ALL, 5)
        basePanel.SetSizer(vbox)


if __name__ == '__main__':
    from visualization import app
    tempFrame()
    app.MainLoop()
