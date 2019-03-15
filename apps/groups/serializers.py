#encoding:utf-8

from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    """
    group序列化类
    """

    def to_representation(self, instance):
        ret = super(GroupSerializer, self).to_representation(instance)
        # instance才是一个实例，ret是一个<class 'collections.OrderedDict'> OrderedDict([('id', 10), ('name', 'CEO')])
        ret['members'] = instance.user_set.count()
        return ret

    class Meta():
        model = Group
        # fields表示要序列化哪些字段
        fields = ('id','name')

class UserGroupsSerializer(serializers.Serializer):
    """
    group序列化类
    """
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    class Meta:
        model = Group
        fields = ("id","name")


class GroupNumbersSerializer(serializers.ModelSerializer):
    """
    user序列化类
    """
    class Meta():
        model = User
        # fields表示要序列化哪些字段
        fields = ("id", "username", "name", "phone", "email")