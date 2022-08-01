import os
import glob

from PyQt6 import QtCore, QtGui, QtWidgets
from functools import reduce
from textwrap import dedent

from rss_tube.database.feeds import Feeds
from rss_tube.utils import center_widget, get_abs_path


class StatisticsDialog(QtWidgets.QDialog):
    def __init__(self, mainwindow: QtWidgets.QMainWindow):
        super(StatisticsDialog, self).__init__()

        feeds: Feeds = mainwindow.feeds

        num_feeds = len(feeds.get_feeds())
        num_categories = len(feeds.get_categories())
        num_entries = reduce(lambda x, feed: x + len(feeds.get_entries(feed["id"])), feeds.get_feeds(), 0)

        path = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.StandardLocation.CacheLocation)[0]
        cache_dir = os.path.join(path, "cache")
        if os.path.exists(cache_dir):
            cache_size_bytes = reduce(lambda x, f: x + os.path.getsize(f), glob.glob(os.path.join(cache_dir, "*")), 0)
        else:
            cache_size_bytes = 0

        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setReadOnly(True)

        self.text_edit.setText(dedent(f"""
        Channels: {num_feeds}
        Entries: {num_entries}
        Categories: {num_categories}
        Cache size: {cache_size_bytes / 1e6 :.2f} MB""".lstrip("\n")))

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.addWidget(self.text_edit)

        self.setWindowTitle("Statistics")

        self.setMinimumSize(250, 140)
        self.resize(self.minimumSize())
        center_widget(mainwindow, self)
