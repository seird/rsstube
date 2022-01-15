import logging
from typing import Iterable, List, Union

from rss_tube.database.settings import Settings
from rss_tube.gui.themes import unviewed_color
from rss_tube.tasks import FeedUpdateTask
from rss_tube.utils import get_abs_path
from PyQt6 import QtCore, QtGui, QtWidgets
from .MyTableWidget import MyTableWidget

logger = logging.getLogger("logger")
settings = Settings()


class TreeWidgetItemYoutubeContextMenu(QtWidgets.QMenu):
    def __init__(self, name: str):
        super(TreeWidgetItemYoutubeContextMenu, self).__init__()

        action_name = self.addAction(name)
        action_name.setDisabled(True)
        self.addSeparator()
        self.action_update = self.addAction("Update")
        self.action_mark_viewed = self.addAction("Mark Viewed")
        self.action_rename = self.addAction("Rename")
        self.addSeparator()
        self.action_open_url = self.addAction("Open Channel URL")
        self.action_open_videos_url = self.addAction("Open Channel Videos URL")
        self.addSeparator()
        self.action_delete = self.addAction("Delete Feed")
        self.action_delete_entries = self.addAction("Delete Entries")


class TreeWidgetItemSoundcloudContextMenu(QtWidgets.QMenu):
    def __init__(self, name: str):
        super(TreeWidgetItemSoundcloudContextMenu, self).__init__()

        action_name = self.addAction(name)
        action_name.setDisabled(True)
        self.addSeparator()
        self.action_update = self.addAction("Update")
        self.action_mark_viewed = self.addAction("Mark Viewed")
        self.action_rename = self.addAction("Rename")
        self.addSeparator()
        self.action_open_url = self.addAction("Open Feed URL")
        self.addSeparator()
        self.action_delete = self.addAction("Delete Feed")
        self.action_delete_entries = self.addAction("Delete Entries")


class TreeWidgetItemCategoryContextMenu(QtWidgets.QMenu):
    def __init__(self, name: str):
        super(TreeWidgetItemCategoryContextMenu, self).__init__()

        action_name = self.addAction(name)
        action_name.setDisabled(True)
        self.addSeparator()
        self.action_mark_viewed = self.addAction("Mark Viewed")
        self.action_rename = self.addAction("Rename")
        self.addSeparator()
        self.action_delete = self.addAction("Delete Category")
        self.action_delete_entries = self.addAction("Delete Entries")


class TreeWidgetItemCategory(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent: QtWidgets.QTreeWidget, text: Iterable[str], category: str):
        super(TreeWidgetItemCategory, self).__init__(text)
        self.category = category
        self.parent = parent
        self.set_font()

    def set_font(self):
        category_viewed = self.parent.feeds.get_category_viewed(self.category)
        font = QtGui.QFont()
        font.setBold(not category_viewed)
        font.setPointSize(8 if category_viewed else 10)
        self.setFont(0, font)
        self.setForeground(
            0,
            QtGui.QBrush(QtGui.QColor(
                self.parent.palette().brush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text) if category_viewed \
                else unviewed_color.get(settings.value("theme", type=str), 0x68B668)
            ))
        )

    def get_entries(self):
        return self.parent.feeds.get_entries_category(self.category)

    def context_callback(self, pos: QtCore.QPoint):
        context_menu = TreeWidgetItemCategoryContextMenu(self.text(0))
        action = context_menu.exec(pos)
        if action is None:
            return
        if action == context_menu.action_delete:
            response = QtWidgets.QMessageBox.warning(
                self.parent,
                "Are you sure?",
                f"Delete category {self.category}",
                QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel,
                defaultButton=QtWidgets.QMessageBox.StandardButton.Cancel
            )
            if response == QtWidgets.QMessageBox.StandardButton.Ok:
                self.parent.feeds.delete_category(self.category)
                self.parent.remove_category(self.category)
                logger.debug(f"Deleted Category {self.category}")
        elif action == context_menu.action_mark_viewed:
            self.parent.feeds.set_viewed(category=self.category)
            self.parent.update_viewed()
            logger.debug(f"Marked category {self.category} status as viewed")
        elif action == context_menu.action_delete_entries:
            response = QtWidgets.QMessageBox.warning(
                self.parent,
                "Are you sure?",
                f"Delete all entries in {self.category}",
                QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel,
                defaultButton=QtWidgets.QMessageBox.StandardButton.Cancel
            )
            if response == QtWidgets.QMessageBox.StandardButton.Ok:
                self.parent.feeds.delete_entries_in_category(self.category)
                logger.debug(f"Deleted all entries in category {self.category}")
                self.parent.table_entries.clear_entries()
        elif action == context_menu.action_rename:
            self.parent.mainwindow.change_category_name(self.category)


