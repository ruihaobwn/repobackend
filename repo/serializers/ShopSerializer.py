from repo.models import Shop, ShopRecord
from common.serializers import BaseSerializer


class ShopSerializer(BaseSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'shop_no', 'shop_name', 'shop_num')


class ShopNameSerializer(BaseSerializer):
    class Meta:
        model = Shop
        fields = ("id", 'shop_no', "shop_name")


class ShopRecordSerializer(BaseSerializer):
    class Meta:
        model = ShopRecord
        fields = ("id", "shop_name", "change_num", "option", "date", "remark")

