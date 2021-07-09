from django_filters import rest_framework as filters

from repo.models import SendOut


class SendOutFilter(filters.FilterSet):
    shop_name = filters.CharFilter(field_name='sendoutshops__shop_name', lookup_expr='icontains')

    class Meta:
        model = SendOut
        fields = ['name', 'status']


