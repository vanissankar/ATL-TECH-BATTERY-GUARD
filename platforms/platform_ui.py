import platform

from core.resource_path import (
    resource_path
)


# ==========================================
# WINDOW ICON
# ==========================================

def set_window_icon(app):

    os_name = platform.system()

    try:

        if os_name == "Windows":

            app.iconbitmap(
                resource_path(
                    "assets/battery_guard.ico"
                )
            )

        elif os_name == "Darwin":

            # macOS uses .icns during app packaging
            # No runtime iconbitmap support needed
            pass

        elif os_name == "Linux":

            # Linux icon handled by desktop environment
            pass

    except Exception as e:

        print(
            f"Icon Error: {e}"
        )


# ==========================================
# WINDOW EFFECTS
# ==========================================

def apply_window_effects(app):

    os_name = platform.system()

    if os_name == "Windows":

        try:

            import pywinstyles

            pywinstyles.apply_style(
                app,
                "acrylic"
            )

        except Exception as e:

            print(
                f"Window Effects Error: {e}"
            )

    elif os_name == "Darwin":

        # Future macOS visual effects
        pass

    elif os_name == "Linux":

        # Future Linux visual effects
        pass