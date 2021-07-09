from django_filters import rest_framework as filters

from repo.models import Product, Commodity, SaleRecord


class ProductFilter(filters.FilterSet):                                                                                        
    product_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['product_no', 'product_name']


class CommodityFilter(filters.FilterSet):
    commodity_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Commodity
        fields = ['commodity_name']


class SaleRecordFilter(filters.FilterSet):
    class Meta:
        model = SaleRecord
        fields = ['commodity_no', 'product_no', 'product_name', 'commodity_name']

