from PyQt6 import QtCore, QtGui, QtWidgets


class SearchWidget(QtWidgets.QLineEdit):
    def __init__(self, height: int, placeholder: str):
        super(SearchWidget, self).__init__()
        self.setPlaceholderText(placeholder)
        self.setClearButtonEnabled(True)
        self.setFixedHeight(height)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == QtCore.Qt.Key.Key_Escape:
            self.clear()
        else:
            super().keyPressEvent(e)
