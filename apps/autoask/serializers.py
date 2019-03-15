#encoding:utf-8
from rest_framework import serializers
from .models import Tasks

class AutoaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = '__all__'

    # 后端格式时间
    add_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    exec_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)