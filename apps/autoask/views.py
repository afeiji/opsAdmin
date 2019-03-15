#encoding:utf-8
from rest_framework import viewsets, response, status
from .models import Tasks
from .serializers import AutoaskSerializer
from utils.ansible_api_simple import ANSRunner
import time
import json

class AutoaskViewset(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = AutoaskSerializer

    def create(self, request, *args, **kwargs):
        print("request.data: ", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        """
        执行任务
        """
        pk = int(kwargs.get("pk"))
        data = request.data
        task = Tasks.objects.get(pk=pk)
        rbt = ANSRunner()
        rbt.run_playbook(task.playbook.path)
        data['detail_result'] = json.dumps(rbt.get_playbook_result(), indent=4)
        data['exec_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        Tasks.objects.filter(pk=pk).update(**data)
        return response.Response(status=status.HTTP_204_NO_CONTENT)