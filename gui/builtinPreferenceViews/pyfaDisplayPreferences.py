# noinspection PyPackageRequirements
import wx

from gui.bitmap_loader import BitmapLoader
from gui.preferenceView import PreferenceView
from service.settings import SettingsProvider

_t = wx.GetTranslation


class PFDisplayPref(PreferenceView):

    def populatePanel(self, panel):
        self.title = _t("Display")
        self.displaySettings = SettingsProvider.getInstance().getSettings(
            "pyfaDisplay", {"darkModeOverride": "system"})
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.stTitle = wx.StaticText(panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.stTitle.Wrap(-1)
        self.stTitle.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        mainSizer.Add(self.stTitle, 0, wx.EXPAND | wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.rbDarkMode = wx.RadioBox(
            panel, -1, _t("Dark Mode"),
            wx.DefaultPosition, wx.DefaultSize,
            [_t("System"), _t("Light"), _t("Dark")],
            1, wx.RA_SPECIFY_COLS)

        currentVal = self.displaySettings["darkModeOverride"]
        if currentVal == "light":
            self.rbDarkMode.SetSelection(1)
        elif currentVal == "dark":
            self.rbDarkMode.SetSelection(2)
        else:
            self.rbDarkMode.SetSelection(0)

        self.rbDarkMode.Bind(wx.EVT_RADIOBOX, self.onDarkModeChange)
        mainSizer.Add(self.rbDarkMode, 0, wx.EXPAND | wx.ALL, 10)

        restartNote = wx.StaticText(panel, wx.ID_ANY,
                                    _t("Requires a restart to take effect."),
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        restartNote.Wrap(-1)
        mainSizer.Add(restartNote, 0, wx.LEFT | wx.BOTTOM, 10)

        panel.SetSizer(mainSizer)
        panel.Layout()

    def onDarkModeChange(self, event):
        selection = self.rbDarkMode.GetSelection()
        if selection == 1:
            self.displaySettings["darkModeOverride"] = "light"
        elif selection == 2:
            self.displaySettings["darkModeOverride"] = "dark"
        else:
            self.displaySettings["darkModeOverride"] = "system"
        # Save immediately so the setting persists for next restart
        self.displaySettings.save()
        event.Skip()

    def getImage(self):
        return BitmapLoader.getBitmap("prefs_settings", "gui")


PFDisplayPref.register()
