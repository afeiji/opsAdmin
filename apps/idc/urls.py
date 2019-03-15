from django.conf.urls import url,include
from . import views

################################## 版本一 #################################################
urlpatterns = [
    url(r'^idcs/$',views.idc_list,name="idc_list"),
    url(r'^idcs/(?P<pk>[0-9]+)/$',views.idc_detail,name="idc_detail"),   # 来一个变量为()，?P可以理解url后面的?，pk为关键字，+表示一个或者多个，相当于?pk=2
]



################################## 版本二 #################################################
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    url(r'^$',views.api_root,name="api_root"),
    url(r'^idcs/$',views.idc_list_v2,name="idc_list_v2"),
    url(r'^idcs/(?P<pk>[0-9]+)/$',views.idc_detail_v2,name="idc_detail_v2"),   # 来一个变量为()，?P可以理解url后面的?，pk为关键字，+表示一个或者多个，相当于?pk=2
]
urlpattern = format_suffix_patterns(urlpatterns)  # 作用是支持后缀


################################## 版本三 #################################################
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    url(r'^$',views.api_root,name="api_root"),
    url(r'^idcs/$',views.IdcList.as_view(),name="IdcList"),
    url(r'^idcs/(?P<pk>[0-9]+)/$',views.IdcDetail.as_view(),name="IdcDetail"),   # 来一个变量为()，?P可以理解url后面的?，pk为关键字，+表示一个或者多个，相当于?pk=2
]
urlpattern = format_suffix_patterns(urlpatterns)  # 作用是支持后缀

################################## 版本四 #################################################
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    url(r'^$',views.api_root,name="api_root"),
    url(r'^idcs/$',views.IdcList_V4.as_view(),name="idc_list_v2"),
    url(r'^idcs/(?P<pk>[0-9]+)/$',views.IdcDetail_V4.as_view(),name="idc_detail_v2"),   # 来一个变量为()，?P可以理解url后面的?，pk为关键字，+表示一个或者多个，相当于?pk=2
]
urlpattern = format_suffix_patterns(urlpatterns)  # 作用是支持后缀

################################## 版本五 #################################################
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    url(r'^$',views.api_root,name="api_root"),
    url(r'^idcs/$',views.IdcList_V5.as_view(),name="idc_list_v2"),
    url(r'^idcs/(?P<pk>[0-9]+)/$',views.IdcDetail_V5.as_view(),name="idc_detail_v2"),   # 来一个变量为()，?P可以理解url后面的?，pk为关键字，+表示一个或者多个，相当于?pk=2
]
urlpattern = format_suffix_patterns(urlpatterns)  # 作用是支持后缀

################################## 版本六 #################################################
idc_list = views.IdcViewSet.as_view({
    "get":"list",
    "post":"create",
})

idc_detail = views.IdcViewSet.as_view({
    "get":"retrieve",
    "put":"update",
    "delete":"destroy",
})
urlpatterns = [
    url(r'^$',views.api_root,name="api_root"),
    url(r'^idcs/$',idc_list,name="idc_list_v2"),
    url(r'^idcs/(?P<pk>[0-9]+)/$',idc_detail,name="idc_detail_v2"),   # 来一个变量为()，?P可以理解url后面的?，pk为关键字，+表示一个或者多个，相当于?pk=2
]
urlpattern = format_suffix_patterns(urlpatterns)  # 作用是支持后缀

################################## 版本七 #################################################
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("idcs",views.IdcViewSet_V7)   # 注册
# router.register("users",views.UserListViewSet)   # 用户
# router.register("usersgroup",views.UsersGroupListViewSet,base_name="usersgroup")   # 用户下面的组
# router.register("groups",views.GroupListViewSet)   # 组
# router.register("groupsuser",views.GroupUserListViewSet,base_name="groupsuser")   # 组下面的用户给
# router.register("permission",views.PermissionListViewSet)   # 权限
urlpatterns = [
    url(r'^',include(router.urls))
]

# ################################## 用户 #################################################
# router = DefaultRouter()
# router.register("users",views.UserListViewSet)   # 注册
# urlpatterns = [
#     url(r'^',include(router.urls))
# ]
#
# ################################## 组 #################################################
# router = DefaultRouter()
# router.register("groups",views.GroupListViewSet)   # 注册
# urlpatterns = [
#     url(r'^',include(router.urls))
# ]














