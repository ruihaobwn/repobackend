from django.db import models
from common.models import BaseModel


class Shop(BaseModel):
    shop_no = models.CharField(verbose_name=u'商品编码', max_length=80)
    shop_name = models.CharField(verbose_name=u'商品名称', max_length=80)
    shop_num = models.IntegerField(verbose_name=u'商品数量', default=0)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.shop_name
