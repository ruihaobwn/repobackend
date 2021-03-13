from django.db import models
from common.models import BaseModel
from datetime import date


class Shop(BaseModel):
    shop_no = models.CharField(verbose_name=u'配件编号', max_length=80)
    shop_name = models.CharField(verbose_name=u'配件名称', max_length=80)
    shop_num = models.IntegerField(verbose_name=u'配件数量', default=0)
    remark = models.TextField(verbose_name='备注', default="", blank=True)
    date = models.DateField(default=date.today, verbose_name="创建日期")
    order_no = models.IntegerField(verbose_name="排列顺序", default=100)

    class Meta:
        verbose_name = '配件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.shop_name
 
 
class ShopRecord(BaseModel):
    OPTIONS = (
        ("Sale", "卖出"),
        ("Order", "订购")
    )
    shop_name = models.CharField(verbose_name=u'配件名称', max_length=80)
    change_num = models.IntegerField(verbose_name=u'变化数量')
    option = models.CharField(max_length=10, choices=OPTIONS, default="Order")
    date = models.DateField(default=date.today, verbose_name='日期')
    remark = models.TextField(verbose_name='备注', null=True, blank=True)   
