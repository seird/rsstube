import abc
import logging

from PyQt6 import QtCore, QtGui, QtWidgets
from rss_tube.database.feeds import Feeds
from rss_tube.database.settings import Settings
from rss_tube.download import Downloader
from rss_tube.player import Player

from .entry_actions import PlayAudioOnlyAction


logger = logging.getLogger("logger")
settings = Settings()


class BaseEntry(QtWidgets.QWidget):
    def __init__(self, parent):
        super(BaseEntry, self).__init__()

        self.video_url = ""
        self.url = ""
        self.thumbnail_url = ""
        self.entry_id = ""

        self.parent = parent
        self.player = Player()
        self.download = Downloader()
        self.feeds: Feeds = self.parent.feeds

        self._link_callbacks()

    @abc.abstractmethod
    def display_entry(self, entry: dict):
        ...

    def show_description(self, show: bool = True):
        self.label_description.setVisible(show)

    def play(self):
        self.player.play(self.video_url)

    def play_video(self, play_quality_once: str = ""):
        self.player.play(self.video_url, play_quality_once=play_quality_once)

    def play_audio(self):
        self.player.play(self.video_url, play_quality_once=PlayAudioOnlyAction().resolution)

    def clear_player_status(self):
        if "Playing" not in self.label_player_status.text():
            self.label_player_status.clear()

    def player_stopped_callback(self):
        self.label_player_status.setText("Stopped")
        QtCore.QTimer.singleShot(5000, self.clear_player_status)

    def player_failed_callback(self, error_code: int):
        self.label_player_status.setText(f"Failed ({error_code})")
        QtCore.QTimer.singleShot(5000, self.clear_player_status)

    def thumbnail_mouse_button(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.player.play(self.video_url)
        else:
            super(BaseEntry, self).mousePressEvent(event)

    def _link_callbacks(self):
        self.player.started.connect(lambda: self.label_player_status.setText("Playing..."))
        self.player.stopped.connect(self.player_stopped_callback)
        self.player.failed.connect(self.player_failed_callback)
