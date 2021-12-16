import logging
from typing import Optional

from PyQt6 import QtCore
from rss_tube.database.settings import Settings
from . import players
from .base import BasePlayer


logger = logging.getLogger("logger")
settings = Settings()


class Player(QtCore.QObject):
    started = QtCore.pyqtSignal()
    stopped = QtCore.pyqtSignal()
    failed = QtCore.pyqtSignal(int)

    def __init__(self):
        super(Player, self).__init__()
        self.players = {}
        self.ids = 0

    def _get_player(self) -> Optional[BasePlayer]:
        player = settings.value("player")
        if instance := players.get_instance(player):
            return instance(
                settings.value(f"player/{player}/path", type=str),
                settings.value(f"player/{player}/args", type=str)
            )

    def _player_finished_callback(self, player_id: int):
        self._delete_player(player_id)
        if len(self.players) == 0:
            self.stopped.emit()

    def _delete_player(self, player_id: int):
        if (player := self.players.get(player_id)) and not player.playing:
            self.players.pop(player_id)

    def play(self, url: str, play_quality_once: str = ""):
        if url and (player := self._get_player()):
            self.ids += 1
            self.players[self.ids] = player
            player.finished.connect(lambda x=self.ids: self._player_finished_callback(x))
            player.started.connect(self.started.emit)
            player.failed.connect(self.failed.emit)
            player.play(url, play_quality_once)
