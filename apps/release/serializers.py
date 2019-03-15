#encoding:utf-8

from rest_framework import serializers
from .models import Deploy
from django.contrib.auth import get_user_model

User = get_user_model()

class ReleaseSerializer(serializers.ModelSerializer):
    """
    发布序列化
    """

    class Meta:
        model = Deploy
        fields = '__all__'

    # 获取当前登录用户，并将其赋值给数据库对应的一段
    applicant = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # 后端格式时间
    apply_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    deploy_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    def to_representation(self, instance):
        applicant_obj = instance.applicant
        reviewer_obj = instance.reviewer
        assign_to_obj = instance.assign_to
        # get_status_display是models定义类选项choices
        status_value = instance.get_status_display()
        ret = super(ReleaseSerializer, self).to_representation(instance)

        ret['applicant'] = {
            'id': applicant_obj.id,
            'name': applicant_obj.username
        }

        ret['status'] = {
            'id': instance.status,
            'name': status_value
        }

        if reviewer_obj:
            ret['reviewer'] = {
                'id': reviewer_obj.id,
                'name': reviewer_obj.username
            }

        if assign_to_obj:
            ret['assign_to'] = {
                'id': assign_to_obj.id,
                'name': assign_to_obj.username
            }
        return ret

