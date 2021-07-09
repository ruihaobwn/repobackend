from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from repo.models import ShopOrder, ShopRecord,Shop, OrderRecord
from repo.serializers import ShopOrderSerializer, OrderRecordSerializer
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

    def create(self, request):
        data = request.data
        shop_no = data.pop('shop_no')
        shop = Shop.objects.get(shop_no=shop_no)
        ShopOrder.objects.create(shop=shop, order_date=data['order_date'], num=data['num'], material=data.get('material'), remark=data.get('remark'))  
        return Response(status=201)

    @action(detail=True, methods=['put'])
    def bring_back(self, request, pk=None):
      #data {
      #    "in_num": 1
      #    "date": "2020-12-06",
      #    "remark": "无"
      #}
      data = request.data
      bring_object = self.get_object()
      bring_object.in_num = bring_object.in_num + data.get('in_num')

      if bring_object.in_num > bring_object.num:
          return Response(status=400, data={"message": "归还的数量不能大于未归还的数量"})
      if bring_object.in_num == bring_object.num:
          bring_object.status = "Done"

      # 记录归还信息 
      OrderRecord.objects.create(order=bring_object, num=data.get('in_num'), date=data.get('date'), remark=data.get('remark'))      
      shop = bring_object.shop
      shop.shop_num = shop.shop_num + data.get('in_num')
      bring_object.save()
      shop.save() 
      return Response()

    @action(detail=True, methods=['get'])
    def get_comebacks(self, request, pk=None):
        bring_object = self.get_object()
        records = bring_object.orderrecord_set.all()
        serializer = OrderRecordSerializer(records, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        delete_object = self.get_object()
        if delete_object.orderrecord_set.count()>0:
            return Response(status=511, data={"message": "已经有归还数据，请先删除归还数据"})
        delete_object.delete()
        
        return Response(status=204)

    def destroy(self, request, *args, **kwargs):
        delete_object = self.get_object()
        if delete_object.bring:
            return Response(status=511, data={"message": "已经有归还数据，不能删除"})
        delete_object.delete()
        
        return Response(status=204)


    @action(detail=True, methods=['put'])
    def change_status(self, request, pk=None):
        data = request.data
        bring_object = self.get_object()
        bring_object.status = data.get('status')
        bring_object.save()
        return Response()


class OrderRecordViewSet(ModelViewSet):
    queryset = OrderRecord.objects.all()
    serializer_class = OrderRecordSerializer

    def destroy(self, request, pk=None):
        delete_object = self.get_object()
        order = delete_object.order
        # 送还数量减少
        order.in_num -= delete_object.num
        shop = order.shop
        # 减少库存数量
        shop.shop_num -= delete_object.num
        order.save()
        shop.save()
        delete_object.delete()
        
        return Response(status=204)
