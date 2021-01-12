from repo.models import ShopOrder
from common.serializers import BaseSerializer
from rest_framework import serializers


class ShopOrderSerializer(BaseSerializer):
    class Meta:
        model = ShopOrder
        fields = ["id", "order_date", "name", "num", 'in_num', 'bring', 'status', "material", "remark"]

