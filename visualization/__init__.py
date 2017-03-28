import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
import wx
#
MARGIN = 10
ADJUSTMENT = 40
RADIUS = 2
WHITE = wx.Colour(255, 255, 255)
RED = wx.Colour(255, 0, 0)
BLUE = wx.Colour(0, 0, 255)
ORANGE = wx.Colour(228, 108, 10)
PURPLE = wx.Colour(115, 28, 96)
#
DEFAULT_FONT = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
SMALL_FONT = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
BIG_FONT = wx.Font(18, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
DEFAULT_BOLD_FONT = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD)
#
grid_adjustment = {}
grid_adjustment['Lv1'] = (161, 206, 23, 17)
grid_adjustment['Lv2'] = (50, 50, 19, 13)
grid_adjustment['Lv3'] = (50, 51, 21, 18)
grid_adjustment['Lv4'] = (81, 80, 23, 24)
grid_adjustment['Lv5'] = (81, 80, 24, 26)
#
checkBoxNames = ['Section', 'Room', 'Landmark', 'Landmark2', 'Grid']
checkBoxValues = {cb_name: False for cb_name in checkBoxNames}

# checkBoxValues['Landmark'] = True
# checkBoxValues['Landmark2'] = True
checkBoxValues['Grid'] = True

dateTimeInfo = {
    'From': '01/02/2007:00',
    'Current': '01/02/2007:00',
    'To': '01/03/2007:00'
}