from repo.models import ShopOrder,OrderRecord
from common.serializers import BaseSerializer
from rest_framework import serializers


class ShopOrderSerializer(BaseSerializer):
    name = serializers.ReadOnlyField(source='shop.shop_name')
    class Meta:
        model = ShopOrder
        fields = ["id", "order_date", "num", 'name', 'in_num', 'status', "material", "remark"]


class OrderRecordSerializer(BaseSerializer):
    class Meta:
        model = OrderRecord 
        fields = ["id", "num", "date", "remark"]

