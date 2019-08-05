from channels.routing import ProtocolTypeRouter, URLRouter

from bowelism.log_streaming import routing as log_streaming_routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(log_streaming_routing.websocket_urlpatterns)
})
