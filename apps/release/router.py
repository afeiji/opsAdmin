#encoding:utf-8

from rest_framework.routers import DefaultRouter
from .views import ReleaseViewset

release_router = DefaultRouter()
release_router.register('release', ReleaseViewset, base_name="release")

