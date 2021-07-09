from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from repo.models import Product, Commodity, SaleRecord, Shop, ShopRecord
from repo.serializers import ProductSerializer, ProductSimpleSerializer, CommoditySerializer, SaleRecordSerializer
from repo.filters import ProductFilter, CommodityFilter, SaleRecordFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

import time 
import logging
import json


log = logging.getLogger(__name__)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend )
    ordering_fields = ('id', 'order_no')

    def get_serializer_class(self):
        params = self.request.query_params.dict()
        if params.get('simple') == "yes":
            return ProductSimpleSerializer
        return ProductSerializer

    @action(detail=True, methods=['put'])
    def partial_change(self, request, pk):
        data = request.data
        data.pop('id')
        patch_object = self.get_object()
        serializer = self.get_serializer(patch_object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=400)

    @action(detail=True, methods=['put'])
    def add_sale(self, request, pk):
        data = request.data
        saled_num = data.get('saled_num')
        product_object = self.get_object()
        t = time.time()
        for item in product_object.included_shops:
            shop = Shop.objects.get(shop_no=item.get('no'))
            change_num = saled_num * item.get('num')
            shop.shop_num -= saled_num * item.get('num')
            shop.save()
            sr_object = ShopRecord.objects.create(shop_no=shop.shop_no, shop_name=shop.shop_name, date=data.get('saled_date'),
                                                  change_num=change_num, option='Sale', remark=data.get('remark'),
                                                  sign=round(t*1000000))
        return Response(status=200)
           


class CommodityViewSet(ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    filterset_class = CommodityFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend )
    ordering_fields = ('id', 'order_no')
    
    @action(detail=True, methods=['put'])
    def partial_change(self, request, pk):
        data = request.data
        data.pop('id')
        patch_object = self.get_object()
        serializer = self.get_serializer(patch_object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=400)

    @action(detail=True, methods=['put'])
    def add_sale(self, request, pk):
        data = request.data
        sale_object = self.get_object()
        saled_products = data['saled_products']
        for product in saled_products:
            #减去货品库存
            product_object = Product.objects.get(product_no=product['no'])
            saled_num = product.get('num')
            saled_shops = []
            # 创建时间戳关联记录
            t = time.time()

            for item in product_object.included_shops:
                shop = Shop.objects.get(shop_no=item.get('no'))
                shop.shop_num -= saled_num * item.get('num')
                saled_shops.append({
                  "no": shop.shop_no,
                  "num": item.get('num')
                })
                shop.save()
                # 创建货品售出记录
#                ShopRecord.objects.create(shop_no=shop.shop_no, shop_name=shop.shop_name,
#                                          change_num = item.get('num'), option='Sale',
#                                          remark = data.get('remark'),
#                                          sign=round(t*1000000))
            # 商品销售记录
            SaleRecord.objects.create(commodity_no=sale_object.commodity_no,
                                      commodity_name=sale_object.commodity_name,
                                      product_no=product['no'],
                                      product_name=product_object.product_name,
                                      saled_num=product['num'],
                                      saled_shops=saled_shops,
                                      remark=data.get('remark'),
                                      sign=round(t*1000000))

        return Response(status=201)


class SaleRecordViewSet(ModelViewSet):
    queryset = SaleRecord.objects.all()
    serializer_class = SaleRecordSerializer
    filterset_class = SaleRecordFilter
    ordering_fields = ('created_time',)

    def destroy(self, request, pk):
        delete_object = self.get_object()
        saled_shops = delete_object.saled_shops
        for item in saled_shops:
            shop = Shop.objects.get(shop_no=item.get('no'))
            shop.shop_num += delete_object.saled_num * item.get('num')
            shop.save()
        sign = delete_object.sign
#        ShopRecord.objects.filter(sign=sign).delete()
        delete_object.delete()
        return Response(status=204)


