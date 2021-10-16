from PyQt6 import QtCore, QtGui, QtWidgets
from typing import Dict
from functools import reduce

from rss_tube.database.settings import Settings
from rss_tube.utils import center_widget
from rss_tube.default_settings import DEFAULT_SETTINGS


settings = Settings()


class MyQKeySequenceEditWidget(QtWidgets.QKeySequenceEdit):
    def __init__(self, key: str, sequence: QtGui.QKeySequence, used_shortcuts: Dict, settings: Settings):
        super(MyQKeySequenceEditWidget, self).__init__(sequence)
        self.key = key
        self.used_shortcuts = used_shortcuts
        settings = settings

    def editingFinished_callback(self):
        # Update the setting, if the key sequence isn't already being used
        new_sequence = self.keySequence().toString()
        sequence_is_used = reduce(
            lambda x, y: x or (y != self and y.keySequence().toString() == new_sequence),
            self.used_shortcuts,
            False
        )

        if not sequence_is_used:
            # Store the new sequence
            settings.setValue(self.key, new_sequence)
            self.used_shortcuts[self] = new_sequence
        else:
            # Restore the previous key sequence
            self.setKeySequence(settings.value(self.key))


class ShortcutsWidget(QtWidgets.QWidget):
    def __init__(self, mainwindow: QtWidgets.QMainWindow):
        super(ShortcutsWidget, self).__init__()

        self.formLayout = QtWidgets.QFormLayout(self)

        self.add_shortcut_widgets()

        center_widget(mainwindow, self)

    def add_shortcut_widgets(self):
        shortcuts = filter(lambda x: "shortcuts/" in x, DEFAULT_SETTINGS.keys())
        self.used_shortcuts = {}
        for i, s in enumerate(shortcuts):
            text = s.split("/")[1].replace("_", " ").title()
            label = QtWidgets.QLabel(f"{text:30s}")
            self.formLayout.setWidget(i, QtWidgets.QFormLayout.ItemRole.LabelRole, label)
            key_str = settings.value(s)
            key = QtGui.QKeySequence.fromString(key_str)

            keySequenceEdit = MyQKeySequenceEditWidget(s, key, self.used_shortcuts, settings)
            keySequenceEdit.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Minimum)
            keySequenceEdit.editingFinished.connect(keySequenceEdit.editingFinished_callback)

            self.used_shortcuts[keySequenceEdit] = key_str

            self.formLayout.setWidget(i, QtWidgets.QFormLayout.ItemRole.FieldRole, keySequenceEdit)

    def restore_defaults(self):
        response = QtWidgets.QMessageBox.warning(
            self,
            "Are you sure?",
            "Reset all shortcuts to their default values?",
            QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel,
            defaultButton=QtWidgets.QMessageBox.StandardButton.Cancel
        )
        if response != QtWidgets.QMessageBox.StandardButton.Ok:
            return

        for row in range(self.formLayout.rowCount()):
            label: QtWidgets.QLabel = self.formLayout.itemAt(row, QtWidgets.QFormLayout.ItemRole.LabelRole).widget()
            keyseq_edit: MyQKeySequenceEditWidget = self.formLayout.itemAt(row, QtWidgets.QFormLayout.ItemRole.FieldRole).widget()

            key = "shortcuts/" + label.text().strip().lower().replace(" ", "_")
            keyseq_edit.setKeySequence(DEFAULT_SETTINGS[key])
            settings.setValue(key, DEFAULT_SETTINGS[key])


class ShortcutsDialog(QtWidgets.QDialog):
    def __init__(self, mainwindow: QtWidgets.QMainWindow):
        super(ShortcutsDialog, self).__init__(flags=QtCore.Qt.WindowType.WindowTitleHint | QtCore.Qt.WindowType.WindowSystemMenuHint | QtCore.Qt.WindowType.WindowCloseButtonHint)

        self.shortcuts_widget = ShortcutsWidget(self)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.addWidget(self.shortcuts_widget)
        self.pb_restore_defaults = QtWidgets.QPushButton("Restore defaults")
        self.gridLayout.addWidget(self.pb_restore_defaults)
        self.pb_restore_defaults.setFocus()

        self.setWindowTitle("Keyboard Shortcuts")
        self.setMinimumWidth(300)
        center_widget(mainwindow, self)

        self.link_callbacks()

    def link_callbacks(self):
        self.pb_restore_defaults.clicked.connect(self.shortcuts_widget.restore_defaults)
