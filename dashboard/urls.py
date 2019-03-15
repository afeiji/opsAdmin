#encoding:utf-8

from django.conf.urls import url
from .views import index,loginview
from . import views

# urlpatterns = [
#     url(r'^$', index, name="index"),
#     url(r'login/$', loginview, name="login"),
#     url(r'articles/(?P<year>[0-9]{4})/$', views.articles, name="articles"),
#     url(r'articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.articles, name="articles"),
#     url(r'articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.articles, name="articles"),
# ]

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^user/$', views.user, name="user"),
    url(r'^LoginView2/$', views.LoginView2.as_view(), name="LoginView2"),
    url(r'^userview/$', views.UserViewV3.as_view(), name="UserView"),
    url(r'^grouplistview/$', views.GroupListView.as_view(), name="GroupListView"),
    url(r'^GroupNumnersView/$', views.GroupNumnersView.as_view(), name="GroupNumnersView"),
    url(r'^UserNumnersView/$', views.UserNumnersView.as_view(), name="UserNumnersView"),
    url(r'^UserNumbersMangeView/$', views.UserNumbersMangeView.as_view(), name="UserNumbersMangeView"),
    url(r'^UserPermissionView/$', views.UserPermissionView.as_view(), name="UserPermissionView"),
    url(r'^GroupPermissionView/$', views.GroupPermissionView.as_view(), name="GroupPermissionView"),
]