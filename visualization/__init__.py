import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
import wx
app = wx.App(False)

WHITE = wx.Colour(255, 255, 255)
RED = wx.Colour(255, 0, 0)
BLUE = wx.Colour(0, 0, 255)
ORANGE = wx.Colour(228, 108, 10)
PURPLE = wx.Colour(115, 28, 96)
#
DEFAULT_FONT = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
DEFAULT_BOLD_FONT = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD)
SMALL_FONT = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
BIG_FONT = wx.Font(24, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
BIG_BOLD_FONT = wx.Font(24, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD)





RADIUS = 2

