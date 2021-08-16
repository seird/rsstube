import logging
import os

from PyQt5 import QtCore, QtWidgets

from .designs.widget_settings import Ui_Dialog
from .FiltersWidget import FiltersWidget
from .ShortcutDialog import ShortcutsDialog
from rss_tube.database.settings import Settings
from rss_tube.gui.themes import styles
from rss_tube.utils import center_widget
from rss_tube.utils import set_icons, set_style


logger = logging.getLogger("logger")
settings = Settings("rss-tube")


class SettingsDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, mainwindow: QtWidgets.QMainWindow):
        super(SettingsDialog, self).__init__(flags=QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)

        self.settings_changed = False
        self.schedule_changed = False
        self.changes_applied = False

        self.mainwindow = mainwindow

        self.initUI()

        center_widget(mainwindow, self)

        self.link_callbacks()

    def initUI(self):
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setEnabled(False)

        # General Tab
        self.combo_theme.addItems(styles.keys())
        self.combo_theme.setCurrentText(settings.value("theme", type=str))

        self.cb_show_menu.setChecked(settings.value("MainWindow/menu/show", type=bool))
        self.cb_show_description.setChecked(settings.value("youtube/show_description", type=bool))

        self.cb_show_tray.setChecked(settings.value("tray/show", type=bool))
        self.cb_minimize_to_tray.setChecked(settings.value("tray/minimize", type=bool))
        self.cb_start_minimized.setChecked(settings.value("MainWindow/start_minimized", type=bool))

        self.spin_notification_duration.setValue(settings.value("tray/notifications/duration_ms", type=int))
        self.cb_notifications.setChecked(settings.value("tray/notifications/enabled", type=bool))

        self.combo_logging.addItems([
            logging.getLevelName(logging.ERROR),
            logging.getLevelName(logging.WARNING),
            logging.getLevelName(logging.INFO),
            logging.getLevelName(logging.DEBUG),
            "Disabled"
        ])
        self.combo_logging.setCurrentText(settings.value("logging/level", type=str))

        # Schedule Tab
        self.spin_update_feed_interval_minutes.setValue(settings.value("feeds/update_interval/minutes", type=int))

        # Player Tab
        self.line_mpv_path.setText(settings.value("mpv/path", type=str))
        self.line_mpv_args.setText(settings.value("mpv/args", type=str))
        self.combo_mpv_quality.setCurrentText(settings.value("mpv/quality", type=str))

        # Shortcuts Tab
        self.gridLayout_tab_shortcuts = QtWidgets.QGridLayout(self.tab_shortcuts)
        self.gridLayout_tab_shortcuts.addWidget(ShortcutsDialog(self))

        # Database Tab
        self.cb_preload_thumbnails.setChecked(settings.value("cache/preload_thumbnails", type=bool))
        self.spin_entries_to_fetch.setValue(settings.value("MainWindow/entries_to_fetch", type=int))
        self.cb_delete_older.setChecked(settings.value("delete/older_than", type=bool))
        self.spin_delete_older.setValue(settings.value("delete/older_than_days", type=int))
        self.cb_delete_added.setChecked(settings.value("delete/added_more_than", type=bool))
        self.spin_delete_added.setValue(settings.value("delete/added_more_than_days", type=int))
        self.cb_keep_unviewed.setChecked(settings.value("delete/keep_unviewed", type=bool))
        self.pb_reset_feeds.hide()
        self.pb_reset_categories.hide()

        # Filters tab
        self.gridLayout_tab_filters = QtWidgets.QGridLayout(self.tab_filters)
        self.gridLayout_tab_filters.addWidget(FiltersWidget(self))

    def settings_changed_callback(self, *args, **kwargs):
        self.settings_changed = True
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setEnabled(True)

    def schedule_changed_callback(self, *args, **kwargs):
        self.schedule_changed = True
        self.settings_changed_callback()

    def reset_settings_callback(self):
        response = QtWidgets.QMessageBox.warning(
            self,
            "Are you sure?",
            "Reset all settings?",
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
            defaultButton=QtWidgets.QMessageBox.Cancel
        )
        if response == QtWidgets.QMessageBox.Ok:
            settings.clear()

    def mpv_path_callback(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Open", os.path.dirname(self.line_mpv_path.text()), "*")[0]
        if fname and os.path.exists(os.path.dirname(fname)):
            self.line_mpv_path.setText(fname)

    def link_callbacks(self):
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.apply_settings)

        # General Tab
        self.combo_theme.currentTextChanged.connect(self.settings_changed_callback)

        self.cb_show_menu.stateChanged.connect(self.settings_changed_callback)
        self.cb_show_description.stateChanged.connect(self.settings_changed_callback)

        self.cb_minimize_to_tray.stateChanged.connect(self.settings_changed_callback)
        self.cb_show_tray.stateChanged.connect(self.settings_changed_callback)
        self.cb_start_minimized.stateChanged.connect(self.settings_changed_callback)

        self.spin_notification_duration.valueChanged.connect(self.settings_changed_callback)
        self.cb_notifications.stateChanged.connect(self.settings_changed_callback)

        self.combo_logging.currentTextChanged.connect(self.settings_changed_callback)
        self.pb_open_log.clicked.connect(self.mainwindow.open_log_callback)

        # Schedule Tab
        self.spin_update_feed_interval_minutes.valueChanged.connect(self.schedule_changed_callback)

        # Player Tab
        self.pb_mpv_path.clicked.connect(self.mpv_path_callback)
        self.line_mpv_path.textChanged.connect(self.settings_changed_callback)
        self.line_mpv_args.textChanged.connect(self.settings_changed_callback)
        self.combo_mpv_quality.currentTextChanged.connect(self.settings_changed_callback)

        # Database Tab
        self.cb_preload_thumbnails.stateChanged.connect(self.settings_changed_callback)
        self.spin_entries_to_fetch.valueChanged.connect(self.settings_changed_callback)
        self.cb_delete_older.stateChanged.connect(self.settings_changed_callback)
        self.spin_delete_older.valueChanged.connect(self.settings_changed_callback)
        self.cb_delete_added.stateChanged.connect(self.settings_changed_callback)
        self.spin_delete_added.valueChanged.connect(self.settings_changed_callback)
        self.cb_keep_unviewed.stateChanged.connect(self.settings_changed_callback)

        self.pb_open_database.clicked.connect(self.mainwindow.open_database_callback)
        self.pb_reset_feeds.clicked.connect(self.mainwindow.feeds.delete_all_feeds)
        self.pb_reset_categories.clicked.connect(self.mainwindow.feeds.delete_all_categories)
        self.pb_reset_settings.clicked.connect(self.reset_settings_callback)
        self.pb_reset_cache.clicked.connect(self.mainwindow.feeds.downloader.cache.clear)

    def apply_settings(self):
        # General Tab
        settings.setValue("theme", self.combo_theme.currentText().lower().replace(" ", "_"))
        set_style(self.mainwindow.app, style=settings.value("theme", "dark", type=str))
        set_icons(self.mainwindow, style=settings.value("theme", "dark", type=str))
        # reapply the font of all the items in the tree widget
        for i in range(self.mainwindow.tree_feeds.topLevelItemCount()):
            item = self.mainwindow.tree_feeds.topLevelItem(i)
            item.set_font()
            for j in range(item.childCount()):
                child = item.child(j)
                child.set_font()

        settings.setValue("MainWindow/menu/show", self.cb_show_menu.isChecked())
        self.mainwindow.menubar.setVisible(settings.value("MainWindow/menu/show", type=bool))
        settings.setValue("youtube/show_description", self.cb_show_description.isChecked())
        self.mainwindow.entry_widgets["youtube"].show_description(settings.value("youtube/show_description", type=bool))

        settings.setValue("tray/show", self.cb_show_tray.isChecked())
        self.mainwindow.tray.setVisible(self.cb_show_tray.isChecked())
        if not self.cb_show_tray.isChecked() and self.mainwindow.isHidden():
            self.mainwindow.show()

        settings.setValue("tray/minimize", self.cb_minimize_to_tray.isChecked())
        settings.setValue("MainWindow/start_minimized", self.cb_start_minimized.isChecked())

        settings.setValue("tray/notifications/enabled", self.cb_notifications.isChecked())
        settings.setValue("tray/notifications/duration_ms", self.spin_notification_duration.value())

        selected_level = self.combo_logging.currentText()
        settings.setValue("logging/level", selected_level)
        if selected_level == "Disabled":
            logging.disable(logging.CRITICAL)
        else:
            logging.disable(logging.NOTSET)
            logger.setLevel(selected_level)

        # Schedule Tab
        settings.setValue("feeds/update_interval/minutes", self.spin_update_feed_interval_minutes.value())

        # Player Tab
        settings.setValue("mpv/path", self.line_mpv_path.text())
        settings.setValue("mpv/args", self.line_mpv_args.text().strip())
        settings.setValue("mpv/quality", self.combo_mpv_quality.currentText())

        # Database Tab
        settings.setValue("cache/preload_thumbnails", self.cb_preload_thumbnails.isChecked())
        settings.setValue("MainWindow/entries_to_fetch", self.spin_entries_to_fetch.value())
        settings.setValue("delete/older_than", self.cb_delete_older.isChecked())
        settings.setValue("delete/added_more_than", self.cb_delete_added.isChecked())
        settings.setValue("delete/older_than_days", self.spin_delete_older.value())
        settings.setValue("delete/added_more_than_days", self.spin_delete_added.value())
        settings.setValue("delete/keep_unviewed", self.cb_keep_unviewed.isChecked())

        settings.sync()

        self.settings_changed = False
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).setEnabled(False)

        self.changes_applied = True
