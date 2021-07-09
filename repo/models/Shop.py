from django.db import models
from common.models import BaseModel
from datetime import date
from django.utils import timezone

class Shop(BaseModel):
    shop_no = models.CharField(verbose_name=u'货物编号', unique=True, max_length=80)
    shop_name = models.CharField(verbose_name=u'货物名称', unique=True,  max_length=80)
    shop_num = models.IntegerField(verbose_name=u'货物数量', default=0)
    remark = models.TextField(verbose_name='备注', default="", blank=True)
    order_no = models.IntegerField(verbose_name="排列顺序", default=100)

    class Meta:
        verbose_name = '货物'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.shop_name
 
 
class ShopRecord(BaseModel):
    OPTIONS = (
        ("Sale", "卖出"),
        ("Inrepo", "直接入库")
    )
    shop_no = models.CharField(verbose_name=u'货品编号', max_length=80)
    shop_name = models.CharField(verbose_name=u'货品名称', max_length=80)
    change_num = models.IntegerField(verbose_name=u'变化数量')
    option = models.CharField(max_length=10, choices=OPTIONS, default="Inrepo")
    date = models.DateTimeField(default=timezone.now, verbose_name="日期")
    remark = models.TextField(verbose_name='备注', null=True, blank=True)   
    sign = models.CharField(verbose_name='时间戳标识', max_length=30, null=True)
