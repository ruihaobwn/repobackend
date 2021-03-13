from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from repo.models import ShopOrder, ShopRecord,Shop
from repo.serializers import ShopOrderSerializer
from repo.filters import OrderFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

import logging
from .. import filters
import json

log = logging.getLogger(__name__)


class OrderViewSet(ModelViewSet):
    queryset = ShopOrder.objects.all()
    serializer_class = ShopOrderSerializer
    filterset_class = OrderFilter 
    filter_backends = (OrderingFilter, DjangoFilterBackend )
    ordering_fields = ('order_date', 'id')

    @action(detail=True, methods=['put'])
    def bring_back(self, request, pk=None):
#data {
#    "in_num": 1
#    "date": "2020-12-06",
#    "backup": "无"
#   }
      data = request.data
      bring_object = self.get_object()
      bring_object.in_num = bring_object.in_num + data.get('in_num')

      if bring_object.in_num > bring_object.num:
          return Response(status=400, data={"message": "归还的数量不能大于未归还的数量"})
      if bring_object.in_num == bring_object.num:
          bring_object.status = "Done"

      # 记录归还信息 
      if (isinstance(bring_object.bring, dict) and bring_object.bring.get('comebacks')):
          bring_object.bring['comebacks'].append(data)
      else:
          bring_object.bring = {
            "comebacks": [data]
          }
      shop = Shop.objects.get(shop_name=bring_object.name)
      shop.shop_num = shop.shop_num + data.get('in_num')
      bring_object.save()
      shop.save() 
      # 记录到库存history中
      ShopRecord.objects.create(shop_name=shop.shop_name, date=data.get('date'), 
                                change_num=data.get('in_num'), option='Order', remark=data.get('backup'))
      return Response()

    @action(detail=True, methods=['get'])
    def get_comebacks(self, request, pk=None):
        bring_object = self.get_object()
        comeback = bring_object.bring
        return Response(comeback)


    @action(detail=True, methods=['put'])
    def change_status(self, request, pk=None):
        data = request.data
        bring_object = self.get_object()
        bring_object.status = data.get('status')
        bring_object.save()
        return Response()

