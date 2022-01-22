import logging
import subprocess

from rss_tube.database.settings import Settings

from .base import BasePlayer

logger = logging.getLogger("logger")
settings = Settings()


class MpvPlayerInstance(BasePlayer):
    def _run(self):
        self.args.append("--force-window")

        if self.play_quality_once == "Audio only":
            self.args.append("--no-video")
        else:
            player_quality = self.play_quality_once or settings.value("player/mpv/quality", type=str)
        
        if "--no-video" in self.args:
            retcode = subprocess.call([self.path, *self.args, self.url])
        else:
            retcode = subprocess.call([self.path, *self.args, f"--ytdl-format=bestvideo[height<={player_quality.rstrip('p')}]+bestaudio", self.url])
        if retcode != 0:
            logger.debug(f"Player Thread: first try returned {retcode}. Trying again without parameters.")
            # Try again without extra parameters in case it's a livestream
            retcode = subprocess.call([self.path, self.url])
            if retcode != 0:
                self.failed.emit(retcode)
