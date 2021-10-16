import logging
import subprocess
from typing import Optional, Union

from PyQt6 import QtCore

from rss_tube.database.settings import Settings

logger = logging.getLogger("logger")
settings = Settings()


class BasePlayer(QtCore.QThread):
    failed = QtCore.pyqtSignal(int)

    def __init__(self, path: str):
        super(BasePlayer, self).__init__()
        self.path = path
        self.url = ""
        self.play_quality_once = ""
        self.playing = False

    def _run(self):
        ...

    def run(self):
        try:
            self.playing = True
            logger.debug(f"Player Thread started playing {self.url}")
            self._run()
        except Exception as e:
            logger.error(f"Player Thread failed to open {self.url}: {e}")
        finally:
            logger.debug(f"Player Thread finished playing {self.url}")
            self.playing = False

    def play(self, url: str, play_quality_once: str = ""):
        if url == "":
            logger.debug("Player Thread received an empty url.")
            return
        if self.playing:
            logger.debug(f"Player Thread tried to play {url}, but {self.url} is already playing.")
            return
        self.play_quality_once = play_quality_once
        self.url = url
        self.start()


class MpvPlayerInstance(BasePlayer):
    def _run(self):
        if self.play_quality_once == "Audio only":
            player_args = "--no-video --force-window"
        else:
            player_args = settings.value("player/mpv/args", type=str)
            player_quality = self.play_quality_once or settings.value("player/mpv/quality", type=str)

        player_args = player_args.split()
        
        if "--no-video" in player_args:
            retcode = subprocess.call([self.path, *player_args, self.url])
        else:
            retcode = subprocess.call([self.path, *player_args, f"--ytdl-format=bestvideo[height<={player_quality.rstrip('p')}]+bestaudio", self.url])
        if retcode != 0:
            logger.debug(f"Player Thread: first try returned {retcode}. Trying again without parameters.")
            # Try again without extra parameters in case it's a livestream
            retcode = subprocess.call([self.path, self.url])
            if retcode != 0:
                self.failed.emit(retcode)


class VlcPlayerInstance(BasePlayer):
    def _run(self):
        player_args = settings.value("player/vlc/args", type=str).split()
        
        retcode = subprocess.call([self.path, *player_args, self.url])
        if retcode != 0:
            self.failed.emit(retcode)


class Player(QtCore.QObject):
    started = QtCore.pyqtSignal()
    stopped = QtCore.pyqtSignal()
    failed = QtCore.pyqtSignal(int)

    def __init__(self):
        super(Player, self).__init__()
        self.players = {}
        self.ids = 0

    def _get_player(self) -> Optional[Union[MpvPlayerInstance, VlcPlayerInstance]]:
        player = settings.value("player")
        if player == "mpv":
            return MpvPlayerInstance(path=settings.value("player/mpv/path", type=str))
        elif player == "vlc":
            return VlcPlayerInstance(path=settings.value("player/vlc/path", type=str))
        else:
            return None

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
