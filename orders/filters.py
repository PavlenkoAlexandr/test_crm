import django_filters
from orders.models import Order


class OrderFilter(django_filters.FilterSet):

    status = django_filters.MultipleChoiceFilter(choices=Order.STATUS)
    order_type = django_filters.ChoiceFilter(choices=Order.ORDER_TYPES)
    created_date = django_filters.DateFilter(field_name='created_date', lookup_expr='icontains')
    created_date__gt = django_filters.DateFilter(field_name='created_date', lookup_expr='gt')
    created_date__lt = django_filters.DateFilter(field_name='created_date', lookup_expr='lt')

    class Meta:
        model = Order
        fields = ['status', 'order_type', 'created_date']
