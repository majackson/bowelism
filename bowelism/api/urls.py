from django.conf.urls import url

from bowelism.api.views.heartbeat import heartbeat


urlpatterns = [
    url(r'^heartbeat/$', heartbeat, name='heartbeat'),
]
