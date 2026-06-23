import json


SETTINGS_FILE = "settings.json"


def load_settings():

    try:

        with open(
            SETTINGS_FILE,
            "r"
        ) as file:

            return json.load(file)

    except Exception:

        return {
            "version": "3.0.0",
            "high_limit": 90,
            "low_limit": 20,
            "startup": True,
            "high_alert_repeat": 30,
            "low_alert_repeat": 30
        }


def save_settings(settings):

    with open(
        SETTINGS_FILE,
        "w"
    ) as file:

        json.dump(
            settings,
            file,
            indent=4
        )