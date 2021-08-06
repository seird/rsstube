from PyQt5 import QtGui, QtWidgets
from rss_tube.__version__ import __title__
from rss_tube.utils import get_abs_path


class Tray(QtWidgets.QSystemTrayIcon):
    def __init__(self, theme: str = "light"):
        super(Tray, self).__init__(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{theme}/tray.png")))

        self.setToolTip(__title__)

        # Tray menu items
        menu = QtWidgets.QMenu()

        self.actionUpdate = QtWidgets.QAction("Update Channels", self)
        menu.addAction(self.actionUpdate)

        menu.addSeparator()

        self.actionNewFeed = QtWidgets.QAction("New Channel", self)
        menu.addAction(self.actionNewFeed)

        self.actionNewCategory = QtWidgets.QAction("New Category", self)
        menu.addAction(self.actionNewCategory)

        menu.addSeparator()

        self.actionSettings = QtWidgets.QAction("Settings", self)
        menu.addAction(self.actionSettings)

        menu.addSeparator()

        self.actionToggleWindow = QtWidgets.QAction("Toggle Window", self)
        menu.addAction(self.actionToggleWindow)

        menu.addSeparator()

        self.actionQuit = QtWidgets.QAction("Quit", self)
        menu.addAction(self.actionQuit)

        self.setContextMenu(menu)
