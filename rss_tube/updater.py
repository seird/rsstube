import logging

from packaging import version
from PyQt6 import QtCore
from rss_tube.download import Downloader
from rss_tube.__version__ import __version__, __versionurl__


logger = logging.getLogger("logger")


class Updater(QtCore.QThread):
    new_update_available = QtCore.pyqtSignal(dict)
    no_update_available = QtCore.pyqtSignal()

    def run(self):
        local_version = __version__

        downloader = Downloader()
        try:
            r = downloader.get(__versionurl__).json()
        except Exception as e:
            logger.error(f"Updater: failed to query remote version: {e}")
            return

        try:
            if version.parse(r["version"]) > version.parse(local_version):
                logger.debug(f"Updater: local_version = {local_version}, remote_version = {r['version']}")
                self.new_update_available.emit(r)
            else:
                self.no_update_available.emit()
        except Exception as e:
            logger.error(f"Error parsing version: {e}")
            return
