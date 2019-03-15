#encoding:utf-8

from rest_framework.routers import DefaultRouter
from groups.views import GroupViewsets, UserGroupsViewset, GroupMembersViewset

route = DefaultRouter()
route.register('groups',GroupViewsets,base_name="groups")
route.register('userGroups',UserGroupsViewset,base_name="userGroups")
route.register('groupMenbers',GroupMembersViewset,base_name="groupMenbers")


# group_router = DefaultRouter()
# group_router.register('groups',GroupViewsets,base_name="groups")
# group_router.register('userGroups',UserGroupsViewset,base_name="userGroups")
# group_router.register('groupMenbers',GroupMembersViewset,base_name="groupMenbers")


