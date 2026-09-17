from django.utils import timezone
from rest_framework import viewsets

from .models import Post
from .serializers import PostDetailSerializer, PostListSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """Yangiliklar. Kelajak sanaga qo'yilgan yangilik o'sha vaqtgacha ko'rinmaydi. Filtr: ?category="""

    lookup_field = 'slug'
    filterset_fields = ('category',)
    search_fields = ('title', 'excerpt')

    def get_queryset(self):
        return Post.objects.filter(is_published=True, published_at__lte=timezone.now())

    def get_serializer_class(self):
        return PostDetailSerializer if self.action == 'retrieve' else PostListSerializer
