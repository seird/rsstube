import logging
import pickle
import sqlite3

from enum import Enum
from typing import Any, Dict, List, Optional

from PyQt6 import QtCore

from rss_tube.database.settings import Settings
from .database import Database


logger = logging.getLogger("logger")
settings = Settings()


class FilterAction(Enum):
    Nop = 0
    Delete = "Delete"
    MarkViewed = "Mark Viewed"
    Star = "Star"
    StarAndMarkViewed = "Star and Mark Viewed"
    RunExternalProgram = "Run external program"


supported_parameters = [
    ("%T", "Title", "title"),
    ("%A", "Author", "author"),
    ("%U", "Url", "link"),
]


class Filter(dict):
    def __init__(self, name: str, enabled: bool, apply_to_group: str, apply_to: str, match: str, action: FilterAction, rules: List[Dict], action_external_program: str, show_console_window: bool, filter_id: int = None):
        super(Filter, self).__init__()
        self.update({
            "id": filter_id,
            "name": name,
            "enabled": enabled,
            "apply_to_group": apply_to_group,
            "apply_to": apply_to,
            "match": match,
            "action": pickle.loads(action) if isinstance(action, bytes) else action,
            "rules": pickle.loads(rules) if isinstance(rules, bytes) else rules,
            "action_external_program": action_external_program,
            "show_console_window": show_console_window,
        })

    def get_rules_list(self) -> List[Dict]:
        return self.get("rules")

    def blobbed(self) -> dict:
        c = dict(self)
        c.update({
            "action": pickle.dumps(c["action"]),
            "rules": pickle.dumps(c["rules"])
        })
        return c

    def __str__(self):
        text = ""
        for key, value in self.items():
            if key == "rules":
                text += "<b>rules</b>:<br>"
                for rule in self.get_rules_list():
                    text += f" - {rule['target']} {rule['type']} {rule['text']}<br>"
            elif key == "action":
                text += f"<b>{key}</b>: {self['action'].value}<br>"
            else:
                text += f"<b>{key}</b>: {value}<br>"
        return text


class Filters(object):
    def __init__(self):
        self.database = Database("filters", QtCore.QStandardPaths.StandardLocation.AppLocalDataLocation)
        self.cursor = self.database.cursor()

        try:
            self.cursor.execute("ALTER TABLE filters ADD COLUMN action_external_program TEXT default null")
        except sqlite3.OperationalError:
            logger.debug(f"Column action_external_program already exists")

        try:
            self.cursor.execute("ALTER TABLE filters ADD COLUMN show_console_window INTEGER default 0")
        except sqlite3.OperationalError:
            logger.debug(f"Column show_console_window already exists")


        # Filters table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS filters (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            name           TEXT,
            enabled        INTEGER,
            invert         INTEGER,
            apply_to_group TEXT,
            apply_to       TEXT,
            match          TEXT,
            action         BLOB,
            rules          BLOB,
            action_external_program TEXT,
            show_console_window INTEGER)
        """)

        self.database.commit()

    def store_filter(self, f: Filter) -> Any:
        self.cursor.execute(
            """
            INSERT INTO filters
                (name, enabled, apply_to_group, apply_to, match, action, rules, action_external_program, show_console_window)
            VALUES
                (:name, :enabled, :apply_to_group, :apply_to, :match, :action, :rules, :action_external_program, :show_console_window)
            """,
            f.blobbed()
        )

        f["id"] = self.cursor.lastrowid

        self.database.commit()
        return f["id"]

    def update_filter(self, f: Filter):
        self.cursor.execute(
            """
            UPDATE filters SET
                name=:name, enabled=:enabled, apply_to_group=:apply_to_group,
                apply_to=:apply_to, match=:match, action=:action, rules=:rules,
                action_external_program=:action_external_program, show_console_window=:show_console_window
            WHERE
                id=:id
            """,
            f.blobbed()
        )
        self.database.commit()

    def get_filter(self, filter_id: int) -> Optional[Filter]:
        r = self.cursor.execute("SELECT * FROM filters WHERE id=?", (filter_id,)).fetchone()
        if r:
            return Filter(
                r["name"],
                r["enabled"],
                r["apply_to_group"],
                r["apply_to"],
                r["match"],
                r["action"],
                r["rules"],
                r["action_external_program"],
                r["show_console_window"],
                filter_id=r["id"]
            )
        else:
            return None

    def get_filters(self) -> List[Filter]:
        filters: List[Filter] = []
        for r in self.cursor.execute("SELECT * FROM filters").fetchall():
            filters.append(Filter(
                r["name"],
                r["enabled"],
                r["apply_to_group"],
                r["apply_to"],
                r["match"],
                r["action"],
                r["rules"],
                r["action_external_program"],
                r["show_console_window"],
                filter_id=r["id"]
            ))
        return filters

    def get_enabled_filters(self) -> List[Filter]:
        filters: List[Filter] = []
        for r in self.cursor.execute("""
                SELECT * FROM filters
                WHERE filters.enabled = 1
                """).fetchall():
            filters.append(Filter(
                r["name"],
                r["enabled"],
                r["apply_to_group"],
                r["apply_to"],
                r["match"],
                r["action"],
                r["rules"],
                r["action_external_program"],
                r["show_console_window"],
                filter_id=r["id"]
            ))
        return filters

    def delete_filter(self, filter_id: int):
        self.cursor.execute("DELETE FROM filters WHERE id=?", (filter_id,))
        self.database.commit()
