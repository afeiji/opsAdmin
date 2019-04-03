#encoding:utf-8

from rest_framework import serializers
from .models import Host

class HostSerilalizer(serializers.ModelSerializer):

    class Meta():
        model = Host
        fields = "__all__"

    # 重新create方法，判断instanceId是否存在，存在就调用update，不存在就创建
    def create(self, validated_data):
        try:
            instance = Host.objects.get(instanceId=validated_data['instanceId'])
        except Host.DoesNotExist:
            instance = None
        if instance is not None:
            return self.update(instance, validated_data)
        # 创建的需要返回一条记录
        instance = Host.objects.create(**validated_data)
        return instance

