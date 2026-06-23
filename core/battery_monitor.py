import time
import threading
import psutil

from core.config_manager import (
    load_settings
)

from core.logger import (
    log_info,
    log_error
)

from ui.alert_window import (
    show_alert
)


class BatteryMonitorService:

    def __init__(self):

        self.running = False

        self.last_high_alert = 0
        self.last_low_alert = 0

        self.popup_open = False

    # ==========================================
    # ALERT WINDOW LAUNCHER
    # ==========================================

    def launch_alert(
        self,
        percent,
        mode
    ):

        if self.popup_open:

            return

        self.popup_open = True

        try:

            show_alert(
                percent,
                mode
            )

        finally:

            self.popup_open = False

    # ==========================================
    # BATTERY CHECK LOOP
    # ==========================================

    def check_battery(self):

        while self.running:

            try:

                settings = load_settings()

                high_limit = settings[
                    "high_limit"
                ]

                low_limit = settings[
                    "low_limit"
                ]

                high_repeat = settings[
                    "high_alert_repeat"
                ]

                low_repeat = settings[
                    "low_alert_repeat"
                ]

                battery = psutil.sensors_battery()

                if battery:

                    percent = battery.percent

                    charging = (
                        battery.power_plugged
                    )

                    print(
                        f"Battery: {percent}% | Charging: {charging}"
                    )

                    current_time = time.time()

                    # ==========================================
                    # HIGH ALERT
                    # ==========================================

                    if (
                        percent >= high_limit
                        and charging
                        and (
                            current_time
                            - self.last_high_alert
                            > high_repeat
                        )
                    ):

                        self.last_high_alert = (
                            current_time
                        )

                        log_info(
                            f"HIGH ALERT {percent}%"
                        )

                        threading.Thread(
                            target=self.launch_alert,
                            args=(
                                percent,
                                "HIGH"
                            ),
                            daemon=True
                        ).start()

                    # ==========================================
                    # LOW ALERT
                    # ==========================================

                    if (
                        percent <= low_limit
                        and not charging
                        and (
                            current_time
                            - self.last_low_alert
                            > low_repeat
                        )
                    ):

                        self.last_low_alert = (
                            current_time
                        )

                        log_info(
                            f"LOW ALERT {percent}%"
                        )

                        threading.Thread(
                            target=self.launch_alert,
                            args=(
                                percent,
                                "LOW"
                            ),
                            daemon=True
                        ).start()

            except Exception as e:

                log_error(
                    str(e)
                )

            time.sleep(30)

    # ==========================================
    # START MONITOR
    # ==========================================

    def start(self):

        if self.running:

            return

        self.running = True

        threading.Thread(
            target=self.check_battery,
            daemon=True
        ).start()

        log_info(
            "Battery Monitor Started"
        )

    # ==========================================
    # STOP MONITOR
    # ==========================================

    def stop(self):

        self.running = False

        log_info(
            "Battery Monitor Stopped"
        )