from . import default, dark, dark_red, light, light_red
from PyQt6 import QtCore, QtWidgets


styles = {
    "automatic": None,
    "default": default,
    "dark": dark,
    "dark_red": dark_red,
    "light": light,
    "light_red": light_red
}


def unviewed_color(theme: str, app: QtWidgets.QApplication) -> int:
    is_dark = app.styleHints().colorScheme() == QtCore.Qt.ColorScheme.Dark

    return {
        "automatic": 0xFFFFF if is_dark else 0x000000,
        "default": 0xFFFFF if is_dark else 0x000000,
        "dark": 0x68B668,
        "dark_red": 0xCF5B5B,
        "light": 0x68B668,
        "light_red": 0xCF5B5B,
    }.get(theme, 0x68B668)

