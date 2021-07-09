from django_filters import rest_framework as filters

from repo.models import Shop, ShopRecord


class ShopFilter(filters.FilterSet):
    shop_name = filters.CharFilter(lookup_expr='icontains')
    shop_no= filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Shop
        fields = ['shop_no', 'shop_name']


class ShopRecordFilter(filters.FilterSet):
    shop_name = filters.CharFilter(lookup_expr='icontains')
    shop_no= filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ShopRecord
        fields = ['shop_name', 'shop_no', 'option']
