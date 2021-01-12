from django_filters import rest_framework as filters

from repo.models import Shop


class ShopFilter(filters.FilterSet):
    shop_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Shop
        fields = ['shop_no', 'shop_name']

