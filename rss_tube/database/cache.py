import glob
import logging
import os
import time

import requests

from PyQt6 import  QtCore

from .database import Database

logger = logging.getLogger("logger")


class Cache(object):
    def __init__(self, expiration=0):
        self.database = Database("cache", QtCore.QStandardPaths.StandardLocation.CacheLocation)
        self.cursor = self.database.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS cache (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            url       TEXT,
            filename  TEXT,
            cached_on TEXT)
        """)

        # create a directory to store cached files
        path = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.StandardLocation.CacheLocation)[0]
        self.cache_dir = os.path.join(path, "cache")
        os.makedirs(self.cache_dir, exist_ok=True)

    def clear(self):
        self.cursor.execute("DELETE FROM cache")
        self.database.isolation_level = None
        self.cursor.execute("VACUUM")
        self.database.isolation_level = ''
        self.database.commit()
        for filename in glob.glob(self.cache_dir + "/*"):
            os.remove(filename)

    def lookup(self, key: str) -> str:
        q = self.cursor.execute("SELECT filename, cached_on FROM cache WHERE url=?", (key,)).fetchone()
        if q:
            # Cache hit
            filename, cached_on = q
            filepath = os.path.join(self.cache_dir, filename)
            return filepath if os.path.exists(filepath) else ""
        else:
            # Cache miss
            return ""

    def store(self, key: str, response: requests.Response, add_time: bool = True) -> str:
        # Create a file and store the response contents
        filename = str(time.time()).replace(".","") if add_time else ""
        if "Content-Disposition" in response.headers.keys():
            filename += response.headers["Content-Disposition"]
        else:
            filename += response.url.split("/")[-1]

        filename = "".join([c for c in filename if c.isalpha() or c.isdigit()]).rstrip()
        filepath = os.path.join(self.cache_dir, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)

        self.cursor.execute(
            "INSERT INTO cache (url, filename, cached_on) VALUES(?, ?, datetime('now', 'localtime'))",
            (key, filename)
        )
        self.database.commit()
        return filepath

    def delete(self, key: str):
        q = self.cursor.execute("SELECT filename FROM cache WHERE url=?", (key,)).fetchone()
        if q:
            filepath = os.path.join(self.cache_dir, q["filename"])
            try:
                os.remove(filepath)
            except FileNotFoundError:
                logger.warning(f"\"{filepath}\" doesn't exist.")
            self.cursor.execute("DELETE FROM cache WHERE url=?", (key,))
            self.database.commit()
