from django_filters import rest_framework as filters

from repo.models import ShopOrder


class OrderFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='shop__shop_name', lookup_expr='icontains')

    class Meta:
        model = ShopOrder
        fields = ['status']
