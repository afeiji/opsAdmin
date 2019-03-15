#encoding:utf-8

from rest_framework.routers import DefaultRouter
from .views import PermissionViewset, GroupPermissionViewset

permission_router = DefaultRouter()
permission_router.register('permission',PermissionViewset,base_name="permission")
permission_router.register('groupPermission',GroupPermissionViewset,base_name="groupPermission")
