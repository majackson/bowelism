from django.urls import re_path

from bowelism.log_streaming import consumers


websocket_urlpatterns = [
    re_path(r'^ws/log-streaming', consumers.LogStreamingConsumer.as_asgi())
]
