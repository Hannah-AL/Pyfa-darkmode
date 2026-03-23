# noinspection PyPackageRequirements
import wx

from gui.utils.dark import isDark

# Dark colour mappings for wx system colours
_DARK_COLOUR_MAP = {
    wx.SYS_COLOUR_WINDOW: wx.Colour(43, 43, 43),
    wx.SYS_COLOUR_WINDOWTEXT: wx.Colour(220, 220, 220),
    wx.SYS_COLOUR_BTNFACE: wx.Colour(51, 51, 51),
    wx.SYS_COLOUR_3DFACE: wx.Colour(51, 51, 51),
    wx.SYS_COLOUR_BTNTEXT: wx.Colour(220, 220, 220),
    wx.SYS_COLOUR_LISTBOX: wx.Colour(43, 43, 43),
    wx.SYS_COLOUR_LISTBOXTEXT: wx.Colour(220, 220, 220),
    wx.SYS_COLOUR_HIGHLIGHT: wx.Colour(0, 120, 215),
    wx.SYS_COLOUR_HIGHLIGHTTEXT: wx.Colour(255, 255, 255),
    wx.SYS_COLOUR_GRAYTEXT: wx.Colour(140, 140, 140),
    wx.SYS_COLOUR_CAPTIONTEXT: wx.Colour(220, 220, 220),
    wx.SYS_COLOUR_BTNHIGHLIGHT: wx.Colour(70, 70, 70),
    wx.SYS_COLOUR_BTNSHADOW: wx.Colour(30, 30, 30),
    wx.SYS_COLOUR_3DLIGHT: wx.Colour(70, 70, 70),
    wx.SYS_COLOUR_3DSHADOW: wx.Colour(30, 30, 30),
    wx.SYS_COLOUR_MENU: wx.Colour(51, 51, 51),
    wx.SYS_COLOUR_MENUTEXT: wx.Colour(220, 220, 220),
    wx.SYS_COLOUR_MENUBAR: wx.Colour(51, 51, 51),
    wx.SYS_COLOUR_SCROLLBAR: wx.Colour(60, 60, 60),
    wx.SYS_COLOUR_APPWORKSPACE: wx.Colour(43, 43, 43),
    wx.SYS_COLOUR_INFOBK: wx.Colour(60, 60, 60),
    wx.SYS_COLOUR_INFOTEXT: wx.Colour(220, 220, 220),
}

# Store the original GetColour so we can call it for unmapped colours
_originalGetColour = wx.SystemSettings.GetColour


def _themedGetColour(index):
    """Replacement for wx.SystemSettings.GetColour that returns dark colours
    when dark mode is active."""
    if isDark() and index in _DARK_COLOUR_MAP:
        return _DARK_COLOUR_MAP[index]
    return _originalGetColour(index)


def installThemeOverride():
    """Install the dark mode colour override.

    Call this once at startup, before any windows are created.
    It monkey-patches wx.SystemSettings.GetColour so that all widgets
    that read system colours will automatically get dark colours."""
    wx.SystemSettings.GetColour = staticmethod(_themedGetColour)


def applyThemeToWindow(window):
    """Recursively apply theme colours to a window and all its children.

    This handles widgets that set their colours at creation time rather
    than reading system colours at paint time."""
    if not isDark():
        return
    bg = _DARK_COLOUR_MAP[wx.SYS_COLOUR_WINDOW]
    fg = _DARK_COLOUR_MAP[wx.SYS_COLOUR_WINDOWTEXT]
    inputBg = _DARK_COLOUR_MAP.get(wx.SYS_COLOUR_LISTBOX, bg)
    _applyRecursive(window, bg, fg, inputBg)


def _applyRecursive(window, bg, fg, inputBg):
    """Walk a window tree and set colours on each widget."""
    try:
        className = window.GetClassName()
        if className in ('wxTextCtrl', 'wxSearchCtrl', 'wxListCtrl',
                         'wxListView', 'wxTreeCtrl', 'wxDataViewCtrl',
                         'wxStyledTextCtrl', 'wxHtmlWindow',
                         'wxScrolledWindow'):
            window.SetBackgroundColour(inputBg)
        else:
            window.SetBackgroundColour(bg)
        window.SetForegroundColour(fg)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        pass
    for child in window.GetChildren():
        _applyRecursive(child, bg, fg, inputBg)
