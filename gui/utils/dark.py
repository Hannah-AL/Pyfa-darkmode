import wx

from service.settings import SettingsProvider


def isDark():
    override = _getDarkModeOverride()
    if override == "light":
        return False
    if override == "dark":
        return True

    # "system" - auto-detect
    if 'wxMSW' in wx.PlatformInfo:
        return _isWindowsDark()
    try:
        return wx.SystemSettings.GetAppearance().IsDark()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return False


def _getDarkModeOverride():
    try:
        settings = SettingsProvider.getInstance().getSettings(
            "pyfaDisplay", {"darkModeOverride": "system"})
        return settings["darkModeOverride"]
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return "system"


def _isWindowsDark():
    """Detect Windows dark mode via the registry."""
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return value == 0
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return False
