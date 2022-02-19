import logging

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
            a_r, b_r, c_r = r["version"].split(".")
            a, b, c = local_version.split(".")
            if int(a_r) > int(a):
                new_version_available = True
            elif int(b_r) > int(b):
                new_version_available = True
            elif int(c_r) > int(c):
                new_version_available = True
            else:
                new_version_available = False
        except Exception as e:
            logger.error(f"Updater: remote version is None: {e}")
            return

        if new_version_available:
            logger.debug("Updater: New update available")
            logger.debug(f"Updater: local_version = {local_version}, remote_version = {r['version']}")
            self.new_update_available.emit(r)
        else:
            logger.debug("Updater: No update available")
            self.no_update_available.emit()
