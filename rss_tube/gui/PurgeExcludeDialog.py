from PyQt6 import QtCore, QtWidgets

from rss_tube.database.settings import Settings
from rss_tube.database.feeds import Feeds
from .SearchWidget import SearchWidget
from rss_tube.utils import center_widget


settings = Settings()


class ChannelCheckbox(QtWidgets.QCheckBox):
    def __init__(self, id: int, author: str, checked: bool):
        super(ChannelCheckbox, self).__init__(author)
        self.id = id
        self.setChecked(checked)
        self.stateChanged.connect(self.stateChanged_callback)
    
    def stateChanged_callback(self, a0: int):
        feeds = Feeds()
        feeds.set_purge_excluded(self.id, self.isChecked())


# A widget that contains a ChannelCheckbox and a horizontal line
class ChannelEntryWidget(QtWidgets.QWidget):
    def __init__(self, id: int, author: str, purge_excluded: bool):
        super(ChannelEntryWidget, self).__init__()
        self.id = id
        self.author = author

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(5, 0, 5, 0)

        self.checkbox = ChannelCheckbox(id, author, purge_excluded)
        self.vertical_layout.addWidget(self.checkbox)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vertical_layout.addWidget(line)


# A searchable list of channels that can be check/unchecked
class PurgeExcludeWidget(QtWidgets.QWidget):
    def __init__(self):
        super(PurgeExcludeWidget, self).__init__()

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.line_search = SearchWidget(32, "Search ...") 
        self.vertical_layout.addWidget(self.line_search)

        self.add_channels()
        self.link_callbacks()

    def add_channels(self):
        feeds = Feeds()
        for channel in feeds.get_feeds():
            entry = ChannelEntryWidget(
                channel["id"],
                channel["author"],
                channel["purge_excluded"] or False
            )
            self.vertical_layout.addWidget(entry)

        self.spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vertical_layout.addItem(self.spacer)
    
    def search_changed(self, text: str):
        text = text.lower()

        for i in range(self.vertical_layout.count()):
            if (w := self.vertical_layout.itemAt(i).widget()) and isinstance(w, ChannelEntryWidget):
                w.setVisible(text == "" or text in w.author.lower())

    def link_callbacks(self):
        self.line_search.textChanged.connect(self.search_changed)


class PurgeExcludeDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget):
        super(PurgeExcludeDialog, self).__init__()

        self.purge_excluded_widget = PurgeExcludeWidget()

        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.purge_excluded_widget)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.addWidget(self.scroll_area)

        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.purge_excluded_widget.line_search.setFocus()

        self.setWindowTitle("Check channels to exclude")
        self.setMinimumSize(int(parent.width()*0.5), int(parent.height()*0.8))
        self.resize(self.minimumSize())
        center_widget(parent, self)
