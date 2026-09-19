from django.contrib import admin

from .models import Equipment, Feature, Partner, SiteSettings, Statistic, TeamMember


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Logotip', {'fields': ('logo',)}),
        ('Aloqa', {'fields': ('phone', 'email', 'address', 'working_hours', 'map_url')}),
        ('Ijtimoiy tarmoqlar', {'fields': ('instagram_url', 'telegram_url', 'facebook_url', 'youtube_url')}),
        ('Bosh sahifa kartasi', {'fields': ('hero_image', 'hero_video_url')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class OrderedAdmin(admin.ModelAdmin):
    list_editable = ('order', 'is_published')
    list_filter = ('is_published',)


@admin.register(Statistic)
class StatisticAdmin(OrderedAdmin):
    list_display = ('label', 'value', 'suffix', 'order', 'is_published')


@admin.register(Feature)
class FeatureAdmin(OrderedAdmin):
    list_display = ('title', 'icon', 'theme', 'order', 'is_published')
    search_fields = ('title',)


@admin.register(Equipment)
class EquipmentAdmin(OrderedAdmin):
    list_display = ('title', 'icon', 'theme', 'order', 'is_published')
    search_fields = ('title',)


@admin.register(TeamMember)
class TeamMemberAdmin(OrderedAdmin):
    list_display = ('name', 'role', 'order', 'is_published')
    search_fields = ('name', 'role')


@admin.register(Partner)
class PartnerAdmin(OrderedAdmin):
    list_display = ('name', 'url', 'order', 'is_published')
    search_fields = ('name',)
