import logging
import os
from datetime import datetime

from PyQt6 import QtCore, QtGui, QtWidgets
from rss_tube.database.settings import Settings
from rss_tube.tasks import SaveThumbnailTask
from rss_tube.utils import convert_links, get_abs_path, load_pixmap

from .entry_actions import PlayAudioOnlyAction, PlayResolutionAction, SaveThumbnailAction
from .BaseEntry import BaseEntry
from ..designs.widget_youtube import Ui_Form

logger = logging.getLogger("logger")
settings = Settings()


class ThumbnailContextMenu(QtWidgets.QMenu):
    def __init__(self, parent):
        super(ThumbnailContextMenu, self).__init__(parent)

        self.action_play_audio_only = PlayAudioOnlyAction()
        self.actions_resolution = [
            PlayResolutionAction("2160p"),
            PlayResolutionAction("1440p"),
            PlayResolutionAction("1080p"),
            PlayResolutionAction("720p"),
            PlayResolutionAction("480p"),
            PlayResolutionAction("360p"),
            PlayResolutionAction("240p"),
            PlayResolutionAction("144p")
        ]
        self.action_save_thumbnail = SaveThumbnailAction()

        self.addAction(self.action_play_audio_only)

        self.addSeparator()

        self.addActions(self.actions_resolution)

        self.addSeparator()

        self.addAction(self.action_save_thumbnail)


class EntryYoutube(BaseEntry, Ui_Form):
    def __init__(self, parent):
        super(EntryYoutube, self).__init__(parent)
        self.setupUi(self)

        self.show_description(settings.value("youtube/show_description", type=bool))
        self.label_thumbnail.setToolTip("Click to play with external player")

        self.pb_audio.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{settings.value('theme', type=str)}/audio.png")))

        self.link_callbacks()

    def display_entry(self, entry: dict):
        self.video_url = entry["link"]
        self.url = self.video_url
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
        self.label_meta_views.setText(f"{entry['views']:,}")
        self.label_description.setHtml(convert_links(entry["description"]).replace("\n", "<br>"))
    
    def pb_play_callback(self):
        self.pb_play.setDisabled(True)
        QtCore.QTimer.singleShot(1000, lambda: self.pb_play.setEnabled(True))
        self.play()
    
    def pb_play_audio_callback(self):
        self.pb_audio.setDisabled(True)
        QtCore.QTimer.singleShot(1000, lambda: self.pb_audio.setEnabled(True))
        self.play_audio()

    def thumbnail_context(self, event: QtGui.QContextMenuEvent):
        context_menu = ThumbnailContextMenu(self)
        action = context_menu.exec(self.label_thumbnail.mapToGlobal(event.pos()))

        if isinstance(action, (PlayAudioOnlyAction, PlayResolutionAction)):
            self.player.play(self.video_url, play_quality_once=action.resolution)
        elif isinstance(action, SaveThumbnailAction):
            thumbnail_url = self.thumbnail_url.replace("hqdefault", "maxresdefault")
            suggested_name = os.path.join(settings.value("EntryYoutube/save_thumbnail_location", type=str), self.entry_id.lstrip("yt:video:") + "_thumbnail.jpg")
            if fname := QtWidgets.QFileDialog.getSaveFileName(self, "Save thumbnail", suggested_name, "*.jpg")[0]:
                self.save_thumbnail_task = SaveThumbnailTask(thumbnail_url, fname)
                self.save_thumbnail_task.start()
                settings.setValue("EntryYoutube/save_thumbnail_location", os.path.dirname(fname))

    def link_callbacks(self):
        self.label_thumbnail.mousePressEvent = self.thumbnail_mouse_button
        self.label_thumbnail.contextMenuEvent = self.thumbnail_context

        self.pb_play.clicked.connect(self.pb_play_callback)
        self.pb_audio.clicked.connect(self.pb_play_audio_callback)

        self.pb_star.clicked.connect(self.star_toggled_callback)
