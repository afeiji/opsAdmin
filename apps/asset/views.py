#encoding:utf-8

from .models import Host
from .serilalizsers import HostSerilalizer
from rest_framework import viewsets, permissions
from .qcloud import aly_ecs_api
from django.http import HttpResponse


class SaveHostViewset(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        aly_ecs_api.save_host()
        return HttpResponse("")

# class HostViewSet(viewsets.ModelViewSet):
#     queryset = Host.objects.all()
#     serializer_class = HostSerilalizer
#
#
#     def create(self, request, *args, **kwargs):
#         host = aly_ecs_api.get_host()
#         host_list = host['Instances']['Instance']
#         for _host in host_list:
#             host_ser = HostSerilalizer(data=_host)

