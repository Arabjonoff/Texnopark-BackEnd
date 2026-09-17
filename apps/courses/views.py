from rest_framework import viewsets

from .models import Course
from .serializers import CourseDetailSerializer, CourseListSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """Kurslar (yo'nalishlar). Detal sahifa slug bo'yicha: /api/courses/flutter/"""

    lookup_field = 'slug'
    search_fields = ('title', 'short_desc')
    ordering_fields = ('order', 'title')

    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True)
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('curriculum')
        return queryset

    def get_serializer_class(self):
        return CourseDetailSerializer if self.action == 'retrieve' else CourseListSerializer
