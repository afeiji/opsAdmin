from .models import Idc
from .serializers import IdcSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse,JsonResponse


##################################### 版本一 ##################################################
class JSONResponse(HttpResponse):   #写这个是为不在每个函数都写content = JSONRenderer().render(serializer.data)
    def __init__(self, data, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        content = JSONRenderer().render(data)
        super(JSONResponse, self).__init__(content=content, **kwargs)

def idc_list(request,*args,**kwargs):
    if request.method == "GET":
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset,many=True)  # 序列化
        # content = JSONRenderer().render(serializer.data)    #别写成serializer，
        # return HttpResponse(content,content_type="application/json")
        return JSONResponse(serializer.data)    #序列化后才会产生serializer.data

    elif request.method == "POST":
        # request.POST.dict() #怎么拿post提交过来的数据
        content = JSONParser().parse(request)   #因为之前使用过BytesIO测试过，知道它的方法有read,readline和request方法类似，所以request也也可以使用JSONParser().parse()序列化
        serializer = IdcSerializer(data=content)    #反序列化
        if serializer.is_valid():
            serializer.save()
            # content = JSONRenderer().render(serializer.data)
            # return HttpResponse(content,content_type="application/json")
            return JSONRenderer(serializer.data)

def idc_detail(request, pk, *args, **kwargs):
    try:
        idc = Idc.objects.get(pk=pk)
    except Idc.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        # 获取指定的idc记录
        serializer = IdcSerializer(idc)
        print(serializer.data)
        return JSONResponse(serializer.data)

    elif request.method == "PUT":
        # 修改一个对象
        content = JSONParser().parse(request)
        serializer = IdcSerializer(idc,data=content) #这个IdcSerializer（），它可以接受两个值，要是接收一个request的值，save后就是新增，要是第一个值时已经查出来的对象，那么会对比第二参数的数据，save就是修改
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)

    elif request.method == "DELETE":
        # 删除这个对象
        idc.delete()
        return HttpResponse(status=206)



##################################### 版本二 ##################################################
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(["GET","POST"])
def idc_list_v2(request,*args,**kwargs):
    if request.method == "GET":
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset,many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        # request.POST.dict() #怎么拿post提交过来的数据
        content = JSONParser().parse(request)   #因为之前使用过BytesIO测试过，知道它的方法有read,readline和request方法类似，所以request也也可以使用JSONParser().parse()序列化
        serializer = IdcSerializer(data=content)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PUT","DELETE"])
def idc_detail_v2(request, pk, *args, **kwargs):
    try:
        idc = Idc.objects.get(pk=pk)
    except Idc.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        # 获取指定的idc记录
        serializer = IdcSerializer(idc)
        return Response(serializer.data)

    elif request.method == "PUT":
        # 修改一个对象
        content = JSONParser().parse(request)
        serializer = IdcSerializer(idc,data=content) #这个IdcSerializer（），它可以接受两个值，要是接收一个request的值，save后就是新增，要是第一个值时已经查出来的对象，那么会对比第二参数的数据，save就是修改
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        # 删除这个对象
        idc.delete()
        return Response(status=status.HTTP_200_OK)

from rest_framework.reverse import reverse

#根路由，要跟随着name="idc_list_v2"走
@api_view(["GET"])
def api_root(request,format=None,*args, **kwargs):
    return Response(
        {"idcs":reverse("idc_list_v2",request=request,format=format)}
    )


##################################### 版本三 ##################################################
from rest_framework.views import APIView
from django.http import Http404

