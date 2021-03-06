from repo.models import Shop, ShopRecord
from common.serializers import BaseSerializer
from rest_framework import serializers


class ShopSerializer(BaseSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'shop_no','updated_time','shop_name', 'shop_num', 'total_num','remark', 'threshold')


class ShopNameSerializer(BaseSerializer):
    class Meta:
        model = Shop
        fields = ("id", 'shop_no', "shop_name")


class ShopRecordSerializer(BaseSerializer):

    class Meta:
        model = ShopRecord
        fields = ("id", 'shop_no', 'creator', "shop_name", "change_num", "option", "date", 'sign', "remark")

