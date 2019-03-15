#encoding:utf-8
from rest_framework import serializers
from django.contrib.auth.models import User,Group

class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False)
    # password = serializers.CharField(required=False)
    # email = serializers.EmailField(required=False)