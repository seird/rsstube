from PyQt5 import QtWidgets

from .designs.widget_rename import Ui_Dialog
from rss_tube.utils import center_widget


class RenameDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, mainwindow: QtWidgets.QMainWindow, current_name: str):
        super(RenameDialog, self).__init__()
        self.setupUi(self)
        self.current_name = current_name
        self.new_name = current_name
        self.line_name.setText(current_name)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        center_widget(mainwindow, self)

        self.link_callbacks()

    def text_changed_callback(self, new_name: str):
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(self.current_name != new_name and new_name != "")
        self.new_name = new_name

    def link_callbacks(self):
        self.line_name.textChanged.connect(self.text_changed_callback)


class RenameCategoryDialog(RenameDialog):
    def __init__(self, mainwindow: QtWidgets.QMainWindow, current_name: str):
        super(RenameCategoryDialog, self).__init__(mainwindow, current_name)
        self.setWindowTitle("Rename category")


class RenameChannelDialog(RenameDialog):
    def __init__(self, mainwindow: QtWidgets.QMainWindow, current_name: str):
        super(RenameChannelDialog, self).__init__(mainwindow, current_name)
        self.setWindowTitle("Rename channel")
