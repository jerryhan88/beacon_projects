import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
#
import wx
#
MARGIN = 10
ADJUSTMENT = 40
WHITE = wx.Colour(255, 255, 255)
RED = wx.Colour(255, 0, 0)
BLUE = wx.Colour(0, 0, 255)
ORANGE = wx.Colour(228, 108, 10)
PURPLE = wx.Colour(115, 28, 96)
#
DEFAULT_BOLD_FONT = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD)
#
levelNames = ['Lv %d' % x for x in range(1, 6)]



