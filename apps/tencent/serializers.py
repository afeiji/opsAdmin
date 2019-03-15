#encoding:utf-8

from rest_framework import serializers
from tencent.models import tencent

class TencentSerrializer(serializers.ModelSerializer):

    class Meta:
        model = tencent
        fields = "__all__"
