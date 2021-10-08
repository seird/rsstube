import abc
from datetime import datetime
import schedule
import logging
import requests
import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from rss_tube.database.feeds import Feeds
from rss_tube.database.settings import Settings


logger = logging.getLogger("logger")
settings = Settings("rss-tube")


class Tasks(QtCore.QThread):
    job_update_info = pyqtSignal(datetime, datetime)

    def __init__(self):
        super(Tasks, self).__init__()
        self.running = False

        self.feed_update_task = FeedUpdateTask()
        self.delete_entries_task = DeleteEntriesTask()

        self.interval = settings.value("tasks/interval", type=int)

        self.set_schedule()

    def set_schedule(self):
        schedule.clear("update-feed")
        schedule.clear("delete_entries")
        self.feed_update_job = schedule.every(settings.value("feeds/update_interval/minutes", type=int)).minutes.do(self.feed_update_task.start).tag("update-feed")
        schedule.every(settings.value("delete/interval/hours", type=int)).hours.do(self.delete_entries_task.start).tag("delete_entries")

        self.job_update_info.emit(self.feed_update_job.last_run or datetime.now(), self.feed_update_job.next_run or datetime.now())
        self.feed_update_task._finished.connect(lambda: self.job_update_info.emit(self.feed_update_job.last_run, self.feed_update_job.next_run))

    def run(self):
        self.running = True
        try:
            schedule.run_all()
            while self.running:
                time.sleep(self.interval)
                schedule.run_pending()
        except Exception as e:
            logger.error(f"Tasks: {e}")
        finally:
            self.running = False


class BaseTask(QtCore.QThread):
    failed = pyqtSignal()

    def __init__(self):
        super(BaseTask, self).__init__()
        self.running = False

    @abc.abstractmethod
    def task(self):
        ...

    def run(self):
        self.running = True
        try:
            self.task()
        except Exception as e:
            logger.error(f"{self.__class__.__name__} failed: {e}")
            self.failed.emit()
        finally:
            self.running = False


class DeleteEntriesTask(BaseTask):
    def task(self):
        delete_added_more_than = settings.value("delete/added_more_than", type=bool)
        days_added_more_than = settings.value("delete/added_more_than_days", type=int)
        keep_unviewed = settings.value("delete/keep_unviewed", type=bool)

        if not delete_added_more_than:
            return

        feeds = Feeds()
        if delete_added_more_than:
            feeds.delete_entries_added_more_than_days(days_added_more_than, keep_unviewed)


class FeedUpdateTask(BaseTask):
    _finished = pyqtSignal()

    def task(self):
        Feeds().update_feeds(interval=0.5)
        self._finished.emit()


class AddFeedTask(BaseTask):
    added = pyqtSignal(int)

    def __init__(self, url: str, category: str, name: str):
        super(AddFeedTask, self).__init__()
        self.url = url
        self.category = category
        self.name = name

    def task(self):
        feeds = Feeds()
        feed_id = feeds.add_feed(self.url, self.category, self.name)
        if feed_id is None:
            logger.error(f"AddFeedTask: adding '{self.url}' failed.")
            self.failed.emit()
            return
        feeds.update_feed_entries(feed_id)
        self.added.emit(feed_id)


class ImportFeedsTask(BaseTask):
    imported = pyqtSignal(int)

    def __init__(self, fname: str):
        super(ImportFeedsTask, self).__init__()
        self.fname = fname

    def task(self):
        try:
            with open(self.fname, "r", encoding="utf-8") as f:
                header = f.readline()
                lines = f.readlines()
        except FileNotFoundError:
            logger.error(f"ImportFeedsTask failed: {self.name} does not exist.")
            self.failed.emit()
            return

        feeds = Feeds()

        for line in lines:
            author, url, category = line.rstrip("\n").split(",")
            feed_id = feeds.add_feed(url, category, feed_name=author)
            if feed_id is None:
                logger.error(f"ImportFeedsTask: adding '{url}' failed.")
                continue
            self.imported.emit(feed_id)


class ExportFeedsTask(BaseTask):
    def __init__(self, fname: str):
        super(ExportFeedsTask, self).__init__()
        self.fname = fname

    def task(self):
        feeds = Feeds()
        with open(self.fname, "w", encoding="utf-8") as f:
            f.write("author,url,category\n")
            for feed in feeds.get_feeds():
                author = feed["author"].replace(",", "")
                f.write(f'{author},{feed["url"]},{feed["category"]}\n')


class SaveThumbnailTask(BaseTask):
    def __init__(self, img_url: str, fname: str):
        super(SaveThumbnailTask, self).__init__()
        self.img_url = img_url
        self.fname = fname

    def task(self):
        response = requests.get(self.img_url)
        if response.ok:
            with open(self.fname, "wb") as f:
                f.write(response.content)