class IdcList(APIView):
    def get(self,request,format=None):
        queryset = Idc.objects.all()
        serializer = IdcSerializer(queryset,many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # content = JSONParser().parse(request)   #因为之前使用过BytesIO测试过，知道它的方法有read,readline和request方法类似，所以request也也可以使用JSONParser().parse()序列化
        # serializer = IdcSerializer(data=content)
        serializer = IdcSerializer(data=request.data)   #content被DRF封装在APIView的request.data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class IdcDetail(APIView):
    def get_object(self, pk):
        try:
            return Idc.objects.get(pk=pk)
        except Idc.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        idc = self.get_object(pk)
        serializer = IdcSerializer(idc)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        idc = self.get_object(pk)
        serializer = IdcSerializer(idc,data=request.data)  # 这个IdcSerializer（），它可以接受两个值，要是接收一个request的值，save后就是新增，要是第一个值时已经查出来的对象，那么会对比第二参数的数据，save就是修改
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        idc = self.get_object(pk)
        idc.delete()
        return Response(status=status.HTTP_200_OK)

##################################### 版本四 ##################################################
from rest_framework import mixins,generics

class IdcList_V4(generics.GenericAPIView,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class IdcDetail_V4(generics.GenericAPIView,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):

    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)


##################################### 版本五 ##################################################
class IdcList_V5(generics.ListCreateAPIView):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

class IdcDetail_V5(generics.RetrieveUpdateDestroyAPIView):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

##################################### 版本六 ##################################################
from rest_framework import viewsets
class IdcViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

##################################### 版本七 ##################################################
class IdcViewSet_V7(viewsets.ModelViewSet):
    """"
    retrieve:
        获取指定IDC记录
    create:
        创建一条IDC记录
    update:
        更新一条IDC记录
    delete:
        删除一条IDC记录
    """
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer



##################################### 用户 ##################################################
from django.contrib.auth.models import User
from .serializers import UserSerializer
class UserListViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

##################################### 用户下面的组 ##################################################
from .serializers import GroupSerializer
class UsersGroupListViewSet(viewsets.GenericViewSet):
    serializer_class = GroupSerializer

    def get_user_object(self):
        lookup_url_kwargs = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwargs in self.kwargs,(
            (self.__class__.__name__,lookup_url_kwargs)
        )
        filter_kwargs = {self.lookup_field:self.kwargs[lookup_url_kwargs]}
        return User.objects.get(**filter_kwargs)

    def get_queryset(self):
        userObj = self.get_user_object()
        return userObj.groups.all()

    def retrieve(self,request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True) # ?
        return response.Response(serializer.data)

    def create(self,request,*args,**kwargs):
        groupObj = Group.objects.get(pk=request.data["gid"])
        userObj = User.objects.get(pk=request.data["uid"])
        userObj.groups.add(groupObj)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self,request,*args,**kwargs):
        userObj = self.get_user_object()
        groupObj = Group.objects.get(pk=request.data["uid"])
        userObj.groups.remove(groupObj)
        return response.Response(status=status.HTTP_204_NO_CONTENT)






##################################### 组 ##################################################
from django.contrib.auth.models import Group
from .serializers import GroupSerializer
class GroupListViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


##################################### 组下面的用户 ##################################################
from django.contrib.auth.models import Group
from .serializers import GroupSerializer
from rest_framework import response
class GroupUserListViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_group_object(self):
        lookup_url_kwargs = self.lookup_url_kwarg or self.lookup_field
        # assert lookup_url_kwargs in self.kwargs,(
        #     (self.__class__.__name__,lookup_url_kwargs)
        # )
        filter_kwargs = {self.lookup_field:self.kwargs[lookup_url_kwargs]}  # lookup_field相当于pk，kwargs[lookup_url_kwargs相当于pk的值
        return Group.objects.get(**filter_kwargs)   # **Group.objects.get的参数

    def get_queryset(self):
        groupObj = self.get_group_object()
        return groupObj.user_set.all()

    def retrieve(self,request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True) # cong
        return response.Response(serializer.data)

    def create(self,request,*args,**kwargs):
        groupObj = Group.objects.get(pk=request.data["gid"])
        userObj = User.objects.get(pk=request.data["uid"])
        print(groupObj,userObj)
        groupObj.user_set.add(userObj)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self,request,*args,**kwargs):
        groupObj = self.get_group_object()
        userObj = User.objects.get(pk=request.data["uid"])
        groupObj.user_set.remove(userObj)
        return response.Response(status=status.HTTP_204_NO_CONTENT)








##################################### 权限 ##################################################
from django.contrib.auth.models import Permission
from .serializers import PermissionSerializer
class PermissionListViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
















