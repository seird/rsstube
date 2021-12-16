import abc
import logging

from PyQt6 import QtCore

logger = logging.getLogger("logger")


class BasePlayer(QtCore.QThread):
    failed = QtCore.pyqtSignal(int)

    def __init__(self, path: str, args: str = ""):
        super(BasePlayer, self).__init__()
        self.path = path
        self.args = args.split()
        self.url = ""
        self.play_quality_once = ""
        self.playing = False

    @abc.abstractmethod
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
