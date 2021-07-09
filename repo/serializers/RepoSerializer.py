from repo.models import SendOut, Product, ProductRecord, SendOutShop, SendRecord
from common.serializers import BaseSerializer
from rest_framework import serializers
from repo.serializers import ShopNameSerializer


class SendOutShopSerializer(BaseSerializer):
    shop_no = serializers.ReadOnlyField(source='shop.shop_no')
    shop_name = serializers.ReadOnlyField(source='shop.shop_name')


    class Meta:
        model = SendOutShop
        fields = ['out_num', 'in_num', 'option', 'shop_no', 'shop_name']


class SendOutSerializer(BaseSerializer):
    sendoutshops= SendOutShopSerializer(source='sendoutshop_set', many=True, read_only=True)

    class Meta:
        model = SendOut
        fields = ["id", "name", "date", "status", "remark", "sendoutshops"]


class SendRecordSerializer(BaseSerializer):
    shop_no = serializers.ReadOnlyField(source='shop.shop_no')
    shop_name = serializers.ReadOnlyField(source='shop.shop_name')

    class Meta:
        model = SendRecord
        fields = ['id', 'shop_no', 'shop_name', 'change_num', 'date', 'remark']

