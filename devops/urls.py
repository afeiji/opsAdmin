"""devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from django.views.static import serve
from devops.settings import STATIC_ROOT


from rest_framework.routers import DefaultRouter
from groupUsers.views import GroupUserViewsets
from rest_framework.documentation import include_docs_urls  #生成接口文档
from users.router import route as user_router
from groups.router import route as group_router
from books.router import router as books_router
from permissions.router import permission_router
from workorder.router import workorder_router
from autoask.router import router as autoask_router
from release.router import release_router
# from resources.router import route as server_router


router = DefaultRouter()
# router.register("groupUsers",GroupUserViewsets,base_name="groupUsers")
router.registry.extend(user_router.registry)
router.registry.extend(group_router.registry)
router.registry.extend(permission_router.registry)
router.registry.extend(books_router.registry)
router.registry.extend(workorder_router.registry)
router.registry.extend(autoask_router.registry)
router.registry.extend(release_router.registry)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth', include('rest_framework.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^docs/', include_docs_urls("接口文档")),
    url(r'^test/', include('resources.urls')),
    url(r'^project/', include('project.urls')),
    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
]



# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     # url(r'^dashboard/', include('dashboard.urls')),
#     url(r'^', include('idc.urls')),
# ]
