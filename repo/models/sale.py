from django.db import models
from common.models import BaseModel
from repo.models import Shop
from django.contrib.auth.models import User
from datetime import date
import jsonfield


class Product(BaseModel):
    # 对应淘宝的SKU
    product_no = models.CharField(verbose_name=u'商品规格编码',null=True, max_length=80)
    product_name = models.CharField(verbose_name=u'商品规格', max_length=80)
    included_shops = jsonfield.JSONField()
    remark = models.TextField(verbose_name='备注', default="", blank=True)
    order_no = models.IntegerField(verbose_name="排列顺序", default=100)

    class Meta:
        verbose_name = '淘宝SKU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.product_name 


class Commodity(BaseModel):
    #对应淘宝的商品
    commodity_no = models.CharField(verbose_name=u'商品编码', unique=True, max_length=80)
    commodity_name = models.CharField(verbose_name=u'商品名称', unique=True, max_length=80)
    included_products = jsonfield.JSONField()
    remark = models.TextField(verbose_name='备注', null=True, blank=True)
    order_no = models.IntegerField(verbose_name='排列顺序', default=100)

    class Meta:
        verbose_name = '淘宝商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.commodity_name
    

class SaleRecord(BaseModel):
    # 销售记录
    commodity_no = models.CharField(verbose_name=u'商品编码',  max_length=80)
    commodity_name = models.CharField(verbose_name='商品名称', max_length=80)
    product_no = models.CharField(verbose_name=u'商品规格编码', max_length=80)
    product_name = models.CharField(verbose_name='规格名称', max_length=80)
    saled_num = models.IntegerField(verbose_name='销售数量', default=0)
    remark = models.TextField(verbose_name='备注', null=True)
    # 标记卖出的具体货品数量
    saled_shops = jsonfield.JSONField()
    sign = models.CharField(verbose_name='时间戳标识', max_length=30, null=True)

    class Meta:
        verbose_name = '销售记录'
        verbose_name_plural = verbose_name

