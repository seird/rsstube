import datetime
import pickle

from typing import Any
from rss_tube.default_settings import DEFAULT_SETTINGS
from rss_tube.__version__ import __title__

from PyQt6 import QtCore


class Settings(QtCore.QSettings):
    def __init__(self, *args, **kwargs):
        title = __title__.replace(" ", "-")
        super(Settings, self).__init__(f"{title}/{title}", *args, **kwargs)

    def value(self, key: str, defaultValue: Any = None, type: Any = None) -> Any:
        if type:
            return super().value(key, defaultValue=defaultValue or DEFAULT_SETTINGS.get(key), type=type)
        else:
            return super().value(key, defaultValue=defaultValue or DEFAULT_SETTINGS.get(key))

    def set_last_refresh(self):
        self.setValue("last_refresh", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def export(self, path: str):
        data = {
            key: self.value(key)
            for key in self.allKeys()
            if not (  # skip settings that might not translate well between platforms
                isinstance(self.value(key), QtCore.QByteArray)
                or key == "MainWindow/export_location"
                or key == "Settings/export_path"
                or key == "player/mpv/path"
                or key == "player/vlc/path"
                or key == "player/generic/path"
            )
        }

        with open(path, "wb") as f:
            pickle.dump(data, f)

    def load(self, path: str):
        with open(path, "rb") as f:
            data = pickle.load(f)

        self.clear()

        for key in data:
            self.setValue(key, data[key])
