from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from pygtail import Pygtail

channel_layer = get_channel_layer()


class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(settings.STREAMED_LOG_FILE):
            for line in Pygtail(event.src_path):
                distribute_messages([line])


class Command(BaseCommand):

    help = (
        "Stream a logfile to connected sockets."
    )

    def handle(self, *args, **kwargs):
        for _ in Pygtail(str(Path(settings.STREAMED_LOG_PATH, settings.STREAMED_LOG_FILE))):
            pass  # ensure file offset is all the way to the bottom of the file when we start

        observer = Observer()
        observer.schedule(LogHandler(), settings.STREAMED_LOG_PATH, recursive=False)
        observer.start()
        observer.join(timeout=None)  # block until stopped


def distribute_messages(messages):
    "Send messages to consumers."
    async_to_sync(channel_layer.group_send)(settings.STREAMING_LOG_GROUP, {
        'type': 'log_lines',
        'data': messages
    })
