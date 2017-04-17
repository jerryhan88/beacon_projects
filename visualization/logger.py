import wx
from wx import stc
import sys

# logger setting
LOG_TO_CONSOLE = False  # for debugging purpose
LOGGING_LEVEL = 1
_log_out = sys.stdout


loggers = {}

class LogView(stc.StyledTextCtrl):
    def __init__(self, parent):
        stc.StyledTextCtrl.__init__(self, parent, style=wx.SUNKEN_BORDER)

    def write(self, s):
        self.AddText(s)
        self.ScrollToLine(self.GetLineCount())


def choose_logger(logger):
    return logger if not LOG_TO_CONSOLE else _log_out

