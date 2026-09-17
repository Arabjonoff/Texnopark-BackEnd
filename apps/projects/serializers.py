from rest_framework import serializers

from .models import VideoStory


class VideoStorySerializer(serializers.ModelSerializer):
    course = serializers.CharField(source='course_label', read_only=True)
    course_slug = serializers.SlugRelatedField(source='course', slug_field='slug', read_only=True)

    class Meta:
        model = VideoStory
        fields = ('id', 'student_name', 'course', 'course_slug', 'result', 'video_url', 'thumbnail', 'theme')
