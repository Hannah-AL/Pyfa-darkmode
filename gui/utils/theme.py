# noinspection PyPackageRequirements
import wx

from gui.utils.dark import isDark

# Discord-inspired dark colour palette
_DARK_COLOUR_MAP = {
    wx.SYS_COLOUR_WINDOW: wx.Colour(49, 51, 56),        # Chat/content background
    wx.SYS_COLOUR_WINDOWTEXT: wx.Colour(242, 243, 245),  # Primary text
    wx.SYS_COLOUR_BTNFACE: wx.Colour(43, 45, 49),        # Panel/button background
    wx.SYS_COLOUR_3DFACE: wx.Colour(43, 45, 49),         # Panel/button background
    wx.SYS_COLOUR_BTNTEXT: wx.Colour(242, 243, 245),     # Button text
    wx.SYS_COLOUR_LISTBOX: wx.Colour(30, 31, 34),        # List/input background (darkest)
    wx.SYS_COLOUR_LISTBOXTEXT: wx.Colour(242, 243, 245), # List text
    wx.SYS_COLOUR_HIGHLIGHT: wx.Colour(88, 101, 242),    # Blurple selection
    wx.SYS_COLOUR_HIGHLIGHTTEXT: wx.Colour(255, 255, 255),
    wx.SYS_COLOUR_GRAYTEXT: wx.Colour(148, 155, 164),    # Muted text
    wx.SYS_COLOUR_CAPTIONTEXT: wx.Colour(242, 243, 245),
    wx.SYS_COLOUR_BTNHIGHLIGHT: wx.Colour(64, 66, 73),   # Hover highlight
    wx.SYS_COLOUR_BTNSHADOW: wx.Colour(30, 31, 34),      # Deepest shadow
    wx.SYS_COLOUR_3DLIGHT: wx.Colour(64, 66, 73),
    wx.SYS_COLOUR_3DSHADOW: wx.Colour(30, 31, 34),
    wx.SYS_COLOUR_MENU: wx.Colour(43, 45, 49),           # Menu background
    wx.SYS_COLOUR_MENUTEXT: wx.Colour(242, 243, 245),
    wx.SYS_COLOUR_MENUBAR: wx.Colour(30, 31, 34),        # Menubar (darkest)
    wx.SYS_COLOUR_SCROLLBAR: wx.Colour(56, 58, 64),      # Scrollbar
    wx.SYS_COLOUR_APPWORKSPACE: wx.Colour(30, 31, 34),   # Darkest background
    wx.SYS_COLOUR_INFOBK: wx.Colour(56, 58, 64),         # Tooltip background
    wx.SYS_COLOUR_INFOTEXT: wx.Colour(242, 243, 245),    # Tooltip text
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
    inputBg = _DARK_COLOUR_MAP[wx.SYS_COLOUR_LISTBOX]
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
