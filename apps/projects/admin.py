from django.contrib import admin

from .models import VideoStory


@admin.register(VideoStory)
class VideoStoryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'course', 'course_name', 'result', 'order', 'is_published')
    list_editable = ('order', 'is_published')
    list_filter = ('is_published', 'course')
    search_fields = ('student_name', 'result')
    autocomplete_fields = ('course',)
