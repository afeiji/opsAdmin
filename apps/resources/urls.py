#encoding:utf-8

from django.conf.urls import url,include
from .views import TestView

urlpatterns = [
    url(r'^$',TestView.as_view())
]