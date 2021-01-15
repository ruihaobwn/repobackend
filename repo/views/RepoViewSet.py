from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from repo.models import RepoIn, SendOut, ProductRecord, Product
from repo.serializers import RepoInSerializer, SendOutSerializer, ProductSerializer, ProductNameSerializer
from repo.filters import RepoInFilter, SendOutFilter, ProductFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

import logging
import json


log = logging.getLogger(__name__)


class RepoInViewSet(ModelViewSet):
    queryset = RepoIn.objects.all()
    serializer_class = RepoInSerializer
    filterset_class = RepoInFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response({
            "data": data, 
            "total": len(data),
            "success": True,
            "page": 1
        })


# 工人领走商品
class SendOutViewSet(ModelViewSet):
    queryset = SendOut.objects.all()
    serializer_class = SendOutSerializer
    filterset_class = SendOutFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('date', 'id')

    @action(detail=True, methods=['put'])
    def bring_back(self, request, pk=None):
        #data {
        #    "shop": [{
        #        "no": 912,
        #        "name": "控笔训练",
        #        "in_num": 1
        #    }],
        #    "data": "2020-12-06",
        #    "backup": "无"
        #   }
        data = request.data
        bring_object = self.get_object()
  
        shop_dict = {item['no']: item['in_num'] for item in data.get('shop')}
        flag = 1
        for each in bring_object.take.get('shop'):
            if shop_dict.get(each['no']):
                if shop_dict.get(each['no']) > each['out_num'] - each['in_num']:
                    return Response(status=400, data={"message": "归还的数量不能大于未归还的数量"})
                each['in_num'] = each['in_num'] + shop_dict.get(each['no'])
            if each['in_num'] != each['out_num']:
                flag = 0
        if flag == 1:
           bring_object.status = "Done"
  
        # 记录归还信息 
        if (isinstance(bring_object.bring, dict) and bring_object.bring.get('comebacks')):
            bring_object.bring['comebacks'].append(data)
        else:
            bring_object.bring = {
              "comebacks": [data]
            }
        products = data.get('product')
        pr_ids = []
        if products:
          for each in products:
            p_object = Product.objects.get(product_no=each.get('product_no'))
            p_object.product_num = p_object.product_num + each.get('change_num')
            p_object.save()
            pr_object = ProductRecord.objects.create(product_no=p_object.product_no, product_name=p_object.product_name, change_num=each.get('change_num'), option='Package',entity=bring_object)
            pr_ids.append(pr_object.id)
        if pr_ids:
            bring_object.bring['pr_isd'] = pr_ids

        bring_object.save()
        return Response()
    
    @action(detail=True, methods=['get'])
    def get_comebacks(self, request, pk=None):
        bring_object = self.get_object()
        comeback = bring_object.bring
        return Response(comeback)
    
#    def list(self, request, *args, **kwargs):
#        queryset = self.filter_queryset(self.get_queryset())
#        serializer = self.get_serializer(queryset, many=True)
#        data = serializer.data
#        return Response({
#          "data": data,
#          "total":len(data),
#          "success": True,
#          "page": 1
#        })


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filterset_class = ProductFilter

    def get_serializer_class(self):
        params = self.request.query_params.dict()
        if params.get('simple') == "yes":
            return ProductNameSerializer
        return ProductSerializer

