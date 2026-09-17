from rest_framework import viewsets

from .models import Event
from .serializers import EventDetailSerializer, EventListSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """Tadbirlar. Filtr: ?status=open, ?category=Ideathon. Detal: /api/events/andijon-ideathon-2026/"""

    lookup_field = 'slug'
    filterset_fields = ('status', 'category')
    search_fields = ('title', 'short_desc')
    ordering_fields = ('date', 'order')

    def get_queryset(self):
        queryset = Event.objects.filter(is_published=True)
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('schedule')
        return queryset

    def get_serializer_class(self):
        return EventDetailSerializer if self.action == 'retrieve' else EventListSerializer
