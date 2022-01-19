from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from repo.models import SendOut, SendRecord, ProductRecord, Product, SendOutShop, Shop
from repo.serializers import SendOutSerializer, SendRecordSerializer
from repo.filters import SendOutFilter, ProductFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

import logging
import json


log = logging.getLogger(__name__)

# 工人领走商品
class SendOutViewSet(ModelViewSet):
    queryset = SendOut.objects.all()
    serializer_class = SendOutSerializer
    filterset_class = SendOutFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('date', 'id')

    def get_queryset(self):
        return super().get_queryset().distinct()

    def create(self, request):
        data = request.data
        take = data.pop('take')
        serializer = SendOutSerializer(data=data)
        if serializer.is_valid():
            sendout = serializer.save()
            for each in take:
                shop = Shop.objects.get(shop_no=each['no'])
                SendOutShop.objects.create(send=sendout, shop=shop, option='Bring', out_num=each['out_num'])  
                # 减少仓库库存
                shop.shop_num -= each['out_num']
                shop.save()
            return Response(status=201)
        else:
            return Response(status=400)



    @action(detail=True, methods=['put'])
    def bring_back(self, request, pk=None):
        data = request.data
        bring_object = self.get_object()
        for each in data.get('shop'):
            shop = Shop.objects.get(shop_no=each['no'])
            try:
                sendoutshop = SendOutShop.objects.get(send=bring_object, shop=shop)
                sendoutshop.in_num += each['in_num']
                sendoutshop.save()
            except SendOutShop.DoesNotExist:
                SendOutShop.objects.create(send=bring_object, shop=shop, option='Back', in_num=each['in_num']) 
            remark = data.get('remark')
            #归还记录
            SendRecord.objects.create(send=bring_object, shop=shop, date=data.get('date'), change_num=each.get('in_num'), remark=data.get('remark'))
            #增加货品库存 文件袋、剪刀、板擦归还不增加库存
            if shop.shop_no in ['001', '700A', '700B', '123', '425A', '425B', '425c', '425D', '425F']:
                pass
            else:
                shop.shop_num += each.get('in_num')
            shop.save()
        return Response()

    def destroy(self, request, *args, **kwargs):
        delete_object = self.get_object()
        if SendRecord.objects.filter(send=delete_object).count() > 0:
            return Response(status=511, data={"message": "归还不为空，不能删除"})
        for sendoutshop in SendOutShop.objects.filter(send=delete_object):
            shop = sendoutshop.shop
            shop.shop_num += sendoutshop.out_num
            shop.save()
            sendoutshop.delete()
        delete_object.delete()

        return Response(status=204, data={'message': '删除成功'})
    
    @action(detail=True, methods=['get'])
    def get_comebacks(self, request, pk=None):
        bring_object = self.get_object()
        sendrecord = SendRecord.objects.filter(send=bring_object)
        serializer = SendRecordSerializer(sendrecord, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def change_status(self, request, pk=None):
        data = request.data
        bring_object = self.get_object()
        bring_object.status = data.get('status')
        bring_object.save()
        return Response()


class SendRecordViewSet(ModelViewSet):
    queryset = SendRecord.objects.all()
    serializer_class = SendRecordSerializer

    def destroy(self, request, pk=None):
        delete_object = self.get_object()
        # 送还数量减少
        send = delete_object.send
        shop = delete_object.shop
        try:
            sendoutshop = SendOutShop.objects.get(send=send, shop=shop)
            # 含有领走货品
            if sendoutshop.option == 'Bring':
                sendoutshop.in_num -= delete_object.change_num
                sendoutshop.save()
            # 不含有领走货品
            else:
                sendoutshop.delete()
        except SendOutShop.DoesNotExist:
            pass
        # 减少库存数量 文件袋、剪刀、板擦归还不影响库存
        if shop.shop_no in ['001', '700A', '700B', '123', '425A', '425B', '425c', '425D', '425F']:
            pass
        else:
            shop.shop_num -= delete_object.change_num
        shop.save()
        delete_object.delete()
        
        return Response(status=204)   


