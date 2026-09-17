from rest_framework import serializers

from apps.core.formatting import format_uz_date

from .models import Post


class PostListSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='slug', read_only=True)
    date = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'excerpt', 'cover', 'date', 'published_at')

    def get_date(self, obj) -> str:
        return format_uz_date(obj.published_at.date())


class PostDetailSerializer(PostListSerializer):
    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ('content',)
