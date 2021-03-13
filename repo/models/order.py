from django.db import models
from common.models import BaseModel
from datetime import date
import jsonfield


class ShopOrder(BaseModel):
    STATUS = (
      ("Done", "已结清"),
      ("Process", "未结清")
    )
    order_date = models.DateField(default=date.today, verbose_name='预定日期')
    name = models.CharField(max_length=80, verbose_name='配件名称')
    num = models.IntegerField(verbose_name=u'预定数量', default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='Process')
    material = models.CharField(max_length=100, verbose_name='材料')
   # {
   #   "date": "2020-02-01",
   #   "in_num": 100
   # }
    bring = jsonfield.JSONField(null=True, blank=True)
    in_num = models.IntegerField(verbose_name=u'归还数量', default=0)
    remark = models.TextField(verbose_name='备注', default="", blank=True)

    class Meta:
        verbose_name = '配件预定'
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.name


