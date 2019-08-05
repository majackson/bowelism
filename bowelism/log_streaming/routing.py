from django.conf.urls import url

from bowelism.log_streaming import consumers


websocket_urlpatterns = [
    url(r'^ws/log-streaming', consumers.LogStreamingConsumer)
]
