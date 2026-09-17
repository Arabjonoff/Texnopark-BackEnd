from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'is_published')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'excerpt', 'content')
    date_hierarchy = 'published_at'
    prepopulated_fields = {'slug': ('title',)}
