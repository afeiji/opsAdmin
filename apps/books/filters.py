#encoding:utf-8

import django_filters
from .models import Publish, Book


class PublishFilter(django_filters.FilterSet):
    # username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Publish
        fields = ["name","city"]

class BookFilter(django_filters.FilterSet):
# class BookFilter(django_filters.rest_framework.FilterSet):
    # 模糊匹配
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    publisher = django_filters.CharFilter(field_name="publisher__name", lookup_expr="icontains")
    authors = django_filters.CharFilter(field_name="authors__name", lookup_expr="icontains")

    class Meta:
        model = Book
        fields = ["name","authors", "publisher"]