from PyQt6 import QtGui, QtWidgets

from .designs.widget_purge_entries import Ui_Dialog
from rss_tube.tasks import PurgeFeedsTask
from rss_tube.database.settings import Settings
from rss_tube.utils import center_widget


settings = Settings()


class PurgeEntriesDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(PurgeEntriesDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Purge Entries")

        self.started = False
        self.purge_feeds_task = PurgeFeedsTask()

        self.checkBox.setChecked(settings.value("purge/keep_unviewed", type=bool))
        self.spinBox.setValue(settings.value("purge/entries_to_keep", type=int))
        self.progressBar.reset()

        center_widget(parent, self)

        self.link_callbacks()

    def set_buttons_enabled(self, enabled: bool):
        self.pb_start.setText("Start" if enabled else "Stop")
        for pb in self.buttonBox.buttons():
            pb.setEnabled(enabled)

    def finished_callback(self):
        self.started = False
        self.set_buttons_enabled(True)
        self.label_current.setText("Finished.")

    def start_callback(self):
        self.started = not self.started
        
        if self.started:
            self.set_buttons_enabled(False)
            self.purge_feeds_task.maximum.connect(lambda m: self.progressBar.setRange(0, m))
            self.purge_feeds_task.current.connect(lambda t: self.label_current.setText(f"Processing '{t}' ..."))
            self.purge_feeds_task.progress.connect(lambda p: self.progressBar.setValue(p))
            self.purge_feeds_task.finished.connect(self.finished_callback)
            self.purge_feeds_task.start()
        else:
            self.purge_feeds_task.request_stop = True
            self.set_buttons_enabled(True)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.started:
            event.ignore()
        else:
            super(PurgeEntriesDialog, self).closeEvent(event)
    
    def link_callbacks(self):
        self.pb_start.clicked.connect(self.start_callback)
        self.spinBox.valueChanged.connect(lambda x: settings.setValue("purge/entries_to_keep", x))
        self.checkBox.stateChanged.connect(lambda x: settings.setValue("purge/keep_unviewed", x))
