import os
import sys
from pathlib import Path

APP_NAME = "ATL TECH BATTERY GUARD"

PLIST_PATH = Path.home() / (
    "Library/LaunchAgents/"
    "com.atltech.batteryguard.plist"
)

# ==========================================
# SOUND
# ==========================================

def play_alert_sound():

    try:

        os.system(
            "afplay /System/Library/Sounds/Glass.aiff"
        )

    except:

        pass


# ==========================================
# STARTUP
# ==========================================

def enable_startup():

    try:

        executable = os.path.abspath(
            sys.argv[0]
        )

        plist_content = f"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">

<plist version="1.0">
<dict>

    <key>Label</key>
    <string>com.atltech.batteryguard</string>

    <key>ProgramArguments</key>
    <array>
        <string>{executable}</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

</dict>
</plist>
"""

        PLIST_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            PLIST_PATH,
            "w"
        ) as file:

            file.write(
                plist_content
            )

    except Exception as e:

        print(
            f"Startup Error: {e}"
        )


def disable_startup():

    try:

        if PLIST_PATH.exists():

            PLIST_PATH.unlink()

    except Exception as e:

        print(
            f"Startup Error: {e}"
        )


def startup_enabled():

    return PLIST_PATH.exists()