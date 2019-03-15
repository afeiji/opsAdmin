#encoding:utf-8
from rest_framework import serializers

# 新添加的
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.auth import get_user_model
from devops.settings import GITLAB_HTTP_URI, GITLAB_TOKEN
import gitlab
User = get_user_model()


# class UsersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         exclude = ("password","groups","user_permissions")
#
#         # fields = "__all__"

class UsersSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """
    last_login  = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                            label="上次登录时间",
                                            help_text="上次登录时间")

    class Meta:
        model = User
        # 返回的字段
        fields = ("id", "username", "name", "phone", "email", "is_active", "last_login")

    def update(self, instance, validated_data):
        instance.phone = validated_data.get("phone",instance.phone)
        instance.is_active = validated_data.get("is_active",instance.is_active)
        instance.save()
        return instance

class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册序列化类
    """
    password = serializers.CharField(style={"input_type": "password"},
                                     label="密码",
                                     write_only=True,
                                     help_text="密码")
    def validate(self, attrs):
        # 创建新用户是否激活用户
        # attrs["is_active"] = False
        attrs["is_active"] = True
        attrs["email"] = "{}{}".format(attrs['username'], settings.DOMAIN)
        return attrs

    def create(self, validated_data):
        instance = super(UserRegSerializer, self).create(validated_data=validated_data)
        # 使存储的密码变成密文
        instance.set_password(validated_data["password"])
        instance.save()
        # 创建用户的同时创建gitlab用户
        # gl = gitlab.Gitlab(GITLAB_HTTP_URI, GITLAB_TOKEN, api_version=4)
        # res = gl.users.create({'username': validated_data['username'], 'password': validated_data['password'], 'email': validated_data['email'], 'name': validated_data['name']})
        return instance

    def update(self, instance, validated_data):
        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    class Meta:
        model = User
        fields = ("username", "password", "name", "id", "phone")
        # fields = ("username", "password", "id")