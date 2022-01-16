import logging
import os
from datetime import datetime

from PyQt6 import QtCore, QtGui, QtWidgets
from rss_tube.database.settings import Settings
from rss_tube.tasks import SaveThumbnailTask
from rss_tube.utils import convert_links, load_pixmap

from .entry_actions import PlayAudioOnlyAction, SaveThumbnailAction
from .BaseEntry import BaseEntry
from ..designs.widget_soundcloud import Ui_Form

logger = logging.getLogger("logger")
settings = Settings()


class ThumbnailContextMenu(QtWidgets.QMenu):
    def __init__(self, parent):
        super(ThumbnailContextMenu, self).__init__(parent)

        self.action_play_audio_only = PlayAudioOnlyAction()
        self.action_save_thumbnail = SaveThumbnailAction()

        self.addAction(self.action_play_audio_only)

        self.addSeparator()

        self.addAction(self.action_save_thumbnail)


class EntrySoundcloud(BaseEntry, Ui_Form):
    def __init__(self, parent):
        super(EntrySoundcloud, self).__init__(parent)
        self.setupUi(self)

        self.show_description(settings.value("youtube/show_description", type=bool))
        self.label_thumbnail.setToolTip("Click to play with external player")
        self.label_thumbnail.setScaledContents(True)

        self.link_callbacks()

    def display_entry(self, entry: dict):        
        self.video_url = entry["link_raw"]
        self.url = entry["link"]
        self.entry_id = entry["entry_id"]
        self._id = entry["id"]

        self.label_title.setText(entry["title"])

        self.starred = entry["star"]
        self.set_star(entry["star"])

        self.thumbnail_url = entry["thumbnail"]
        image_bytes = self.download.get_bytes(entry["thumbnail"])
        self.label_thumbnail.setPixmap(load_pixmap(image_bytes))
        self.label_date.setText(datetime.strptime(entry["published"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d, %H:%M"))
        channel_url = self.feeds.get_feed(entry["feed_id"])["channel_url"]
        self.label_meta_author.setText(f"<a href=\"{channel_url}\">{entry['author']}</a>")
        self.label_meta_website.setText(f"<a href=\"{entry['link']}\">{entry['link']}</a>")
        self.label_meta_duration.setText(entry['duration'])
        self.label_description.setHtml(convert_links(entry["description"]).replace("\n", "<br>"))

    def thumbnail_context(self, event: QtGui.QContextMenuEvent):
        context_menu = ThumbnailContextMenu(self)
        action = context_menu.exec(self.label_thumbnail.mapToGlobal(event.pos()))

        if isinstance(action, PlayAudioOnlyAction):
            self.player.play(self.video_url, play_quality_once=action.resolution)
        elif isinstance(action, SaveThumbnailAction):
            suggested_name = os.path.join(settings.value("EntryYoutube/save_thumbnail_location", type=str), self.entry_id.lstrip("yt:video:") + "_thumbnail.jpg")
            if fname := QtWidgets.QFileDialog.getSaveFileName(self, "Save thumbnail", suggested_name, "*.jpg")[0]:
                self.save_thumbnail_task = SaveThumbnailTask(self.thumbnail_url, fname)
                self.save_thumbnail_task.start()
                settings.setValue("EntryYoutube/save_thumbnail_location", os.path.dirname(fname))

    def link_callbacks(self):
        self.label_thumbnail.mousePressEvent = self.thumbnail_mouse_button
        self.label_thumbnail.contextMenuEvent = self.thumbnail_context

        self.pb_play.clicked.connect(self.play)

        self.pb_star.clicked.connect(self.star_toggled_callback)
