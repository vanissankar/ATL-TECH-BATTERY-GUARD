from core.logger import (
    setup_logger
)

from core.battery_monitor import (
    BatteryMonitorService
)

from core.tray_manager import (
    TrayManager
)

from ui.main_window import (
    open_main_window
)

import threading

from core.single_instance import (
    IS_PRIMARY
)

if not IS_PRIMARY:

    print(
        "Application already running"
    )

    exit()

def main():

    setup_logger()

    monitor = (
        BatteryMonitorService()
    )

    monitor.start()

    tray = TrayManager(
        monitor
    )

    # ==========================================
    # OPEN MAIN WINDOW ON STARTUP
    # ==========================================

    threading.Thread(
        target=open_main_window,
        daemon=True
    ).start()

    # ==========================================
    # START TRAY
    # ==========================================

    tray.run()


if __name__ == "__main__":

    main()