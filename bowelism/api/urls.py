from django.urls import re_path

from bowelism.api.views.heartbeat import heartbeat


urlpatterns = [
    re_path(r'^heartbeat/$', heartbeat, name='heartbeat'),
]
