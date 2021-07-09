from django.db import models
from common.models import BaseModel
from repo.models import Shop
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
import jsonfield


class SendOut(BaseModel):
    STATUS = (
        ("Done", "已结清"),
        ("Process", "未结清")
    )
    name = models.CharField(max_length=30, verbose_name='领取人')
    date = models.DateTimeField(default=timezone.now,verbose_name='领取时间')
    status = models.CharField(max_length=10, choices=STATUS, default='Process')
    remark = models.TextField(verbose_name='备注', null=True, blank=True)
    sendoutshops = models.ManyToManyField(Shop, through='SendOutShop')

    class Meta:
        verbose_name = "领取商品"
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.id


# 外包任务具体领走的商品数量
class SendOutShop(BaseModel):
    OPTIONS = (
        ("Bring", "拿走"),
        ("Back", "归还")
    )
    send = models.ForeignKey('SendOut', on_delete=models.CASCADE)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    out_num = models.IntegerField(verbose_name='领取数量', default=0)
    in_num = models.IntegerField(verbose_name='归还数量', default=0)
    option = models.CharField(max_length=10, choices=OPTIONS, default='Bring')


# 每个外包任务送回记录
class SendRecord(BaseModel):
    send = models.ForeignKey('SendOut', on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, null=True)
    change_num = models.IntegerField(default=0,verbose_name='归还数量')
    date = models.DateField(default=date.today, verbose_name='归还日期')
    remark = models.TextField(verbose_name='备注', null=True)


class ProductRecord(BaseModel):
    OPTIONS = (
        ("Sale", "卖出"),
        ("Pakage", "装货"),
        ("Inrepo", "入库")
    )
    product_no = models.CharField(verbose_name=u'商品编码',max_length=80)
    product_name = models.CharField(verbose_name=u'商品名称', max_length=80)
    change_num = models.IntegerField(verbose_name=u'变化数量')
    option = models.CharField(max_length=10, choices=OPTIONS, default="Pakage")
    date = models.DateField(default=date.today, verbose_name='日期')
    # 配件合成成品
    entity = models.ForeignKey(SendOut, verbose_name='配送', on_delete=models.CASCADE, null=True, blank=True)
    remark = models.TextField(verbose_name='备注', null=True, blank=True)

