import json
import os

APP_NAME = "GestureLock"

APP_DATA_DIR = os.path.join(
    os.environ.get("APPDATA", os.path.expanduser("~")),
    APP_NAME
)

CONFIG_FILE = os.path.join(
    APP_DATA_DIR,
    "settings.json"
)

DEFAULT_SETTINGS = {
    "unlock_sequence": [
        "PEACE",
        "BRO",
        "FUCK_YOU",
        "HELLO"
    ],
    "camera_width": 1280,
    "camera_height": 720,
    "gesture_stable_time": 0.5,
    "auto_lock_enabled": True,
    "auto_lock_seconds": 30
}


def load_settings():

    os.makedirs(
        APP_DATA_DIR,
        exist_ok=True
    )

    if not os.path.exists(CONFIG_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:

        with open(
            CONFIG_FILE,
            "r"
        ) as file:

            settings = json.load(file)

        for key, value in DEFAULT_SETTINGS.items():

            if key not in settings:
                settings[key] = value

        return settings

    except:

        save_settings(DEFAULT_SETTINGS)

        return DEFAULT_SETTINGS.copy()


def save_settings(settings):

    os.makedirs(
        APP_DATA_DIR,
        exist_ok=True
    )

    with open(
        CONFIG_FILE,
        "w"
    ) as file:

        json.dump(
            settings,
            file,
            indent=4
        )


settings = load_settings()

UNLOCK_SEQUENCE = settings["unlock_sequence"]
CAMERA_WIDTH = settings["camera_width"]
CAMERA_HEIGHT = settings["camera_height"]
GESTURE_STABLE_TIME = settings["gesture_stable_time"]
AUTO_LOCK_ENABLED = settings["auto_lock_enabled"]
AUTO_LOCK_SECONDS = settings["auto_lock_seconds"]