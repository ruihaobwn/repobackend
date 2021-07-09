from django.db import models
from common.models import BaseModel
from datetime import date
from django.utils import timezone
from repo.models import Shop
import jsonfield


class ShopOrder(BaseModel):
    STATUS = (
      ("Done", "已结清"),
      ("Process", "未结清")
    )
    order_date = models.DateTimeField(default=timezone.now, verbose_name='预定日期')
    shop =models.ForeignKey('Shop', on_delete=models.CASCADE, null=True)
    num = models.IntegerField(verbose_name=u'预定数量', default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='Process')
    material = models.CharField(max_length=100, verbose_name='材料', null=True)
    in_num = models.IntegerField(verbose_name=u'已归还数量', default=0)
    remark = models.TextField(verbose_name='备注', null=True, blank=True)

    class Meta:
        verbose_name = '配件预定'
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.shop__name


class OrderRecord(BaseModel):
    order = models.ForeignKey('ShopOrder', on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name='送回数量')
    date = models.DateTimeField(default=timezone.now, verbose_name='送回时间')
    remark = models.TextField(verbose_name='备注', null=True) 


