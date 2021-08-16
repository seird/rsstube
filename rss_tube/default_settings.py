import os

from pathlib import Path


DEFAULT_SETTINGS = {
    "theme": "light",
    "logging/level": "Disabled",
    "tasks/interval": 240,
    # "proxies/https": "socks5://127.0.0.1:9050",
    # "proxies/http": "socks5://127.0.0.1:9050",
    "MainWindow/icon/width": 32,
    "MainWindow/icon/height": 32,
    "MainWindow/menu/show": True,
    "MainWindow/start_minimized": False,
    "MainWindow/export_location": os.path.join(Path.home(), "rsstube-channels.csv"),
    "MainWindow/entries_to_fetch": 10000,
    "tray/show": True,
    "tray/minimize": True,
    "tray/notifications/enabled": False,
    "tray/notifications/duration_ms": 2000,
    "feeds/update_interval/minutes": 10,
    "youtube/show_description": True,
    "mpv/path": "mpv",
    "mpv/args": "",
    "mpv/quality": "1080p",
    "cache/preload_thumbnails": False,
    "delete/older_than": False,
    "delete/older_than_days": 14,
    "delete/added_more_than": False,
    "delete/added_more_than_days": 14,
    "delete/interval/hours": 2,
    "delete/keep_unviewed": True,
    "shortcuts/filter": "Ctrl+F",
    "shortcuts/quit": "Ctrl+Q",
    "shortcuts/refresh": "F5",
    "shortcuts/new_feed": "Ctrl+N",
    "shortcuts/new_category": "Ctrl+Shift+N",
    "shortcuts/play": "Ctrl+O",
    "shortcuts/play_audio": "Ctrl+Alt+O",
    "shortcuts/play_in_browser": "Ctrl+Shift+O",
    "shortcuts/previous_entry": "Ctrl+,",
    "shortcuts/next_entry": "Ctrl+."
}
