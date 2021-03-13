from rest_framework import routers
from repo.views.ShopViewSet import ShopViewSet, ShopRecordViewSet
from repo.views.RepoViewSet import RepoInViewSet, SendOutViewSet, ProductViewSet, ProductRecordViewSet
from repo.views.OrderViewSet import OrderViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'shop', ShopViewSet)
router.register(r'product', ProductViewSet)
router.register(r'repoin', RepoInViewSet)
router.register(r'sendout', SendOutViewSet)
router.register(r'order', OrderViewSet)
router.register(r'productrecord', ProductRecordViewSet)
router.register(r'shoprecord', ShopRecordViewSet)
urlpatterns = router.urls

