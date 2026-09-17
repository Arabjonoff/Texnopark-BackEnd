from rest_framework.routers import DefaultRouter

from .views import PostViewSet

router = DefaultRouter()
router.register('news', PostViewSet, basename='news')

urlpatterns = router.urls
