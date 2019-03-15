#encoding:utf-8

import django_filters

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        fields = ["username"]