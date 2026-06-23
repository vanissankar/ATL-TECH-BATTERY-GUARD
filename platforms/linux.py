import os

APP_NAME = "ATL TECH BATTERY GUARD"


# ==========================================
# SOUND
# ==========================================

def play_alert_sound():

    try:

        os.system(
            "paplay /usr/share/sounds/freedesktop/stereo/complete.oga"
        )

    except:

        pass


# ==========================================
# STARTUP
# ==========================================

def enable_startup():

    # Will be implemented later
    pass


def disable_startup():

    # Will be implemented later
    pass


def startup_enabled():

    return False