#encoding:utf-8

from rest_framework import viewsets, response, status, mixins, permissions
from .models import Deploy
from .serializers import ReleaseSerializer, CountProjectSerializer, CountUserSerializer
from .filters import ReleaseFilter
from utils.jenkins_api import JenkinsApi
from .tasks import code_release, send_email
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.db.models import Count
User = get_user_model()
from django.http import JsonResponse

import time

class ReleaseViewset(viewsets.ModelViewSet):
    queryset = Deploy.objects.all()
    serializer_class = ReleaseSerializer
    filter_class = ReleaseFilter
    filter_fields = ("name", "detail")


    def get_queryset(self):
        status = self.request.GET.get('status', None)
        applicant = self.request.user
        # 获取当前用户的所有组的信息,组名， RBAC 用户-->组-->权限
        role = applicant.groups.all().values('name')
        # 列表推倒式[]，[]就是append，把组名添加到一个列表
        role_name = [r['name'] for r in role]
        queryset = super(ReleaseViewset, self).get_queryset()

        if status and int(status) <= 2:
            queryset = Deploy.objects.filter(status__lte=(2))
        elif status and int(status) > 2:
            queryset = Deploy.objects.filter(status__gt=(2))
        else:
            queryset = Deploy.objects.all()

        if "运维组" not in role_name:
            queryset = queryset.filter(applicant=applicant)
        return queryset

    def create(self, request, *args, **kwargs):
        email_list = []
        email_title = request.data['name'] + '上线申请'
        email_content = request.data['detail'] + '\n 点击访问：http://devops.169kang.com/release/list'
        assign_to_id = request.data['assign_to']
        assign_to_email = User.objects.get(pk=assign_to_id).email
        email_list.append(assign_to_email)

        if request.data.get('reviewer', ''):
            reviewer_id = request.data['reviewer']
            reviewer_email = User.objects.get(pk=reviewer_id).email
            email_list.append(reviewer_email)
        # 使用异步发送邮件
        send_email.delay(email_title, email_content, email_list)
        # send_mail(email_title, email_content, 'service@notice.169kang.com', email_list,
        #           fail_silently=False)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def partial_update(self, request, *args, **kwargs):
    #     pk = int(kwargs.get("pk"))
    #     assign_to = self.request.user
    #     data = request.data
    #     data['assign_to'] = assign_to
    #     # 获取处理时间
    #     data['deploy_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #     Deploy.objects.filter(pk=pk).update(**data)
    #     return response.Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        data = request.data
        data['assign_to'] = request.user
        # 获取处理时间
        data['deploy_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # Deploy.objects.filter(pk=pk).update(**data)
        if int(data['status']) == 3:
            # 使用异步进行jenking构建
            code_release.delay(pk, data)
            # jenkins = JenkinsApi()
            # number = jenkins.get_next_build_number(data['name'])
            # # Tag是自己在jenkins命名的tag变量名
            # jenkins.build_job(data['name'], parameters={'Tag': data['version']})
            # time.sleep(20)
            # console_output = jenkins.get_build_console_output(data['name'], number)
            # data['console_output'] = console_output
        Deploy.objects.filter(pk=pk).update(**data)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class CountChartsViewsetV2(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    NowMonth = time.strftime("%Y-%m", time.localtime())
    def list(self, request, *args, **kwargs):
        valuemonth = request.GET.get('valuemonth',None)
        if valuemonth:
            queryset = Deploy.objects.filter(status__exact=3, deploy_time__startswith=valuemonth).values_list(
                "name").annotate(Count('name')).order_by('-name__count')
        else:
            queryset = Deploy.objects.filter(status__exact=3, deploy_time__startswith=self.NowMonth).values_list("name").annotate(Count('name')).order_by('-name__count')

        queryset = {
            "columns": ['项目名', '上线次数'],
            "rows": [{'项目名': i[0], '上线次数': i[1]} for i in queryset]
        }
        return JsonResponse(queryset)


class CountUserCViewsetV2(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    NowMonth = time.strftime("%Y-%m", time.localtime())

    def list(self, request, *args, **kwargs):
        projectuser_list = []
        valuemonth = request.GET.get('valuemonth', None)
        if valuemonth:
            _x = Deploy.objects.filter(status__exact=3, deploy_time__startswith=valuemonth)
        else:
            _x = Deploy.objects.filter(status__exact=3, deploy_time__startswith=self.NowMonth)
        for project in _x:
            projectuser_list.append(project.applicant.username)
        projectuser_set = set(projectuser_list)
        queryset = {
            "columns": ['上线人', '上线次数'],
            "rows": [{'上线人': i, '上线次数': projectuser_list.count(i)} for i in projectuser_set]
        }
        # print("_x", _x)
        # queryset = Deploy.objects.filter(status__exact=3, deploy_time__startswith=self.NowMonth).values_list("applicant_id").annotate(Count('applicant_id')).order_by('-applicant_id__count')
        #
        # queryset = {
        #     "columns": ['上线人', '上线次数'],
        #     "rows": [{'上线人': i[0], '上线次数': i[1]} for i in queryset]
        # }
        return JsonResponse(queryset)