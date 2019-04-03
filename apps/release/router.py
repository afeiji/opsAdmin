#encoding:utf-8

from rest_framework.routers import DefaultRouter
from .views import ReleaseViewset, CountChartsViewsetV2, CountUserCViewsetV2

release_router = DefaultRouter()
release_router.register('release', ReleaseViewset, base_name="release")
release_router.register('countpv2', CountChartsViewsetV2, base_name="countpv2")
release_router.register('countuv2', CountUserCViewsetV2, base_name="countuv2")

