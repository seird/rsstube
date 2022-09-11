import datetime
import logging
import subprocess
import sqlite3
import time
import os

from typing import Any, Iterator, List, Optional, Tuple

from PyQt6 import QtCore

from rss_tube.database.settings import Settings
from rss_tube.database.cache import Cache
from rss_tube.download import Downloader
from rss_tube.parser import parse_url, parse_feed
from .database import Database
from .filters import Filter, FilterAction, Filters, supported_parameters


logger = logging.getLogger("logger")
settings = Settings()


class Feeds(object):
    def __init__(self):
        self.database = Database("feeds", QtCore.QStandardPaths.StandardLocation.AppLocalDataLocation)
        self.downloader = Downloader()
        self.cache = Cache()
        self.filters = Filters()
        self.cursor = self.database.cursor()

        # Categories table
        self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS categories (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            category     TEXT);
            
        INSERT INTO categories (category) SELECT 'default' WHERE (SELECT COUNT(*) FROM categories) = 0;
        """)
        
        # Feeds table
        try:
            self.cursor.execute("ALTER TABLE feeds ADD COLUMN purge_excluded INTEGER default 0")
        except sqlite3.OperationalError:
            logger.debug(f"Column purge_excluded already exists")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS feeds (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            notify         INTEGER,
            purge_excluded INTEGER,
            author         TEXT,
            category       TEXT,
            type           TEXT,
            url            TEXT,
            channel_url    TEXT,
            added_on       TEXT,
            refreshed_on   TEXT)
        """)

        # Feed Entries table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            feed_id        INTEGER,
            added_on       TEXT,
            refreshed_on   TEXT,
            viewed         INTEGER,
            deleted        INTEGER,
            author         TEXT,
            title          TEXT,
            link           TEXT,
            entry_id       TEXT,
            published      TEXT,
            updated        TEXT,
            thumbnail      TEXT,
            description    TEXT,
            rating_average REAL,
            rating_count   INTEGER,
            views          INTEGER,
            duration       TEXT,
            link_raw       TEXT,
            star           INTEGER)
        """)

        # Purged entries table -- blacklist for new entries
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS purged (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            link         TEXT
        )
        """)

        self.database.commit()

    def delete_all_feeds(self):
        self.cursor.execute("DELETE FROM feeds")
        self.database.commit()

    def delete_feed(self, feed_id: int):
        self.cursor.execute("DELETE FROM entries WHERE feed_id = ?", (feed_id,))
        self.cursor.execute("DELETE FROM feeds WHERE id = ?", (feed_id,))
        self.database.commit()

    def delete_category(self, category: str):
        self.cursor.execute("DELETE FROM entries WHERE feed_id IN (SELECT id FROM feeds WHERE category = ?)", (category,))
        self.cursor.execute("DELETE FROM feeds WHERE category = ?", (category,))
        self.cursor.execute("DELETE FROM categories WHERE category = ?", (category,))
        self.database.commit()

    def delete_entry(self, entry_id: int):
        self.cursor.execute("UPDATE entries SET deleted=1 WHERE id=?", (entry_id,))
        self.database.commit()

    def delete_entries(self, entry_ids: List[int]):
        self.cursor.executemany("UPDATE entries SET deleted=1 WHERE id=?", entry_ids)
        self.database.commit()

    def delete_entries_in_feed(self, feed_id: int):
        self.cursor.execute("UPDATE entries SET deleted=1 WHERE feed_id = ?", (feed_id,))
        self.database.commit()

    def delete_entries_in_category(self, category: str):
        self.cursor.execute(
            """
            UPDATE entries SET deleted=1
            WHERE feed_id IN 
                (SELECT DISTINCT id FROM feeds WHERE category=?)
            """,
            (category,)
        )
        self.database.commit()
    
    def purge_feed(self, feed_id: int, num_entries_to_keep: int, keep_unviewed: bool = True) -> int:
        # Delete all the saved thumbnails
        params = {
            "feed_id": feed_id,
            "num_entries_to_keep": num_entries_to_keep
        }

        links = []
        for q in self.cursor.execute(
            f"""
            SELECT * FROM (SELECT thumbnail, link FROM entries
                WHERE feed_id=:feed_id AND star=0 AND deleted=0 {'AND viewed=1' if keep_unviewed else ''}
                ORDER BY published DESC
                LIMIT -1 OFFSET :num_entries_to_keep)
            UNION ALL
            SELECT thumbnail, link FROM entries
                WHERE feed_id=:feed_id AND deleted=1
            """,
            params
        ).fetchall():
            self.cache.delete(q["thumbnail"])
            links.append((q["link"],))

        # Delete the entry from the entries table
        self.cursor.execute(
            f"""
            DELETE FROM entries
            WHERE id in (
                SELECT id FROM (SELECT id FROM entries
                    WHERE feed_id=:feed_id AND star=0 {'AND viewed=1' if keep_unviewed else ''}
                    ORDER BY published DESC
                    LIMIT -1 OFFSET :num_entries_to_keep)
                UNION ALL
                SELECT id FROM entries
                    WHERE feed_id=:feed_id AND deleted=1 
            )
            """,
            params
        )

        # Add the entry link to the purged table to prevent it from being re-added
        self.cursor.executemany("INSERT INTO purged (link) VALUES (?)", links)
        
        self.database.isolation_level = None
        self.cursor.execute("VACUUM")
        self.database.isolation_level = ''
        self.database.commit()

        return len(links)

    def purge_feeds(self, num_entries_to_keep: int, keep_unviewed: bool = True) -> int:
        entries_purged = 0
        for feed in self.get_feeds():
            entries_purged += self.purge_feed(feed["id"], num_entries_to_keep, keep_unviewed=keep_unviewed)
        return entries_purged

    def unblacklist_purged_entries(self):
        self.cursor.execute("DELETE FROM purged")
        self.database.isolation_level = None
        self.cursor.execute("VACUUM")
        self.database.isolation_level = ''
        self.database.commit()

    def add_feed(self, url: str, category: str, feed_name: str = "") -> Optional[int]:
        url = parse_url(url)
        if url == "":
            return None

        if self.cursor.execute("SELECT * FROM feeds WHERE url = ?", (url,)).fetchone():
            # feed already exists
            logger.debug(f"add_feed: feed {url} already exists")
            return None

        if "youtube.com/feeds/videos.xml" in url:
            feed_type = "youtube"
            if ".xml?user=" in url:
                # https://www.youtube.com/feeds/videos.xml?user=USERNAME
                channel_url = "https://www.youtube.com/user/" + url.split(".xml?user=")[-1]
            else:
                # https://www.youtube.com/feeds/videos.xml?channel_id=CHANNELID
                channel_url = "https://www.youtube.com/channel/" + url.split(".xml?channel_id=")[-1]
        elif "feeds.soundcloud.com" in url:
            feed_type = "soundcloud"
            channel_url = url # TODO "https://feeds.soundcloud.com/users/soundcloud:users:<id>/sounds.rss" to "soundcloud.com/<user>" ?
        else:
            return None

        feed_bytes = self.downloader.get_bytes(url, cached=False, add_time=False)

        if feed_bytes == b"":
            logging.debug(f"add_feed: Adding {url} failed.")
            return None

        parsed_feed = parse_feed(feed_bytes, feed_type=feed_type)

        if not parsed_feed:
            return None

        parsed_feed.update({
            "url": url,
            "channel_url": channel_url,
            "category": category,
            "author": feed_name if feed_name else parsed_feed["author"]
        })

        self.cursor.execute(
            """
            INSERT OR IGNORE INTO categories
                (id, category)
            VALUES
                ((SELECT id FROM categories WHERE category=:category), :category);
            """,
            parsed_feed
        )

        self.cursor.execute(
            """
            INSERT INTO feeds 
                (author, category, type, url, channel_url, added_on, refreshed_on, purge_excluded) 
            VALUES
                (:author, :category, :type, :url, :channel_url, datetime('now', 'localtime'),
                 datetime('now', 'localtime'), :purge_excluded);
            """,
            parsed_feed
        )

        feed_id = self.cursor.lastrowid
        logger.debug(f"add_feed: Adding {url} success. id = {feed_id}")
        self.database.commit()
        return feed_id

    def add_category(self, category: str) -> bool:
        """
        Add a new category

        Returns True if the category was added successfully
        """
        rowid_before = self.cursor.lastrowid
        self.cursor.execute(
            """
            INSERT OR IGNORE INTO categories 
                (id, category)
            VALUES
                ((SELECT id FROM categories WHERE category=:category), :category);
            """,
            {"category": category}
        )
        self.database.commit()
        success = self.cursor.lastrowid != rowid_before
        return success

    def delete_all_categories(self):
        for category in self.get_categories():
            self.delete_category(category)

    def get_category_viewed(self, category: str) -> bool:
        """
        Get the viewed status of a category.
        Return True if all entries in the category are viewed.
        """
        return self.cursor.execute(
            """
            SELECT COUNT(*) as count FROM entries
            WHERE feed_id IN (SELECT id FROM feeds WHERE category=?) AND viewed=0 AND deleted=0
            """,
            (category,)
        ).fetchone()["count"] == 0

    def get_feed_viewed(self, feed_id: int) -> bool:
        """
        Get the viewed status of a feed.
        Return True if all entries in the feed are viewed.
        """
        return self.cursor.execute(
            """
            SELECT COUNT(*) as count FROM entries
            WHERE feed_id=? AND viewed=0 AND deleted=0
            """,
            (feed_id,)
        ).fetchone()["count"] == 0

    def get_stars_viewed(self) -> bool:
        """
        Get the viewed status of all stars.
        Return True if all stard entries are viewed.
        """
        return self.cursor.execute(
            """
            SELECT COUNT(*) as count FROM entries
            WHERE star=1 AND viewed=0 AND deleted=0
            """
        ).fetchone()["count"] == 0

    def get_categories(self) -> List[str]:
        return [x["category"] for x in self.cursor.execute("SELECT category FROM categories").fetchall()]

    def get_feeds_in_category(self, category: str) -> List:
        return self.cursor.execute("SELECT * FROM feeds WHERE category = ? ORDER BY author ASC", (category,)).fetchall()

    def get_feeds(self) -> List:
        return self.cursor.execute("SELECT * FROM feeds ORDER BY author ASC").fetchall()
    
    def get_purgeable_feeds(self) -> List:
        return self.cursor.execute("SELECT * FROM feeds WHERE purge_excluded=0").fetchall()

    def get_feed(self, feed_id: int) -> Any:
        return self.cursor.execute("SELECT * FROM feeds WHERE id = ?", (feed_id,)).fetchone()

    def update_feed(self, feed_id: int, commit: bool = True):
        """
        Update a feed and all its entries
        """
        feed = self.cursor.execute("SELECT * FROM feeds WHERE id = ?", (feed_id,)).fetchone()

        if feed:
            self.update_feed_entries(feed_id, commit=commit)
            logger.debug(f"Feeds: Updated {feed['url']}")

    def update_feeds(self, interval: float = 0):
        """
        Update all feeds and their entries
        """
        for q in self.cursor.execute("SELECT id FROM feeds ORDER BY refreshed_on ASC").fetchall():
            time.sleep(interval)
            self.update_feed(feed_id=q["id"], commit=False)
            self.database.commit()

        logger.debug("update_feeds: Feeds updated.")

    def get_feed_type(self, feed_id: int) -> str:
        q = self.cursor.execute("SELECT type FROM feeds WHERE id = ?", (feed_id,)).fetchone()
        return q["type"] if q else ""

    def get_feed_id(self, entry_id: int) -> int:
        q = self.cursor.execute("SELECT feed_id FROM entries WHERE id = ?  AND deleted=0 LIMIT 1", (entry_id,)).fetchone()
        return q["feed_id"] if q else None

    def get_feed_author(self, entry_id: int) -> str:
        q = self.cursor.execute("SELECT author FROM entries WHERE id = ?  AND deleted=0 LIMIT 1", (entry_id,)).fetchone()
        return q["feed_id"] if q else None

    def get_feed_from_entry(self, entry_id: int) -> Any:
        return self.cursor.execute(
            """
            SELECT * FROM feeds
            WHERE id = (SELECT feed_id FROM entries WHERE id=? AND deleted=0)
            """,
            (entry_id,)
        ).fetchone()

    def get_category(self, feed_id: int) -> str:
        q = self.cursor.execute("SELECT category FROM feeds WHERE id = ? LIMIT 1", (feed_id,)).fetchone()
        return q["category"] if q else None

    def get_category_by_author(self, author: str) -> str:
        q = self.cursor.execute("SELECT category FROM feeds WHERE author = ? LIMIT 1", (author,)).fetchone()
        return q["category"] if q else None

    def get_entries(self, feed_id: int) -> List:
        """
        Get all entries in a feed
        """
        limit = settings.value("MainWindow/entries_to_fetch", type=int)
        return self.cursor.execute(
            """
            SELECT * FROM entries 
            WHERE feed_id = ? AND deleted=0
            ORDER BY published DESC
            LIMIT ?
            """,
            (feed_id, limit)
        ).fetchall()

    def get_entries_category(self, category: str) -> List:
        """
        Get all entries in a category
        """
        limit = settings.value("MainWindow/entries_to_fetch", type=int)
        return self.cursor.execute(
            """
            SELECT * FROM entries 
            WHERE 
                feed_id IN (
                    SELECT id FROM feeds WHERE category = ?
                ) AND deleted=0
            ORDER BY published DESC
            LIMIT ?
            """,
            (category, limit)
        ).fetchall()

    def get_entry(self, entry_id: int) -> Any:
        """
        Get a single entry in a feed
        """
        return self.cursor.execute("SELECT * FROM entries WHERE id = ? AND deleted=0", (entry_id,)).fetchone()

    def get_stars(self) -> List:
        """
        Get all entries that are marked as star
        """
        limit = settings.value("MainWindow/entries_to_fetch", type=int)
        return self.cursor.execute(
            """
            SELECT * FROM entries
            WHERE star=1 AND deleted=0
            ORDER BY published DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

    def set_entry_viewed(self, entry_id: int, viewed: bool = True):
        """
        Set the viewed status of an entry.
        """
        self.cursor.execute("UPDATE entries SET viewed=? WHERE id=?", (viewed, entry_id))
        self.database.commit()

    def get_entry_viewed(self, entry_id: int) -> bool:
        """
        Get the viewed status of an entry.
        """
        return self.cursor.execute("SELECT viewed FROM entries WHERE id=? AND deleted=0", (entry_id,)).fetchone()["viewed"]

    def delete_entries_older_than_days(self, days: int, keep_unviewed: bool):
        """
        Delete all entries older than "days"
        """
        cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S")
        if keep_unviewed:
            entry_ids = self.cursor.execute("SELECT id FROM entries WHERE published<? AND viewed=1", (cutoff,)).fetchall()
        else:
            entry_ids = self.cursor.execute("SELECT id FROM entries WHERE published<?", (cutoff,)).fetchall()
        self.delete_entries(entry_ids)

    def delete_entries_added_more_than_days(self, days: int, keep_unviewed: bool):
        """
        Delete all entries added more than "days" ago
        """
        cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S")
        if keep_unviewed:
            entry_ids = self.cursor.execute("SELECT id FROM entries WHERE added_on<? AND viewed=1", (cutoff,)).fetchall()
        else:
            entry_ids = self.cursor.execute("SELECT id FROM entries WHERE added_on<?", (cutoff,)).fetchall()
        self.delete_entries(entry_ids)

    def update_feed_name(self, feed_id: int, new_name: str):
        self.cursor.execute("UPDATE feeds SET author=? WHERE id=?", (new_name, feed_id))
        self.cursor.execute("UPDATE entries SET author=? WHERE feed_id=?", (new_name, feed_id))
        self.database.commit()

    def update_category_name(self, current_name: str, new_name: str):
        self.cursor.execute("UPDATE categories SET category=? WHERE category=?", (new_name, current_name))
        self.cursor.execute("UPDATE feeds SET category=? WHERE category=?", (new_name, current_name))
        self.database.commit()

    def apply_filters(self, feed: dict, entry: dict) -> Iterator[Tuple[FilterAction, dict]]:
        for f in self.filters.get_enabled_filters():
            # check if this filter should be applied to the feed
            if f["apply_to_group"].lower() == "all":
                # apply the filter
                pass
            elif f["apply_to_group"].lower() == "category":
                # apply filter if feed is in the category
                if self.get_category_by_author(feed["author"]) != f["apply_to"]:
                    continue
            elif f["apply_to_group"].lower() == "channel":
                # apply filter if the feed is equal to the channel
                if feed["author"] != f["apply_to"]:
                    continue

            if f["match"] == "any":
                match = False
                for rule in f.get_rules_list():
                    if match := match or apply_rule(feed, entry, rule):
                        break
            elif f["match"] == "all":
                match = True
                for rule in f.get_rules_list():
                    match = match and apply_rule(feed, entry, rule)
            else:
                continue
            
            if match:
                yield FilterAction(f["action"]), {
                    "action_external_program": f["action_external_program"],
                    "show_console_window": f["show_console_window"]
                }

    def update_feed_entries(self, feed_id: int, commit: bool = True):
        """
        Update all entries in a single feed
        """
        q = self.cursor.execute("SELECT url, type, author FROM feeds WHERE id = ?", (feed_id,)).fetchone()

        if q is None:
            return

        feed_bytes = self.downloader.get_bytes(q["url"], cached=False, add_time=False)

        if feed_bytes == b"":
            logging.debug(f"update_feed_entries: Updating feed {feed_id} failed.")
            return

        parsed_feed = parse_feed(feed_bytes, q["type"], q["author"])
        refresh_entries = settings.value("feeds/refresh_entries", type=bool)
        preload_thumbnails = settings.value("cache/preload_thumbnails", type=bool)

        for i, entry in parsed_feed["entries"].items():
            if self.cursor.execute("SELECT * FROM purged WHERE link=:link", entry).fetchall():
                logger.debug(f"Entry {entry['link']} has been purged, skippping.")
                continue

            entry_fetched = self.cursor.execute("SELECT * FROM entries WHERE entry_id=:entry_id", entry).fetchone()
            if not entry_fetched:
                # Filter the new entry
                entry.update({
                    "feed_id": feed_id,
                    "deleted": 0,
                    "viewed": 0,
                    "star": 0,
                })
                for action, action_args in self.apply_filters(parsed_feed, entry):
                    if action == FilterAction.Delete:
                        entry.update({"deleted": 1})
                    elif action == FilterAction.MarkViewed:
                        entry.update({"viewed": 1})
                    elif action == FilterAction.Star:
                        entry.update({"star": 1})
                    elif action == FilterAction.StarAndMarkViewed:
                        entry.update({"viewed": 1, "star": 1})
                    elif action == FilterAction.RunExternalProgram:
                        command = action_args["action_external_program"]
                        show_console = action_args["show_console_window"]
                        for p in supported_parameters:
                            command = command.replace(p[0], entry[p[2]])
                        logger.debug(f"Executing command '{command}' on entry")
                        try:
                            if os.name == "nt":
                                si = subprocess.STARTUPINFO()
                                if not show_console:
                                    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                                subprocess.Popen(command, startupinfo=si)
                            else:
                                # TODO: show console on linux
                                subprocess.Popen(command, shell=True)
                        except Exception as e:
                            logger.error(f"Error executing [{command}]: {e}")

                self.cursor.execute(
                    """
                    INSERT INTO entries
                        (feed_id, viewed, deleted, added_on, refreshed_on, author, 
                         title, link, entry_id, published, updated, thumbnail,
                         description, rating_average, rating_count, views, duration, link_raw, star)
                    VALUES
                        (:feed_id, :viewed, :deleted, datetime('now', 'localtime'), datetime('now', 'localtime'),
                         :author, :title, :link, :entry_id, :published, :updated, :thumbnail,
                         :description, :rating_average, :rating_count, :views, :duration, :link_raw, :star)
                    """,
                    entry
                )
            elif refresh_entries:
                # Entry already exists, update the entries
                entry['star'] = entry_fetched['star']
                self.cursor.execute(
                    """
                    UPDATE entries SET
                        title=:title, link=:link, published=:published, updated=:updated,
                        thumbnail=:thumbnail, description=:description, rating_average=:rating_average,
                        rating_count=:rating_count, views=:views, duration=:duration, link_raw=:link_raw, star=:star
                    WHERE entry_id=:entry_id AND deleted=0
                    """,
                    entry
                )
            if preload_thumbnails:
                self.downloader.get_filename(entry["thumbnail"])

        self.cursor.execute("UPDATE feeds SET refreshed_on=datetime('now', 'localtime') WHERE id=?", (feed_id,))

        if commit:
            self.database.commit()

    def get_new_entries(self, last_refreshed: str):
        """
        Get new entries since 'last_refreshed' ('%Y-%m-%d %H:%M:%S')
        """
        return self.cursor.execute("SELECT * FROM entries WHERE refreshed_on > ? AND deleted=0", (last_refreshed,)).fetchall()

    def get_new_entries_unviewed(self, last_refreshed: str):
        """
        Get new entries since 'last_refreshed' ('%Y-%m-%d %H:%M:%S') that haven't been viewed
        """
        return self.cursor.execute("SELECT * FROM entries WHERE refreshed_on > ? AND deleted=0 AND viewed=0", (last_refreshed,)).fetchall()


    def set_viewed(self, feed_id: int = None, category: str = None):
        if feed_id:
            self.cursor.execute("UPDATE entries SET viewed=1 WHERE feed_id=?", (feed_id,))
            self.database.commit()
        if category:
            self.cursor.execute(
                """
                UPDATE entries SET viewed=1
                WHERE feed_id IN (SELECT id FROM feeds WHERE category=?)
                """,
                (category,)
            )
            self.database.commit()

    def set_viewed_stars(self):
        self.cursor.execute("UPDATE entries SET viewed=1 WHERE star=1")
        self.database.commit()

    def clear_stars(self):
        self.cursor.execute("UPDATE entries SET star=0 WHERE star=1")
        self.database.commit()

    def delete_stars(self):
        self.cursor.execute("UPDATE entries SET deleted=1 WHERE star=1")
        self.database.commit()

    def mark_star(self, entry_id: int, star: bool):
        self.cursor.execute("UPDATE entries SET star=? WHERE id=?", (star, entry_id))
        self.database.commit()

    def get_excluded_channels(self) -> List:
        return self.cursor.execute("SELECT * FROM feeds WHERE purge_excluded=1").fetchall()

    def set_purge_excluded(self, id: int, excluded: bool):
        self.cursor.execute("UPDATE feeds SET purge_excluded=? WHERE id=?", (excluded, id))
        self.database.commit()

    def __len__(self):
        return self.cursor.execute("SELECT COUNT(*) as count FROM feeds").fetchone()["count"]


def apply_rule(feed: dict, entry: dict, rule: dict) -> bool:
    target = rule["target"].lower()
    text = rule["text"].lower()

    feed_target = feed.get(target, "").lower()
    entry_target = entry.get(target, "").lower()

    if rule["type"] == "contains":
        if text in feed_target or text in entry_target:
            return True
    elif rule["type"] == "equals":
        if text == feed_target or text == entry_target:
            return True
    elif rule["type"] == "doesn't contain":
        if (text not in feed_target and feed_target != "") or (text not in entry_target and entry_target != ""):
            return True
    elif rule["type"] == "doesn't equal":
        if (text != feed_target and feed_target != "") or (text != entry_target and entry_target != ""):
            return True

    return False
