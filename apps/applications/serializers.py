import re

from rest_framework import serializers

from apps.courses.models import Course
from apps.events.models import Event

from .models import Application

PHONE_RE = re.compile(r'^\+?[\d\s\-()]{9,20}$')


class ApplicationSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(
        slug_field='slug', queryset=Course.objects.filter(is_published=True), required=False, allow_null=True,
    )
    event = serializers.SlugRelatedField(
        slug_field='slug', queryset=Event.objects.filter(is_published=True), required=False, allow_null=True,
    )

    class Meta:
        model = Application
        fields = ('id', 'type', 'name', 'phone', 'message', 'course', 'event', 'created_at')
        read_only_fields = ('id', 'created_at')
        extra_kwargs = {
            'name': {'error_messages': {'blank': 'Ismingizni kiriting.', 'required': 'Ismingizni kiriting.'}},
            'phone': {'error_messages': {'blank': 'Telefon raqamni kiriting.', 'required': 'Telefon raqamni kiriting.'}},
        }

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError('Ismingizni to\'liq kiriting.')
        return value

    def validate_phone(self, value):
        value = value.strip()
        if not PHONE_RE.match(value):
            raise serializers.ValidationError("Telefon raqam noto'g'ri. Namuna: +998 90 123 45 67")
        return value

    def validate(self, attrs):
        kind = attrs.get('type', Application.Type.CONTACT)
        if kind == Application.Type.COURSE and not attrs.get('course'):
            raise serializers.ValidationError({'course': 'Kursni tanlang.'})
        if kind == Application.Type.EVENT and not attrs.get('event'):
            raise serializers.ValidationError({'event': 'Tadbirni tanlang.'})
        if kind == Application.Type.EVENT and attrs['event'].status == Event.Status.CLOSED:
            raise serializers.ValidationError({'event': "Bu tadbirga ro'yxatdan o'tish yopilgan."})
        if kind == Application.Type.CONTACT and not attrs.get('message', '').strip():
            raise serializers.ValidationError({'message': 'Xabaringizni yozing.'})
        return attrs
