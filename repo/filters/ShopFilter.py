from django_filters import rest_framework as filters
from django.db.models import F
from repo.models import Shop, ShopRecord


class ShopFilter(filters.FilterSet):
    shop_name = filters.CharFilter(lookup_expr='icontains')
    shop_no= filters.CharFilter(lookup_expr='icontains')
    lte_total = filters.NumberFilter(field_name='total_num', method='total_lt_threshold')

    def total_lt_threshold(self, queryset, name, value):
        queryset = Shop.objects.filter(total_num__lte=F('threshold'))
        return queryset

    class Meta:
        model = Shop
        fields = ['shop_no', 'shop_name', 'lte_total']


class ShopRecordFilter(filters.FilterSet):
    shop_name = filters.CharFilter(lookup_expr='icontains')
    shop_no= filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ShopRecord
        fields = ['shop_name', 'shop_no', 'option']
