from django.contrib import admin
from repo import models


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_no', 'shop_name', 'shop_num')



@admin.register(models.RepoIn)
class RepoInAdmin(admin.ModelAdmin):
    list_display = ('shop', 'creator', 'in_time', 'shop_num')


@admin.register(models.SendOut)
class SendOutAdmin(admin.ModelAdmin):
    list_display=('name', 'date')


@admin.register(models.ShopOrder)
class ShopOrderAdmin(admin.ModelAdmin):
    list_display=('order_date', 'name', 'material', 'num')

