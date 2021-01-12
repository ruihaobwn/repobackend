from django.db import models
from common.models import BaseModel
from repo.models import Shop
from django.contrib.auth.models import User
from datetime import date
import jsonfield


class RepoIn(BaseModel):
    shop = models.ForeignKey(Shop, verbose_name='产品', on_delete=models.CASCADE)
    shop_num = models.IntegerField(verbose_name=u'商品数量', default=0)
    creator = models.ForeignKey(User, verbose_name=u'创建者', on_delete=models.CASCADE)
    is_custom = models.BooleanField(default=False, verbose_name=u'是否定制')
    in_time = models.DateField( default=date.today, verbose_name=u'入库时间')

    class Meta:
        verbose_name = '入库'
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.shop.name


class SendOut(BaseModel):
    STATUS = (
        ("Done", "已结清"),
        ("Process", "未结清")
    )
    name = models.CharField(max_length=30, verbose_name='领取人')
    date = models.DateField(default=date.today,verbose_name='领取时间')

   # {
   #   "shop_no":{
   #     "shop_name":"控笔画线",
   #     "out_num":300,
   #     "in_num":200
   #   }
   # }

    # 领走与未归还的产品
    take = jsonfield.JSONField()
    status = models.CharField(max_length=10, choices=STATUS, default='Process')
    # 归还的产品

   #{
   #    "shop":{
   #        "no":"",
   #        "name":"",
   #        "num":""
   #    },
   #    "backup":"",
   #    "date":""
   #}
    bring = jsonfield.JSONField(null=True, blank=True)
    backup = models.TextField(verbose_name='备注', default="", blank=True)
    class Meta:
        verbose_name = "领取商品"
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.id

