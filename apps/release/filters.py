#encoding:utf-8
import django_filters
from .models import Deploy

class ReleaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    detail = django_filters.CharFilter(field_name="detail", lookup_expr="icontains")

    class Meta:
        model = Deploy
        fields = ["name", "detail"]