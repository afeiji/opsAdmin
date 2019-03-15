from rest_framework import viewsets, mixins, response, status
from django.contrib.auth.models import Permission,Group
from .serializers import PermissionSerializer



class PermissionViewset(viewsets.ModelViewSet):

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class GroupPermissionViewset(viewsets.GenericViewSet,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin):
    """
    retrieve:
        获取当前用户组的所有权限
    """
    queryset = Group.objects.all()
    serializer_class = PermissionSerializer


    def retrieve(self, request, *args, **kwargs):
        groupObj = self.get_object()
        queryset = groupObj.permissions.all()
        # 获取queryset后，要进行反序列化
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def update(self, request, *args, **kwargs):
        groupObj = self.get_object()
        pids = request.data.get("pids",[])
        groupObj.permissions = Permission.objects.filter(id__in=pids)
        ret = {}
        ret["status"] = 0
        return response.Response(ret, status=status.HTTP_200_OK)