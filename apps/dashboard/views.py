from datetime import timedelta

from django.contrib.auth import authenticate
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.applications.models import Application
from apps.content.models import Equipment, Feature, Partner, SiteSettings, Statistic, TeamMember
from apps.courses.models import Course
from apps.events.models import Event
from apps.news.models import Post
from apps.projects.models import VideoStory

from . import serializers as s
from .authentication import ExpiringTokenAuthentication, token_expires_at


class DashboardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class DashboardMixin:
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAdminUser,)


class DashboardViewSet(DashboardMixin, viewsets.ModelViewSet):
    pagination_class = DashboardPagination


# --- Auth ------------------------------------------------------------------------------

@extend_schema(
    request=s.LoginSerializer,
    responses={200: s.LoginResponseSerializer, 400: OpenApiResponse(description="Login yoki parol noto'g'ri")},
)
class LoginView(APIView):
    """Login/parol -> token. Faqat staff (is_staff) foydalanuvchilar kira oladi."""

    authentication_classes = ()
    permission_classes = (AllowAny,)
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'login'

    def post(self, request):
        serializer = s.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.validated_data)
        if user is None or not user.is_staff:
            return Response(
                {'non_field_errors': ["Login yoki parol noto'g'ri."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Har kirishda yangi token — eski sessiyalar bekor bo'ladi
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return Response({
            'token': token.key,
            'expires_at': token_expires_at(token),
            'user': s.UserSerializer(user).data,
        })


@extend_schema(request=None, responses={204: OpenApiResponse(description="Token o'chirildi")})
class LogoutView(DashboardMixin, APIView):
    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(responses=s.UserSerializer)
class MeView(DashboardMixin, APIView):
    def get(self, request):
        return Response(s.UserSerializer(request.user).data)


# --- Bosh sahifa statistikasi -----------------------------------------------------------

@extend_schema(responses={200: OpenApiResponse(description='Dashboard statistikasi (arizalar, kurslar, tadbirlar, yangiliklar)')})
class StatsView(DashboardMixin, APIView):
    DAYS = 30

    def get(self, request):
        now = timezone.localtime()
        today = now.date()
        start = today - timedelta(days=self.DAYS - 1)

        daily = dict(
            Application.objects.filter(created_at__date__gte=start)
            .annotate(day=TruncDate('created_at'))
            .values_list('day')
            .annotate(count=Count('id'))
        )
        series = [
            {'date': day, 'count': daily.get(day, 0)}
            for day in (start + timedelta(days=i) for i in range(self.DAYS))
        ]
        last_period = sum(point['count'] for point in series)
        previous_period = Application.objects.filter(
            created_at__date__gte=start - timedelta(days=self.DAYS),
            created_at__date__lt=start,
        ).count()

        applications = Application.objects.all()
        return Response({
            'applications': {
                'total': applications.count(),
                'new': applications.filter(status=Application.Status.NEW).count(),
                'last_30_days': last_period,
                'previous_30_days': previous_period,
                'by_type': dict(applications.values_list('type').annotate(c=Count('id'))),
                'by_status': dict(applications.values_list('status').annotate(c=Count('id'))),
                'daily': series,
            },
            'courses': {
                'total': Course.objects.count(),
                'published': Course.objects.filter(is_published=True).count(),
            },
            'events': {
                'total': Event.objects.count(),
                'upcoming': Event.objects.filter(date__gte=today).count(),
                'open': Event.objects.filter(date__gte=today, status=Event.Status.OPEN).count(),
            },
            'news': {
                'total': Post.objects.count(),
                'published': Post.objects.filter(is_published=True, published_at__lte=now).count(),
            },
            'recent_applications': s.ApplicationSerializer(
                applications.select_related('course', 'event')[:6], many=True,
            ).data,
            'upcoming_events': s.EventSerializer(
                Event.objects.filter(date__gte=today).annotate(applications_count=Count('applications'))
                .order_by('date', 'start_time')[:4],
                many=True,
            ).data,
        })


# --- CRUD ------------------------------------------------------------------------------

class CourseViewSet(DashboardViewSet):
    serializer_class = s.CourseSerializer
    search_fields = ('title', 'short_desc', 'slug')
    filterset_fields = ('is_published', 'theme')
    ordering_fields = ('order', 'title', 'seats', 'created_at')
    ordering = ('order', 'id')

    def get_queryset(self):
        return Course.objects.prefetch_related('curriculum').annotate(applications_count=Count('applications'))


class EventViewSet(DashboardViewSet):
    serializer_class = s.EventSerializer
    search_fields = ('title', 'short_desc', 'category', 'location')
    filterset_fields = ('status', 'category', 'is_published')
    ordering_fields = ('date', 'title', 'seats', 'created_at')
    ordering = ('-date',)

    def get_queryset(self):
        return Event.objects.prefetch_related('schedule').annotate(applications_count=Count('applications'))


class PostViewSet(DashboardViewSet):
    serializer_class = s.PostSerializer
    queryset = Post.objects.all()
    search_fields = ('title', 'excerpt', 'category')
    filterset_fields = ('is_published', 'category')
    ordering_fields = ('published_at', 'title', 'created_at')
    ordering = ('-published_at',)


class OrderedContentViewSet(DashboardViewSet):
    filterset_fields = ('is_published',)
    ordering_fields = ('order', 'id')
    ordering = ('order', 'id')


class StatisticViewSet(OrderedContentViewSet):
    serializer_class = s.StatisticSerializer
    queryset = Statistic.objects.all()
    search_fields = ('label',)


class FeatureViewSet(OrderedContentViewSet):
    serializer_class = s.FeatureSerializer
    queryset = Feature.objects.all()
    search_fields = ('title', 'description')


class EquipmentViewSet(OrderedContentViewSet):
    serializer_class = s.EquipmentSerializer
    queryset = Equipment.objects.all()
    search_fields = ('title', 'description')


class TeamMemberViewSet(OrderedContentViewSet):
    serializer_class = s.TeamMemberSerializer
    queryset = TeamMember.objects.all()
    search_fields = ('name', 'role')


class PartnerViewSet(OrderedContentViewSet):
    serializer_class = s.PartnerSerializer
    queryset = Partner.objects.all()
    search_fields = ('name',)


class VideoStoryViewSet(OrderedContentViewSet):
    serializer_class = s.VideoStorySerializer
    queryset = VideoStory.objects.select_related('course')
    search_fields = ('student_name', 'result', 'course_name', 'course__title')


class ApplicationViewSet(DashboardViewSet):
    serializer_class = s.ApplicationSerializer
    queryset = Application.objects.select_related('course', 'event')
    http_method_names = ('get', 'patch', 'delete', 'head', 'options')
    search_fields = ('name', 'phone', 'message')
    filterset_fields = ('status', 'type', 'course', 'event')
    ordering_fields = ('created_at', 'status', 'name')
    ordering = ('-created_at',)


class SiteSettingsView(DashboardMixin, generics.RetrieveUpdateAPIView):
    serializer_class = s.SiteSettingsSerializer
    http_method_names = ('get', 'put', 'patch', 'head', 'options')

    def get_object(self):
        settings = SiteSettings.load()
        if settings is None:
            settings = SiteSettings(phone='', email='info@example.com', address='')
        return settings
