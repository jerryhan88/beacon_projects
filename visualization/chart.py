import __init__
'''

'''
#
import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg

from random import random

_rgb = lambda r, g, b: (r / 255, g / 255, b / 255)

clists = (
    'blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black',
    _rgb(255, 165, 0),  # orange
    _rgb(238, 130, 238),  # violet
    _rgb(255, 228, 225),  # misty rose
    _rgb(127, 255, 212),  # aqua-marine
    _rgb(220, 220, 220)  # gray
)

class LineChart(object):
    def __init__(self, subplot_pos, cName):
        self.axes = plt.subplot(*subplot_pos)
        self.axes.set_facecolor('white')
        self.axes.set_title(cName, fontsize=11)
        plt.plot([1, 2, 3], [random() for _ in xrange(3)], linewidth=1)
        plt.plot([1, 2, 3], [random() for _ in xrange(3)], linewidth=1)


class ChartView(wx.Panel):
    def __init__(self, parent, APL_measures, FPL_measures):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        # self.SetBackgroundColour(PURPLE)
        #
        # Organize chart
        #
        self.sizer = wx.GridSizer(4, 1, 0, 0)
        self.SetSizer(self.sizer)
        #
        # create chart canvases.
        #
        self.charts = []
        self.charts_dataset = {}
        for cName in ['minBattery', 'numZone', 'popularity', 'numUniUser']:
            dataset = [APL_measures[cName]]
            for fpl_m in FPL_measures:
                dataset += [fpl_m[cName]]
            # for s in dataset:
            #     for i in range(10):
            #         s.record(i, random())
            self.charts_dataset[cName] = dataset
            chart, canvas = self.create_chart(cName, dataset)
            self.sizer.Add(canvas, 0, wx.EXPAND)
            self.charts += [[chart, canvas]]
        self.SendSizeEvent()

    def create_chart(self, cName, dataset):
        fig = plt.figure()
        fig.set_facecolor('white')
        legend_labels = ['APL', 'F10', 'F20', 'F30']
        chart = line_chart(legend_labels, dataset, cName)
        return chart, FigureCanvasWxAgg(self, wx.ID_ANY, fig)

    def refresh_charts(self):
        for chart, canvas in self.charts:
            chart.refresh()
            canvas.draw()



SMALL_VALUE_FOR_INIT_MAX = 0.01

class line_chart(object):
    '''
    input data
      cdata_set[i] = cd: i'th sim's data object
        cd.X: series of x values
        cd.Y: series of y values
        cd.xmax = max(cd.X)
        cd.ymax = max(cd.Y)

    chart_data_object[i]: i'th line data in chart
    '''

    def __init__(self, legend_labels, cdata_set, title):
        self.cdata_set, self.title = cdata_set, title
        self.legend_labels = legend_labels
        self.chart_data_object = []
        # create chart.
        self.axes = plt.subplot(*(1, 1, 1))
        self.axes.set_facecolor('white')
        self.axes.set_title(title, fontsize=11)
        plt.xlim(0)
        plt.ylim(0)
        plt.xticks(fontsize=9.5)
        plt.yticks(fontsize=9.5)
        plt.subplots_adjust(left=0.085, right=0.98, top=0.85, bottom=0.1)
        # get data object from chart
        for i, cdata in enumerate(self.cdata_set):
            self.chart_data_object.append(plt.plot(cdata.X, cdata.Y, linewidth=1, color=clists[i])[0])
        plt.legend(legend_labels, ncol=1, loc='upper left', fontsize=10)

    def refresh(self):
        xmax, ymax = SMALL_VALUE_FOR_INIT_MAX, SMALL_VALUE_FOR_INIT_MAX
        for i, d in enumerate(self.chart_data_object):
            cd = self.cdata_set[i]
            d.set_xdata(cd.X)
            d.set_ydata(cd.Y)
            if xmax < cd.xmax:
                xmax = cd.xmax
            if ymax < cd.ymax:
                ymax = cd.ymax
        self.axes.set_xbound(upper=xmax * 1.05)
        self.axes.set_ybound(upper=ymax * 1.05)


class series(object):
    def __init__(self):
        self.X, self.Y = [], []
        self.xmax, self.ymax = -1e400, -1e400
    def record(self, t, v):
        '''
        ASSUME t >= X[-1]
        '''
        self.X.append(t)
        self.Y.append(v)
        self.xmax = t
        if self.ymax < v:
            self.ymax = v


TIMER_INTERVAL = 1000  # milliseconds

class tempFrame(wx.Frame):
    def __init__(self, title="AdaptivePowerLevel", pos=(30, 30), size=(500, 900)):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        #
        self.InitUI()
        self.Centre()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(TIMER_INTERVAL)
        # self.Maximize()
        self.Show(True)

    def InitUI(self):
        basePanel = wx.Panel(self)
        basePanel.logger = None
        basePanel.SetBackgroundColour('#4f5049')
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.chart_view = ChartView(basePanel)
        vbox.Add(self.chart_view, 1, wx.EXPAND | wx.ALL, 5)
        basePanel.SetSizer(vbox)

    def OnTimer(self, _e):
        s1 = self.chart_view.charts_dataset['minBattery'][0]
        s1.record(s1.X[-1]+1, random())
        self.chart_view.refresh_charts()


    def OnClose(self, _e):
        self.timer.Stop()
        self.Destroy()

    def OnExit(self, _e):
        self.Close()

if __name__ == '__main__':
    from visualization import app
    tempFrame()
    app.MainLoop()
