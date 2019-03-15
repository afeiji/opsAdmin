#encoding:utf-8

from django.views import View
from django.http import HttpResponse
from resources.qcloud import cvm
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import ServerSerializer
from .models import Server

class TestView(View):
    def get(self,request,*args,**kwargs):
        cvm.getCvmList()
        return HttpResponse("")


class ServerViewset(ReadOnlyModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
