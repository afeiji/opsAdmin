#encoding:utf-8
from rest_framework import viewsets, response,status
from .models import WorkOrder
from .filters import WorkorderFilter
from .serializers import WorkOrderSerializer
import time

class WorkOrderViewset(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    filter_class = WorkorderFilter
    filter_fields = ("title", "order_contents")

    def get_queryset(self):
        status = self.request.GET.get('status',None)
        applicant = self.request.user
        # 获取当前登录用户的所有组的信息，RBAC 用户-->组-->权限
        role = applicant.groups.all().values('name')
		# 列表推倒式[]，把组名添加到一个列表
        role_name = [r['name'] for r in role]
        queryset = super(WorkOrderViewset, self).get_queryset()

        #判断传来的status值是申请列表还是历史列表
        if status and int(status) == 1:
            queryset = WorkOrder.objects.filter(status__lte=int(status))
        elif status and int(status) == 2:
            queryset = WorkOrder.objects.filter(status__gte=int(status))
        else:
            queryset = WorkOrder.objects.all()

        # 判断登录用户是否为管理员，是则显示所有工单，否则只显示自己的，ops是我的组名
        if "ops" not in role_name:
            queryset = queryset.filter(applicant=applicant)
        return queryset

    def partial_update(self, request, *args, **kwargs):
        pk = int(kwargs.get("pk"))
        final_processor = self.request.user
        data = request.data
        data['final_processor'] = final_processor
        # 获取处理时间
        data['complete_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        WorkOrder.objects.filter(pk=pk).update(**data)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