class TreeWidgetItemFeed(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent: QtWidgets.QTreeWidget, text: Iterable[str], feed_id: int):
        super(TreeWidgetItemFeed, self).__init__(text)
        self.feed_id = feed_id
        self.parent = parent
        self.set_font()
        self.context_menu = None

    def set_font(self):
        feed_viewed = self.parent.feeds.get_feed_viewed(self.feed_id)
        font = QtGui.QFont()
        font.setBold(not feed_viewed)
        font.setPointSize(8 if feed_viewed else 10)
        self.setFont(0, font)
        self.setForeground(
            0,
            QtGui.QBrush(QtGui.QColor(
                self.parent.palette().brush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text) if feed_viewed \
                else unviewed_color.get(settings.value("theme", type=str), 0x68B668)
            ))
        )

    def get_entries(self):
        return self.parent.feeds.get_entries(self.feed_id)

    def context_callback(self, pos: QtCore.QPoint):
        if not self.context_menu:
            return
        context_menu = self.context_menu(self.text(0))
        action = context_menu.exec(pos)
        if action is None:
            return
        if action == getattr(context_menu, "action_delete"):
            response = QtWidgets.QMessageBox.warning(
                self.parent,
                "Are you sure?",
                f"Delete feed {self.text(0)}",
                QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel,
                defaultButton=QtWidgets.QMessageBox.StandardButton.Cancel
            )
            if response == QtWidgets.QMessageBox.StandardButton.Ok:
                self.parent.remove_feed(self.feed_id)
                self.parent.feeds.delete_feed(self.feed_id)
                self.parent.update_viewed()
                logger.debug(f"Deleted Feed {self.feed_id}")
        elif action == getattr(context_menu, "action_mark_viewed"):
            self.parent.feeds.set_viewed(feed_id=self.feed_id)
            self.parent.update_viewed()
            logger.debug(f"Marked feed {self.feed_id} status as viewed")
        elif action == getattr(context_menu, "action_rename"):
            self.parent.mainwindow.change_channel_name(self.text(0), self.feed_id)
        elif action == getattr(context_menu, "action_delete_entries"):
            response = QtWidgets.QMessageBox.warning(
                self.parent,
                "Are you sure?",
                f"Delete all entries in {self.text(0)}",
                QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel,
                defaultButton=QtWidgets.QMessageBox.StandardButton.Cancel
            )
            if response == QtWidgets.QMessageBox.StandardButton.Ok:
                self.parent.feeds.delete_entries_in_feed(self.feed_id)
                logger.debug(f"Deleted all entries in feed {self.feed_id}")
                self.parent.table_entries.clear_entries()
        elif action == getattr(context_menu, "action_update"):
            self.feed_update_task = FeedUpdateTask(self.feed_id)
            self.feed_update_task.finished.connect(lambda: self.parent.mainwindow.update_feeds_finished(enable_buttons=False))
            self.feed_update_task.start()
        elif action == getattr(context_menu, "action_open_url"):
            channel_url = self.parent.feeds.get_feed(self.feed_id)["channel_url"]
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(channel_url))
        elif action == getattr(context_menu, "action_open_videos_url"):
            channel_url = self.parent.feeds.get_feed(self.feed_id)["channel_url"]
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(channel_url + "/videos"))


