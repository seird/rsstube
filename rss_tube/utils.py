import logging
import os
import re

from pathlib import Path

from PyQt6 import QtGui, QtWidgets
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


def set_style(app: QtWidgets.QApplication, style: str = "dark"):
    app.setStyle("fusion")

    if style not in styles.keys():
        logger.error(f"set_style: style {style} is unsupported.")
        return

    stylesheet = ""
    with open(get_abs_path(f"rss_tube/gui/themes/{style}/{style}.css"), "r") as f:
        stylesheet += f.read()
    with open(get_abs_path(f"rss_tube/gui/themes/{style}/MainWindow.css"), "r") as f:
        s = f.read()
        s = s.replace("rss_tube", get_abs_path("rss_tube"))
        stylesheet += s
    with open(get_abs_path(f"rss_tube/gui/themes/{style}/EntryYoutube.css"), "r") as f:
        stylesheet += f.read()

    app.setPalette(styles[style].get_palette())
    app.setStyleSheet(stylesheet)

    app.setWindowIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/logo.png")))


def set_icons(w: QtWidgets.QMainWindow, style: str = "dark"):
    w.actionQuit.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/quit.png")))
    w.actionNewFeed.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/feed_new.png")))
    w.actionNewCategory.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/category_new.png")))
    w.actionImportChannels.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/import.png")))
    w.actionExportChannels.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/export.png")))
    w.actionSettings.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/settings.png")))
    w.actionCheck_for_updates.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/check_for_updates.png")))
    w.actionAbout.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/about.png")))
    w.actionShortcuts.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/shortcuts.png")))

    w.tray.actionQuit.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/quit.png")))
    w.tray.actionNewFeed.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/feed_new.png")))
    w.tray.actionNewCategory.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/category_new.png")))
    w.tray.actionUpdate.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/update_feeds.png")))
    w.tray.actionSettings.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/settings.png")))
    w.tray.actionToggleWindow.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/toggle.png")))

    w.entry_widgets["youtube"].pb_audio.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/audio.png")))

    w.tree_feeds.set_tree_icons()

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
