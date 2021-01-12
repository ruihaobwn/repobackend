from repo.models import RepoIn, SendOut
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


