#encoding:utf-8

from rest_framework.routers import DefaultRouter
from .views import ProjectListView, ProjectVersionView

project_router = DefaultRouter()
project_router.register('project/list', ProjectListView, base_name="list")
project_router.register('project/tag', ProjectVersionView, base_name="tag")

