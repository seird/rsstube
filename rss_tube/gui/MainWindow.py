import datetime
import getpass
import logging
import os
import sys
import tempfile
from typing import Optional
import webbrowser

from PyQt6 import QtWidgets, QtGui, QtCore, QtNetwork

from rss_tube.__version__ import __title__, __version__
from rss_tube.database.feeds import Feeds
from rss_tube.database.settings import Settings
from rss_tube.gui.EntryWidgets.BaseEntry import BaseEntry
from rss_tube.updater import Updater
from rss_tube.utils import get_abs_path, set_icons, set_style
from rss_tube.tasks import Tasks, AddFeedTask, ExportFeedsTask, ImportFeedsTask
from .AboutDialog import AboutDialog
from .RenameDialog import RenameCategoryDialog, RenameChannelDialog
from .ShortcutDialog import ShortcutsDialog
from .StatisticsDialog import StatisticsDialog
from .EntryWidgets import EntryYoutube, EntrySoundcloud
from .MyTableWidget import MyTableWidget
from .MyTreeWidget import MyTreeWidget, TreeWidgetItemStarred
from .NewFeedDialog import NewFeedDialog
from .SearchWidget import SearchWidget
from .SettingsDialog import SettingsDialog
from .Tray import Tray
from .designs.main_window import Ui_MainWindow

settings = Settings()
logger = logging.getLogger("logger")

if (level := settings.value("logging/level", type=str)) != "Disabled":
    logger.setLevel(level)
