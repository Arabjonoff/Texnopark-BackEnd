from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.text import slugify
from rest_framework import serializers

from apps.applications.models import Application
from apps.content.models import Equipment, Feature, Partner, SiteSettings, Statistic
from apps.courses.models import Course, CurriculumItem
from apps.events.models import Event, ScheduleItem
from apps.news.models import Post
from apps.projects.models import VideoStory


# --- Umumiy yordamchilar ---------------------------------------------------------------

def unique_slug(model, source, instance=None, max_length=100):
    """Nomdan takrorlanmas slug: "Python & AI" -> "python-ai", band bo'lsa "python-ai-2"."""
    base = slugify(source)[:max_length].strip('-') or 'item'
    slug, n = base, 2
    queryset = model.objects.all()
    if instance is not None and instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    while queryset.filter(slug=slug).exists():
        suffix = f'-{n}'
        slug = f'{base[:max_length - len(suffix)]}{suffix}'
        n += 1
    return slug


class AutoSlugMixin:
    """slug bo'sh yuborilsa sarlavhadan avtomatik yaratiladi."""

    slug_source = 'title'

    def validate(self, attrs):
        attrs = super().validate(attrs)
        slug = attrs.get('slug')
        if slug:
            taken = self.Meta.model.objects.filter(slug=slug)
            if self.instance is not None:
                taken = taken.exclude(pk=self.instance.pk)
            if taken.exists():
                raise serializers.ValidationError({'slug': 'Bu slug band. Boshqasini yozing yoki bo\'sh qoldiring.'})
        elif self.instance is None or 'slug' in attrs:
            source = attrs.get(self.slug_source) or getattr(self.instance, self.slug_source, '')
            attrs['slug'] = unique_slug(self.Meta.model, source, self.instance)
        return attrs


class ImageClearMixin:
    """Multipart formada `<maydon>Clear=true` yuborilsa rasm olib tashlanadi."""

    image_fields = ()

    def to_internal_value(self, data):
        clear = {
            name for name in self.image_fields
            if str(data.get(f'{name}_clear', '')).lower() in ('1', 'true', 'on')
        }
        attrs = super().to_internal_value(data)
        for name in clear:
            attrs[name] = ''
        return attrs


class StringListField(serializers.ListField):
    child = serializers.CharField(max_length=300, allow_blank=False, trim_whitespace=True)


# --- Kurslar va tadbirlar -------------------------------------------------------------

class CurriculumItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumItem
        fields = ('week', 'topic')


class CourseSerializer(AutoSlugMixin, serializers.ModelSerializer):
    slug = serializers.SlugField(max_length=100, required=False, allow_blank=True)
    skills = StringListField(required=False)
    outcomes = StringListField(required=False)
    curriculum = CurriculumItemSerializer(many=True, required=False)
    applications_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Course
        fields = (
            'id', 'slug', 'title', 'short_desc', 'description', 'icon', 'theme', 'duration', 'level',
            'format', 'price', 'seats', 'skills', 'outcomes', 'curriculum', 'order', 'is_published',
            'applications_count', 'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')

    @transaction.atomic
    def create(self, validated_data):
        curriculum = validated_data.pop('curriculum', [])
        course = super().create(validated_data)
        self._save_curriculum(course, curriculum)
        return course

    @transaction.atomic
    def update(self, instance, validated_data):
        curriculum = validated_data.pop('curriculum', None)
        course = super().update(instance, validated_data)
        if curriculum is not None:
            self._save_curriculum(course, curriculum)
        return course

    @staticmethod
    def _save_curriculum(course, rows):
        course.curriculum.all().delete()
        CurriculumItem.objects.bulk_create(
            CurriculumItem(course=course, order=i, **row) for i, row in enumerate(rows)
        )


class ScheduleItemSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M', '%H:%M:%S'])

    class Meta:
        model = ScheduleItem
        fields = ('time', 'activity')


