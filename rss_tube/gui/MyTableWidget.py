from datetime import datetime
from typing import List

from PyQt5 import QtCore, QtGui, QtWidgets


class TableWidgetItemEntryContextMenu(QtWidgets.QMenu):
    def __init__(self):
        super(TableWidgetItemEntryContextMenu, self).__init__()

        self.action_delete = self.addAction("Delete Entry")


class TableWidgetItemEntry(QtWidgets.QTableWidgetItem):
    def __init__(self, text: str, entry_id: int, *args, **kwargs):
        super(TableWidgetItemEntry, self).__init__(text, *args, **kwargs)
        self.entry_id = entry_id


class MyTableWidget(QtWidgets.QTableWidget):
    def __init__(self, mainwindow):
        super(MyTableWidget, self).__init__()
        self.mainwindow = mainwindow
        self.feeds = self.mainwindow.feeds
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setColumnCount(0)
        self.setRowCount(0)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.setSortingEnabled(True)
        self.setMouseTracking(True)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # make the table cells non editable
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)  # allow only 1 cell selected at a time
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # select entire row
        self.setColumnCount(3)  # Title, Author, Date
        self.setHorizontalHeaderLabels(["Title", "Author", "Date"])
        self.setMinimumHeight(50)
        self.setShowGrid(False)
        vertical_header = self.verticalHeader()
        vertical_header.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        vertical_header.setDefaultSectionSize(22)
        table_header = self.horizontalHeader()
        table_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        table_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.last_hovered_row = None

        self.link_callbacks()

    def insert_entry(self, entry, row):
        self.insertRow(row)

        entry_viewed = self.feeds.get_entry_viewed(entry["id"])

        item_title = TableWidgetItemEntry(entry["title"], entry["id"])
        item_author = TableWidgetItemEntry(entry["author"], entry["id"])
        item_published = TableWidgetItemEntry(
            datetime.strptime(entry["published"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d, %H:%M"),
            entry["id"]
        )

        if not entry_viewed:
            # item_title.setData(QtCore.Qt.BackgroundRole, QtCore.QVariant(QtGui.QColor(QtCore.Qt.lightGray)))
            font = QtGui.QFont()
            font.setBold(True)
            item_title.setFont(font)
            item_author.setFont(font)
            item_published.setFont(font)

        self.setItem(row, 0, item_title)
        self.setItem(row, 1, item_author)
        self.setItem(row, 2, item_published)

    def get_selected_entry_id(self) -> int:
        if selected_items := self.selectedItems():
            item: TableWidgetItemEntry = selected_items[0]
            return item.entry_id
        else:
            return None

    def select_entry_id(self, entry_id: int):
        for row in range(self.rowCount()):
            item: TableWidgetItemEntry = self.item(row, 0)
            if item.entry_id == entry_id:
                self.selectRow(row)
                return

    def clear_entries(self):
        self.setRowCount(0)
        # self.clearContents()

    def display_entries(self, entries: List, select_first_row=True):
        self.clearContents()
        self.setRowCount(0)
        for row, entry in enumerate(entries):
            self.insert_entry(entry, row)

        self.sortByColumn(2, QtCore.Qt.DescendingOrder)
        if select_first_row:
            self.selectRow(0)

    def redisplay_entries(self, entries: List):
        # Get the entry ids of the currently displayed entries
        entry_ids_in_table = [self.item(i, 0).entry_id for i in range(self.rowCount())]
        # Filter out the already displayed entries
        entries_new = filter(lambda x: x["id"] not in entry_ids_in_table, entries)

        for entry in entries_new:
            self.insert_entry(entry, 0)

        self.sortByColumn(2, QtCore.Qt.DescendingOrder)

    def delete_entry(self, item: TableWidgetItemEntry):
        # Delete the entry from the table
        self.removeRow(self.row(item))

        # Delete the entry from the database
        self.feeds.delete_entry(item.entry_id)

    def current_item_changed_callback(self, current: TableWidgetItemEntry, previous: TableWidgetItemEntry):
        if not current:
            return
        current_row = current.row()
        font = QtGui.QFont()
        font.setBold(False)
        self.item(current_row, 0).setFont(font)
        self.item(current_row, 1).setFont(font)
        self.item(current_row, 2).setFont(font)

        self.mainwindow.display_entry(current.entry_id)
        self.feeds.set_entry_viewed(current.entry_id, viewed=True)

        self.mainwindow.tree_feeds.table_entry_clicked_callback(current.entry_id)

    def context_callback(self, pos: QtCore.QPoint):
        item: TableWidgetItemEntry = self.itemAt(pos)
        if item is None:
            return
        pos_mapped = self.mapToGlobal(pos)

        context_menu = TableWidgetItemEntryContextMenu()
        action = context_menu.exec_(pos_mapped)
        if action is None:
            return

        if action == context_menu.action_delete:
            self.delete_entry(item)

    def style_row_hovered(self, row: int):
        for c in range(3):
            if item := self.item(row, c):
                item.setBackground(QtGui.QBrush(QtGui.QColor(120, 120, 120, alpha=50)))

    def style_row_unhovered(self, row: int):
        for c in range(3):
            if item := self.item(row, c):
                item.setBackground(QtGui.QBrush())

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Delete:
            items = self.selectedItems()
            if items:
                self.delete_entry(items[0])
        super(MyTableWidget, self).keyPressEvent(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() in (QtCore.Qt.BackButton, QtCore.Qt.ForwardButton):
            self.mainwindow.mousePressEvent(event)
        else:
            super(MyTableWidget, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() in (QtCore.Qt.BackButton, QtCore.Qt.ForwardButton):
            self.mainwindow.mousePressEvent(event)
        else:
            super(MyTableWidget, self).mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if hovered_item := self.itemAt(event.pos()):
            row = hovered_item.row()

            if row == self.last_hovered_row:
                return super(MyTableWidget, self).mouseMoveEvent(event)

            # we entered a new row/item, reset the old row items
            if self.last_hovered_row is not None:
                self.style_row_unhovered(self.last_hovered_row)

            # highlight the new row items
            self.style_row_hovered(row)

            self.last_hovered_row = row

        return super(MyTableWidget, self).mouseMoveEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        if self.last_hovered_row is not None:
            self.style_row_unhovered(self.last_hovered_row)
            self.last_hovered_row = None
        super(MyTableWidget, self).leaveEvent(event)

    def link_callbacks(self):
        self.currentItemChanged.connect(self.current_item_changed_callback)
        self.customContextMenuRequested.connect(self.context_callback)
