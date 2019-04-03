from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url('^list/$', ProjectListView.as_view(), name="project_list"),
    url('^tag/$', ProjectVersionView.as_view(), name="project_tag")
]