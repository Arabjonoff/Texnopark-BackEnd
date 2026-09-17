from rest_framework import serializers

from .models import Course, CurriculumItem


class CurriculumItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumItem
        fields = ('week', 'topic')


class CourseListSerializer(serializers.ModelSerializer):
    # Frontend `id` sifatida slug'dan foydalanadi (/courses/flutter)
    id = serializers.CharField(source='slug', read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'short_desc', 'icon', 'theme', 'duration', 'level', 'price', 'seats')


class CourseDetailSerializer(CourseListSerializer):
    curriculum = CurriculumItemSerializer(many=True, read_only=True)

    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + (
            'description', 'format', 'skills', 'curriculum', 'outcomes',
        )
