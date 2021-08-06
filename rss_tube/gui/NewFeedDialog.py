from typing import List

from PyQt5 import QtWidgets

from rss_tube.database.settings import Settings
from rss_tube.utils import center_widget
from .designs.widget_new_feed import Ui_Dialog


settings = Settings("rss-tube")


class NewFeedDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, mainwindow: QtWidgets.QMainWindow, categories: List[str], theme="light"):
        super(NewFeedDialog, self).__init__()
        self.setupUi(self)

        self.combo_categories.addItems(categories)

        self.setFixedSize(self.size())

        self.mainwindow = mainwindow

        notifications_checked = settings.value("new_feed_dialog/receive_notifications", type=bool)
        self.cb_receive_notifications.setChecked(notifications_checked if notifications_checked is not None else True)

        category_selected = settings.value("new_feed_dialog/selected_category", "", type=str)
        if self.combo_categories.findText(category_selected) >= 0:
            self.combo_categories.setCurrentText(category_selected)

        center_widget(mainwindow, self)

        self.link_callbacks()

    def link_callbacks(self):
        self.cb_receive_notifications.stateChanged.connect(
            lambda _: settings.setValue("new_feed_dialog/receive_notifications", self.cb_receive_notifications.isChecked())
        )

        self.combo_categories.currentTextChanged.connect(
            lambda _: settings.setValue("new_feed_dialog/selected_category", self.combo_categories.currentText())
        )
