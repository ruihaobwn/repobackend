from repo.models import RepoIn, SendOut, Product, ProductRecord
from common.serializers import BaseSerializer
from rest_framework import serializers
from repo.serializers import ShopSerializer

class RepoInSerializer(BaseSerializer):
    shop = serializers.CharField(source='shop.shop_name')
    shop_no = serializers.CharField(source='shop.shop_no')
    creator_name = serializers.CharField(source='creator.first_name')

    class Meta:
        model = RepoIn
        fields = ['id', 'shop_no', 'shop', 'shop_num', 'in_time', 'is_custom', 'creator_name']


class SendOutSerializer(BaseSerializer):
    class Meta:
        model = SendOut
        fields = ["id", "name", "date", "take", "status", "backup"]


                                                                                                                                                                                                                                                          
class ProductSerializer(BaseSerializer):
    class Meta:
        model = Product
        fields = ('id', 'product_no', 'product_name', 'product_num', "date", "remark")


class ProductNameSerializer(BaseSerializer):
    class Meta:
        model = Product
        fields = ("id", "product_no", "product_name")


class ProductRecordSerializer(BaseSerializer):
    class Meta:
        model = ProductRecord
        fields = ("id", "change_num", "date", "option", "remark")
