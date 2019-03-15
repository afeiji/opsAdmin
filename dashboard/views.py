from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,QueryDict
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.db.utils import IntegrityError

import json




def index(request):
    # print(request.GET)
    # # print(dir(request))
    if request.method == "GET":
        print(request.GET)
        print(request.GET.get('aa'))
        print(request.GET.getlist('cc'))
    elif request.method == "POST":
        print(request.POST)
        # print(request.GET.POST('aa'))
        # print(request.GET.POST('cc'))
    # elif request.method == "DELETE":
    #     delete = QueryDict(request.body)
    #     print(dir(request.body))
    #     print(delete.get('name'))
    # # data = ["a", "b", "c"]
    # # data = {"a":1,"b":2}
    # # return JsonResponse("")
    return HttpResponse('hello world')

# def login(request):
#     if request.method == "GET":
#         name = request.GET.get("name")
#         password = request.GET.get("password")
#         if name == "root" and password == "root":
#             print("登陆成功")
#         else:
#             print("登陆失败")
#
#     elif request.method == "POST":
#         name = request.POST.get("name")
#         password = request.POST.get("password")
#         print(name,password)
#         if name == "root" and password == "root":
#             msg = "登陆成功"
#         else:
#             msg = "登陆失败"
#
#     else:
#         msg = "请求错误"
#     return HttpResponse(msg)

def loginview(request):
    print(request.method)
    if request.method == "POST":
        username = request.POST.get("username")
        userpass = request.POST.get("userpass")
        print(username,userpass)
        user = authenticate(request,username=username,password=userpass)
        if user is not None:
            login(request,user)
            return HttpResponse("用户登录成功")
        else:
            return HttpResponse("用户登录失败")
    return render(request,'login.html')

# 位置参数
# def articles(request, *args,**kwarg):
#     return HttpResponse(json.dumps(args))

# 关键字参数
def articles(request, *args,**kwarg):
    return HttpResponse(json.dumps(kwarg))


#############################################################################
from django.views import View
class IndexView(View):
    def get(self,request,*args,**kwargs):
        return HttpResponse("hello index")


# 函数视图
def user(request,*args,**kwargs):
    if request.method == "GET":
        return HttpResponse("视图函数获取用户信息")

    if request.method == "POST":
        return HttpResponse("视图函数用户信息提交")

    if request.method == "PUT":
        return HttpResponse("视图函数增加用户信息")

    if request.method == "DELETE":
        return HttpResponse("视图函数删除用户信息")

# 类视图
from django.contrib.auth.models import User

class UserView(View):
    def get(self,request,*args,**kwargs):
        per = 10
        try:
            page = int(request.GET.get("page"))
        except:
            page = 1
        if page < 1:
            page = 1
        end = page * per
        start = end - per
        queryset = User.objects.all()[start:end]
        data = [{"id":user.id,"email":user.email,"username":user.username } for user in queryset]
        return JsonResponse(data,safe=False)
        # return HttpResponse("获取用户信息")


from django.core.paginator import Paginator
class UserViewV2(View):
    def post(self,request,*args,**kwargs):
        queryset = User.objects.all()
        paginator = Paginator(queryset,10)
        try:
            page = int(request.GET.get("page"))
        except:
            page = 1
        if page < 1:
            page = 1
        page = paginator.page(page)
        data = [{"id": user.id, "email": user.email, "username": user.username} for user in page]
        print(paginator)
        return JsonResponse(data,safe=False)

# class UserViewV3(View):
#     def post(self, request, *args, **kwargs):
#         # print(request.method)
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         user = User.objects.create_user(username, email, password)
#         data= {"id":user.id,"email":user.email,"username":user.username}
#         return JsonResponse(data,safe=False)
#         # return HttpResponse("用户创建成功")

    # def post(self,requset,*args,**kwargs):
    #     return HttpResponse("用户信息提交")
    #
    # def put(self,request,*args,**kwargs):
    #     return HttpResponse("增加用户信息")
    #
    # def delete(self,request,*args,**kwargs):
    #     return HttpResponse("删除用户信息")

import logging

logger = logging.getLogger("reboot")
class UserViewV3(View):
    def post(self, request, *args, **kwargs):
        logger.debug("创建用户")
        data = request.POST.dict()
        try:
            user = User.objects.create_user(**data)
        except IntegrityError:
            return JsonResponse({"errmsg":"用户已存在"})
        return JsonResponse(data)



from django.views.generic import TemplateView
class LoginView2(TemplateView):
    template_name = "dashboard/login.html"

    def get_context_data(self, **kwargs):
        kwargs['title'] = "reboot"
        return kwargs

    def post(self, *args, **kwargs):
        return HttpResponse("用户信息提交")

from django.contrib.auth.models import User,Group
from django.core import serializers
class GroupListView(View):

    def get(self, request,*args, **kwargs):
        queryset = Group.objects.all()
        return HttpResponse(serializers.serialize("json",queryset),content_type="application/json")


from django.http import Http404
class GroupNumnersView(View):

    def get_queryset(self):
        groupobj = self.group_obj()
        return groupobj.user_set.all()

    def group_obj(self):
        try:
            group_obj = Group.objects.get(name=self.request.GET.get("groupname"))
        except Group.DoesNotExist:
            raise Http404
        return group_obj

    def get(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        return HttpResponse(serializers.serialize("json",queryset),content_type="application/json")


class UserNumnersView(View):

    def get_queryset(self):
        userobj = self.user_obj()
        userobj.groups.all()
        return userobj.groups.all()

    def user_obj(self):
        try:
            user_obj = User.objects.get(username =self.request.GET.get("username"))
        except User.DoesNotExist:
            raise Http404
        return user_obj

    def get(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        return HttpResponse(serializers.serialize("json",queryset),content_type="application/json")

class UserNumbersMangeView(View):

    def user_obj(self):
        try:
            print(self.request.body,type(self.request.body),QueryDict(self.request.body))
            user_obj = User.objects.get(username =QueryDict(self.request.body).get("username"))
        except User.DoesNotExist:
            raise Http404
        return user_obj

    def group_obj(self):
        try:
            group_obj = Group.objects.get(name=QueryDict(self.request.body).get("groupname"))
        except Group.DoesNotExist:
            raise Http404
        return group_obj

    def delete(self, request, *args, **kwargs):
        """将用户从用户组中删除"""
        userobj = self.user_obj()
        groupobj = self.group_obj()
        userobj.groups.remove(groupobj)
        return HttpResponse("")

    def put(self, request, *args, **kwargs):
        """将用户添加到指定的用户组中"""
        userobj = self.user_obj()
        groupobj = self.group_obj()
        userobj.groups.add(groupobj)
        return HttpResponse("")


"""
作业：
    get：获取指定用户的所有权限列表
        参数：用户名
    get：获取指定组的所有权限列表
        参数：组名
"""
class UserPermissionView(View):

    def get_queryset(self):
        getqueryset =self.user_obj()
        return getqueryset.user_permissions.all()

    def user_obj(self):
        userobj = User.objects.get(username = self.request.GET.get("username"))
        return userobj

    def get(self, request, *args,**kwargs):
        queryset = self.get_queryset()
        return HttpResponse(serializers.serialize("json",queryset),content_type="application/json")

class GroupPermissionView(View):

    def get_queryset(self):
        getqueryset =self.group_obj()
        return getqueryset.permissions.all()

    def group_obj(self):
        groupobj = Group.objects.get(name = self.request.GET.get("groupname"))
        return groupobj

    def get(self, request, *args,**kwargs):
        queryset = self.get_queryset()
        return HttpResponse(serializers.serialize("json",queryset),content_type="application/json")

