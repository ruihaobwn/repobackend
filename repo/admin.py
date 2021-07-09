from django.contrib import admin
from repo import models


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shop_no', 'shop_name', 'shop_num')


@admin.register(models.SendOut)
class SendOutAdmin(admin.ModelAdmin):
    list_display=('name', 'date')


@admin.register(models.ShopOrder)
class ShopOrderAdmin(admin.ModelAdmin):
    list_display=('order_date', 'material', 'num')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_no', 'product_name', 'product_name')


@admin.register(models.ProductRecord)
class ProductRecordAdmin(admin.ModelAdmin):
    list_display = ('product_no', 'product_name', 'change_num')
