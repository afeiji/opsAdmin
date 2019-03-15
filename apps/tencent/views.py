from django.shortcuts import render

# Create your views here.
from tencent.serializers import TencentSerrializer
from rest_framework import viewsets,mixins,status
from tencent.models import tencent
from rest_framework.response import Response

class TencentCreate( viewsets.ModelViewSet):
    queryset = tencent.objects.all()
    serializer_class = TencentSerrializer

