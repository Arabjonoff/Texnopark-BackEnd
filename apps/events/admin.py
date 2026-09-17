from django.contrib import admin

from .models import Event, ScheduleItem


class ScheduleItemInline(admin.TabularInline):
    model = ScheduleItem
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'status', 'seats', 'is_published')
    list_editable = ('status', 'is_published')
    list_filter = ('status', 'category', 'is_published')
    search_fields = ('title', 'short_desc')
    date_hierarchy = 'date'
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ScheduleItemInline,)
