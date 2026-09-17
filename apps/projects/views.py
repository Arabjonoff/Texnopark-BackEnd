from apps.content.views import PublishedListViewSet

from .models import VideoStory
from .serializers import VideoStorySerializer


class VideoStoryViewSet(PublishedListViewSet):
    model = VideoStory
    serializer_class = VideoStorySerializer

    def get_queryset(self):
        return super().get_queryset().select_related('course')
