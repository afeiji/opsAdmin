from rest_framework import serializers
from idc.models import Idc

class IdcSerializer(serializers.Serializer):
    id      = serializers.IntegerField(read_only=True,help_text="id")
    name    = serializers.CharField(required=False,help_text="IDC名称",label="IDC名称")    #不设置的时候，PUT时单传一个值会报错
    address = serializers.CharField(required=False,help_text="IDC地址",label="IDC地址")
    phone = serializers.CharField(required=False,help_text="IDC联系方式",label="IDC联系方式")
    email = serializers.EmailField(required=False,help_text="IDC的email",label="IDC的email")

    def update(self, instance, validated_data): #instance表示当前的Idc，validated_data验证之后，非常干净的数据
        instance.name = validated_data.get("name",instance.name)
        instance.address = validated_data.get("address",instance.address)
        instance.phone = validated_data.get("phone",instance.phone)
        instance.email = validated_data.get("email",instance.email)
        instance.save()
        return instance

    def create(self,validated_data):
        return Idc.objects.create(**validated_data)

    def to_internal_value(self, data):
        # 这是序列化第一步
        ret = super(IdcSerializer,self).to_internal_value(data)
        return ret

    def to_representation(self, instance):
        # 这是序列化最后一步
        ret = super(IdcSerializer,self).to_representation(instance)
        ret["text"] = "aa"
        return ret

##################################### 用户 ##################################################
from django.contrib.auth.models import User,Group
class UserSerializer(serializers.Serializer):
    id      = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=False)
    password    = serializers.CharField(required=False)    #不设置的时候，PUT时单传一个值会报错
    email = serializers.EmailField(required=False)

    def update(self, instance, validated_data): #instance表示当前的Idc，validated_data验证之后，非常干净的数据
        instance.username = validated_data.get("username",instance.name)
        instance.password = validated_data.get("password",instance.address)
        instance.email = validated_data.get("email",instance.email)
        instance.save()
        return instance

    def create(self,validated_data):
        return User.objects.create(**validated_data)

##################################### 组 ##################################################
from django.contrib.auth.models import Group
class GroupSerializer(serializers.Serializer):
    id      = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)

    def update(self, instance, validated_data): #instance表示当前的Idc，validated_data验证之后，非常干净的数据
        instance.name = validated_data.get("name",instance.name)
        instance.save()
        return instance

    def create(self,validated_data):
        return Group.objects.create(**validated_data)


##################################### 权限 ##################################################
from django.contrib.auth.models import Permission
class PermissionSerializer(serializers.Serializer):
    id      = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)

    def update(self, instance, validated_data): #instance表示当前的Idc，validated_data验证之后，非常干净的数据
        instance.name = validated_data.get("name",instance.name)
        instance.save()
        return instance

    def create(self,validated_data):
        return Permission.objects.create(**validated_data)

























