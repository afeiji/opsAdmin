#encoding:utf-8

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import WorkOrder

User = get_user_model()

class WorkOrderSerializer(serializers.ModelSerializer):
    """
    工单序列化
    """

    class Meta:
        model = WorkOrder
        fields = '__all__'

    # 获取当前登录用户，并将其赋值给数据库对应的一段
    applicant = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # print("applicant:",applicant)

    # 后端格式时间
    apply_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    complete_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)


    def to_representation(self, instance):
        applicant_obj = instance.applicant
        assign_to_obj = instance.assign_to
        final_processor_obj = instance.final_processor
        type_value = instance.get_type_display()
        status_value = instance.get_status_display()
        ret = super(WorkOrderSerializer, self).to_representation(instance)
        ret['type'] = {
            "id": instance.type,
            "name": type_value
        }
        # print("status_value:",status_value)
        ret['status'] = {
            "id": instance.status,
            "name": status_value
        }
        ret['applicant'] = {
            "id": applicant_obj.id,
            "name": applicant_obj.username
        }
        ret['assign_to'] = {
            "id": assign_to_obj.id,
            "name":assign_to_obj.username
        }

        if final_processor_obj:
            ret["final_processor"] = {
                "id": final_processor_obj.id,
                "name": final_processor_obj.name
            }
        return ret
