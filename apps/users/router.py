#encoding:utf-8

from rest_framework.routers import DefaultRouter
from users.views import UserViewsets,UserRegViewset,UserInfoViewset

route = DefaultRouter()
route.register('users',UserViewsets,base_name="users")
route.register('userReg',UserRegViewset,base_name="userReg")
route.register('UserInfo',UserInfoViewset,base_name="UserInfo")