#encoding:utf-8

import gitlab
from devops.settings import GITLAB_HTTP_URI, GITLAB_TOKEN

gl = gitlab.Gitlab(GITLAB_HTTP_URI, GITLAB_TOKEN, api_version=4)

def get_user_projects(request):
    """
    获取gitlab里所有的项目，和登陆用户所拥有的项目，以及登陆用户所拥有项目的项目成员]
    """
    user_projects = []
    user_groups = []
    # 获取用户有哪些组
    all_groups = gl.groups.list(all=True)
    for group in all_groups:
        for user_member in group.members.list():
            # 根据登录用户获取gitlab项目，username是前端params传进来的
            if user_member.username == request.user.username:
            # if user_member.username == request.GET.get('username',''):
            # if user_member.username == "ullone":
                for project in group.projects.list(all=True):
                    user_projects.append(project)
                    # user_groups.append(group)
    # print("group: ",user_projects)

    # all=True获取所有的project，默认获取第一页
    all_projects = gl.projects.list(all=True)
    for project in all_projects:
        for member in project.members.list():
            # 根据登录用户获取gitlab项目，username是前端params传进来的
            if member.username == request.user.username:
            # if member.username == request.GET.get('username',''):
            # if member.username == "ullone":
                user_projects.append(project)
    # print(user_projects)
    return user_projects

def get_project_versions(project_id):
    """
    获取某个项目的版本号
    :param project_id:
    :return:
    """
    project = gl.projects.get(project_id)
    tags = project.tags.list()
    return tags