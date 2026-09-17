from rest_framework import serializers

from apps.core.formatting import format_time_range, format_uz_date

from .models import Event, ScheduleItem


class ScheduleItemSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format='%H:%M')

    class Meta:
        model = ScheduleItem
        fields = ('time', 'activity')


class EventListSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='slug', read_only=True)
    # Frontendga tayyor matn ("12 Oktabr, 2026"); saralash uchun ISO sana alohida beriladi
    date = serializers.SerializerMethodField()
    date_iso = serializers.DateField(source='date', read_only=True)
    time = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            'id', 'title', 'category', 'date', 'date_iso', 'time', 'location',
            'short_desc', 'theme', 'seats', 'status',
        )

    def get_date(self, obj) -> str:
        return format_uz_date(obj.date)

    def get_time(self, obj) -> str:
        return format_time_range(obj.start_time, obj.end_time)


class EventDetailSerializer(EventListSerializer):
    schedule = ScheduleItemSerializer(many=True, read_only=True)

    class Meta(EventListSerializer.Meta):
        fields = EventListSerializer.Meta.fields + (
            'description', 'prizes', 'schedule', 'requirements', 'organizer',
        )
