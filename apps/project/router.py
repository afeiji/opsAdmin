#encoding:utf-8

from rest_framework.routers import DefaultRouter
from .views import ProjectListView, ProjectVersionView

project_router = DefaultRouter()
project_router.register('list', ProjectListView, base_name="list")
project_router.register('tag', ProjectVersionView, base_name="tag")


# from django.conf.urls import url
# from .views import *
#
# urlpatterns = [
#     url('^list/$', ProjectListView.as_view(), name="project_list"),
#     url('^tag/$', ProjectVersionView.as_view(), name="project_tag")
# ]