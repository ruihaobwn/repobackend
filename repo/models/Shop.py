from django.db import models
from common.models import BaseModel


class Shop(BaseModel):
    shop_no = models.CharField(verbose_name=u'配件编号', max_length=80)
    shop_name = models.CharField(verbose_name=u'配件名称', max_length=80)
    shop_num = models.IntegerField(verbose_name=u'配件数量', default=0)

    class Meta:
        verbose_name = '配件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.shop_name
