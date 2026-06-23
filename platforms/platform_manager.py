import platform

OS = platform.system()

# ==========================================
# WINDOWS
# ==========================================

if OS == "Windows":

    from platforms.windows import (
        play_alert_sound,
        enable_startup,
        disable_startup,
        startup_enabled
    )

# ==========================================
# MACOS
# ==========================================

elif OS == "Darwin":

    from platforms.macos import (
        play_alert_sound,
        enable_startup,
        disable_startup,
        startup_enabled
    )

# ==========================================
# LINUX
# ==========================================

elif OS == "Linux":

    from platforms.linux import (
        play_alert_sound,
        enable_startup,
        disable_startup,
        startup_enabled
    )

# ==========================================
# UNKNOWN
# ==========================================

else:

    raise Exception(
        f"Unsupported OS: {OS}"
    )