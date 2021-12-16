import subprocess

from rss_tube.database.settings import Settings

from .base import BasePlayer

settings = Settings()


class VlcPlayerInstance(BasePlayer):
    def _run(self):        
        retcode = subprocess.call([self.path, *self.args, self.url])
        if retcode != 0:
            self.failed.emit(retcode)
