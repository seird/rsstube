import logging

import requests

from rss_tube.database.cache import Cache
from rss_tube.database.settings import Settings

try:
    import socks
    _socks_enabled = True
except ImportError:
    _socks_enabled = False


logger = logging.getLogger("logger")
settings = Settings("rss-tube")


class Downloader(object):
    def __init__(self):
        self.cache = Cache()
        self.session = requests.Session()
        self.update_proxy()

    def update_proxy(self):
        if _socks_enabled and settings.value("proxies/enabled", type=bool):
            host = settings.value("proxies/socks/host", type=str)
            port = settings.value("proxies/socks/port", type=int)
            self.session.proxies.update({
                    "https": f'socks5://{host}:{port}',
                    "http": f'socks5://{host}:{port}'
            })
        else:
            self.session.proxies.clear()

    def get(self, url: str) -> requests.Response:
        """
        Get the response of an http get request.
        Bypasses the cache.
        """
        return self.session.get(url)

    def get_bytes(self, url: str, cached: bool = True, add_time: bool = True) -> bytes:
        """
        Get the content of an http get request, as bytes.
        Optionally use the cache.
        """
        if cached:
            # Retrieve from cache
            filename = self.cache.lookup(url)
            if filename:
                with open(filename, "rb") as f:
                    return f.read()

        try:
            response = self.get(url)
        except Exception as e:
            logger.error(f"get_bytes: downloading {url} failed.: {e}")
            return b""

        if not response.ok:
            return b""

        if cached:
            # Store in cache
            self.cache.store(url, response, add_time=add_time)

        return response.content

    def get_filename(self, url: str, cached: bool = True, add_time: bool = True) -> str:
        """
        Get the content of an http get request, as a filename.
        """
        if cached:
            filename = self.cache.lookup(url)
            if filename:
                return filename

        try:
            response = self.get(url)
        except Exception as e:
            logger.error(f"get_filename: downloading {url} failed.: {e}")
            return ""

        if not response.ok:
            return ""

        return self.cache.store(url, response, add_time=add_time)
