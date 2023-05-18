import logging
import os
import platform
import re
import subprocess

from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets
from rss_tube.__version__ import __title__, __version__, __url__, __description__
from textwrap import dedent
from rss_tube.gui.themes import styles
from rss_tube.database.settings import Settings


logger = logging.getLogger("logger")
settings = Settings()


def load_pixmap(image_bytes: bytes) -> QtGui.QPixmap:
    image = QtGui.QImage()
    image.loadFromData(image_bytes)
    return QtGui.QPixmap(image)


def center_widget(parent, widget):
    # Move the dialog to the center of the calling widget
    parent_pos = parent.pos()
    parent_size = parent.size()
    size = widget.size()
    widget.move(
        int(parent_pos.x() + parent_size.width() * 0.5 - size.width() * 0.5),
        int(parent_pos.y() + parent_size.height() * 0.5 - size.height() * 0.5)
    )


def get_abs_path(s) -> str:
    h = Path(__file__).parent.parent
    p = Path(s)
    return os.path.join(h, p).replace("\\", "/")


def automatic_to_style(app: QtWidgets.QApplication) -> str:
    if app.styleHints().colorScheme() == QtCore.Qt.ColorScheme.Dark:
        return "dark"
    else:
        return "light"


def set_style(app: QtWidgets.QApplication, style: str = "dark"):
    app.setStyle("fusion")

    if style not in styles.keys():
        logger.error(f"set_style: style {style} is unsupported.")
        return
    
    if style == "automatic":
        style = automatic_to_style(app)  

    stylesheet = ""
    with open(get_theme_file(app, f"{style}.css"), "r") as f:
        stylesheet += f.read()
    with open(get_theme_file(app, f"EntryYoutube.css"), "r") as f:
        stylesheet += f.read()
    with open(get_theme_file(app, f"EntrySoundcloud.css"), "r") as f:
        stylesheet += f.read()

    app.setPalette(styles[style].get_palette())
    app.setStyleSheet(stylesheet)

    app.setWindowIcon(QtGui.QIcon(get_theme_file(app, f"logo.png")))


def set_icons(w: QtWidgets.QMainWindow, style: str = "dark"):
    if style == "automatic":
        style = automatic_to_style(w.app) 

    w.pb_new_category.setIcon(QtGui.QIcon(get_theme_file(w.app, "category_new.svg")))
    w.pb_new_feed.setIcon(QtGui.QIcon(get_theme_file(w.app, "feed_new.svg")))
    w.pb_update_feeds.setIcon(QtGui.QIcon(get_theme_file(w.app, "update_feeds.svg")))
    w.pb_settings.setIcon(QtGui.QIcon(get_theme_file(w.app, "settings.svg")))
    w.tray.setIcon(QtGui.QIcon(get_theme_file(w.app, "tray.png")))

    w.entry_widgets["youtube"].pb_audio.setIcon(QtGui.QIcon(get_theme_file(w.app, f"audio.png")))

    w.tree_feeds.set_tree_icons()


def get_theme_file(app: QtWidgets.QApplication, file: str, style: str = None) -> str:
    style = settings.value("theme", type=str) if not style else style
    if style in ("automatic", "default"):
        style = automatic_to_style(app)
    return get_abs_path(f"rss_tube/gui/themes/{style.replace(' ', '_')}/{file}")


def get_about() -> str:
    about = dedent(f"""
    Website: <a href={__url__}>{__url__}</a><br><br>

    {__description__}
    """).strip("\n")

    return about


def get_debug_info() -> str:
    import sys
    import platform
    import lxml
    from PyQt6.QtCore import QT_VERSION_STR
    import requests
    import subprocess

    try:
        output = subprocess.check_output([settings.value("player/mpv/path", type=str), "--version"])
        mpv_version = str(output).split(" ")[1]
    except Exception:
        mpv_version = "not available"

    debug_info = dedent(f"""
    {__title__} - Version {__version__} <br><br>

    <b>Python</b>: {sys.version} <br>
    <b>Operating system</b>: {platform.system()} <br>
    <b>CPU</b>: {platform.machine()} <br>
    <b>Kernel</b>: {platform.version()} <br><br>

    <b>PyQt6</b>: {QT_VERSION_STR} <br>
    <b>lxml</b>: {lxml.__version__} <br>
    <b>requests</b>: {requests.__version__} <br><br>

    <b>mpv</b>: {mpv_version}
    """).strip("\n")

    return debug_info


def convert_links(text: str):
    if not text:
        return ""
        
    _link = re.compile(
        r'(?:(https://|http://)|(www\.))(\S+\b/?)([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]*)(\s|$)',
        re.I,
    )

    def replace(match):
        groups = match.groups()
        protocol = groups[0] or ""  # may be None
        www_lead = groups[1] or ""  # may be None
        return '<a href="http://{1}{2}" rel="nofollow">{0}{1}{2}</a>{3}{4}'.format(
            protocol, www_lead, *groups[2:]
        )

    return _link.sub(replace, text)

def open_file(filename: str):
    if platform.system() == "Linux":
        subprocess.call(["xdg-open", filename])
    elif platform.system() == "Windows":
        os.startfile(filename)
    elif platform.system() == "Darwin":
        subprocess.call(["open", filename])
