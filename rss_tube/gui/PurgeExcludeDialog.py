from PyQt6 import QtWidgets

from rss_tube.database.settings import Settings
from rss_tube.database.feeds import Feeds
from rss_tube.utils import center_widget


settings = Settings()


class ChannelCheckbox(QtWidgets.QCheckBox):
    def __init__(self, id: int, author: str):
        super(ChannelCheckbox, self).__init__(author)
        self.id = id
    
    def stateChanged_callback(self, a0: int):
        feeds = Feeds()
        feeds.set_purge_excluded(self.id, self.isChecked())        


class PurgeExcludeWidget(QtWidgets.QWidget):
    def __init__(self, mainwindow: QtWidgets.QMainWindow):
        super(PurgeExcludeWidget, self).__init__()

        self.vertical_layout = QtWidgets.QVBoxLayout(self)

        self.add_channels()

        center_widget(mainwindow, self)

    def add_channels(self):
        feeds = Feeds()
        for channel in feeds.get_feeds():
            cb = ChannelCheckbox(
                id=channel["id"],
                author=channel["author"]
            )
            cb.setChecked(channel["purge_excluded"])
            cb.stateChanged.connect(cb.stateChanged_callback)
            self.vertical_layout.addWidget(cb)


class PurgeExcludeDialog(QtWidgets.QDialog):
    def __init__(self, mainwindow: QtWidgets.QMainWindow):
        super(PurgeExcludeDialog, self).__init__()

        self.purge_excluded_widget = PurgeExcludeWidget(self)

        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidget(self.purge_excluded_widget)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.addWidget(self.scroll_area)

        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.setWindowTitle("Check channels to exclude from the purge")
        self.setMinimumWidth(300)
        center_widget(mainwindow, self)
