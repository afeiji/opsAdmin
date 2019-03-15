from django.conf.urls import url
from idc import views


############################# 版本一 #####################
urlpatterns = [
    # url(r'^$', views.idc_list, name="idc_list"),
    url(r'idcs$', views.idc_list, name="idc_list"),
    url(r'^([0-9])/$', views.idc_detail, name="idc_detail"),
]

urlpatterns = [
    # url(r'^$', views.idc_list, name="idc_list"),
    url(r'idcs$', views.idc_list_v2, name="idc_list"),
    url(r'^([0-9])/$', views.idc_detail_v2, name="idc_detail"),
]

############################# 版本二 #####################
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    # url(r'^$', views.idc_list, name="idc_list"),
    url(r'^$', views.IdcList.as_view(), name="idc_list"),
    url(r'^([0-9])/$', views.IdcDetail.as_view(), name="idc_detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)


############################# 版本四 #####################
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    # url(r'^$', views.idc_list, name="idc_list"),
    url(r'^$', views.IdcList_V4.as_view(), name="idc_list"),
    # url(r'^([0-9])/$', views.IdcDetail_v4.as_view(), name="idc_detail"),
    url(r'^(?P<pk>[0-9]+)/$', views.IdcDetail_v4.as_view(), name="idc_detail"),
]
urlpatterns = format_suffix_patterns(urlpatterns)