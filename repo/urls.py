from rest_framework import routers
from repo.views.ShopViewSet import ShopViewSet, ShopRecordViewSet
from repo.views.RepoViewSet import SendOutViewSet, SendRecordViewSet
from repo.views.OrderViewSet import OrderViewSet, OrderRecordViewSet
from repo.views.SaleViewSet import ProductViewSet, CommodityViewSet, SaleRecordViewSet
from django.urls import path, include


router = routers.SimpleRouter(trailing_slash=False)
#router = routers.DefaultRouter()

router.register(r'shop', ShopViewSet)
router.register(r'product', ProductViewSet)
router.register(r'commodity', CommodityViewSet)
router.register(r'sendout', SendOutViewSet)
router.register(r'salerecord', SaleRecordViewSet)
router.register(r'sendrecord', SendRecordViewSet)
router.register(r'order', OrderViewSet)
router.register(r'orderrecord', OrderRecordViewSet)
router.register(r'shoprecord', ShopRecordViewSet)
urlpatterns = router.urls
