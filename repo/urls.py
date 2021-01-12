from rest_framework import routers
from repo.views.ShopViewSet import ShopViewSet
from repo.views.RepoViewSet import RepoInViewSet, SendOutViewSet
from repo.views.OrderViewSet import OrderViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'shop', ShopViewSet)
router.register(r'repoin', RepoInViewSet)
router.register(r'sendout', SendOutViewSet)
router.register(r'order', OrderViewSet)
urlpatterns = router.urls

