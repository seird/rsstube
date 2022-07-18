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
    def __init__(self, name: str, enabled: bool, invert: bool, apply_to_group: str, apply_to: str, match: str, action: FilterAction, rules: List[Dict], action_external_program: str, filter_id: int = None):
        super(Filter, self).__init__()
        self.update({
            "id": filter_id,
            "name": name,
            "enabled": enabled,
            "invert": invert,
            "apply_to_group": apply_to_group,
            "apply_to": apply_to,
            "match": match,
            "action": pickle.loads(action) if isinstance(action, bytes) else action,
            "rules": pickle.loads(rules) if isinstance(rules, bytes) else rules,
            "action_external_program": action_external_program,
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
            action_external_program TEXT)
        """)

        # Filter order table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS filter_rank (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            filter_id      INTEGER,
            rank          INTEGER)
        """)

        self.database.commit()

    def store_filter(self, f: Filter) -> Any:
        self.cursor.execute(
            """
            INSERT INTO filters
                (name, enabled, invert, apply_to_group, apply_to, match, action, rules, action_external_program)
            VALUES
                (:name, :enabled, :invert, :apply_to_group, :apply_to, :match, :action, :rules, :action_external_program)
            """,
            f.blobbed()
        )

        f["id"] = self.cursor.lastrowid

        self.cursor.execute(
            """
            INSERT INTO filter_rank
                (filter_id, rank)
            VALUES
                (:id, (SELECT
                          CASE WHEN (SELECT id from filter_rank) IS NOT NULL THEN
                              MAX(rank)+1
                          ELSE 
                              0
                          END
                      FROM filter_rank)
                )
            """,
            f
        )
        self.database.commit()
        return f["id"]

    def update_filter(self, f: Filter):
        self.cursor.execute(
            """
            UPDATE filters SET
                name=:name, enabled=:enabled, invert=:invert, apply_to_group=:apply_to_group,
                apply_to=:apply_to, match=:match, action=:action, rules=:rules, action_external_program=:action_external_program
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
                r["invert"],
                r["apply_to_group"],
                r["apply_to"],
                r["match"],
                r["action"],
                r["rules"],
                r["action_external_program"],
                filter_id=r["id"]
            )
        else:
            return None

    def get_filters(self) -> List[Filter]:
        filters: List[Filter] = []
        for r in self.cursor.execute("""
                SELECT * FROM filters
                INNER JOIN filter_rank ON filters.id = filter_rank.filter_id
                ORDER BY rank ASC
                """).fetchall():
            filters.append(Filter(
                r["name"],
                r["enabled"],
                r["invert"],
                r["apply_to_group"],
                r["apply_to"],
                r["match"],
                r["action"],
                r["rules"],
                r["action_external_program"],
                filter_id=r["id"]
            ))
        return filters

    def get_enabled_filters(self) -> List[Filter]:
        filters: List[Filter] = []
        for r in self.cursor.execute("""
                SELECT * FROM filters
                INNER JOIN filter_rank ON filters.id = filter_rank.filter_id
                WHERE filters.enabled = 1
                ORDER BY rank ASC                
                """).fetchall():
            filters.append(Filter(
                r["name"],
                r["enabled"],
                r["invert"],
                r["apply_to_group"],
                r["apply_to"],
                r["match"],
                r["action"],
                r["rules"],
                r["action_external_program"],
                filter_id=r["id"]
            ))
        return filters

    def delete_filter(self, filter_id: int):
        self.cursor.execute("DELETE FROM filters WHERE id=?", (filter_id,))
        self.cursor.execute("DELETE FROM filter_rank WHERE filter_id=?", (filter_id,))
        self.database.commit()
