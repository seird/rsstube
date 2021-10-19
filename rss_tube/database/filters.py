import logging
import pickle

from enum import Enum
from typing import Any, Dict, List, Optional

from PyQt6 import QtCore

from rss_tube.database.settings import Settings
from .database import Database


logger = logging.getLogger("logger")
settings = Settings()


class FilterAction(Enum):
    Nop = 0
    Delete = 1
    MarkViewed = 2


class Filter(dict):
    def __init__(self, name: str, enabled: bool, invert: bool, apply_to_group: str, apply_to: str, match: str, action: FilterAction, rules: List[Dict], filter_id: int = None):
        super(Filter, self).__init__()
        self.update({
            "id": filter_id,
            "name": name,
            "enabled": enabled,
            "invert": invert,
            "apply_to_group": apply_to_group,
            "apply_to": apply_to,
            "match": match,
            "action": action.value if isinstance(action, FilterAction) else action,
            "rules": pickle.dumps(rules)
        })

    def get_rules_list(self) -> List[Dict]:
        return pickle.loads(self.get("rules"))

    def __str__(self):
        text = ""
        for key, value in self.items():
            if key == "rules":
                text += "<b>rules</b>:<br>"
                for rule in self.get_rules_list():
                    text += f" - {rule['target']} {rule['type']} {rule['text']}<br>"
            elif key == "action":
                text += f"<b>{key}</b>: {FilterAction(value).name}<br>"
            else:
                text += f"<b>{key}</b>: {value}<br>"
        return text


class Filters(object):
    def __init__(self):
        self.database = Database("filters", QtCore.QStandardPaths.StandardLocation.AppLocalDataLocation)
        self.cursor = self.database.cursor()

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
            action         INT,
            rules          BLOB)
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
                (name, enabled, invert, apply_to_group, apply_to, match, action, rules)
            VALUES
                (:name, :enabled, :apply_to_group, :apply_to, :match, :action, :rules)
            """,
            f
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
                apply_to=apply_to, match=:match, action=:action, rules=:rules
            WHERE
                id=:id
            """,
            f
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
                pickle.loads(r["rules"]),
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
                pickle.loads(r["rules"]),
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
                pickle.loads(r["rules"]),
                filter_id=r["id"]
            ))
        return filters

    def delete_filter(self, filter_id: int):
        self.cursor.execute("DELETE FROM filters WHERE id=?", (filter_id,))
        self.cursor.execute("DELETE FROM filter_rank WHERE filter_id=?", (filter_id,))
        self.database.commit()

    def rank_top(self, f: Filter):
        self.cursor.execute(
            """
            UPDATE filter_rank SET
                rank=rank+1
            WHERE
                rank < (SELECT rank FROM filter_rank WHERE filter_id=:id)
            """,
            f
        )
        self.cursor.execute(
            """
            UPDATE filter_rank SET
                rank=0
            WHERE
                filter_id=:id
            """,
            f
        )
        self.database.commit()

    def rank_up(self, f: Filter):
        self.cursor.execute(
            """
            UPDATE filter_rank SET
                rank=rank+1
            WHERE
                rank=((SELECT rank FROM filter_rank WHERE filter_id=:id)-1)
            """,
            f
        )
        self.cursor.execute(
            """
            UPDATE filter_rank SET
                rank=rank-1
            WHERE
                filter_id=:id
            """,
            f
        )
        self.database.commit()

    def rank_down(self, f: Filter):
        self.cursor.execute(
            """
            UPDATE filter_rank SET
                rank=rank-1
            WHERE
                rank=((SELECT rank FROM filter_rank WHERE filter_id=:id)+1)
            """,
            f
        )
        self.cursor.execute(
            """
            UPDATE filter_rank SET
                rank=rank+1
            WHERE
                filter_id=:id
            """,
            f
        )
        self.database.commit()

    def rank_bottom(self, f: Filter):
        self.cursor.execute(
            """
            UPDATE filter_rank SET
                rank=rank-1
            WHERE
                rank > (SELECT rank FROM filter_rank WHERE filter_id=:id)
            """,
            f
        )
        self.cursor.execute(
            """
            UPDATE filter_rank SET
                rank=(SELECT MAX(rank)+1 FROM filter_rank)
            WHERE
                filter_id=:id
            """,
            f
        )
        self.database.commit()
