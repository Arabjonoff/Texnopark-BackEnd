from django.contrib import admin

from .models import Course, CurriculumItem


class CurriculumItemInline(admin.TabularInline):
    model = CurriculumItem
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'duration', 'price', 'seats', 'order', 'is_published')
    list_editable = ('order', 'is_published')
    list_filter = ('is_published', 'theme')
    search_fields = ('title', 'short_desc')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (CurriculumItemInline,)
