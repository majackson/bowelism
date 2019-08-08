from datetime import datetime, timedelta
from time import sleep

from django.conf import settings
from django.core.management.base import BaseCommand

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


SLEEP_PERIOD = 0.5
REOPEN_FILE_AFTER = timedelta(hours=1)  # reopen the file to allow log rotation etc


channel_layer = get_channel_layer()


class Command(BaseCommand):

    help = (
        "Stream a logfile to connected sockets."
    )

    def handle(self, *args, **kwargs):
        while True:
            with open(settings.STREAMED_LOG_FILE, 'r') as log_file:
                opened_time = datetime.now()

                # consumers already send existing contents when they first open,
                # so we can throw initial log contents away.
                # we only want new stuff as it appears.
                log_file.read()

                while True:  # continue periodically polling for changes
                    if (datetime.now() - opened_time) > REOPEN_FILE_AFTER:
                        break

                    sleep(SLEEP_PERIOD)
                    log_entries = log_file.read().splitlines()
                    if log_entries:
                        distribute_messages(log_entries)


def distribute_messages(messages):
    "Send messages to consumers."
    async_to_sync(channel_layer.group_send)(settings.STREAMING_LOG_GROUP, {
        'type': 'log_lines',
        'data': messages
    })
