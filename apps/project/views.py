#encoding:utf-8

from django.views.generic import View
from django.http import HttpResponse
from utils.gitlab_api import get_user_projects, get_project_versions
import json
from rest_framework import permissions, viewsets

# class ProjectListView(View):
class ProjectListView(viewsets.ViewSet):

    permission_classes = (permissions.IsAuthenticated,)
    """
    登陆用户所有项目
    """

    def list(self,request, *args, **kwargs):
    # def get(self, request):
        my_projects = get_user_projects(request)
        project_num = len(my_projects)
        json_list = []
        json_res = {}
        for project in my_projects:
            json_dict = {}
            json_dict['id'] = project.id
            json_dict['name'] = project.name
            json_dict['path_with_namespace'] = project.path_with_namespace
            json_dict['web_url'] = project.web_url
            json_dict['description'] = project.description
            json_list.append(json_dict)
        json_res['result'] = json_list
        json_res['count'] = project_num
        return HttpResponse(json.dumps(json_res), content_type="application/json")


# class ProjectVersionView(View):
class ProjectVersionView(viewsets.ViewSet):

    permission_classes = (permissions.IsAuthenticated,)
    """
    获取指定的项目所有版本
    """
    def list(self,request, *args, **kwargs):
    # def get(self,request):
        project_id = request.GET.get('project_id')
        tag_list = []
        tags = get_project_versions(int(project_id))
        for tag in tags:
            tag_dict = {}
            tag_dict['name'] = tag.name
            tag_dict['info'] = tag.attributes['commit']['message']
            tag_list.append(tag_dict)
        return HttpResponse(json.dumps(tag_list),content_type='application/json')

