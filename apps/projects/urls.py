from rest_framework.routers import DefaultRouter

from .views import VideoStoryViewSet

router = DefaultRouter()
router.register('video-stories', VideoStoryViewSet, basename='video-story')

urlpatterns = router.urls
