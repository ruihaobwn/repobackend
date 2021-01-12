from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from repo.models import Shop
from repo.serializers.ShopSerializer import ShopSerializer, ShopNameSerializer
import logging
from .. import filters


log = logging.getLogger(__name__)


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    filterset_class = filters.ShopFilter

    def get_serializer_class(self):
        params = self.request.query_params.dict()
        if params.get('simple') == "yes":
            return ShopNameSerializer
        return ShopSerializer

#    def list(self, request, *args, **kwargs):
#      queryset = self.filter_queryset(self.get_queryset())
#      serializer = self.get_serializer(queryset, many=True)
#      data = serializer.data
#      return Response({
#          "data": data, 
#          "total": len(data),
#          "success": True,
#          "pageSize": 100,
#          "current": 1
#        })
