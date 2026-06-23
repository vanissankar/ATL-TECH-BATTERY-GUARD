import customtkinter as ctk
from plyer import battery
import psutil
import platform
import sys
import json

from core.config_manager import (
    load_settings,
    save_settings
)

from core.startup_manager import (
    enable_startup,
    disable_startup
)

from platforms.platform_ui import (
    set_window_icon
)

ctk.set_appearance_mode("dark")

MAIN_WINDOW = None

def close_main_window():

    global MAIN_WINDOW

    if MAIN_WINDOW is not None:

        try:

            MAIN_WINDOW.after(
                0,
                MAIN_WINDOW.destroy
            )

        except:

            pass

        MAIN_WINDOW = None


def open_main_window():

    global MAIN_WINDOW

    if MAIN_WINDOW is not None:

        try:

            MAIN_WINDOW.lift()
            MAIN_WINDOW.focus_force()

            return

        except:

            MAIN_WINDOW = None

    settings = load_settings()

    app = ctk.CTk()
    set_window_icon(
        app
    )

    MAIN_WINDOW = app

    app.title(
        "ATL TECH ANIS BATTERY GUARD"
    )

    app.geometry(
        "800x700"
    )

    app.resizable(
        False,
        False
    )

    def on_close():

        global MAIN_WINDOW

        MAIN_WINDOW = None

        app.destroy()

    app.protocol(
        "WM_DELETE_WINDOW",
        on_close
    )

    # ==========================================
    # TAB VIEW
    # ==========================================

    tabview = ctk.CTkTabview(
        app,
        width=760,
        height=540
    )

    tabview.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )

    dashboard_tab = tabview.add(
        "Dashboard"
    )

    settings_tab = tabview.add(
        "Settings"
    )

    about_tab = tabview.add(
        "About"
    )

    # ==========================================
