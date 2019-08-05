from django.conf import settings
from django.conf.urls import include, url

from django.contrib import admin

from bowelism.log_streaming import views as log_streaming_views

urlpatterns = [
    url(r'^$', log_streaming_views.homepage, name='homepage'),
    url(r'^', include('bowelism.api.urls')),
]
