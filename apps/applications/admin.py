from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'type', 'course', 'event', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'type', 'course', 'event')
    search_fields = ('name', 'phone', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('type', 'name', 'phone', 'message', 'course', 'event', 'created_at')
    fields = readonly_fields + ('status', 'admin_note')

    def has_add_permission(self, request):
        return False
