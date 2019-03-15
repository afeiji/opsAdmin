#encoding:utf-8

import django_filters
from django.contrib.auth.models import Group


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Group
        # fields是一个元组
        fields = ("name",)