import logging
import subprocess

from PyQt5 import QtCore

from rss_tube.database.settings import Settings

logger = logging.getLogger("logger")
settings = Settings("rss-tube")


class PlayerInstance(QtCore.QThread):
    def __init__(self):
        super(PlayerInstance, self).__init__()
        self.url = ""
        self.playing = False
        self.play_quality_once = ""

    def run(self):
        if self.play_quality_once == "Audio only":
            player_args = "--no-video --force-window"
        else:
            player_args = settings.value("mpv/args", type=str)
            player_quality = self.play_quality_once or settings.value("mpv/quality", type=str)
        self.play_quality_once = ""

        if self.url == "":
            logging.error("Player Thread: self.url == \"\" and thread was started")
            return

        self.playing = True

        mpv_path = settings.value("mpv/path", type=str)
        player_args = player_args.split()

        try:
            logger.debug(f"Player Thread started playing {self.url}")
            if "--no-video" in player_args:
                retcode = subprocess.call([mpv_path, *player_args, self.url])
            else:
                retcode = subprocess.call([mpv_path, *player_args, f"--ytdl-format=bestvideo[height<={player_quality.rstrip('p')}]+bestaudio", self.url])
            if retcode != 0:
                logger.debug(f"Player Thread: first try returned {retcode}. Trying again without parameters.")
                # Try again without extra parameters in case it's a livestream
                subprocess.call([mpv_path, self.url])
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


class Player(object):
    def __init__(self):
        self.players = [PlayerInstance()]

    def _get_available_player(self) -> PlayerInstance:
        available_players = list(filter(lambda player: not player.playing, self.players))
        if not available_players:
            self.players.append(PlayerInstance())
            return self.players[-1]
        else:
            return available_players[0]

    def play(self, url: str, play_quality_once: str = ""):
        if url:
            self._get_available_player().play(url, play_quality_once)
