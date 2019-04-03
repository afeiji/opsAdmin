#encoding:utf-8

from rest_framework.routers import DefaultRouter
from . import views

asset_router = DefaultRouter()
# asset_router.register('asset', views.HostViewSet, base_name="asset")
asset_router.register('asset/save', views.SaveHostViewset, base_name="asset")