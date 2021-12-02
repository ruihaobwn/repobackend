from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from repo.models import Shop, ShopRecord, SendOutShop, ShopOrder
from repo.serializers.ShopSerializer import ShopSerializer, ShopNameSerializer, ShopRecordSerializer
from rest_framework.filters import OrderingFilter 
from django_filters.rest_framework import DjangoFilterBackend
import logging
from .. import filters
from repo.util import sum_shop


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


    @action(detail=True, methods=['get'])
    def detail_num(self, request, pk=None):
        shop_object = self.get_object()
        detail_num = {}
        detail_num['stock_num'] = shop_object.shop_num
        total_out = SendOutShop.objects.filter(shop=shop_object, option='Bring', send__status='Process').aggregate(Sum('out_num'))
        total_in = SendOutShop.objects.filter(shop=shop_object, option='Bring', send__status='Process').aggregate(Sum('in_num'))
        total_out_sum = total_out['out_num__sum'] if total_out['out_num__sum'] else 0
        total_in_sum = total_in['in_num__sum'] if total_in['in_num__sum'] else 0
        detail_num['send_num'] = total_out_sum - total_in_sum

        total_order = ShopOrder.objects.filter(shop=shop_object, status='Process').aggregate(Sum('num'))
        total_back = ShopOrder.objects.filter(shop=shop_object, status='Process').aggregate(Sum('in_num'))
        total_order_sum = total_order['num__sum'] if total_order['num__sum'] else 0
        total_back_sum = total_back['in_num__sum'] if total_back['in_num__sum'] else 0
        detail_num['order_num'] = total_order_sum - total_back_sum
        return Response(detail_num)


# 直接入库和售出
    @action(detail=True, methods=['put'])
    def change_num(self, request, pk=None):
#       data= {
#          id: 32,
#          date: '2021-03-04 17:05',
#          num: 100,
#          option: 'increase',
#          remark: '备注'
#        }

        data = request.data
        shop = self.get_object()
        if data.get('option') == 'increase':
            shop.shop_num = shop.shop_num + data.get('num')
            sr_object = ShopRecord.objects.create(shop_no=shop.shop_no, shop_name=shop.shop_name, date=data.get('date'), 
                                                  change_num=data.get('num'), option='Inrepo', remark=data.get('remark'),
                                                  creator=request.user.last_name)
        else:
            shop.shop_num = shop.shop_num - data.get('num')
            sr_object = ShopRecord.objects.create(shop_no=shop.shop_no, shop_name=shop.shop_name, date=data.get('date'), 
                                                  change_num=data.get('num'), option='Sale', remark=data.get('remark'),
                                                  creator=request.user.last_name)
        shop.save()
        sum_shop(shop)
        return Response()

# 设置预警阀值
    @action(detail=True, methods=['put'])
    def set_threshold(self, request, pk=None):
        data = request.data
        shop = self.get_object()
        if data.get('threshold'):
            shop.threshold = data.get('threshold')
        shop.remark = data.get('remark', '')
        shop.save()
        return Response()


class ShopRecordViewSet(ModelViewSet):
    queryset = ShopRecord.objects.all()
    serializer_class = ShopRecordSerializer
    filterset_class = filters.ShopRecordFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend )
    ordering_fields = ('created_time',)

    def destroy(self, request, pk):
        delete_object = self.get_object()
        shop = Shop.objects.get(shop_no=delete_object.shop_no)
        if delete_object.option == 'Sale':
            shop.shop_num += delete_object.change_num
        else:
            shop.shop_num -= delete_object.change_num
        shop.save()
        sum_shop(shop)
        delete_object.delete()
        return Response(status=204)

