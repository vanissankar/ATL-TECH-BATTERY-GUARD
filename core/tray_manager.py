import pystray
import threading
import time
import os

from PIL import Image

from ui.main_window import (
    open_main_window,
    close_main_window
)

from core.resource_path import (
    resource_path
)


class TrayManager:

    def __init__(
        self,
        monitor
    ):

        self.icon = None
        self.monitor = monitor

    # ==========================================
    # ICON
    # ==========================================

    def create_icon(self):

        return Image.open(
            resource_path(
                "assets/battery_guard.png"
            )
        )

    # ==========================================
    # OPEN MAIN WINDOW
    # ==========================================

    def open_app(
        self,
        icon,
        item
    ):

        threading.Thread(
            target=open_main_window,
            daemon=True
        ).start()

    # ==========================================
    # EXIT
    # ==========================================

    def quit_app(
        self,
        icon,
        item
    ):

        print(
            "Stopping Battery Monitor..."
        )

        self.monitor.stop()

        close_main_window()

        if self.icon:

            self.icon.stop()

        time.sleep(
            0.5
        )

        os._exit(
            0
        )

    # ==========================================
    # RUN
    # ==========================================

    def run(self):

        menu = pystray.Menu(

            pystray.MenuItem(
                "Open ATL TECH ANIS BATTERY GUARD",
                self.open_app
            ),

            pystray.MenuItem(
                "Exit",
                self.quit_app
            )
        )

        self.icon = pystray.Icon(
            "ATL Battery Guard",
            self.create_icon(),
            "ATL TECH ANIS BATTERY GUARD V3",
            menu
        )

        self.icon.run()