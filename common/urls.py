from rest_framework import routers
from common.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'user', UserViewSet)
urlpatterns = router.urls
