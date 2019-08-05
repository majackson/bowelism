import json

from django.conf import settings

from channels.generic.websocket import WebsocketConsumer


INITIAL_LOG_LINES = 60  # send the last n lines when a client first connects


class LogStreamingConsumer(WebsocketConsumer):

    groups = [settings.STREAMING_LOG_GROUP]

    def connect(self):
        self.accept()
        with open(settings.STREAMED_LOG_FILE, 'r') as log_file:
            self.send(json.dumps(log_file.read().splitlines()[-INITIAL_LOG_LINES:]))

    def log_lines(self, event):
        self.send(json.dumps(event['data']))
