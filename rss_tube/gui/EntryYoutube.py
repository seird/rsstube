import logging
import os
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from rss_tube.database.feeds import Feeds
from rss_tube.database.settings import Settings
from rss_tube.download import Downloader
from rss_tube.player import Player
from rss_tube.tasks import SaveThumbnailTask
from rss_tube.utils import convert_links, get_abs_path, load_pixmap

from .designs.widget_youtube import Ui_Form

logger = logging.getLogger("logger")
settings = Settings("rss-tube")


class RatingWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(RatingWidget, self).__init__()

        self.parent = parent

        self.star_layout = QtWidgets.QHBoxLayout()
        self.star_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.star_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.star_layout)

        self.set_pixmaps(settings.value("theme", type=str))

    def set_pixmaps(self, theme: str):
        size = self.parent.label_static_meta_rating.height()/2

        self.star_pixmap = QtGui.QPixmap(get_abs_path(f"rss_tube/gui/themes/{theme}/star.png"))
        self.star_pixmap = self.star_pixmap.scaled(size, size, QtCore.Qt.KeepAspectRatio)

        self.star_half_pixmap = QtGui.QPixmap(get_abs_path(f"rss_tube/gui/themes/{theme}/star_half.png"))
        self.star_half_pixmap = self.star_half_pixmap.scaled(size, size, QtCore.Qt.KeepAspectRatio)

    def clear_stars(self):
        for i in reversed(range(self.star_layout.count())):
            self.star_layout.itemAt(i).widget().deleteLater()

    def set_rating(self, rating: float, count: int):
        self.setToolTip(f"{rating} ({count:,})")
        self.clear_stars()
        for i in range(0, int(rating)):
            label_star = QtWidgets.QLabel()
            label_star.setPixmap(self.star_pixmap)
            self.star_layout.insertWidget(i, label_star)

        if (rating - int(rating)) >= 0.75:
            label_star = QtWidgets.QLabel()
            label_star.setPixmap(self.star_pixmap)
            self.star_layout.insertWidget(int(rating), label_star)
        elif (rating - int(rating)) >= 0.25:
            label_star_half = QtWidgets.QLabel()
            label_star_half.setPixmap(self.star_half_pixmap)
            self.star_layout.insertWidget(int(rating), label_star_half)


class PlayResolutionAction(QtWidgets.QAction):
    def __init__(self, resolution: str):
        self.resolution = resolution
        super(PlayResolutionAction, self).__init__(resolution)


class PlayAudioOnlyAction(PlayResolutionAction):
    def __init__(self):
        super(PlayAudioOnlyAction, self).__init__("Audio only")


class SaveThumbnailAction(QtWidgets.QAction):
    def __init__(self):
        super(SaveThumbnailAction, self).__init__("Save thumbnail")


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


class EntryYoutube(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent):
        super(EntryYoutube, self).__init__()
        self.setupUi(self)

        self.url = ""
        self.video_url = ""
        self.thumbnail_url = ""
        self.entry_id = ""

        self.parent = parent
        self.player = Player()
        self.download = Downloader()
        self.feeds: Feeds = self.parent.feeds

        self.label_thumbnail.setToolTip("Click to play with MPV")
        self.show_description(settings.value("youtube/show_description", type=bool))

        self.pb_audio.setIcon(QtGui.QIcon(get_abs_path(f"rss_tube/gui/themes/{settings.value('theme', type=str)}/audio.png")))

        self.widget_rating = RatingWidget(self)
        self.formLayout_meta.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.widget_rating)

        self.link_callbacks()

    def display_entry(self, entry: dict):
        self.video_url = entry["link"]
        self.url = self.video_url
        self.entry_id = entry["entry_id"]

        self.label_title.setText(entry["title"])

        self.thumbnail_url = entry["thumbnail"]
        image_bytes = self.download.get_bytes(entry["thumbnail"])
        self.label_thumbnail.setPixmap(load_pixmap(image_bytes))
        self.label_date.setText(datetime.strptime(entry["published"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d, %H:%M"))
        channel_url = self.feeds.get_feed(entry["feed_id"])["channel_url"]
        self.label_meta_author.setText(f"<a href=\"{channel_url}\">{entry['author']}</a>")
        self.label_meta_website.setText(f"<a href=\"{entry['link']}\">{entry['link']}</a>")
        self.label_meta_views.setText(f"{entry['views']:,}")
        self.label_description.setHtml(convert_links(entry["description"]).replace("\n", "<br>"))
        self.widget_rating.set_rating(entry["rating_average"], entry["rating_count"])

    def show_description(self, show: bool = True):
        self.label_description.setHidden(not show)

    def play_video(self, play_quality_once: str = ""):
        self.player.play(self.video_url, play_quality_once=play_quality_once)

    def thumbnail_mouse_button(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            self.player.play(self.video_url)
        else:
            super(EntryYoutube, self).mousePressEvent(event)

    def thumbnail_context(self, event: QtGui.QContextMenuEvent):
        context_menu = ThumbnailContextMenu(self)
        action = context_menu.exec_(self.label_thumbnail.mapToGlobal(event.pos()))

        if isinstance(action, (PlayAudioOnlyAction, PlayResolutionAction)):
            self.player.play(self.video_url, play_quality_once=action.resolution)
        elif isinstance(action, SaveThumbnailAction):
            thumbnail_url = self.thumbnail_url.replace("hqdefault", "maxresdefault")
            suggested_name = os.path.join(settings.value("EntryYoutube/save_thumbnail_location", type=str), self.entry_id.lstrip("yt:video:") + "_thumbnail.jpg")
            if fname := QtWidgets.QFileDialog.getSaveFileName(self, "Save thumbnail", suggested_name, "*.jpg")[0]:
                self.save_thumbnail_task = SaveThumbnailTask(thumbnail_url, fname)
                self.save_thumbnail_task.start()
                settings.setValue("EntryYoutube/save_thumbnail_location", os.path.dirname(fname))

    def play_callback(self):
        self.player.play(self.video_url)

    def play_audio_callback(self):
        self.player.play(self.video_url, play_quality_once=PlayAudioOnlyAction().resolution)

    def clear_player_status(self):
        if "Playing" not in self.label_player_status.text():
            self.label_player_status.clear()

    def player_stopped_callback(self):
        self.label_player_status.setText("Stopped")
        QtCore.QTimer.singleShot(5000, self.clear_player_status)

    def player_failed_callback(self, error_code: int):
        self.label_player_status.setText(f"Failed ({error_code})")
        QtCore.QTimer.singleShot(5000, self.clear_player_status)

    def link_callbacks(self):
        self.label_thumbnail.mousePressEvent = self.thumbnail_mouse_button
        self.label_thumbnail.contextMenuEvent = self.thumbnail_context
        self.pb_play.clicked.connect(self.play_callback)
        self.pb_audio.clicked.connect(self.play_audio_callback)

        self.player.started.connect(lambda: self.label_player_status.setText("Playing..."))
        self.player.stopped.connect(self.player_stopped_callback)
        self.player.failed.connect(self.player_failed_callback)
