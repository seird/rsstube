from typing import List

from PyQt6 import QtCore, QtWidgets

from rss_tube.database.settings import Settings
from rss_tube.utils import center_widget
from .designs.widget_new_feed import Ui_Dialog


settings = Settings()


class NewFeedDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, mainwindow: QtWidgets.QMainWindow, categories: List[str], theme="light"):
        super(NewFeedDialog, self).__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.WindowContextHelpButtonHint)

        self.setupUi(self)

        self.combo_categories.addItems(categories)

        self.resize(self.size().width(), self.sizeHint().height())

        self.mainwindow = mainwindow

        category_selected = settings.value("new_feed_dialog/selected_category", "", type=str)
        if self.combo_categories.findText(category_selected) >= 0:
            self.combo_categories.setCurrentText(category_selected)

        self.set_whatsthis()

        center_widget(mainwindow, self)

        self.link_callbacks()

    def set_whatsthis(self):
        str_valid_url = "Valid URL formats:\n"
        str_valid_url += " - https://www.youtube.com/user/<username>\n"
        str_valid_url += " - https://www.youtube.com/channel/<channel_id>\n"
        str_valid_url += " - https://www.youtube.com/c/<channel_name>\n"
        str_valid_url += " - https://www.youtube.com/@<username>\n"
        str_valid_url += " - https://www.youtube.com/feeds/videos.xml?user=<username>\n"
        str_valid_url += " - https://www.youtube.com/feeds/videos.xml?channel_id=<channel_id>\n"
        str_valid_url += " - https://soundcloud.com/<username>\n"
        str_valid_url += " - https://feeds.soundcloud.com/users/soundcloud:users:<user_id>/sounds.rss"
        self.line_new_feed.setWhatsThis(str_valid_url)

    def link_callbacks(self):
        self.combo_categories.currentTextChanged.connect(
            lambda _: settings.setValue("new_feed_dialog/selected_category", self.combo_categories.currentText())
        )
