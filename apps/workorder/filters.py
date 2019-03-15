import django_filters
from .models import WorkOrder


class WorkorderFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    order_contents = django_filters.CharFilter(field_name="order_contents", lookup_expr="icontains")

    class Meta:
        model = WorkOrder
        fields = ["title", "order_contents"]