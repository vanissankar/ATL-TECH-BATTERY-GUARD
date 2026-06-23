import customtkinter as ctk
import psutil

from datetime import datetime

from platforms.platform_manager import (
    play_alert_sound
)

from platforms.platform_ui import (
    apply_window_effects,
    set_window_icon
)
# ==========================================
# THEME
# ==========================================

CYAN = "#00F5FF"
RED = "#FF5555"

ctk.set_appearance_mode("dark")


# ==========================================
# ALERT WINDOW
# ==========================================

def show_alert(percent, mode):

    play_alert_sound()

    app = ctk.CTk()
    set_window_icon(
        app
    )
    apply_window_effects(
        app
    )

    # Remove title bar
    app.overrideredirect(True)

    # Always on top
    app.attributes("-topmost", True)

    # Window Size
    WIDTH = 900
    HEIGHT = 600

    screen_w = app.winfo_screenwidth()
    screen_h = app.winfo_screenheight()

    x = (screen_w - WIDTH) // 2
    y = (screen_h - HEIGHT) // 2

    app.geometry(
        f"{WIDTH}x{HEIGHT}+{x}+{y}"
    )

    app.configure(
        fg_color="black"
    )

    # ==========================================
    # DRAG WINDOW
    # ==========================================

    drag_x = 0
    drag_y = 0

    def start_drag(event):

        nonlocal drag_x, drag_y

        drag_x = event.x_root
        drag_y = event.y_root

    def drag_window(event):

        nonlocal drag_x, drag_y

        dx = event.x_root - drag_x
        dy = event.y_root - drag_y

        new_x = app.winfo_x() + dx
        new_y = app.winfo_y() + dy

        app.geometry(
            f"+{new_x}+{new_y}"
        )

        drag_x = event.x_root
        drag_y = event.y_root

    # ==========================================
    # ALERT STYLE
    # ==========================================

    if mode == "HIGH":

        color = CYAN

        message = (
            "UNPLUG THE CHARGER"
        )

    else:

        color = RED

        message = (
            "CONNECT THE CHARGER"
        )

    # ==========================================
    # MAIN FRAME
    # ==========================================

    frame = ctk.CTkFrame(
        app,
        fg_color="transparent",
        corner_radius=25,
        border_width=1,
        border_color=color
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    frame.bind(
        "<Button-1>",
        start_drag
    )

    frame.bind(
        "<B1-Motion>",
        drag_window
    )

    # ==========================================
    # TITLE
    # ==========================================

    title_label = ctk.CTkLabel(
        frame,
        text="ATL TECH BATTERY GUARD",
        font=("Segoe UI", 32, "bold"),
        text_color=color
    )

    title_label.pack(
        pady=(40, 20)
    )

    # ==========================================
    # BATTERY PERCENTAGE
    # ==========================================

    percent_label = ctk.CTkLabel(
        frame,
        text=f"{percent}%",
        font=("Segoe UI", 120, "bold"),
        text_color=color
    )

    percent_label.pack(
        pady=(10, 10)
    )

    # ==========================================
    # MESSAGE
    # ==========================================

    message_label = ctk.CTkLabel(
        frame,
        text=message,
        font=("Segoe UI", 34),
        text_color="white"
    )

    message_label.pack(
        pady=(0, 20)
    )

    # ==========================================
    # CLOCK
    # ==========================================

    clock_label = ctk.CTkLabel(
        frame,
        text="",
        font=("Consolas", 24),
        text_color="#DDDDDD"
    )

    clock_label.pack(
        pady=(0, 40)
    )

    def update_clock():

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        clock_label.configure(
            text=current_time
        )

        app.after(
            1000,
            update_clock
        )

    update_clock()

    # ==========================================
    # AUTO CLOSE LOGIC
    # ==========================================

    def monitor_battery_status():

        battery = psutil.sensors_battery()

        if battery:

            # HIGH ALERT
            if (
                mode == "HIGH"
                and not battery.power_plugged
            ):

                app.destroy()
                return

            # LOW ALERT
            if (
                mode == "LOW"
                and battery.power_plugged
            ):

                app.destroy()
                return

        app.after(
            2000,
            monitor_battery_status
        )

    monitor_battery_status()

    # ==========================================
    # ACKNOWLEDGE BUTTON
    # ==========================================

    ack_btn = ctk.CTkButton(
        frame,
        text="⚡ ACKNOWLEDGE ALERT",
        width=500,
        height=90,
        corner_radius=30,
        font=("Segoe UI", 26, "bold"),
        fg_color=color,
        hover_color="#00C8D7"
        if mode == "HIGH"
        else "#CC4444",
        border_width=2,
        border_color="#FFFFFF",
        text_color="#000000",
        command=app.destroy
    )

    ack_btn.pack(
        pady=(20, 40)
    )

    # ==========================================
    # HOVER EFFECT
    # ==========================================

    def on_enter(event):

        ack_btn.configure(
            text_color="#FFFFFF"
        )

    def on_leave(event):

        ack_btn.configure(
            text_color="#000000"
        )

    ack_btn.bind(
        "<Enter>",
        on_enter
    )

    ack_btn.bind(
        "<Leave>",
        on_leave
    )

    # ==========================================
    # ENTER KEY
    # ==========================================

    app.bind(
        "<Return>",
        lambda e: app.destroy()
    )

    # ==========================================
    # RUN
    # ==========================================

    app.mainloop()