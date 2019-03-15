#encoding:utf-8

from rest_framework.routers import DefaultRouter
from tencent.views import TencentCreate

router = DefaultRouter()
router.register("tencent",TencentCreate,base_name="tencent")