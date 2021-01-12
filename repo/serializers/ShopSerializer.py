from repo.models import Shop
from common.serializers import BaseSerializer


class ShopSerializer(BaseSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'shop_no', 'shop_name', 'shop_num')


class ShopNameSerializer(BaseSerializer):
    class Meta:
        model = Shop
        fields = ("id", "shop_no", "shop_name")

