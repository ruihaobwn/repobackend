from django_filters import rest_framework as filters

from repo.models import ShopOrder


class OrderFilter(filters.FilterSet):
    
    class Meta:
        model = ShopOrder
        fields = ['status']
