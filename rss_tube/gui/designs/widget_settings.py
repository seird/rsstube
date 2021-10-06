# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rss_tube/gui/designs\widget_settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(451, 515)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_general = QtWidgets.QWidget()
        self.tab_general.setObjectName("tab_general")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_general)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.tab_general)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.cb_show_menu = QtWidgets.QCheckBox(self.groupBox)
        self.cb_show_menu.setObjectName("cb_show_menu")
        self.gridLayout_3.addWidget(self.cb_show_menu, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.combo_theme = QtWidgets.QComboBox(self.groupBox)
        self.combo_theme.setObjectName("combo_theme")
        self.horizontalLayout.addWidget(self.combo_theme)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.cb_show_description = QtWidgets.QCheckBox(self.groupBox)
        self.cb_show_description.setObjectName("cb_show_description")
        self.gridLayout_3.addWidget(self.cb_show_description, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_10 = QtWidgets.QGroupBox(self.tab_general)
        self.groupBox_10.setObjectName("groupBox_10")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_10)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_10)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.combo_logging = QtWidgets.QComboBox(self.groupBox_10)
        self.combo_logging.setObjectName("combo_logging")
        self.horizontalLayout_2.addWidget(self.combo_logging)
        self.pb_open_log = QtWidgets.QPushButton(self.groupBox_10)
        self.pb_open_log.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pb_open_log.setObjectName("pb_open_log")
        self.horizontalLayout_2.addWidget(self.pb_open_log)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_10, 3, 0, 1, 1)
        self.groupBox_12 = QtWidgets.QGroupBox(self.tab_general)
        self.groupBox_12.setObjectName("groupBox_12")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_12)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_8 = QtWidgets.QLabel(self.groupBox_12)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.gridLayout_6.addWidget(self.label_8, 0, 0, 1, 1)
        self.spin_update_feed_interval_minutes = QtWidgets.QSpinBox(self.groupBox_12)
        self.spin_update_feed_interval_minutes.setMaximumSize(QtCore.QSize(60, 16777215))
        self.spin_update_feed_interval_minutes.setMinimum(5)
        self.spin_update_feed_interval_minutes.setMaximum(999)
        self.spin_update_feed_interval_minutes.setProperty("value", 10)
        self.spin_update_feed_interval_minutes.setObjectName("spin_update_feed_interval_minutes")
        self.gridLayout_6.addWidget(self.spin_update_feed_interval_minutes, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_12)
        self.label_2.setObjectName("label_2")
        self.gridLayout_6.addWidget(self.label_2, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_12, 2, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_general)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout_3.setObjectName("formLayout_3")
        self.cb_minimize_to_tray = QtWidgets.QCheckBox(self.groupBox_3)
        self.cb_minimize_to_tray.setObjectName("cb_minimize_to_tray")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.cb_minimize_to_tray)
        self.cb_show_tray = QtWidgets.QCheckBox(self.groupBox_3)
        self.cb_show_tray.setObjectName("cb_show_tray")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.cb_show_tray)
        self.cb_start_minimized = QtWidgets.QCheckBox(self.groupBox_3)
        self.cb_start_minimized.setObjectName("cb_start_minimized")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.cb_start_minimized)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_4.setObjectName("groupBox_4")
        self.formLayout_4 = QtWidgets.QFormLayout(self.groupBox_4)
        self.formLayout_4.setObjectName("formLayout_4")
        self.cb_notifications = QtWidgets.QCheckBox(self.groupBox_4)
        self.cb_notifications.setObjectName("cb_notifications")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.cb_notifications)
        self.spin_notification_duration = QtWidgets.QSpinBox(self.groupBox_4)
        self.spin_notification_duration.setMinimum(100)
        self.spin_notification_duration.setMaximum(10000)
        self.spin_notification_duration.setSingleStep(100)
        self.spin_notification_duration.setProperty("value", 2000)
        self.spin_notification_duration.setObjectName("spin_notification_duration")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.spin_notification_duration)
        self.label = QtWidgets.QLabel(self.groupBox_4)
        self.label.setObjectName("label")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label)
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.groupBox_4)
        self.gridLayout_2.addWidget(self.groupBox_3, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_general, "")
        self.tab_player = QtWidgets.QWidget()
        self.tab_player.setObjectName("tab_player")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_player)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_13 = QtWidgets.QGroupBox(self.tab_player)
        self.groupBox_13.setObjectName("groupBox_13")
        self.formLayout_9 = QtWidgets.QFormLayout(self.groupBox_13)
        self.formLayout_9.setObjectName("formLayout_9")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.combo_player = QtWidgets.QComboBox(self.groupBox_13)
        self.combo_player.setMinimumSize(QtCore.QSize(100, 0))
        self.combo_player.setObjectName("combo_player")
        self.horizontalLayout_5.addWidget(self.combo_player)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.formLayout_9.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout_5)
        self.verticalLayout_3.addWidget(self.groupBox_13)
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_player)
        self.groupBox_5.setObjectName("groupBox_5")
        self.formLayout_5 = QtWidgets.QFormLayout(self.groupBox_5)
        self.formLayout_5.setObjectName("formLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.line_player_path = QtWidgets.QLineEdit(self.groupBox_5)
        self.line_player_path.setReadOnly(True)
        self.line_player_path.setObjectName("line_player_path")
        self.horizontalLayout_3.addWidget(self.line_player_path)
        self.pb_player_path = QtWidgets.QPushButton(self.groupBox_5)
        self.pb_player_path.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pb_player_path.setObjectName("pb_player_path")
        self.horizontalLayout_3.addWidget(self.pb_player_path)
        self.formLayout_5.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout_3)
        self.verticalLayout_3.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab_player)
        self.groupBox_6.setObjectName("groupBox_6")
        self.formLayout_6 = QtWidgets.QFormLayout(self.groupBox_6)
        self.formLayout_6.setObjectName("formLayout_6")
        self.line_player_args = QtWidgets.QLineEdit(self.groupBox_6)
        self.line_player_args.setText("")
        self.line_player_args.setPlaceholderText("")
        self.line_player_args.setObjectName("line_player_args")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.line_player_args)
        self.verticalLayout_3.addWidget(self.groupBox_6)
        self.groupBox_player_quality = QtWidgets.QGroupBox(self.tab_player)
        self.groupBox_player_quality.setObjectName("groupBox_player_quality")
        self.formLayout_7 = QtWidgets.QFormLayout(self.groupBox_player_quality)
        self.formLayout_7.setObjectName("formLayout_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.combo_player_quality = QtWidgets.QComboBox(self.groupBox_player_quality)
        self.combo_player_quality.setMinimumSize(QtCore.QSize(70, 0))
        self.combo_player_quality.setObjectName("combo_player_quality")
        self.combo_player_quality.addItem("")
        self.combo_player_quality.addItem("")
        self.combo_player_quality.addItem("")
        self.combo_player_quality.addItem("")
        self.combo_player_quality.addItem("")
        self.combo_player_quality.addItem("")
        self.combo_player_quality.addItem("")
        self.combo_player_quality.addItem("")
        self.horizontalLayout_4.addWidget(self.combo_player_quality)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.formLayout_7.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout_4)
        self.verticalLayout_3.addWidget(self.groupBox_player_quality)
        self.tabWidget.addTab(self.tab_player, "")
        self.tab_shortcuts = QtWidgets.QWidget()
        self.tab_shortcuts.setObjectName("tab_shortcuts")
        self.tabWidget.addTab(self.tab_shortcuts, "")
        self.tab_filters = QtWidgets.QWidget()
        self.tab_filters.setObjectName("tab_filters")
        self.tabWidget.addTab(self.tab_filters, "")
        self.tab_connection = QtWidgets.QWidget()
        self.tab_connection.setObjectName("tab_connection")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_connection)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_proxy = QtWidgets.QGroupBox(self.tab_connection)
        self.groupBox_proxy.setCheckable(True)
        self.groupBox_proxy.setObjectName("groupBox_proxy")
        self.formLayout_10 = QtWidgets.QFormLayout(self.groupBox_proxy)
        self.formLayout_10.setObjectName("formLayout_10")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.groupBox_proxy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.line_proxy_host = QtWidgets.QLineEdit(self.groupBox_proxy)
        self.line_proxy_host.setText("")
        self.line_proxy_host.setObjectName("line_proxy_host")
        self.horizontalLayout_6.addWidget(self.line_proxy_host)
        self.label_9 = QtWidgets.QLabel(self.groupBox_proxy)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.spin_proxy_port = QtWidgets.QSpinBox(self.groupBox_proxy)
        self.spin_proxy_port.setMinimumSize(QtCore.QSize(80, 0))
        self.spin_proxy_port.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spin_proxy_port.setMaximum(65535)
        self.spin_proxy_port.setObjectName("spin_proxy_port")
        self.horizontalLayout_6.addWidget(self.spin_proxy_port)
        self.formLayout_10.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout_6)
        self.verticalLayout_2.addWidget(self.groupBox_proxy)
        self.tabWidget.addTab(self.tab_connection, "")
        self.tab_database = QtWidgets.QWidget()
        self.tab_database.setObjectName("tab_database")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_database)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_8 = QtWidgets.QGroupBox(self.tab_database)
        self.groupBox_8.setObjectName("groupBox_8")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_8)
        self.formLayout.setObjectName("formLayout")
        self.cb_preload_thumbnails = QtWidgets.QCheckBox(self.groupBox_8)
        self.cb_preload_thumbnails.setObjectName("cb_preload_thumbnails")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.cb_preload_thumbnails)
        self.verticalLayout.addWidget(self.groupBox_8)
        self.groupBox_11 = QtWidgets.QGroupBox(self.tab_database)
        self.groupBox_11.setObjectName("groupBox_11")
        self.formLayout_8 = QtWidgets.QFormLayout(self.groupBox_11)
        self.formLayout_8.setObjectName("formLayout_8")
        self.spin_entries_to_fetch = QtWidgets.QSpinBox(self.groupBox_11)
        self.spin_entries_to_fetch.setMinimumSize(QtCore.QSize(60, 0))
        self.spin_entries_to_fetch.setMinimum(1)
        self.spin_entries_to_fetch.setMaximum(10000000)
        self.spin_entries_to_fetch.setProperty("value", 10000)
        self.spin_entries_to_fetch.setObjectName("spin_entries_to_fetch")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.spin_entries_to_fetch)
        self.label_7 = QtWidgets.QLabel(self.groupBox_11)
        self.label_7.setObjectName("label_7")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_7)
        self.verticalLayout.addWidget(self.groupBox_11)
        self.groupBox_9 = QtWidgets.QGroupBox(self.tab_database)
        self.groupBox_9.setObjectName("groupBox_9")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_9)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.cb_keep_unviewed = QtWidgets.QCheckBox(self.groupBox_9)
        self.cb_keep_unviewed.setObjectName("cb_keep_unviewed")
        self.gridLayout_4.addWidget(self.cb_keep_unviewed, 1, 0, 1, 1)
        self.cb_delete_added = QtWidgets.QCheckBox(self.groupBox_9)
        self.cb_delete_added.setObjectName("cb_delete_added")
        self.gridLayout_4.addWidget(self.cb_delete_added, 0, 0, 1, 1)
        self.spin_delete_added = QtWidgets.QSpinBox(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spin_delete_added.sizePolicy().hasHeightForWidth())
        self.spin_delete_added.setSizePolicy(sizePolicy)
        self.spin_delete_added.setMinimumSize(QtCore.QSize(65, 0))
        self.spin_delete_added.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.spin_delete_added.setMinimum(2)
        self.spin_delete_added.setProperty("value", 14)
        self.spin_delete_added.setObjectName("spin_delete_added")
        self.gridLayout_4.addWidget(self.spin_delete_added, 0, 1, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.groupBox_9)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_9)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_database)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.pb_reset_feeds = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_reset_feeds.setObjectName("pb_reset_feeds")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.pb_reset_feeds)
        self.pb_reset_categories = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_reset_categories.setObjectName("pb_reset_categories")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.pb_reset_categories)
        self.pb_reset_settings = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_reset_settings.setObjectName("pb_reset_settings")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.pb_reset_settings)
        self.pb_reset_cache = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_reset_cache.setObjectName("pb_reset_cache")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.pb_reset_cache)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.pb_open_database = QtWidgets.QPushButton(self.tab_database)
        self.pb_open_database.setObjectName("pb_open_database")
        self.verticalLayout.addWidget(self.pb_open_database)
        self.tabWidget.addTab(self.tab_database, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.tabWidget, self.combo_theme)
        Dialog.setTabOrder(self.combo_theme, self.cb_show_menu)
        Dialog.setTabOrder(self.cb_show_menu, self.cb_show_description)
        Dialog.setTabOrder(self.cb_show_description, self.cb_show_tray)
        Dialog.setTabOrder(self.cb_show_tray, self.cb_minimize_to_tray)
        Dialog.setTabOrder(self.cb_minimize_to_tray, self.cb_start_minimized)
        Dialog.setTabOrder(self.cb_start_minimized, self.cb_notifications)
        Dialog.setTabOrder(self.cb_notifications, self.spin_notification_duration)
        Dialog.setTabOrder(self.spin_notification_duration, self.spin_update_feed_interval_minutes)
        Dialog.setTabOrder(self.spin_update_feed_interval_minutes, self.combo_logging)
        Dialog.setTabOrder(self.combo_logging, self.line_player_args)
        Dialog.setTabOrder(self.line_player_args, self.combo_player_quality)
        Dialog.setTabOrder(self.combo_player_quality, self.cb_preload_thumbnails)
        Dialog.setTabOrder(self.cb_preload_thumbnails, self.spin_entries_to_fetch)
        Dialog.setTabOrder(self.spin_entries_to_fetch, self.cb_delete_added)
        Dialog.setTabOrder(self.cb_delete_added, self.spin_delete_added)
        Dialog.setTabOrder(self.spin_delete_added, self.cb_keep_unviewed)
        Dialog.setTabOrder(self.cb_keep_unviewed, self.pb_reset_feeds)
        Dialog.setTabOrder(self.pb_reset_feeds, self.pb_reset_categories)
        Dialog.setTabOrder(self.pb_reset_categories, self.pb_reset_settings)
        Dialog.setTabOrder(self.pb_reset_settings, self.pb_reset_cache)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.groupBox.setTitle(_translate("Dialog", "Interface"))
        self.cb_show_menu.setText(_translate("Dialog", "Show menu bar"))
        self.label_3.setText(_translate("Dialog", "Theme"))
        self.cb_show_description.setText(_translate("Dialog", "Show video description"))
        self.groupBox_10.setTitle(_translate("Dialog", "Logging"))
        self.label_6.setText(_translate("Dialog", "Level"))
        self.pb_open_log.setToolTip(_translate("Dialog", "Open logfile"))
        self.pb_open_log.setText(_translate("Dialog", "..."))
        self.groupBox_12.setTitle(_translate("Dialog", "Schedule"))
        self.label_8.setText(_translate("Dialog", "Update channels every"))
        self.label_2.setText(_translate("Dialog", "minutes"))
        self.groupBox_3.setTitle(_translate("Dialog", "Desktop"))
        self.cb_minimize_to_tray.setText(_translate("Dialog", "Minimize to tray"))
        self.cb_show_tray.setText(_translate("Dialog", "Show tray icon"))
        self.cb_start_minimized.setText(_translate("Dialog", "Start Minimized"))
        self.groupBox_4.setTitle(_translate("Dialog", "Notifications"))
        self.cb_notifications.setText(_translate("Dialog", "Receive desktop notifications"))
        self.label.setText(_translate("Dialog", "Notification duration [ms]"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_general), _translate("Dialog", "General"))
        self.groupBox_13.setTitle(_translate("Dialog", "Player"))
        self.groupBox_5.setTitle(_translate("Dialog", "Path"))
        self.pb_player_path.setText(_translate("Dialog", "..."))
        self.groupBox_6.setTitle(_translate("Dialog", "Commandline arguments"))
        self.groupBox_player_quality.setTitle(_translate("Dialog", "Video quality"))
        self.combo_player_quality.setItemText(0, _translate("Dialog", "2160p"))
        self.combo_player_quality.setItemText(1, _translate("Dialog", "1440p"))
        self.combo_player_quality.setItemText(2, _translate("Dialog", "1080p"))
        self.combo_player_quality.setItemText(3, _translate("Dialog", "720p"))
        self.combo_player_quality.setItemText(4, _translate("Dialog", "480p"))
        self.combo_player_quality.setItemText(5, _translate("Dialog", "360p"))
        self.combo_player_quality.setItemText(6, _translate("Dialog", "240p"))
        self.combo_player_quality.setItemText(7, _translate("Dialog", "144p"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_player), _translate("Dialog", "Player"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_shortcuts), _translate("Dialog", "Shortcuts"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_filters), _translate("Dialog", "Filters"))
        self.groupBox_proxy.setTitle(_translate("Dialog", "Proxy"))
        self.label_4.setText(_translate("Dialog", "SOCKS Host:"))
        self.label_9.setText(_translate("Dialog", "Port:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_connection), _translate("Dialog", "Connection"))
        self.groupBox_8.setTitle(_translate("Dialog", "Cache"))
        self.cb_preload_thumbnails.setText(_translate("Dialog", "Preload thumbnails"))
        self.groupBox_11.setTitle(_translate("Dialog", "Fetch upto"))
        self.label_7.setText(_translate("Dialog", "most recent entries"))
        self.groupBox_9.setTitle(_translate("Dialog", "Delete"))
        self.cb_keep_unviewed.setText(_translate("Dialog", "Keep unviewed entries"))
        self.cb_delete_added.setText(_translate("Dialog", "Delete entries added more than"))
        self.label_5.setText(_translate("Dialog", "days ago"))
        self.groupBox_2.setTitle(_translate("Dialog", "Reset"))
        self.pb_reset_feeds.setText(_translate("Dialog", "Reset Feeds"))
        self.pb_reset_categories.setText(_translate("Dialog", "Reset Categories"))
        self.pb_reset_settings.setText(_translate("Dialog", "Reset Settings"))
        self.pb_reset_cache.setText(_translate("Dialog", "Reset Cache"))
        self.pb_open_database.setText(_translate("Dialog", "Open database directory"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_database), _translate("Dialog", "Database"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