class EventSerializer(AutoSlugMixin, serializers.ModelSerializer):
    slug = serializers.SlugField(max_length=150, required=False, allow_blank=True)
    start_time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M', '%H:%M:%S'])
    end_time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M', '%H:%M:%S'], required=False, allow_null=True)
    prizes = StringListField(required=False)
    requirements = StringListField(required=False)
    schedule = ScheduleItemSerializer(many=True, required=False)
    applications_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Event
        fields = (
            'id', 'slug', 'title', 'category', 'date', 'start_time', 'end_time', 'location', 'short_desc',
            'description', 'theme', 'prizes', 'requirements', 'schedule', 'organizer', 'seats', 'status',
            'order', 'is_published', 'applications_count', 'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, attrs):
        attrs = super().validate(attrs)
        start = attrs.get('start_time', getattr(self.instance, 'start_time', None))
        end = attrs.get('end_time', getattr(self.instance, 'end_time', None))
        if start and end and end <= start:
            raise serializers.ValidationError({'end_time': "Tugash vaqti boshlanish vaqtidan keyin bo'lishi kerak."})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        schedule = validated_data.pop('schedule', [])
        event = super().create(validated_data)
        self._save_schedule(event, schedule)
        return event

    @transaction.atomic
    def update(self, instance, validated_data):
        schedule = validated_data.pop('schedule', None)
        event = super().update(instance, validated_data)
        if schedule is not None:
            self._save_schedule(event, schedule)
        return event

    @staticmethod
    def _save_schedule(event, rows):
        event.schedule.all().delete()
        ScheduleItem.objects.bulk_create(ScheduleItem(event=event, **row) for row in rows)


# --- Yangiliklar va sayt kontenti -----------------------------------------------------

class PostSerializer(AutoSlugMixin, ImageClearMixin, serializers.ModelSerializer):
    image_fields = ('cover',)
    slug = serializers.SlugField(max_length=150, required=False, allow_blank=True)

    class Meta:
        model = Post
        fields = (
            'id', 'slug', 'title', 'category', 'excerpt', 'content', 'cover', 'is_published',
            'published_at', 'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ('id', 'value', 'suffix', 'label', 'order', 'is_published')


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'title', 'description', 'icon', 'theme', 'order', 'is_published')


class EquipmentSerializer(ImageClearMixin, serializers.ModelSerializer):
    image_fields = ('image',)

    class Meta:
        model = Equipment
        fields = ('id', 'title', 'description', 'icon', 'theme', 'image', 'order', 'is_published')


class PartnerSerializer(ImageClearMixin, serializers.ModelSerializer):
    image_fields = ('logo',)

    class Meta:
        model = Partner
        fields = ('id', 'name', 'logo', 'url', 'order', 'is_published')


class VideoStorySerializer(ImageClearMixin, serializers.ModelSerializer):
    image_fields = ('thumbnail',)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False, allow_null=True)
    course_title = serializers.CharField(source='course_label', read_only=True)

    class Meta:
        model = VideoStory
        fields = (
            'id', 'student_name', 'course', 'course_name', 'course_title', 'result', 'video_url',
            'thumbnail', 'theme', 'order', 'is_published',
        )

    def to_internal_value(self, data):
        # Multipart formada bo'sh select "" bo'lib keladi — "kurs tanlanmagan" deb qabul qilinadi
        if hasattr(data, 'get') and data.get('course') == '':
            data = data.copy()
            data['course'] = None
        return super().to_internal_value(data)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        course = attrs.get('course', getattr(self.instance, 'course', None))
        course_name = attrs.get('course_name', getattr(self.instance, 'course_name', ''))
        if not course and not course_name:
            raise serializers.ValidationError({'course': 'Kursni tanlang yoki kurs nomini yozing.'})
        return attrs


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = (
            'phone', 'email', 'address', 'working_hours', 'map_url',
            'instagram_url', 'telegram_url', 'facebook_url', 'youtube_url', 'updated_at',
        )
        read_only_fields = ('updated_at',)


# --- Murojaatlar ----------------------------------------------------------------------

class ApplicationSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True, default=None)
    event_title = serializers.CharField(source='event.title', read_only=True, default=None)

    class Meta:
        model = Application
        fields = (
            'id', 'type', 'name', 'phone', 'message', 'course', 'course_title', 'event', 'event_title',
            'status', 'admin_note', 'created_at', 'updated_at',
        )
        # Saytdan kelgan ma'lumot tahrirlanmaydi — faqat holat va izoh
        read_only_fields = (
            'type', 'name', 'phone', 'message', 'course', 'event', 'created_at', 'updated_at',
        )


# --- Auth ------------------------------------------------------------------------------

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(error_messages={'blank': 'Loginni kiriting.', 'required': 'Loginni kiriting.'})
    password = serializers.CharField(
        trim_whitespace=False,
        error_messages={'blank': 'Parolni kiriting.', 'required': 'Parolni kiriting.'},
    )


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'full_name', 'email', 'is_superuser', 'last_login')

    def get_full_name(self, obj) -> str:
        return obj.get_full_name() or obj.username
