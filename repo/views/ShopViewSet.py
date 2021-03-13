from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from repo.models import Shop, ShopRecord
from repo.serializers.ShopSerializer import ShopSerializer, ShopNameSerializer, ShopRecordSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
import logging
from .. import filters

log = logging.getLogger(__name__)


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    filterset_class = filters.ShopFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend )
    ordering_fields = ('id', 'order_no')

    def get_serializer_class(self):
        params = self.request.query_params.dict()
        if params.get('simple') == "yes":
            return ShopNameSerializer
        return ShopSerializer

    @action(detail=True, methods=['put'])
    def change(self, request, pk=None):
#       data= {
#          id: 32,
#          date: '2021-03-04',
#          num: 100,
#          option: 'increase',
#          remark: '备注'
#        }

        data = request.data
        shop = self.get_object()
        if data.get('option') == 'increase':
            shop.shop_num = shop.shop_num + data.get('num')
            sr_object = ShopRecord.objects.create(shop_name=shop.shop_name, date=data.get('date'), 
                                                  change_num=data.get('num'), option='Order', remark=data.get('remark'))
        else:
            shop.shop_num = shop.shop_num - data.get('num')
            sr_object = ShopRecord.objects.create(shop_name=shop.shop_name, date=data.get('date'), 
                                                  change_num=data.get('num'), option='Sale', remark=data.get('remark'))
        shop.save()
        return Response()


class ShopRecordViewSet(ModelViewSet):
    queryset = ShopRecord.objects.all()
    serializer_class = ShopRecordSerializer

    @action(detail=False, methods=['get'])
    def record(self, request):
        params = request.query_params
        record_set = ShopRecord.objects.filter(shop_name=params.get("shop_name")).order_by('-date')[:20]
        serializer = ShopRecordSerializer(record_set, many=True)
        return Response(serializer.data)
