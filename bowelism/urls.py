from django.urls import re_path
from django.conf.urls import include

from bowelism.log_streaming import views as log_streaming_views

urlpatterns = [
    re_path(r'^$', log_streaming_views.homepage, name='homepage'),
    re_path(r'^user-manual', log_streaming_views.homepage, name='homepage'),
    re_path(r'^bowelism', log_streaming_views.homepage, name='homepage'),
    re_path(r'^intro', log_streaming_views.homepage, name='homepage'),
    re_path(r'^', include('bowelism.api.urls')),
]
