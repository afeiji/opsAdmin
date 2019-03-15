#encoding:utf-8

from django.contrib.auth.models import Group
from rest_framework import viewsets,mixins,response,status
from .serializers import GroupSerializer,UserGroupsSerializer, GroupNumbersSerializer
from .filters import GroupFilter
from django.contrib.auth import get_user_model
User = get_user_model()

class GroupViewsets(viewsets.ModelViewSet):
    # ListModelMixin 自己调用settings分页
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    filter_class = GroupFilter
    filter_fields = ("name",)

class UserGroupsViewset(viewsets.GenericViewSet,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin):
    """
    retrieve:
        获取当前用户的所有用户组列表
    update:
        修改当用户的角色
    """
    # 获取所有的user，然后通过pk来查
    queryset = User.objects.all()
    serializer_class = UserGroupsSerializer

    def retrieve(self, request, *args, **kwargs):
        userObj = self.get_object()
        queryset = userObj.groups.all()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


    def update(self, request, *args, **kwargs):
        userObj = self.get_object()
        print(type(request.data), request.data)
        groupIds = request.data.get("gids", [])
        userObj.groups = Group.objects.filter(id__in=groupIds)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

class GroupMembersViewset(viewsets.GenericViewSet,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin):
    """
    retrieve:
        获取当前用户组的所有用户
    destroy:
        删除一个用户组中的一个用户
    """
    queryset = Group.objects.all()
    serializer_class = GroupNumbersSerializer

    def retrieve(self, request, *args, **kwargs):
        groupObj = self.get_object()
        queryset = groupObj.user_set.all()
        # RetrieveModelMixin 默认是不调用settings的分页，需要自己定义
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        groupObj = self.get_object()
        userId = request.data.get("uid", 0)
        # 自定义错误提示词
        ret = {"status": 0}
        try:
            userObj = User.objects.get(pk=userId)
            groupObj.user_set.remove(userObj)
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "用户错误"
        return response.Response(ret, status=status.HTTP_200_OK)