class TreeWidgetItemYoutube(TreeWidgetItemFeed):
    def __init__(self, parent: QtWidgets.QTreeWidget, text: Iterable[str], feed_id: int):
        super(TreeWidgetItemYoutube, self).__init__(parent, text, feed_id)
        self.context_menu = TreeWidgetItemYoutubeContextMenu    


class TreeWidgetItemSoundcloud(TreeWidgetItemFeed):
    def __init__(self, parent: QtWidgets.QTreeWidget, text: Iterable[str], feed_id: int):
        super(TreeWidgetItemSoundcloud, self).__init__(parent, text, feed_id)
        self.context_menu = TreeWidgetItemSoundcloudContextMenu   


class MyTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, mainwindow):
        super(MyTreeWidget, self).__init__()
        self.mainwindow = mainwindow
        self.table_entries: MyTableWidget = mainwindow.table_entries
        self.feeds = mainwindow.feeds

        self.setIndentation(10)
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setAlternatingRowColors(False)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)

        self.build_tree()

        self.link_callbacks()

    def build_tree(self):
        """
        Initialize the tree
        """
        self.clear()
        categories = self.feeds.get_categories()
        for category in categories:
            self.add_category(category)
        self.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)

        self.set_tree_icons()

    def add_category(self, category: str):
        """
        Add a single category and all its corresponding feeds
        """
        twi = TreeWidgetItemCategory(self, [category], category)
        for feed in self.feeds.get_feeds_in_category(category):
            if feed["type"] == "youtube":
                child_item = TreeWidgetItemYoutube(self, [feed["author"]], feed["id"])
            elif feed["type"] == "soundcloud":
                child_item = TreeWidgetItemSoundcloud(self, [feed["author"]], feed["id"])
            else:
                continue 
            twi.addChild(child_item)
        category_expanded = settings.value(f"MyTreeWidget/{category}_expanded", 1, type=bool)
        self.addTopLevelItem(twi)
        twi.setExpanded(category_expanded)
        self.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)

        self.set_tree_icons()

    def add_feed(self, feed_id: int):
        """
        Add a single feed
        """
        category = self.feeds.get_category(feed_id)
        category_items: List[TreeWidgetItemCategory] = self.findItems(category, QtCore.Qt.MatchFlag.MatchExactly)
        if not category_items:
            twi = TreeWidgetItemCategory(self, [category], category)
            twi.setExpanded(True)
            self.addTopLevelItem(twi)
            self.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
            category_item = twi
        else:
            category_item = category_items[0]

        feed = self.feeds.get_feed(feed_id)
        if feed["type"] == "youtube":
            child_item = TreeWidgetItemYoutube(self, [feed["author"]], feed["id"])
        elif feed["type"] == "soundcloud":
            child_item = TreeWidgetItemSoundcloud(self, [feed["author"]], feed["id"])
        else:
            return
        category_item.addChild(child_item)
        self.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.update_viewed()

        self.set_tree_icons()

    def remove_category(self, category: str):
        category_items = self.findItems(category, QtCore.Qt.MatchFlag.MatchExactly)
        if not category_items:
            return
        category_item_to_remove = category_items[0]
        self.takeTopLevelItem(self.indexOfTopLevelItem(category_item_to_remove))

    def remove_feed(self, feed_id: int):
        feed = self.feeds.get_feed(feed_id)
        if not feed:
            return
        category = self.feeds.get_category(feed["id"])
        if category is None:
            return

        category_items = self.findItems(category, QtCore.Qt.MatchFlag.MatchExactly)
        if not category_items:
            return

        feed_items = self.findItems(feed["author"], QtCore.Qt.MatchFlag.MatchExactly | QtCore.Qt.MatchFlag.MatchRecursive)
        if not feed_items:
            return
        feed_item_to_remove = feed_items[0]
        category_item = category_items[0]
        category_item.removeChild(feed_item_to_remove)

    def set_tree_icons(self):
        style = settings.value("theme", type=str)
        show_category_icon = settings.value("MainWindow/category_icon/show", type=bool)
        show_feed_icon = settings.value("MainWindow/feed_icon/show", type=bool)
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)

            if show_category_icon:
                item.setIcon(0, QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/category.svg")))
            
            if not show_feed_icon:
                continue
            
            for j in range(item.childCount()):
                child = item.child(j)
                if isinstance(child, TreeWidgetItemYoutube):
                    icon = "youtube"
                elif isinstance(child, TreeWidgetItemSoundcloud):
                    icon = "soundcloud"
                else:
                    continue
                child.setIcon(0, QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{style}/{icon}.svg")))


    def table_entry_clicked_callback(self, entry_id: int):
        """ Update viewed status of tree entries """
        # Get the corresponding feed and category
        feed = self.feeds.get_feed_from_entry(entry_id)
        if feed is None:
            return
        category = self.feeds.get_category(feed["id"])
        if category is None:
            return

        for item_category in self.findItems(category, QtCore.Qt.MatchFlag.MatchExactly):
            item_category.set_font()

        for item_feed in self.findItems(feed["author"], QtCore.Qt.MatchFlag.MatchExactly | QtCore.Qt.MatchFlag.MatchRecursive):
            item_feed.set_font()

    def redisplay_selected(self):
        selected_items: List[Union[TreeWidgetItemFeed, TreeWidgetItemCategory]] = self.selectedItems()
        if not selected_items:
            logger.debug("MyTreeWidget: redisplay_selected: no category or feed selected.")
            return

        selected_item = selected_items[0]

        if isinstance(selected_item, TreeWidgetItemFeed):
            entries = self.feeds.get_entries(selected_item.feed_id)
            logger.debug(f"MyTreeWidget: redisplay_selected: feed {selected_item.feed_id} selected")
        elif isinstance(selected_item, TreeWidgetItemCategory):
            entries = self.feeds.get_entries_category(selected_item.category)
            logger.debug(f"MyTreeWidget: redisplay_selected: category {selected_item.category} selected")
        else:
            return

        self.table_entries.redisplay_entries(entries)

    def update_viewed(self):
        # Update the font of all items in the tree widget
        for i in range(self.topLevelItemCount()):
            category_item: TreeWidgetItemCategory = self.topLevelItem(i)
            category_item.set_font()
            for j in range(category_item.childCount()):
                feed_item: TreeWidgetItemFeed = category_item.child(j)
                feed_item.set_font()

        # Update the font of all the items in the table widget
        self.item_changed_callback(select_first_row=False)

    def item_changed_callback(self, select_first_row=True):
        self.mainwindow.line_search.clear()
        item: Union[TreeWidgetItemFeed, TreeWidgetItemCategory] = self.selectedItems()
        if not item:
            return

        item = item[0]

        entries = item.get_entries()

        if entries:
            self.table_entries.display_entries(entries, select_first_row=select_first_row)
        else:
            self.table_entries.clear_entries()

    def context_callback(self, pos: QtCore.QPoint):
        item: Union[TreeWidgetItemFeed, TreeWidgetItemCategory, QtWidgets.QTreeWidgetItem] = self.itemAt(pos)
        if item is None:
            return
        pos_mapped = self.mapToGlobal(pos)
        item.context_callback(pos_mapped)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() in (QtCore.Qt.MouseButton.BackButton, QtCore.Qt.MouseButton.ForwardButton):
            self.mainwindow.mousePressEvent(event)
        elif event.button() != QtCore.Qt.MouseButton.RightButton:
            super(MyTreeWidget, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() in (QtCore.Qt.MouseButton.BackButton, QtCore.Qt.MouseButton.ForwardButton):
            self.mainwindow.mousePressEvent(event)
        else:
            super(MyTreeWidget, self).mouseDoubleClickEvent(event)

    def link_callbacks(self):
        self.itemSelectionChanged.connect(self.item_changed_callback)
        self.itemExpanded.connect(lambda x: settings.setValue(f"MyTreeWidget/{x.category}_expanded", 1))
        self.itemCollapsed.connect(lambda x: settings.setValue(f"MyTreeWidget/{x.category}_expanded", 0))
        self.customContextMenuRequested.connect(self.context_callback)
