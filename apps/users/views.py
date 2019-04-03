#encoding:utf-8
from rest_framework import viewsets, mixins,permissions,response
from users.serializers import UsersSerializer,UserRegSerializer
from rest_framework.pagination import PageNumberPagination
from .filters import UserFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
User = get_user_model()


class UserViewsets(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """"
    retrieve:
        获取指定user记录
    list:
        获取user列表
    update:
        更新user记录
    partial_update:
        更新user的部分记录
    destroy:
        删除user记录
    """
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UsersSerializer

    filter_class = UserFilter
    filter_fields = ("username",)


class UserRegViewset(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin):
    """
    create:
        用户注册
    partial_update:
        修改密码
    update:
        修改密码
    """
    queryset = User.objects.all()
    serializer_class = UserRegSerializer


class UserInfoViewset(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    # 默认是get请求
    def list(self,request,*args, **kwargs):
        data = {
            "username": self.request.user.username,
            "name": self.request.user.name,
            "permission": self.request.user.get_all_permissions()   #传递所有权限给前端，让前端控制权限
        }
        return response.Response(data)





