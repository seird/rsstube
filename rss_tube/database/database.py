import logging
import os
import sqlite3

from PyQt6 import QtCore


logger = logging.getLogger("logger")


class Database(sqlite3.Connection):
    def __init__(self, database: str, dir: QtCore.QStandardPaths.StandardLocation, *args, **kwargs):
        self.dir = QtCore.QStandardPaths.standardLocations(dir)[0]
        os.makedirs(self.dir, exist_ok=True)
        path = os.path.join(self.dir, database + ".db.sqlite3")
        super(Database, self).__init__(database=path, *args, **kwargs)
        self.row_factory = sqlite3.Row