# DASHBOARD TAB
# ==========================================

    title_label = ctk.CTkLabel(
        dashboard_tab,
        text="ATL TECH ANIS BATTERY GUARD",
        font=("Segoe UI", 28, "bold"),
        text_color="#00F5FF"
    )

    title_label.pack(pady=(20, 10))

    battery_label = ctk.CTkLabel(
        dashboard_tab,
        text="0%",
        font=("Segoe UI", 90, "bold"),
        text_color="#00F5FF"
    )

    battery_label.pack()

    status_dashboard_label = ctk.CTkLabel(
        dashboard_tab,
        text="UNKNOWN",
        font=("Segoe UI", 24, "bold")
    )

    status_dashboard_label.pack(pady=(0, 20))

    high_alert_label = ctk.CTkLabel(
        dashboard_tab,
        text=""
    )

    high_alert_label.pack(pady=5)

    low_alert_label = ctk.CTkLabel(
        dashboard_tab,
        text=""
    )

    low_alert_label.pack(pady=5)

    monitor_label = ctk.CTkLabel(
        dashboard_tab,
        text="✓ Monitoring Active",
        text_color="#00FF88"
    )

    monitor_label.pack(pady=20)
    
    def update_dashboard():

        battery = psutil.sensors_battery()

        if battery:

            battery_label.configure(
                text=f"{battery.percent}%"
            )

            if battery.power_plugged:

                status_dashboard_label.configure(
                    text="⚡ CHARGING",
                    text_color="#00FF88"
                )

            else:

                status_dashboard_label.configure(
                    text="🔋 DISCHARGING",
                    text_color="#FFA500"
                )

        current_settings = load_settings()

        high_alert_label.configure(
            text=f"High Alert : {current_settings['high_limit']}%"
        )

        low_alert_label.configure(
            text=f"Low Alert : {current_settings['low_limit']}%"
        )

        app.after(
            1000,
            update_dashboard
        )


    update_dashboard()

    # ==========================================
    # SETTINGS TAB
    # ==========================================

    def validate_number(value):

        if value == "":
            return True

        return value.isdigit()

    validation = app.register(
        validate_number
    )

    ctk.CTkLabel(
        settings_tab,
        text="High Battery Alert (%)"
    ).pack(
        pady=(20, 5)
    )

    high_limit = ctk.CTkEntry(
        settings_tab,
        width=250,
        validate="key",
        validatecommand=(
            validation,
            "%P"
        )
    )

    high_limit.pack()
    ctk.CTkLabel(
        settings_tab,
        text="Valid Range: 51 - 100",
        text_color="#888888",
        font=("Segoe UI", 11)
    ).pack(
        pady=(2, 10)
    )

    high_limit.insert(
        0,
        str(settings["high_limit"])
    )


    ctk.CTkLabel(
        settings_tab,
        text="Low Battery Alert (%)"
    ).pack(
        pady=(20, 5)
    )

    low_limit = ctk.CTkEntry(
        settings_tab,
        width=250,
        validate="key",
        validatecommand=(
            validation,
            "%P"
        )
    )

    low_limit.pack()
    ctk.CTkLabel(
        settings_tab,
        text="Valid Range: 1 - 49",
        text_color="#888888",
        font=("Segoe UI", 11)
    ).pack(
        pady=(2, 10)
    )

    low_limit.insert(
        0,
        str(settings["low_limit"])
    )


    ctk.CTkLabel(
        settings_tab,
        text="High Alert Repeat (Seconds)"
    ).pack(
        pady=(20, 5)
    )

    high_repeat = ctk.CTkEntry(
        settings_tab,
        width=250,
        validate="key",
        validatecommand=(
            validation,
            "%P"
        )
    )

    high_repeat.pack()

    high_repeat.insert(
        0,
        str(settings["high_alert_repeat"])
    )

    
    
    

    ctk.CTkLabel(
        settings_tab,
        text="Low Alert Repeat (Seconds)"
    ).pack(
        pady=(20, 5)
    )

    low_repeat = ctk.CTkEntry(
        settings_tab,
        width=250,
        validate="key",
        validatecommand=(
            validation,
            "%P"
        )
    )

    low_repeat.pack()

    low_repeat.insert(
        0,
        str(settings["low_alert_repeat"])
    )
    


    startup_var = ctk.BooleanVar(
        value=settings["startup"]
    )

    ctk.CTkCheckBox(
        settings_tab,
        text="Start With System",
        variable=startup_var,
        command=lambda: status_label.configure(text="")
    ).pack(
        pady=20
    )
    status_label = ctk.CTkLabel(
        settings_tab,
        text=""
    )

    status_label.pack()

    high_limit.bind(
        "<KeyRelease>",
        lambda e: status_label.configure(text="")
    )

    low_limit.bind(
        "<KeyRelease>",
        lambda e: status_label.configure(text="")
    )

    high_repeat.bind(
        "<KeyRelease>",
        lambda e: status_label.configure(text="")
    )

    low_repeat.bind(
        "<KeyRelease>",
        lambda e: status_label.configure(text="")
    )


    def save():

        try:

            new_high = int(
                high_limit.get()
            )

            new_low = int(
                low_limit.get()
            )

            new_high_repeat = int(
                high_repeat.get()
            )

            new_low_repeat = int(
                low_repeat.get()
            )

        # ==========================
        # VALIDATION
        # ==========================

            if not (51 <= new_high <= 100):

                status_label.configure(
                    text="❌ High Alert must be between 51 and 100",
                    text_color="#FF5555"
                )

                return

            if not (1 <= new_low <= 49):

                status_label.configure(
                    text="❌ Low Alert must be between 1 and 49",
                    text_color="#FF5555"
                )

                return

            if new_low >= new_high:

                status_label.configure(
                    text="❌ Low Alert must be lower than High Alert",
                    text_color="#FF5555"
                )

                return

            new_settings = {

                "version":
                settings["version"],

                "high_limit":
                new_high,

                "low_limit":
                new_low,

                "startup":
                startup_var.get(),

                "high_alert_repeat":
                new_high_repeat,

                "low_alert_repeat":
                new_low_repeat
            }

            save_settings(
                new_settings
            )

            if startup_var.get():

                enable_startup()

            else:

                disable_startup()

            status_label.configure(
                text="✓ Settings Saved",
                text_color="#00FF88"
            )
            app.after(
                3000,
                lambda: status_label.configure(text="")
            )

        except Exception:

            status_label.configure(
                text="❌ Please enter valid numbers",
                text_color="#FF5555"
            )

    ctk.CTkButton(
        settings_tab,
        text="SAVE SETTINGS",
        width=300,
        height=50,
        command=save
    ).pack(
        pady=20
    )

    # ==========================================
    # ABOUT TAB
    # ==========================================

    try:

        with open(
            "version.json",
            "r"
        ) as file:

            version_info = json.load(
                file
            )

    except:

        version_info = {

            "app_name":
            "ATL TECH BATTERY GUARD",

            "version":
            "3.0.0",

            "author":
            "Anis Sankar"
        }

    ctk.CTkLabel(
        about_tab,
        text=version_info[
            "app_name"
        ],
        font=(
            "Segoe UI",
            28,
            "bold"
        )
    ).pack(
        pady=20
    )

    ctk.CTkLabel(
        about_tab,
        text=f"Version : {version_info['version']}"
    ).pack(
        pady=10
    )

    ctk.CTkLabel(
        about_tab,
        text=f"Author : {version_info['author']}"
    ).pack(
        pady=10
    )

    ctk.CTkLabel(
        about_tab,
        text=f"Platform : {platform.system()}"
    ).pack(
        pady=10
    )

    ctk.CTkLabel(
        about_tab,
        text=f"Python : {sys.version.split()[0]}"
    ).pack(
        pady=10
    )

    app.mainloop()
    tabview.set(
        "About"
    )