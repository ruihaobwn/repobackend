from repo.models import Product, Commodity, SaleRecord, Shop
from common.serializers import BaseSerializer
from rest_framework import serializers


class ProductSerializer(BaseSerializer):
    shop_list = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'product_no', 'product_name', 'included_shops', 'shop_list', 'created_time', 'remark')

    def get_shop_list(self, obj):
        shops = []
        for item in obj.included_shops:
            shop = Shop.objects.get(shop_no=item.get('no'))
            shops.append({
                'no': shop.shop_no,
                'name': shop.shop_name,
                'num': item.get('num')
            })
        return shops


class ProductSimpleSerializer(BaseSerializer):
    class Meta:
        model = Product
        fields = ('id', 'product_no', 'product_name')


class CommoditySerializer(BaseSerializer):
    product_list = serializers.SerializerMethodField()

    class Meta:
        model = Commodity
        fields = ('id', 'commodity_no', 'commodity_name', 'included_products', 'product_list', 'created_time', 'remark')

    def get_product_list(self, obj):
        products = []
        for item in obj.included_products:
            product = Product.objects.get(product_no=item.get('no'))
            products.append({
                'no': product.product_no,
                'name': product.product_name,
                'num': item.get('num')
            })
        return products


class SaleRecordSerializer(BaseSerializer):
    shop_list = serializers.SerializerMethodField()

    class Meta:
        model = SaleRecord
        fields = ('id', 'commodity_no', 'commodity_name', 'product_no', 'product_name', 'shop_list', 'created_time', 'saled_num', 'sign', 'remark')


    def get_shop_list(self, obj):
        shops = []
        for item in obj.saled_shops:
            shop = Shop.objects.get(shop_no=item.get('no'))
            shops.append({
                'no': shop.shop_no,
                'name': shop.shop_name,
                'num': item.get('num')
            })
        return shops
