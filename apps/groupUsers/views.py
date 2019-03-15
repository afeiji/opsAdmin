#encoding:utf-8
from rest_framework import viewsets,mixins,status
from django.contrib.auth.models import User, Group
from groupUsers.serializers import UserSerializer,GroupSerializer
from rest_framework.response import Response

class GroupUserViewsets(viewsets.GenericViewSet,
                        mixins.DestroyModelMixin):
    serializer_class = UserSerializer

    def get_group_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        return Group.objects.get(**filter_kwargs)

    def get_queryset(self):
        groupObj = self.get_group_object()
        return groupObj.user_set.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        groupobj = Group.objects.get(pk=request.data['gid'])
        userobj = User.objects.get(pk=request.data['uid'])
        groupobj.user_set.add(userobj)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        groupObj = self.get_group_object()
        userobj = User.objects.get(pk=request.data['uid'])
        groupObj.user_set.remove(userobj)
        return Response(status=status.HTTP_204_NO_CONTENT)
