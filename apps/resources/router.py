#encoding:utf-8

from rest_framework.routers import DefaultRouter
from resources.views import ServerViewset

route = DefaultRouter()
route.register('server',ServerViewset,base_name="server")