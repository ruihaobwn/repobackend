from repo.models import Shop, ShopOrder, SendOutShop
from django.db.models import Sum

def sum_shop(shop_object):
    total_out = SendOutShop.objects.filter(shop=shop_object, option='Bring', send__status='Process').aggregate(Sum('out_num'))
    total_in = SendOutShop.objects.filter(shop=shop_object, option='Bring', send__status='Process').aggregate(Sum('in_num'))
    total_out_sum = total_out['out_num__sum'] if total_out['out_num__sum'] else 0
    total_in_sum = total_in['in_num__sum'] if total_in['in_num__sum'] else 0
    send_num = total_out_sum - total_in_sum

    total_order = ShopOrder.objects.filter(shop=shop_object, status='Process').aggregate(Sum('num'))
    total_back = ShopOrder.objects.filter(shop=shop_object, status='Process').aggregate(Sum('in_num'))
    total_order_sum = total_order['num__sum'] if total_order['num__sum'] else 0
    total_back_sum = total_back['in_num__sum'] if total_back['in_num__sum'] else 0
    order_num = total_order_sum - total_back_sum
    shop_object.total_num = shop_object.shop_num + send_num + order_num
    shop_object.save()
    return
