from PyQt6 import QtCore, QtGui, QtWidgets

from rss_tube.__version__ import __version__, __title__
from .designs.widget_help import Ui_Dialog
from rss_tube.database.settings import Settings
from rss_tube.utils import get_abs_path, center_widget, get_about, get_debug_info


settings = Settings()


class AboutDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, mainwindow: QtWidgets.QMainWindow):
        super(AboutDialog, self).__init__()
        self.setupUi(self)

        self.setWindowTitle(f"About {__title__}")

        self.text_debug_info.setHtml(get_debug_info())
        self.label_about.setText(get_about())
        self.label_about.setOpenExternalLinks(True)
        self.label_about.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label_about.setWordWrap(True)

        self.label_logo.setPixmap(QtGui.QPixmap(get_abs_path(f"rss_tube/gui/themes/{settings.value('theme', type=str)}/logo.png")))
        self.label_title.setText(f"  {__title__} {__version__}")
        self.label_title.setFont(QtGui.QFont("", 22, QtGui.QFont.Weight.Bold))

        center_widget(mainwindow, self)

        self.link_callbacks()

    def copy_to_clipboard_callback(self):
        text_to_copy = self.text_debug_info.toPlainText()
        cb = QtWidgets.QApplication.clipboard()
        cb.clear(mode=QtGui.QClipboard.Mode.Clipboard)
        cb.setText(text_to_copy, mode=QtGui.QClipboard.Mode.Clipboard)

    def link_callbacks(self):
        self.pb_copy_to_clipboard.clicked.connect(self.copy_to_clipboard_callback)
