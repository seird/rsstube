import datetime

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