else:
    logging.disable()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow, QtCore.QCoreApplication):
    def __init__(self, app: QtWidgets.QApplication):
        super(MainWindow, self).__init__()
        self.app = app

    def init_ui(self):
        self.setupUi(self)

        self.setWindowTitle(__title__)

        set_style(self.app, style=settings.value("theme", type=str))

        self.feeds = Feeds()
        self.tasks_thread = Tasks()
        
        self.lock_server = QtNetwork.QLocalServer()
        self.lock_server.setSocketOptions(QtNetwork.QLocalServer.SocketOption.UserAccessOption)
        self.lock_server.listen("rsstube.socket")

        self.table_entries = MyTableWidget(self)
        self.horizontalLayout_entries.addWidget(self.table_entries)

        self.tree_feeds = MyTreeWidget(self)
        self.verticalLayout.addWidget(self.tree_feeds)

        icon_height = settings.value("MainWindow/icon/height", type=int)
        icon_width = settings.value("MainWindow/icon/width", type=int)
        self.pb_settings.setFixedSize(QtCore.QSize(icon_width, icon_height))
        self.pb_settings.setToolTip("Settings")
        self.pb_new_feed.setFixedSize(QtCore.QSize(icon_width, icon_height))
        self.pb_new_feed.setToolTip("Add a new channel")
        self.pb_new_category.setFixedSize(QtCore.QSize(icon_width, icon_height))
        self.pb_new_category.setToolTip("Add a new category")
        self.pb_update_feeds.setFixedSize(QtCore.QSize(icon_width, icon_height))
        self.pb_update_feeds.setToolTip("Update channels")

        self.line_search = SearchWidget(icon_height, f"  Filter {settings.value('shortcuts/filter', type=str)} ...")
        self.horizontalLayout_buttons.addWidget(self.line_search)

        self.menubar.setVisible(settings.value("MainWindow/menu/show", type=bool))

        self.tray = Tray(settings.value("theme", type=str))
        if settings.value("tray/show", type=bool):
            self.tray.show()

        self.restore_window_state()

        self.entry_widgets = {
            # "": None,  # default entry TODO
            "youtube": EntryYoutube(self),
            "soundcloud": EntrySoundcloud(self),
        }
        for feed_type in self.entry_widgets:
            self.layout_entry.insertWidget(0, self.entry_widgets[feed_type])
            self.entry_widgets[feed_type].hide()

        self.link_callbacks()
        self.tasks_thread.start()
        self.init_shortcuts()
        self.set_shortcuts()

        # self.resize(self.minimumSizeHint())
        set_icons(self, style=settings.value("theme", type=str))

        self.show()
        self.window_state_to_restore = QtCore.Qt.WindowState.WindowNoState
        
        if settings.value("MainWindow/start_minimized", type=bool) and settings.value("tray/show", type=bool):
            self.tray_activated_callback(QtWidgets.QSystemTrayIcon.ActivationReason.Trigger)
        

    def acquire_lock(self, force: bool = False) -> bool:
        temp_dir = tempfile.gettempdir()
        lock_filename = os.path.join(temp_dir, "rsstube-" + getpass.getuser() + ".lock")
        self.lock_file = QtCore.QLockFile(lock_filename)
        if force:
            self.lock_file.removeStaleLockFile()
        self.lock_file.setStaleLockTime(0)
        return self.lock_file.tryLock()

    def restore_window_state(self):
        # settings.beginGroup("MainWindow")
        window_geometry = settings.value("MainWindow/geometry", type=QtCore.QByteArray)
        window_state = settings.value("MainWindow/state", type=QtCore.QByteArray)
        splitter_horizontal = settings.value("MainWindow/splitter_horizontal", type=QtCore.QByteArray)
        splitter_vertical = settings.value("MainWindow/splitter_vertical", type=QtCore.QByteArray)
        # settings.endGroup()

        if window_geometry:
            self.restoreGeometry(window_geometry)
        if window_state:
            self.restoreState(window_state)
        if splitter_horizontal:
            self.splitter_horizontal.restoreState(splitter_horizontal)
        if splitter_vertical:
            self.splitter_vertical.restoreState(splitter_vertical)

    def save_window_state(self):
        # settings.beginGroup("MainWindow")
        settings.setValue("MainWindow/geometry", self.saveGeometry())
        settings.setValue("MainWindow/state", self.saveState())
        settings.setValue("MainWindow/splitter_horizontal", self.splitter_horizontal.saveState())
        settings.setValue("MainWindow/splitter_vertical", self.splitter_vertical.saveState())
        # settings.endGroup()

    def tray_activated_callback(self, reason: QtWidgets.QSystemTrayIcon.ActivationReason):
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            if self.windowState() & QtCore.Qt.WindowState.WindowMinimized or self.windowState() == (QtCore.Qt.WindowState.WindowMinimized | QtCore.Qt.WindowState.WindowMaximized):
                self.show()
                self.setWindowState(self.window_state_to_restore | QtCore.Qt.WindowState.WindowActive)  # Set the window to its normal state
            else:
                window_state_temp = self.windowState()
                self.setWindowState(QtCore.Qt.WindowState.WindowMinimized)
                self.hide()
                self.window_state_to_restore = window_state_temp

    def settings_callback(self):
        settings_dialog = SettingsDialog(self)
        accepted = settings_dialog.exec()

        self.set_shortcuts()

        if accepted and settings_dialog.settings_changed:
            settings_dialog.apply_settings()
            logger.debug("MainWindow: settings_dialog: user clicked Ok and new settings are applied.")

        if settings_dialog.changes_applied and settings_dialog.schedule_changed:
            self.tasks_thread.set_schedule()

    def search_text_changed_callback(self, text):
        text = text.lower()

        if text == "":
            for row in range(self.table_entries.rowCount()):
                self.table_entries.showRow(row)
            return

        for row in range(self.table_entries.rowCount()):
            title = self.table_entries.item(row, 0).text()
            author = self.table_entries.item(row, 1).text()
            if text in title.lower() or text in author.lower():
                self.table_entries.showRow(row)
            else:
                self.table_entries.hideRow(row)

    def check_for_updates_callback(self):
        self.updater = Updater()
        self.updater.new_update_available.connect(self.new_update_available_callback)
        self.updater.no_update_available.connect(
            lambda: QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Icon.Information,
                f"Already using the latest {__title__} version.",
                "No updates available.\nYou are already using the latest version.",
                parent=self
            ).exec()
        )
        self.updater.start()

    def new_update_available_callback(self, message: dict):
        text = f"Version {message['version']} is available.\nYou are currently using version {__version__}.\nGo to the download page?"
        if message['releaseNotes']:
            text += "\n\nRelease Notes:\n"
            text += "\n".join(message['releaseNotes'])
        mb = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Icon.Information,
            "New version available",
            text,
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel,
            parent=self
        )

        r = mb.exec()

        if r == QtWidgets.QMessageBox.StandardButton.Yes:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(message['url']))

    def about_callback(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def shortcuts_callback(self):
        dialog = ShortcutsDialog(self)
        dialog.exec()
        self.set_shortcuts()

    def statistics_callback(self):
        dialog = StatisticsDialog(self)
        dialog.exec()

    def play_video(self, play_quality_once: str = ""):
        if entry_widget := self.get_current_entry_widget():
            entry_widget.play_video(play_quality_once=play_quality_once)

    def play_in_browser(self):
        if entry_widget := self.get_current_entry_widget():
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(entry_widget.video_url))

    def toggle_star_callback(self):
        if entry_widget := self.get_current_entry_widget():
            entry_widget.toggle_star()

    def new_feed_callback(self):
        categories = self.feeds.get_categories()
        dialog = NewFeedDialog(self, categories, theme=settings.value("theme", type=str))
        accepted = dialog.exec()
        if not accepted:
            return
        feed_url = dialog.line_new_feed.text()
        category = dialog.combo_categories.currentText()
        feed_name = dialog.line_name.text()
        if feed_url and category:
            self.add_feed_task = AddFeedTask(feed_url, category, feed_name)
            self.add_feed_task.added.connect(lambda feed_id: self.tree_feeds.add_feed(feed_id))
            self.add_feed_task.run()

    def new_category_callback(self):
        category, ok = QtWidgets.QInputDialog.getText(self, "Add new a category", "New category:" + " " * 96)
        if ok and category:
            if self.feeds.add_category(category):
                self.tree_feeds.add_category(category)

    def import_channels_callback(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Import", settings.value("MainWindow/export_location", type=str), "*")[0]
        if fname and os.path.exists(fname):
            self.import_feeds_task = ImportFeedsTask(fname)
            self.import_feeds_task.imported.connect(self.channel_imported_callback)
            self.import_feeds_task.start()

    def channel_imported_callback(self, feed_id: int):
        self.feeds.update_feed_entries(feed_id)
        self.tree_feeds.add_feed(feed_id)

    def export_channels_callback(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, "Save", settings.value("MainWindow/export_location", type=str), "*")[0]
        if fname and os.path.exists(os.path.dirname(fname)):
            self.export_feeds_task = ExportFeedsTask(fname)
            self.export_feeds_task.start()
            settings.setValue("MainWindow/export_location", fname)

    def update_feeds_callback(self):
        settings.set_last_refresh()
        self.tasks_thread.feed_update_task.start()

    def job_update_info_callback(self, last_run: datetime.datetime, next_run: datetime.datetime):
        tooltip = "Update channels"
        tooltip += f"\nLast run: {last_run.strftime('%H:%M')}"
        tooltip += f"\nNext run: {next_run.strftime('%H:%M')}"
        self.pb_update_feeds.setToolTip(tooltip)

    def update_feeds_started(self):
        self.pb_update_feeds.setEnabled(False)
        self.tray.actionUpdate.setEnabled(False)
        self.pb_update_feeds.setToolTip("Updating channels...")

    def update_feeds_finished(self, enable_buttons: bool = True):
        if enable_buttons:
            self.pb_update_feeds.setEnabled(True)
            self.tray.actionUpdate.setEnabled(True)

        last_refresh = settings.value("last_refresh", type=str)
        settings.set_last_refresh()

        if self.feeds.get_new_entries(last_refresh):
            # Insert the new entries
            selected_entry_id = self.table_entries.get_selected_entry_id()

            self.tree_feeds.redisplay_selected()
            self.tree_feeds.update_viewed()

            self.table_entries.select_entry_id(selected_entry_id)
        else:
            return

        if new_entries_unviewed := self.feeds.get_new_entries_unviewed(last_refresh):
            # Display a popup notification
            if settings.value("tray/notifications/enabled", type=bool):
                titles = ", ".join(x["title"] for x in new_entries_unviewed)
                logger.debug(f"update_feeds_finished: {len(new_entries_unviewed)} new entries to notify." + titles)
                self.display_notification(f"{len(new_entries_unviewed)} new entries.")

            # Change to tray icon to show that there are new entries
            if settings.value("tray/show", type=bool) and (self.windowState() & QtCore.Qt.WindowState.WindowMinimized):
                self.tray.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{settings.value('theme', type=str)}/tray_new.png")))

    def display_entry(self, entry_id: int):
        entry = self.feeds.get_entry(entry_id)
        if not entry:
            return
        feed_id = entry["feed_id"]
        feed_type = self.feeds.get_feed_type(feed_id)
        if entry is None:
            logger.debug(f"MainWindow: feed_id {feed_id} ({feed_type}), entry_id {entry_id}: entry does not exist.")
            return
        entry_to_display = self.entry_widgets.get(feed_type)
        entry_to_display.display_entry(entry)
        for entry_type in self.entry_widgets:
            if feed_type != entry_type:
                self.entry_widgets[entry_type].hide()
        entry_to_display.show()

    def get_current_entry_widget(self) -> Optional[BaseEntry]:
        for entry_type in self.entry_widgets:
            if self.entry_widgets[entry_type].isVisible():
                return self.entry_widgets[entry_type]
        return None

    def unstarred_callback(self):
        if self.tree_feeds.is_itemtype_selected(TreeWidgetItemStarred):
            self.table_entries.pop_selected_entry()
            # self.tree_feeds.redisplay_selected()

    def display_previous_entry(self):
        current_row = self.table_entries.currentRow()
        self.table_entries.selectRow(max(0, current_row-1))

    def display_next_entry(self):
        current_row = self.table_entries.currentRow()
        self.table_entries.selectRow(min(self.table_entries.rowCount(), current_row + 1))

    def open_database_callback(self):
        webbrowser.open(self.feeds.database.dir)

    def open_log_callback(self):
        webbrowser.open(logger.root.handlers[0].baseFilename)

    def change_category_name(self, current_name: str):
        dialog = RenameCategoryDialog(self, current_name)
        current_categories = [c for c in self.feeds.get_categories() if c != current_name]
        if dialog.exec() and dialog.new_name not in current_categories:
            self.feeds.update_category_name(current_name, dialog.new_name)
            self.tree_feeds.build_tree()

    def change_channel_name(self, current_name: str, feed_id: int):
        dialog = RenameChannelDialog(self, current_name)
        if dialog.exec():
            self.feeds.update_feed_name(feed_id, dialog.new_name)
            self.tree_feeds.build_tree()

    def display_notification(self,
                             message: str,
                             icon: QtWidgets.QSystemTrayIcon.MessageIcon = QtWidgets.QSystemTrayIcon.MessageIcon.Information):
        if not settings.value("tray/notifications/enabled", type=bool) or not settings.value("tray/show", type=bool):
            return

        self.tray.showMessage(
            self.windowTitle(),
            message,
            icon,
            settings.value("tray/notifications/duration_ms", type=int)
        )

    def bring_to_front(self):
        self.ensurePolished()
        self.setWindowState((self.windowState() & ~QtCore.Qt.WindowState.WindowMinimized) | QtCore.Qt.WindowState.WindowActive)
        self.show()
        self.activateWindow()

    def link_callbacks(self):
        self.pb_previous.hide()
        self.pb_next.hide()
        self.pb_previous.clicked.connect(self.display_previous_entry)
        self.pb_next.clicked.connect(self.display_next_entry)
        self.pb_new_feed.clicked.connect(self.new_feed_callback)
        self.pb_update_feeds.clicked.connect(self.update_feeds_callback)
        self.pb_new_category.clicked.connect(self.new_category_callback)
        self.pb_settings.clicked.connect(self.settings_callback)

        self.actionNewFeed.triggered.connect(self.new_feed_callback)
        self.actionNewCategory.triggered.connect(self.new_category_callback)
        self.actionExportChannels.triggered.connect(self.export_channels_callback)
        self.actionImportChannels.triggered.connect(self.import_channels_callback)
        self.actionSettings.triggered.connect(self.settings_callback)
        self.actionQuit.triggered.connect(self.close)
        self.actionCheck_for_updates.triggered.connect(self.check_for_updates_callback)
        self.actionAbout.triggered.connect(self.about_callback)
        self.actionShortcuts.triggered.connect(self.shortcuts_callback)
        self.actionStatistics.triggered.connect(self.statistics_callback)

        self.tray.actionQuit.triggered.connect(self.close)
        self.tray.actionNewFeed.triggered.connect(self.new_feed_callback)
        self.tray.actionNewCategory.triggered.connect(self.new_category_callback)
        self.tray.actionUpdate.triggered.connect(self.update_feeds_callback)
        self.tray.actionSettings.triggered.connect(self.settings_callback)
        self.tray.actionToggleWindow.triggered.connect(lambda: self.tray_activated_callback(QtWidgets.QSystemTrayIcon.ActivationReason.Trigger))
        self.tray.activated.connect(self.tray_activated_callback)

        self.tasks_thread.feed_update_task.finished.connect(self.update_feeds_finished)
        self.tasks_thread.feed_update_task.started.connect(self.update_feeds_started)
        self.tasks_thread.job_update_info.connect(self.job_update_info_callback)

        self.line_search.textChanged.connect(self.search_text_changed_callback)

        for entry in self.entry_widgets.values():
            entry.unstarred.connect(self.unstarred_callback)

        self.lock_server.newConnection.connect(self.bring_to_front)

    def init_shortcuts(self):
        self.shortcut_search = QtGui.QShortcut(QtGui.QKeySequence.fromString(settings.value("shortcuts/filter", type=str)), self)
        self.shortcut_quit = QtGui.QShortcut(QtGui.QKeySequence.fromString(settings.value("shortcuts/quit", type=str)), self)
        self.shortcut_refresh = QtGui.QShortcut(QtGui.QKeySequence.fromString(settings.value("shortcuts/refresh", type=str)), self)
        self.shortcut_new_feed = QtGui.QShortcut(QtGui.QKeySequence.fromString(settings.value("shortcuts/new_feed", type=str)), self)
        self.shortcut_new_category = QtGui.QShortcut(QtGui.QKeySequence.fromString(settings.value("shortcuts/new_category", type=str)), self)
        self.shortcut_play = QtGui.QShortcut(QtGui.QKeySequence.fromString(settings.value("shortcuts/play", type=str)), self)
        self.shortcut_play_audio = QtGui.QShortcut(QtGui.QKeySequence.fromString(settings.value("shortcuts/play_audio", type=str)), self)
        self.shortcut_play_in_browser = QtGui.QShortcut(QtGui.QKeySequence.fromString(settings.value("shortcuts/play_in_browser", type=str)), self)
        self.shortcut_previous_entry = QtGui.QShortcut(QtGui.QKeySequence.fromString(settings.value("shortcuts/previous_entry", type=str)), self)
        self.shortcut_next_entry = QtGui.QShortcut(QtGui.QKeySequence.fromString(settings.value("shortcuts/next_entry", type=str)), self)
        self.shortcut_toggle_star = QtGui.QShortcut(QtGui.QKeySequence.fromString(settings.value("shortcuts/toggle_star", type=str)), self)

        self.shortcut_search.activated.connect(self.line_search.setFocus)
        self.shortcut_quit.activated.connect(self.close)
        self.shortcut_refresh.activated.connect(self.update_feeds_callback)
        self.shortcut_new_feed.activated.connect(self.new_feed_callback)
        self.shortcut_new_category.activated.connect(self.new_category_callback)
        self.shortcut_play.activated.connect(self.play_video)
        self.shortcut_play_audio.activated.connect(lambda:self.play_video(play_quality_once="Audio only"))
        self.shortcut_play_in_browser.activated.connect(self.play_in_browser)
        self.shortcut_previous_entry.activated.connect(self.display_previous_entry)
        self.shortcut_next_entry.activated.connect(self.display_next_entry)
        self.shortcut_toggle_star.activated.connect(self.toggle_star_callback)

    def set_shortcuts(self):
        self.shortcut_search.setKey(QtGui.QKeySequence.fromString(settings.value("shortcuts/filter", type=str)))
        self.shortcut_quit.setKey(QtGui.QKeySequence.fromString(settings.value("shortcuts/quit", type=str)))
        self.shortcut_refresh.setKey(QtGui.QKeySequence.fromString(settings.value("shortcuts/refresh", type=str)))
        self.shortcut_new_feed.setKey(QtGui.QKeySequence.fromString(settings.value("shortcuts/new_feed", type=str)))
        self.shortcut_new_category.setKey(QtGui.QKeySequence.fromString(settings.value("shortcuts/new_category", type=str)))
        self.shortcut_play.setKey(QtGui.QKeySequence.fromString(settings.value("shortcuts/play", type=str)))
        self.shortcut_play_audio.setKey(QtGui.QKeySequence.fromString(settings.value("shortcuts/play_audio", type=str)))
        self.shortcut_play_in_browser.setKey(QtGui.QKeySequence.fromString(settings.value("shortcuts/play_in_browser", type=str)))
        self.shortcut_previous_entry.setKey(QtGui.QKeySequence.fromString(settings.value("shortcuts/previous_entry", type=str)))
        self.shortcut_next_entry.setKey(QtGui.QKeySequence.fromString(settings.value("shortcuts/next_entry", type=str)))
        self.shortcut_toggle_star.setKey(QtGui.QKeySequence.fromString(settings.value("shortcuts/toggle_star", type=str)))

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # TODO: child widgets?
        if event.button() == QtCore.Qt.MouseButton.BackButton:
            self.display_previous_entry()
        elif event.button() == QtCore.Qt.MouseButton.ForwardButton:
            self.display_next_entry()
        event.accept()

    def changeEvent(self, event: QtCore.QEvent) -> None:
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            if settings.value("tray/show", type=bool) and settings.value("tray/minimize", type=bool):
                if self.windowState() & QtCore.Qt.WindowState.WindowMinimized:
                    self.window_state_to_restore = self.windowState() & ~QtCore.Qt.WindowState.WindowMinimized | QtCore.Qt.WindowState.WindowActive
                    self.hide()
                else:
                    # Restore tray icon in case of new entries
                    self.tray.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{settings.value('theme', type=str)}/tray.png")))

        event.accept()

    def handle_close(self):
        logger.debug("MainWindow: closeEvent detected.")
        self.save_window_state()

        if settings.value("tray/show", type=bool):
            self.tray.hide()

        self.lock_file.unlock()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.handle_close()
        event.accept()
        self.quit()


def start_gui():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(__title__.replace(" ", "-"))
    app.setQuitOnLastWindowClosed(False)  # Prevent dialogs from quitting the application when the main window is minimized

    logdir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.StandardLocation.AppDataLocation)[0]
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logging.basicConfig(filename=os.path.join(logdir, __title__.replace(" ", "-") + ".log"), format='%(levelname)s > %(name)s > %(asctime)s > %(message)s')

    window = MainWindow(app)

    # prevent multiple instances
    if window.acquire_lock() or "--no-lock" in sys.argv:
        window.init_ui()
        sys.exit(app.exec())
    else:
        # connect to the process that's already running
        client = QtNetwork.QLocalSocket()
        already_running = False
        for _ in range(3):
            client.connectToServer("rsstube.socket")
            if (client.waitForConnected(150)):
                # connection succeeded, this will bring the window of that process to the front
                already_running = True
                client.abort()
                break

        if not already_running:
            logger.warning("start_gui: Existing lockfile is not valid. Forcing a new instance.")
            window.acquire_lock(force=True)
            window.init_ui()
            sys.exit(app.exec())
