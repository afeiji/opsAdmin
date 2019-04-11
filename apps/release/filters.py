#encoding:utf-8
import django_filters
from .models import Deploy
from django.db.models import Q

class ReleaseFilter(django_filters.rest_framework.FilterSet):
    # name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    # applicant = django_filters.CharFilter(field_name="applicant", lookup_expr="icontains")
    name = django_filters.CharFilter(method="search_name")


    def search_name(self, queryset, name, value):
        return  queryset.filter(Q(name__icontains=value)|Q(applicant__username__icontains=value))

    class Meta:
        model = Deploy
        fields = ["name",]