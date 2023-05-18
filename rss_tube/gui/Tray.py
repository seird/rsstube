from PyQt6 import QtGui, QtWidgets
from rss_tube.__version__ import __title__
from rss_tube.utils import get_theme_file


class Tray(QtWidgets.QSystemTrayIcon):
    def __init__(self, mainwindow: QtWidgets.QMainWindow, theme: str = "light"):
        super(Tray, self).__init__(QtGui.QIcon(get_theme_file(mainwindow.app, f"rss_tube/gui/themes/{theme}/tray.png")))

        self.setToolTip(__title__)

        # Tray menu items
        menu = QtWidgets.QMenu()

        self.actionUpdate = QtGui.QAction("Update Channels", self)
        menu.addAction(self.actionUpdate)

        menu.addSeparator()

        self.actionNewFeed = QtGui.QAction("New Channel", self)
        menu.addAction(self.actionNewFeed)

        self.actionNewCategory = QtGui.QAction("New Category", self)
        menu.addAction(self.actionNewCategory)

        menu.addSeparator()

        self.actionSettings = QtGui.QAction("Settings", self)
        menu.addAction(self.actionSettings)

        menu.addSeparator()

        self.actionToggleWindow = QtGui.QAction("Toggle Window", self)
        menu.addAction(self.actionToggleWindow)

        menu.addSeparator()

        self.actionQuit = QtGui.QAction("Quit", self)
        menu.addAction(self.actionQuit)

        self.setContextMenu(menu)
