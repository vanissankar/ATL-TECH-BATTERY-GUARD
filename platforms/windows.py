import os
import sys
import winsound
import winreg

APP_NAME = "ATL TECH BATTERY GUARD"


# ==========================================
# SOUND
# ==========================================

def play_alert_sound():

    winsound.PlaySound(
        "SystemExclamation",
        winsound.SND_ALIAS
    )


# ==========================================
# STARTUP
# ==========================================

def get_app_path():

    if getattr(
        sys,
        "frozen",
        False
    ):

        return sys.executable

    return os.path.abspath(
        sys.argv[0]
    )


def enable_startup():

    path = get_app_path()

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    )

    winreg.SetValueEx(
        key,
        APP_NAME,
        0,
        winreg.REG_SZ,
        path
    )

    winreg.CloseKey(
        key
    )


def disable_startup():

    try:

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )

        winreg.DeleteValue(
            key,
            APP_NAME
        )

        winreg.CloseKey(
            key
        )

    except:

        pass


def startup_enabled():

    try:

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run"
        )

        winreg.QueryValueEx(
            key,
            APP_NAME
        )

        winreg.CloseKey(
            key
        )

        return True

    except:

        return False