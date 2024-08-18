"""
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'oauth', UserViewSet.as_view(), basename='user')
urlpatterns = router.urls

"""