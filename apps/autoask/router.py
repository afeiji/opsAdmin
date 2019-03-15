#encoding:utf-8

from rest_framework.routers import DefaultRouter
from .views import AutoaskViewset

router = DefaultRouter()
router.register('task',AutoaskViewset,base_name="task")