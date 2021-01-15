from django_filters import rest_framework as filters

from repo.models import RepoIn, SendOut, Product


class RepoInFilter(filters.FilterSet):

    class Meta:                                                                                   
        model = RepoIn
        fields = ['shop_num']


class SendOutFilter(filters.FilterSet):
    
    class Meta:
        model = SendOut
        fields = ['name', 'status']




class ProductFilter(filters.FilterSet):
    product_name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['product_no', 'product_name']


